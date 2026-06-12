#!/usr/bin/env python3
"""Run Sector Investment Agent validator fixtures.

Pass fixtures must pass. Fail fixtures must fail with exit code 1.
Scenario docs are intentionally not executed.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_report.py"
PASS_DIR = ROOT / "evals" / "fixtures" / "pass"
FAIL_DIR = ROOT / "evals" / "fixtures" / "fail"


def mode_for(path: Path) -> str:
    text = path.read_text(encoding="utf-8-sig", errors="ignore")
    m = re.search(r"<!--\s*mode:\s*(short|standard|deep)\s*-->", text, re.I)
    if m:
        return m.group(1).lower()
    if "standard" in path.name.lower():
        return "standard"
    if "short" in path.name.lower():
        return "short"
    return "deep"


def run_fixture(path: Path) -> int:
    mode = mode_for(path)
    cmd = [sys.executable, str(VALIDATOR), "--mode", mode, str(path)]
    result = subprocess.run(cmd, cwd=str(ROOT), text=True, capture_output=True)
    print(f"\n=== {path.relative_to(ROOT)} (mode={mode}) ===")
    print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip())
    return result.returncode


def main() -> int:
    failures: list[str] = []
    for path in sorted(PASS_DIR.glob("*.md")):
        code = run_fixture(path)
        if code != 0:
            failures.append(f"Expected PASS but failed: {path}")
    for path in sorted(FAIL_DIR.glob("*.md")):
        code = run_fixture(path)
        if code != 1:
            failures.append(f"Expected FAIL exit=1 but got {code}: {path}")
    if failures:
        print("\nEVAL RESULT: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("\nEVAL RESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
