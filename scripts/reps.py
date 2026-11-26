#!/usr/bin/env python3
"""interview-reps: the deterministic core.

Decides what is due today, records results, runs task tests and reports
progress. Standard library only, so it runs on any Python 3.9+.

    python scripts/reps.py today            # today's session (stable for the day)
    python scripts/reps.py start <task_id>  # copy a task's starter file into work/
    python scripts/reps.py check <task_id>  # run the task's tests against work/
    python scripts/reps.py record <task_id> clean|errors|failed [--note "..."]
    python scripts/reps.py progress         # streak, progress bars, readiness
    python scripts/reps.py library              # what is in the rotation, per topic
    python scripts/reps.py flag <id|topic:name> on|off   # personal flags (profile/focus.json)
    python scripts/reps.py import-anki <file>   # turn an Anki text export into theory cards

Add --json to today / progress for machine-readable output.
"""
import argparse
from collections import Counter
import json
import os
import shutil
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / "tasks"
DATA = Path(os.environ.get("REPS_DATA_DIR", ROOT / "data"))
WORK = Path(os.environ.get("REPS_WORK_DIR", ROOT / "work"))
PROGRESS = DATA / "progress.json"
LOG = DATA / "log.jsonl"
TODAY = DATA / "today.json"
BUG_LOG = DATA / "bug-log.md"
TRIAGE = DATA / "triage.json"        # cards marked "weak" in the fast pass: they come first as new cards
PROFILE = Path(os.environ.get("REPS_PROFILE_DIR", ROOT / "profile"))
FOCUS = PROFILE / "focus.json"      # personal flags: which topics and cards are in the rotation
TOPIC_DEFAULTS = ROOT / "config" / "topics.json"

# Leitner boxes: a task in box N comes back after INTERVALS[N] days.
INTERVALS = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16}
MASTERED_BOX = 4

# The main coding task by weekday (Monday = 0).
WEEK_PLAN = {0: "pattern", 1: "oop", 2: "pattern", 3: "debug", 4: "pattern", 5: "free", 6: "free"}
CASE_DAY = 4            # one case card on Fridays
THEORY_PER_DAY = 5      # default; override with: reps.py set theory_per_day 10
THEORY_REVIEWS = 3     # at most this many review cards before new ones are added

TYPES = ("warmup", "theory", "oop", "debug", "pattern", "case")
CODING = ("warmup", "oop", "debug", "pattern")
RESULTS = ("clean", "errors", "failed")
PILLARS = {
    "Theory": ("theory", "case"),
    "OOP": ("oop", "debug"),
    "Problems": ("pattern",),
    "Fluency": ("warmup",),
}


# ---------- loading and saving ----------

def load_focus():
    """Topic weights (defaults overlaid with personal ones) and per-card flags."""
    weights = {k: v for k, v in load_json(TOPIC_DEFAULTS, {}).items() if not k.startswith("_")}
    focus = load_json(FOCUS, {})
    personal = focus.get("topics", {})
    weights.update(personal)
    return weights, personal, focus.get("cards", {})


def in_rotation(item, weights, personal, card_flags):
    """A card flag wins. Otherwise: 'off' is out, 'parked' needs its topic switched on by you,
    'active' is in unless its topic weight is 0."""
    flag = card_flags.get(item["id"])
    if flag in ("on", "off"):
        return flag == "on"
    status = item.get("status", "active")
    topic = item.get("topic")
    if status == "off":
        return False
    if status == "parked":
        return personal.get(topic, 0) > 0
    return weights.get(topic, 1) > 0


def load_tasks(include_all=False):
    """Tasks from tasks/*.json, in file order then list order. Only tasks in rotation unless include_all."""
    tasks = []
    seen = set()
    weights, personal, card_flags = load_focus()
    for path in sorted(TASKS_DIR.glob("*.json")):
        for item in json.loads(path.read_text(encoding="utf-8")):
            if item["type"] not in TYPES:
                sys.exit(f"{path.name}: task {item.get('id')} has unknown type {item['type']!r}")
            if item["id"] in seen:
                sys.exit(f"{path.name}: duplicate task id {item['id']!r}")
            seen.add(item["id"])
            item["_order"] = len(seen)
            item["_weight"] = weights.get(item.get("topic"), 1)
            item["_in"] = in_rotation(item, weights, personal, card_flags)
            if item["_in"] or include_all:
                tasks.append(item)
    return tasks


def load_json(path, default):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_log():
    if not LOG.exists():
        return []
    return [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]


def today_date(args):
    return date.fromisoformat(args.date) if getattr(args, "date", None) else date.today()


# ---------- scheduling ----------

def is_due(task, progress, day):
    state = progress.get(task["id"])
    return state is None or state["due"] <= day.isoformat()


def settings():
    """Session sizes: defaults overlaid with profile/focus.json -> settings."""
    personal = load_json(FOCUS, {}).get("settings", {})
    per_day = int(personal.get("theory_per_day", THEORY_PER_DAY))
    reviews = int(personal.get("theory_reviews", max(1, round(per_day * 0.6))))
    return {"theory_per_day": per_day, "theory_reviews": min(reviews, per_day)}


def group(task):
    return task.get("topic") or task.get("pattern") or task["type"]


def pick_session(tasks, progress, day):
    by_type = {name: [t for t in tasks if t["type"] == name] for name in TYPES}
    chosen = set()
    weak = set(load_json(TRIAGE, {}).get("weak", []))
    size = settings()

    def reviews(kind):
        """Seen tasks that are due again, oldest due date first."""
        pool = [t for t in by_type[kind] if t["id"] in progress and is_due(t, progress, day)
                and t["id"] not in chosen]
        return sorted(pool, key=lambda t: (progress[t["id"]]["due"], t["_order"]))

    def fresh(kind):
        """Tasks never done, in curriculum order. Theory cards: heaviest topic first."""
        pool = [t for t in by_type[kind] if t["id"] not in progress and t["id"] not in chosen]
        if kind == "theory":
            # Cards marked weak in the fast pass first, then the heaviest topic.
            return sorted(pool, key=lambda t: (t["id"] not in weak, -t["_weight"], t["_order"]))
        if kind == "pattern":
            # Rotate through the topics, so matrix, hash map, ML coding ... take turns.
            done = Counter(group(t) for t in by_type[kind] if t["id"] in progress)
            rank, position = {}, Counter()
            # Within a topic: pinned tasks, then problems not solved before, then redos of old ones.
            for t in sorted(pool, key=lambda t: (-t.get("priority", 0), t.get("solved_before", False), t["_order"])):
                rank[t["id"]] = done[group(t)] + position[group(t)]
                position[group(t)] += 1
            return sorted(pool, key=lambda t: (rank[t["id"]], -t["_weight"], t["_order"]))
        return pool

    def take(pool, count=1):
        picked = pool[:count]
        chosen.update(t["id"] for t in picked)
        return picked

    session = {"date": day.isoformat(), "warmup": [], "theory": [], "main": [], "redo": [], "case": []}

    # Warm-up: a review if one is due, otherwise the next new snippet.
    session["warmup"] = [t["id"] for t in (take(reviews("warmup")) or take(fresh("warmup")))]

    # Theory: up to THEORY_REVIEWS reviews, filled with new cards, then more reviews if short.
    cards = take(reviews("theory"), size["theory_reviews"])
    cards += take(fresh("theory"), size["theory_per_day"] - len(cards))
    cards += take(reviews("theory"), size["theory_per_day"] - len(cards))
    session["theory"] = [t["id"] for t in cards]

    # Main task: new material of today's type; fall back to other types, then to reviews.
    plan = WEEK_PLAN[day.weekday()]
    order = {"pattern": ["pattern", "oop", "debug"],
             "oop": ["oop", "debug", "pattern"],
             "debug": ["debug", "oop", "pattern"],
             "free": ["pattern", "oop", "debug"]}[plan]
    main = []
    for kind in order:
        main = take(fresh(kind))
        if main:
            break
    if not main:
        for kind in order:
            main = take(reviews(kind))
            if main:
                break
    session["main"] = [t["id"] for t in main]

    # Redo: one coding task that is due again. Tasks that went wrong come first.
    pool = [t for kind in ("pattern", "oop", "debug") for t in reviews(kind)]
    pool.sort(key=lambda t: (progress[t["id"]]["last_result"] == "clean", progress[t["id"]]["due"], t["_order"]))
    session["redo"] = [t["id"] for t in take(pool)]

    if day.weekday() == CASE_DAY:
        session["case"] = [t["id"] for t in (take(fresh("case")) or take(reviews("case")))]
    return session


def get_session(tasks, progress, day, refresh=False):
    saved = load_json(TODAY, None)
    if saved and saved.get("date") == day.isoformat() and not refresh:
        return saved
    session = pick_session(tasks, progress, day)
    save_json(TODAY, session)
    return session


# ---------- progress ----------

def streaks(log, day):
    """Current and longest streak. Weekends are optional: a missed Saturday or Sunday does not break it."""
    practised = {date.fromisoformat(entry["date"]) for entry in log}
    if not practised:
        return 0, 0

    def is_weekend(d):
        return d.weekday() >= 5

    longest = run = 0
    cursor = min(practised)
    while cursor <= max(practised):
        if cursor in practised:
            run += 1
            longest = max(longest, run)
        elif not is_weekend(cursor):
            run = 0
        cursor += timedelta(days=1)

    current = 0
    cursor = day
    if cursor not in practised:          # today not done yet: the streak still stands
        cursor -= timedelta(days=1)
    while cursor >= min(practised):
        if cursor in practised:
            current += 1
        elif not is_weekend(cursor):
            break
        cursor -= timedelta(days=1)
    return current, longest


def bar(done, total, width=20):
    filled = round(width * done / total) if total else 0
    return "[" + "#" * filled + "." * (width - filled) + "]"


def progress_report(tasks, progress, log, day):
    current, longest = streaks(log, day)
    week_start = day - timedelta(days=day.weekday())
    week_days = {entry["date"] for entry in log if entry["date"] >= week_start.isoformat()}
    pillars = {}
    for name, kinds in PILLARS.items():
        group = [t for t in tasks if t["type"] in kinds]
        seen = [t for t in group if t["id"] in progress]
        mastered = [t for t in seen if progress[t["id"]]["box"] >= MASTERED_BOX]
        pillars[name] = {"total": len(group), "seen": len(seen), "mastered": len(mastered)}
    last_patterns = [entry["result"] for entry in log if entry["type"] == "pattern"][-10:]
    return {
        "date": day.isoformat(),
        "streak": current,
        "longest_streak": longest,
        "days_this_week": len(week_days),
        "practised_today": day.isoformat() in {entry["date"] for entry in log},
        "pillars": pillars,
        "pattern_readiness": {"clean": last_patterns.count("clean"), "of": len(last_patterns), "target": 8},
        "total_reps": len(log),
    }


def print_progress(report):
    print(f"Streak: {report['streak']} day(s)   longest: {report['longest_streak']}   "
          f"this week: {report['days_this_week']}/5 days   total reps: {report['total_reps']}")
    for name, numbers in report["pillars"].items():
        print(f"  {name:<9}{bar(numbers['mastered'], numbers['total'])} "
              f"{numbers['mastered']}/{numbers['total']} mastered, {numbers['seen']} seen")
    ready = report["pattern_readiness"]
    print(f"  Problem readiness: {ready['clean']}/{ready['of']} of the last pattern problems clean "
          f"(target {ready['target']} of 10)")


# ---------- commands ----------

def cmd_today(args):
    tasks = load_tasks()
    index = {t["id"]: t for t in tasks}
    progress = load_json(PROGRESS, {})
    day = today_date(args)
    session = get_session(tasks, progress, day, refresh=args.refresh)
    done_today = {entry["id"] for entry in read_log() if entry["date"] == day.isoformat()}
    if args.json:
        full = {slot: [dict({k: v for k, v in index[i].items() if not k.startswith("_")},
                            done=i in done_today, box=progress.get(i, {}).get("box", 0))
                       for i in ids if i in index]
                for slot, ids in session.items() if slot != "date"}
        print(json.dumps({"date": session["date"], "session": full,
                          "progress": progress_report(tasks, progress, read_log(), day)},
                         indent=2, ensure_ascii=False))
        return
    print(f"Session for {day.strftime('%A %d %B %Y')}")
    print_progress(progress_report(tasks, progress, read_log(), day))
    labels = [("warmup", "Warm-up"), ("theory", "Theory cards"), ("main", "Main task"),
              ("redo", "Redo"), ("case", "Case card")]
    for slot, label in labels:
        ids = [i for i in session.get(slot, []) if i in index]
        if not ids:
            continue
        print(f"\n{label}:")
        for task_id in ids:
            task = index[task_id]
            mark = "x" if task_id in done_today else " "
            where = task.get("url") or task.get("readme") or ""
            print(f"  [{mark}] {task_id}  {task['title']}" + (f"  ({where})" if where else ""))


def cmd_start(args):
    task = {t["id"]: t for t in load_tasks()}.get(args.task_id)
    if task is None:
        sys.exit(f"Unknown task id: {args.task_id}")
    WORK.mkdir(parents=True, exist_ok=True)
    target = WORK / f"{task['id']}.py"
    if target.exists():
        print(f"Already there: {target}")
        return
    starter = task.get("starter")
    if starter:
        shutil.copyfile(ROOT / starter, target)
    else:
        target.write_text(f"# {task['id']}: {task['title']}\n\n", encoding="utf-8")
    print(f"Write your solution in: {target}")


def cmd_check(args):
    task = {t["id"]: t for t in load_tasks()}.get(args.task_id)
    if task is None:
        sys.exit(f"Unknown task id: {args.task_id}")
    if not task.get("test"):
        sys.exit(f"{args.task_id} has no local tests (check it on the linked site, or by review).")
    if not (WORK / f"{task['id']}.py").exists():
        sys.exit(f"No solution yet. Run: python scripts/reps.py start {task['id']}")
    env = dict(os.environ, PYTHONPATH=str(WORK), PYTHONDONTWRITEBYTECODE="1")
    result = subprocess.run([sys.executable, str(ROOT / task["test"])], env=env)
    sys.exit(result.returncode)


def cmd_record(args):
    tasks = load_tasks()
    task = {t["id"]: t for t in tasks}.get(args.task_id)
    if task is None:
        sys.exit(f"Unknown task id: {args.task_id}")
    day = today_date(args)
    progress = load_json(PROGRESS, {})
    state = progress.get(task["id"], {"box": 0, "seen": 0})
    previous = max(state["box"], 1)
    if args.result == "clean":
        box = min(previous + 1, 5)
    elif args.result == "errors":
        box = previous
    else:
        box = 1
    due = day + timedelta(days=INTERVALS[box])
    progress[task["id"]] = {"box": box, "seen": state["seen"] + 1, "last": day.isoformat(),
                            "due": due.isoformat(), "last_result": args.result}
    save_json(PROGRESS, progress)
    DATA.mkdir(parents=True, exist_ok=True)
    entry = {"ts": datetime.now().isoformat(timespec="seconds"), "date": day.isoformat(),
             "id": task["id"], "type": task["type"], "result": args.result}
    if args.note:
        entry["note"] = args.note
    with LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
    if args.note:
        if not BUG_LOG.exists():
            BUG_LOG.write_text("# Bug log\n\nOne line per mistake. Read it before each session.\n\n", encoding="utf-8")
        with BUG_LOG.open("a", encoding="utf-8") as handle:
            handle.write(f"- {day.isoformat()} · `{task['id']}` · {args.result} · {args.note}\n")
    print(f"Recorded {task['id']}: {args.result}. Box {box}, back on {due.isoformat()}.")


def cmd_progress(args):
    tasks = load_tasks()
    report = progress_report(tasks, load_json(PROGRESS, {}), read_log(), today_date(args))
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_progress(report)


def cmd_import_anki(args):
    """Anki 'Notes in Plain Text' export (tab-separated) or 'Front;Back' lines -> theory cards."""
    source = Path(args.file)
    out = TASKS_DIR / "theory_anki.json"
    existing = load_json(out, [])
    fronts = {card["front"] for card in existing}
    added = 0
    for line in source.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        sep = "\t" if "\t" in line else ";"
        parts = [part.strip().strip('"') for part in line.split(sep)]
        if len(parts) < 2 or not parts[0] or parts[0] in fronts:
            continue
        fronts.add(parts[0])
        existing.append({"id": f"anki_{len(existing) + 1:04d}", "type": "theory", "title": parts[0][:70],
                         "front": parts[0], "back": parts[1], "tags": ["anki"]})
        added += 1
    save_json(out, existing)
    print(f"Imported {added} new card(s) into {out.relative_to(ROOT)} ({len(existing)} in total).")


def cmd_triage(args):
    """The fast pass over theory cards never seen before.
    triage [--topic T] [--limit N]   list the next unseen cards (fronts only)
    triage --known ID ...            you know these: box 3, coming back spread over the next weeks
    triage --weak ID ...             you don't: they stay new and jump the queue"""
    tasks = [t for t in load_tasks() if t["type"] == "theory"]
    index = {t["id"]: t for t in tasks}
    progress = load_json(PROGRESS, {})
    triage = load_json(TRIAGE, {"weak": []})
    day = today_date(args)
    for card_id in (args.known or []) + (args.weak or []):
        if card_id not in index:
            sys.exit(f"No theory card in the rotation with id {card_id!r}.")
    if args.known or args.weak:
        spread = sum(1 for state in progress.values() if state.get("last_result") == "known" and state["due"] > day.isoformat())
        added = 0
        for card_id in args.known or []:
            if card_id in progress:
                continue
            due = day + timedelta(days=INTERVALS[3] + spread // 5)     # about five known cards come back per day
            progress[card_id] = {"box": 3, "seen": 0, "last": day.isoformat(), "due": due.isoformat(), "last_result": "known"}
            spread += 1
            added += 1
        triage["weak"] = sorted(set(triage["weak"]) | set(args.weak or []) - set(progress))
        save_json(PROGRESS, progress)
        save_json(TRIAGE, triage)
        if TODAY.exists():
            TODAY.unlink()
        print(f"Marked {added} known and {len(args.weak or [])} weak.")
    unseen = [t for t in tasks if t["id"] not in progress and t["id"] not in triage["weak"]]
    unseen.sort(key=lambda t: (-t["_weight"], t.get("topic", ""), t["_order"]))
    pool = [t for t in unseen if not args.topic or t.get("topic") == args.topic]
    batch = pool[:args.limit]
    summary = {"left_to_triage": len(unseen), "known": sum(1 for v in progress.values() if v.get("last_result") == "known"),
               "weak": len(triage["weak"])}
    if args.json:
        print(json.dumps({"summary": summary, "cards": [{"id": t["id"], "topic": t.get("topic"), "front": t["front"]} for t in batch]},
                         indent=2, ensure_ascii=False))
        return
    for number, t in enumerate(batch, start=1):
        front = " ".join(t["front"].split())
        print(f"{number:>2}. {t['id']}  [{t.get('topic')}]  {front[:110]}")
    print(f"Left to triage: {summary['left_to_triage']}   known: {summary['known']}   weak: {summary['weak']}")


def cmd_set(args):
    if args.name not in ("theory_per_day", "theory_reviews"):
        sys.exit("Settings: theory_per_day, theory_reviews")
    if not args.value.isdigit() or int(args.value) < 1:
        sys.exit("The value must be a whole number, 1 or more.")
    focus = load_json(FOCUS, {})
    focus.setdefault("settings", {})[args.name] = int(args.value)
    save_json(FOCUS, focus)
    if TODAY.exists():
        TODAY.unlink()
    print(f"{args.name} = {args.value}. Now: {settings()}")


def cmd_library(args):
    """Every card and task by track and topic, with how many are in the rotation."""
    rows = {}
    for t in load_tasks(include_all=True):
        key = (t.get("track", t["type"]), t.get("topic", t["type"]))
        row = rows.setdefault(key, {"in": 0, "parked": 0, "off": 0, "weight": t["_weight"]})
        row["in" if t["_in"] else ("parked" if t.get("status") == "parked" else "off")] += 1
    if args.json:
        print(json.dumps([dict(track=k[0], topic=k[1], **v) for k, v in sorted(rows.items())], indent=2))
        return
    print(f"{'track':<10}{'topic':<17}{'weight':>6}{'in':>6}{'parked':>8}{'off':>6}")
    for (track, topic), row in sorted(rows.items()):
        print(f"{track:<10}{topic:<17}{row['weight']:>6}{row['in']:>6}{row['parked']:>8}{row['off']:>6}")
    print(f"In rotation: {sum(r['in'] for r in rows.values())} of {sum(r['in'] + r['parked'] + r['off'] for r in rows.values())}")


def cmd_flag(args):
    """flag <card id> on|off|default   or   flag topic:<name> on|off|<weight>|default"""
    focus = load_json(FOCUS, {})
    all_tasks = load_tasks(include_all=True)
    if args.target.startswith("topic:"):
        name = args.target[6:]
        if name not in {t.get("topic") for t in all_tasks}:
            sys.exit(f"No topic called {name!r}. Run: python scripts/reps.py library")
        topics = focus.setdefault("topics", {})
        if args.value == "default":
            topics.pop(name, None)
        elif args.value in ("on", "off"):
            topics[name] = 1 if args.value == "on" else 0
        elif args.value.isdigit():
            topics[name] = int(args.value)
        else:
            sys.exit("For a topic use on, off, default or a whole number weight.")
    else:
        if args.target not in {t["id"] for t in all_tasks}:
            sys.exit(f"No card or task with id {args.target!r}.")
        if args.value not in ("on", "off", "default"):
            sys.exit("For a card use on, off or default.")
        cards = focus.setdefault("cards", {})
        if args.value == "default":
            cards.pop(args.target, None)
        else:
            cards[args.target] = args.value
    save_json(FOCUS, focus)
    if TODAY.exists():
        TODAY.unlink()   # today's session is re-picked with the new flags
    print(f"{args.target} -> {args.value}. Saved in {FOCUS}.")


def main():
    parser = argparse.ArgumentParser(description="interview-reps: daily practice scheduler")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("today", help="show today's session")
    p.add_argument("--json", action="store_true")
    p.add_argument("--refresh", action="store_true", help="re-pick today's session")
    p.add_argument("--date", help="pretend today is YYYY-MM-DD (testing)")
    p.set_defaults(func=cmd_today)

    p = sub.add_parser("start", help="copy a task's starter file into work/")
    p.add_argument("task_id")
    p.set_defaults(func=cmd_start)

    p = sub.add_parser("check", help="run a task's tests against work/")
    p.add_argument("task_id")
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("record", help="record a result")
    p.add_argument("task_id")
    p.add_argument("result", choices=RESULTS)
    p.add_argument("--note", help="what went wrong, for the bug log")
    p.add_argument("--date", help="record for YYYY-MM-DD (testing)")
    p.set_defaults(func=cmd_record)

    p = sub.add_parser("progress", help="streak and progress bars")
    p.add_argument("--json", action="store_true")
    p.add_argument("--date", help="pretend today is YYYY-MM-DD (testing)")
    p.set_defaults(func=cmd_progress)

    p = sub.add_parser("import-anki", help="import an Anki text export as theory cards")
    p.add_argument("file")
    p.set_defaults(func=cmd_import_anki)

    p = sub.add_parser("triage", help="fast pass over unseen theory cards: list, --known, --weak")
    p.add_argument("--topic")
    p.add_argument("--limit", type=int, default=15)
    p.add_argument("--known", nargs="*", metavar="ID")
    p.add_argument("--weak", nargs="*", metavar="ID")
    p.add_argument("--json", action="store_true")
    p.add_argument("--date", help="pretend today is YYYY-MM-DD (testing)")
    p.set_defaults(func=cmd_triage)

    p = sub.add_parser("set", help="personal session size: set theory_per_day 10")
    p.add_argument("name")
    p.add_argument("value")
    p.set_defaults(func=cmd_set)

    p = sub.add_parser("library", help="cards and tasks per topic: in rotation, parked, off")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_library)

    p = sub.add_parser("flag", help="switch a card or a topic on or off: flag py_153 off | flag topic:trees on")
    p.add_argument("target")
    p.add_argument("value")
    p.set_defaults(func=cmd_flag)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
