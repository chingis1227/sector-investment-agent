#!/usr/bin/env python3
"""Create reproducible run artifacts for the Sector Investment Agent.

This runner intentionally does not call model APIs or require API keys. It locks
the report mode, records the request, and writes Codex handoff artifacts plus the
validation command that must be used for any saved report.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
AGENTS_PATH = ROOT / "AGENTS.md"
CONTRACT_PATH = ROOT / "configs" / "report_contract.yaml"
VALIDATOR_PATH = ROOT / "scripts" / "validate_report.py"
DEFAULT_OUTPUT_DIR = ROOT / "outputs" / "runs"
DEFAULT_REPORT_DIR = ROOT / "outputs" / "sector"


def load_json_contract(path: Path = CONTRACT_PATH) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"contract not found: {path}")
    # The project contract is YAML-compatible JSON.
    return json.loads(path.read_text(encoding="utf-8-sig"))


def require_agents_contract(path: Path = AGENTS_PATH) -> str:
    if not path.exists():
        raise FileNotFoundError(f"AGENTS.md not found: {path}")
    return path.read_text(encoding="utf-8-sig")


def slugify(text: str) -> str:
    lower = text.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", lower).strip("-")
    if not slug:
        digest = hashlib.sha1(text.encode("utf-8")).hexdigest()[:8]
        slug = f"request-{digest}"
    return slug[:64].strip("-") or "request"


def unique_run_dir(output_dir: Path, date_part: str, slug: str) -> Path:
    base = output_dir / f"{date_part}-{slug}"
    candidate = base
    n = 2
    while candidate.exists():
        candidate = output_dir / f"{date_part}-{slug}-{n}"
        n += 1
    return candidate


def relative_or_absolute(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def validation_command(mode: str, report_path: Path) -> str:
    return f"py -3 scripts/validate_report.py --mode {mode} {relative_or_absolute(report_path)}"


def write_run_plan(
    path: Path,
    *,
    request: str,
    mode: str,
    mode_source: str,
    created_at: str,
    final_report_path: Path,
    max_validation_attempts: int,
) -> None:
    body = f"""# Sector Agent Run Plan

- Created at: {created_at}
- Request: {request}
- Report mode: `{mode}`
- Mode source: {mode_source}
- Agent contract: `AGENTS.md`
- Report contract: `configs/report_contract.yaml`
- Final report path: `{relative_or_absolute(final_report_path)}`
- Max validation attempts: {max_validation_attempts}

## Assumptions

- `deep` is used by default unless `--mode standard` or `--mode short` is passed explicitly.
- This runner does not call OpenAI API or require API keys.
- Codex app/agent performs source collection, evidence extraction, report writing, and repair.
- A saved report must be validated with the command in `validation_command.txt`.

## Next action

Follow `codex_handoff.md` to produce the report, then run validation.
"""
    path.write_text(body, encoding="utf-8")


def write_task(path: Path, *, request: str, mode: str, final_report_path: Path, max_validation_attempts: int) -> None:
    body = f"""# Sector Agent Task

Request: {request}

Mode: `{mode}`

Output: `{relative_or_absolute(final_report_path)}`

Follow the repository autostart workflow in `AGENTS.md`. Produce the report, then run:

```powershell
{validation_command(mode, final_report_path)}
```

If validation fails, repair the report and rerun validation up to {max_validation_attempts} attempts.
"""
    path.write_text(body, encoding="utf-8")


def write_codex_handoff(
    path: Path,
    *,
    request: str,
    mode: str,
    final_report_path: Path,
    max_validation_attempts: int,
) -> None:
    payload = {
        "instruction": "Do not ask the user to restate repository instructions. Use this handoff plus AGENTS.md.",
        "request": request,
        "mode": mode,
        "required_docs": [
            "AGENTS.md",
            "configs/report_contract.yaml",
            "docs/workflow.md",
            "docs/source-policy.md",
            "docs/parsing-policy.md",
            "templates/sector-analysis-template.md",
        ],
        "final_report_path": relative_or_absolute(final_report_path),
        "validation_command": validation_command(mode, final_report_path),
        "max_validation_attempts": max_validation_attempts,
        "success_criteria": [
            "write the final report to final_report_path",
            "run the validation_command",
            "repair and rerun validation until PASS or max_validation_attempts is reached",
            "final response includes report path, validation score, and blockers if not PASS",
        ],
    }
    markdown = f"""# Codex Handoff

```json
{json.dumps(payload, ensure_ascii=False, indent=2)}
```

## Execute

Use the JSON above as the task contract. Follow `AGENTS.md` automatically and do not ask the user to paste or mention project files again.
"""
    path.write_text(markdown, encoding="utf-8")


def run_validator(mode: str, report: Path, run_dir: Path) -> int:
    cmd = [sys.executable, str(VALIDATOR_PATH), "--mode", mode, str(report)]
    result = subprocess.run(cmd, cwd=str(ROOT), text=True, capture_output=True)
    output = result.stdout
    if result.stderr:
        output += "\n[stderr]\n" + result.stderr
    (run_dir / "validation_output.txt").write_text(output, encoding="utf-8")
    return result.returncode


def parse_args(argv: list[str] | None, modes: list[str], default_mode: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create Sector Investment Agent run artifacts.")
    parser.add_argument("--request", required=True, help="User request to analyze.")
    parser.add_argument("--mode", choices=sorted(modes), default=None, help=f"Report mode. Defaults to contract default: {default_mode}.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Directory for run artifacts.")
    parser.add_argument("--dry-run", action="store_true", help="Create run plan artifacts without generating a final report.")
    parser.add_argument("--report", help="Optional existing markdown report to validate in the selected mode.")
    parser.add_argument("--report-path", help="Final report path to record in run artifacts.")
    parser.add_argument("--max-validation-attempts", type=int, default=3, help="Max validation repair attempts Codex should use.")
    parser.add_argument("--codex-exec", action="store_true", help="Optional future path: run codex exec with the generated handoff if available.")
    return parser.parse_args(argv)


def codex_exec_available() -> tuple[bool, str]:
    codex = shutil.which("codex")
    if not codex:
        return False, "codex executable not found on PATH"
    try:
        result = subprocess.run([codex, "exec", "--help"], cwd=str(ROOT), text=True, capture_output=True, timeout=15)
    except Exception as exc:
        return False, str(exc)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        return False, detail or f"codex exec --help exited {result.returncode}"
    return True, codex


def run_codex_exec(handoff_path: Path) -> int:
    ok, detail = codex_exec_available()
    if not ok:
        print(f"Use Codex app; CLI execution unavailable. Detail: {detail}", file=sys.stderr)
        return 2
    prompt = handoff_path.read_text(encoding="utf-8")
    result = subprocess.run(["codex", "exec", "--sandbox", "workspace-write", prompt], cwd=str(ROOT))
    return result.returncode


def main(argv: list[str] | None = None) -> int:
    try:
        require_agents_contract()
        contract = load_json_contract()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    modes = list(contract.get("modes", {}).keys())
    default_mode = contract.get("default_mode", "deep")
    args = parse_args(argv, modes, default_mode)

    mode = args.mode or default_mode
    mode_source = "explicit --mode" if args.mode else "configs/report_contract.yaml default_mode"
    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = ROOT / output_dir

    report = Path(args.report).resolve() if args.report else None
    if report and not report.exists():
        print(f"ERROR: report not found: {report}", file=sys.stderr)
        return 2
    if args.max_validation_attempts < 1:
        print("ERROR: --max-validation-attempts must be >= 1", file=sys.stderr)
        return 2

    if args.report_path:
        final_report_path = Path(args.report_path)
        if not final_report_path.is_absolute():
            final_report_path = ROOT / final_report_path
    elif report:
        final_report_path = report
    else:
        final_report_path = DEFAULT_REPORT_DIR / f"{slugify(args.request)}.md"

    now = datetime.now().astimezone()
    date_part = now.date().isoformat()
    run_dir = unique_run_dir(output_dir, date_part, slugify(args.request))
    run_dir.mkdir(parents=True, exist_ok=False)

    request_payload = {
        "request": args.request,
        "mode": mode,
        "mode_source": mode_source,
        "created_at": now.isoformat(),
        "agent_contract": str(AGENTS_PATH.relative_to(ROOT)),
        "report_contract": CONTRACT_PATH.relative_to(ROOT).as_posix(),
        "dry_run": bool(args.dry_run),
        "report": str(report) if report else None,
        "final_report_path": relative_or_absolute(final_report_path),
        "max_validation_attempts": args.max_validation_attempts,
        "assumptions": [
            "deep is the default mode unless --mode standard or --mode short is passed explicitly",
            "runner does not call OpenAI API or require API keys",
            "Codex app/agent collects sources and writes the final report",
            "saved reports must pass scripts/validate_report.py for the selected mode",
        ],
    }
    (run_dir / "request.json").write_text(json.dumps(request_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_run_plan(
        run_dir / "run_plan.md",
        request=args.request,
        mode=mode,
        mode_source=mode_source,
        created_at=now.isoformat(),
        final_report_path=final_report_path,
        max_validation_attempts=args.max_validation_attempts,
    )
    write_task(run_dir / "task.md", request=args.request, mode=mode, final_report_path=final_report_path, max_validation_attempts=args.max_validation_attempts)
    write_codex_handoff(run_dir / "codex_handoff.md", request=args.request, mode=mode, final_report_path=final_report_path, max_validation_attempts=args.max_validation_attempts)
    (run_dir / "validation_command.txt").write_text(validation_command(mode, final_report_path) + "\n", encoding="utf-8")

    validation_code: int | None = None
    if report:
        validation_code = run_validator(mode, report, run_dir)

    print(f"mode: {mode}")
    print(f"mode_source: {mode_source}")
    print(f"run_dir: {run_dir.relative_to(ROOT).as_posix()}")
    print(f"final_report_path: {relative_or_absolute(final_report_path)}")
    print("artifacts: request.json, run_plan.md, task.md, codex_handoff.md, validation_command.txt")
    if report:
        print(f"validation_exit_code: {validation_code}")
        return int(validation_code)
    if args.codex_exec:
        return run_codex_exec(run_dir / "codex_handoff.md")
    if args.dry_run:
        print("dry_run: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
