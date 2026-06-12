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


def mode_for(path: Path) -> tuple[str, bool]:
    text = path.read_text(encoding="utf-8-sig", errors="ignore")
    m = re.search(r"<!--\s*mode:\s*(short|standard|deep|default)\s*-->", text, re.I)
    if m:
        mode = m.group(1).lower()
        if mode == "default":
            return "deep", True
        return mode, False
    if "standard" in path.name.lower():
        return "standard", False
    if "short" in path.name.lower():
        return "short", False
    return "deep", False


def run_fixture(path: Path) -> int:
    mode, use_default = mode_for(path)
    cmd = [sys.executable, str(VALIDATOR), str(path)] if use_default else [sys.executable, str(VALIDATOR), "--mode", mode, str(path)]
    result = subprocess.run(cmd, cwd=str(ROOT), text=True, capture_output=True)
    label = "default(deep)" if use_default else mode
    print(f"\n=== {path.relative_to(ROOT)} (mode={label}) ===")
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
