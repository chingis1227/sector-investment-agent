# Sector Investment Agent

AI agent workflow for investment-oriented sector and industry analysis. The goal is not to write a generic overview; the goal is to decide whether a sector deserves deeper work, where the profit pool is, who wins or loses, what is already priced in, and which metrics should be monitored.

## Use in Codex

Open this repository in Codex and type a normal sector question, for example:

```text
Analyze the AI infrastructure sector
```

Codex should automatically load `AGENTS.md`, create a run folder, write a deep report under `outputs/sector/`, run the validator, and repair the report until PASS or a clear blocker. You should not need to type "use AGENTS.md, workflow, template, and validator" every time.

## Normal workflow

```text
user sector request
-> AGENTS.md autostart rule
-> scripts/run_sector_agent.py creates run artifacts
-> Codex reads codex_handoff.md
-> Codex writes outputs/sector/<slug>.md
-> scripts/validate_report.py validates report
-> Codex repairs until PASS or blocker
-> final response with report path and validation score
```

Default report mode is `deep` unless the user explicitly asks for `standard` or `short`.

## Optional runner usage

Create a reproducible run folder without generating the report yourself:

```powershell
py -3 scripts/run_sector_agent.py --request "Analyze the AI infrastructure sector"
```

Expected artifacts:

```text
outputs/runs/YYYY-MM-DD-<slug>/
  request.json
  run_plan.md
  task.md
  codex_handoff.md
  validation_command.txt
```

Optional flags:

```powershell
py -3 scripts/run_sector_agent.py --request "Short sector view" --mode short
py -3 scripts/run_sector_agent.py --request "Test" --report-path outputs/sector/test.md
py -3 scripts/run_sector_agent.py --request "Test" --max-validation-attempts 5
```

`--codex-exec` is optional and future-facing. It only works if `codex exec` is runnable in the local environment. Normal Codex app usage does not require an OpenAI API key.

## Report modes

| Mode | When to use | Contract |
|---|---|---|
| `deep` | Default for sector analysis | 18 sections from `templates/sector-analysis-template.md`, evidence, sources, confidence, anti-thesis, monitoring metrics |
| `standard` | Only when the user explicitly asks for compact report | scope, verdict, evidence table, drivers/profit pool/valuation, anti-thesis, monitoring, conclusion, sources |
| `short` | Only when the user explicitly asks for short answer | 6 blocks: verdict, drivers, profit pool, valuation, risks/anti-thesis, next steps + sources/confidence |

## Project map

| Path | Purpose |
|---|---|
| `AGENTS.md` | Primary runtime contract for Codex |
| `configs/report_contract.yaml` | Single source of truth for modes, sections, evidence/source schema, pass/fail rules |
| `docs/workflow.md` | Analysis state machine |
| `docs/source-policy.md` | Source priority and reliability rules |
| `docs/parsing-policy.md` | Evidence extraction policy |
| `docs/validation-rubric.md` | Quality rubric |
| `docs/reviewer-checklist.md` | Deep-report review checklist |
| `templates/sector-analysis-template.md` | Deep template with 18 sections |
| `scripts/run_sector_agent.py` | Creates run artifacts and Codex handoff |
| `scripts/validate_report.py` | Validates reports against the contract |
| `scripts/run_evals.py` | Runs pass/fail regression fixtures |
| `evals/fixtures/` | Validator regression fixtures |
| `outputs/sector/` | Final sector reports |
| `outputs/runs/` | Local run artifacts, ignored by git |

## Validation commands

Run the full regression suite:

```powershell
py -3 scripts/run_evals.py
```

Validate a deep report using default mode:

```powershell
py -3 scripts/validate_report.py outputs/sector/example-report.md
```

Validate fixtures by mode:

```powershell
py -3 scripts/validate_report.py evals/fixtures/pass/normal-deep.md
py -3 scripts/validate_report.py --mode standard evals/fixtures/pass/standard-valid.md
py -3 scripts/validate_report.py --mode short evals/fixtures/pass/short-valid.md
```

## Real behavior test

1. Start a new Codex thread in this repository.
2. Type only: `Analyze the AI infrastructure sector`.
3. Expected: Codex automatically creates `outputs/runs/...`, writes `outputs/sector/...`, runs validation, and reports the score.
4. A deep report is complete only when it reaches `18/18 checks passed`.

## Done When

A sector report is complete only when:

- it is saved under `outputs/sector/`;
- it passes `scripts/validate_report.py` in the selected mode;
- deep mode reaches `18/18 checks passed`;
- the final response includes report path, validation score, and blockers if any.
