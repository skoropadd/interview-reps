"""Tiny test runner so tasks need no pytest. Each test.py calls run(globals())."""
import sys
import traceback


def raises(exc, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except exc:
        return True
    except Exception:
        return False
    return False


def run(namespace):
    tests = [(name, fn) for name, fn in namespace.items() if name.startswith("test_") and callable(fn)]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"  pass  {name}")
        except Exception:
            failed += 1
            print(f"  FAIL  {name}")
            traceback.print_exc(limit=1)
    print(f"{len(tests) - failed}/{len(tests)} tests passed")
    sys.exit(1 if failed else 0)
