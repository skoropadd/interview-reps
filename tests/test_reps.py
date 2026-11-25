"""Checks for scripts/reps.py. Run: python tests/test_reps.py"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tasks"))
from _runner import run  # noqa: E402


def reps(tmp, *args):
    env = dict(os.environ, REPS_DATA_DIR=str(Path(tmp) / "data"), REPS_WORK_DIR=str(Path(tmp) / "work"),
               REPS_PROFILE_DIR=str(Path(tmp) / "profile"))
    out = subprocess.run([sys.executable, str(ROOT / "scripts" / "reps.py"), *args],
                         env=env, capture_output=True, text=True)
    return out


def session(tmp, day):
    return json.loads(reps(tmp, "today", "--json", "--date", day).stdout)


def test_task_bank_loads_and_every_file_exists():
    for path in sorted((ROOT / "tasks").glob("*.json")):
        for task in json.loads(path.read_text(encoding="utf-8")):
            for key in ("readme", "starter", "test", "solution"):
                if key in task:
                    assert (ROOT / task[key]).exists(), f"{task['id']}: missing {task[key]}"


def test_session_is_stable_within_a_day():
    with tempfile.TemporaryDirectory() as tmp:
        assert session(tmp, "2026-11-26")["session"] == session(tmp, "2026-11-26")["session"]


def test_weekday_plan_and_case_on_friday():
    with tempfile.TemporaryDirectory() as tmp:
        thursday = session(tmp, "2026-11-26")["session"]
        assert thursday["main"][0]["type"] == "debug"
        assert thursday["case"] == []
        assert len(thursday["theory"]) == 5 and len(thursday["warmup"]) == 1
    with tempfile.TemporaryDirectory() as tmp:
        friday = session(tmp, "2026-11-27")["session"]
        assert friday["main"][0]["type"] == "pattern"
        assert len(friday["case"]) == 1


def test_failed_task_comes_back_as_redo_and_main_is_new():
    with tempfile.TemporaryDirectory() as tmp:
        main = session(tmp, "2026-11-26")["session"]["main"][0]["id"]
        reps(tmp, "record", main, "failed", "--note", "missed super()", "--date", "2026-11-26")
        friday = session(tmp, "2026-11-27")["session"]
        assert [t["id"] for t in friday["redo"]] == [main]
        assert friday["main"][0]["id"] != main and friday["main"][0]["box"] == 0
        assert "missed super()" in (Path(tmp) / "data" / "bug-log.md").read_text()


def test_boxes_move_up_on_clean_and_reset_on_failed():
    with tempfile.TemporaryDirectory() as tmp:
        out = reps(tmp, "record", "warm_01", "clean", "--date", "2026-11-26").stdout
        assert "Box 2" in out and "2026-11-28" in out
        out = reps(tmp, "record", "warm_01", "errors", "--date", "2026-11-28").stdout
        assert "Box 2" in out
        out = reps(tmp, "record", "warm_01", "failed", "--date", "2026-11-30").stdout
        assert "Box 1" in out and "2026-12-01" in out


def test_streak_survives_a_weekend_but_not_a_missed_weekday():
    with tempfile.TemporaryDirectory() as tmp:
        for day in ("2026-11-26", "2026-11-27", "2026-11-30"):      # Thu, Fri, Mon
            reps(tmp, "record", "warm_01", "clean", "--date", day)
        report = json.loads(reps(tmp, "progress", "--json", "--date", "2026-11-30").stdout)
        assert report["streak"] == 3 and report["longest_streak"] == 3
        report = json.loads(reps(tmp, "progress", "--json", "--date", "2026-12-02").stdout)   # Tue missed
        assert report["streak"] == 0 and report["longest_streak"] == 3


def test_check_runs_the_task_tests():
    with tempfile.TemporaryDirectory() as tmp:
        reps(tmp, "start", "oop_01_bank_account")
        assert reps(tmp, "check", "oop_01_bank_account").returncode == 1
        solution = (ROOT / "solutions" / "oop_01_bank_account.py").read_text()
        (Path(tmp) / "work" / "oop_01_bank_account.py").write_text(solution)
        assert reps(tmp, "check", "oop_01_bank_account").returncode == 0


def test_cards_per_day_setting_and_fast_pass():
    with tempfile.TemporaryDirectory() as tmp:
        assert len(session(tmp, "2026-11-26")["session"]["theory"]) == 5
        assert reps(tmp, "set", "theory_per_day", "10").returncode == 0
        cards = session(tmp, "2026-11-26")["session"]["theory"]
        assert len(cards) == 10
        listed = json.loads(reps(tmp, "triage", "--json", "--limit", "12", "--date", "2026-11-26").stdout)["cards"]
        ids = [c["id"] for c in listed]
        known, weak = ids[:10], ids[10:]
        assert reps(tmp, "triage", "--known", *known, "--weak", *weak, "--date", "2026-11-26").returncode == 0
        progress = json.loads((Path(tmp) / "data" / "progress.json").read_text())
        assert all(progress[i]["box"] == 3 and progress[i]["last_result"] == "known" for i in known)
        assert sorted({progress[i]["due"] for i in known}) == ["2026-11-30", "2026-12-01"]   # five a day, from day 4
        assert not (Path(tmp) / "data" / "log.jsonl").exists()                            # self-report is not a rep
        tomorrow = [c["id"] for c in session(tmp, "2026-11-27")["session"]["theory"]]
        assert tomorrow[:2] == weak and not set(tomorrow) & set(known)                    # weak cards jump the queue
        again = [c["id"] for c in json.loads(reps(tmp, "triage", "--json", "--date", "2026-11-27").stdout)["cards"]]
        assert not set(again) & set(ids)


run(globals())
