# Sector Investment Agent

Проект для создания AI-агента, который анализирует сектора и индустрии для инвестиционного исследовательского решения.

Агент не пишет обзор ради обзора. Его задача — помочь понять:

- сектор стоит изучать глубже или нет;
- где находится profit pool;
- кто выигрывает и проигрывает;
- какие драйверы реально двигают рынок;
- что уже заложено в цену;
- какие метрики мониторить дальше.

## Что изменилось в v1 stabilization

В проект добавлен единый контракт отчета:

- `configs/report_contract.yaml` — single source of truth для режимов `short / standard / deep`, обязательных секций, evidence schema, source schema и pass/fail правил;
- `scripts/validate_report.py` — config-driven валидатор с `--mode`;
- `scripts/run_evals.py` — runner для pass/fail fixtures;
- `evals/fixtures/` — исполняемые тестовые отчеты;
- `evals/scenarios/` — сценарные описания, которые не запускаются валидатором напрямую.

## Report modes

| Режим | Когда использовать | Контракт |
|---|---|---|
| `deep` | Полный секторный отчет | 18 секций из `templates/sector-analysis-template.md`; default режим валидатора |
| `standard` | Компактный инвестиционный отчет | evidence table, drivers/profit pool/valuation, anti-thesis, monitoring metrics, conclusion, sources |
| `short` | Короткий ответ в чате | 6 блоков: вердикт, драйверы, profit pool, valuation, риски/anti-thesis, next steps + sources/confidence |

Даже в коротком режиме нельзя убирать источники, свежесть, confidence и ограничения данных.

## Что лежит в проекте

| Файл / папка | Для чего нужен |
|---|---|
| `agent.md` | Главная инструкция для AI-агента |
| `configs/report_contract.yaml` | Единый контракт режимов, секций, evidence/source schema и pass/fail правил |
| `configs/source_tiers.yaml` | Справочник по типам источников и их надежности |
| `docs/workflow.md` | Порядок работы агента и state machine |
| `docs/source-policy.md` | Какие источники надежные, какие вторичные |
| `docs/parsing-policy.md` | Как извлекать evidence items из сайтов, PDF и отчетов |
| `docs/validation-rubric.md` | Как оценивать качество отчета |
| `docs/reviewer-checklist.md` | Независимый чек-лист для глубоких отчетов |
| `templates/sector-analysis-template.md` | Deep template на 18 секций |
| `examples/example-output-skeleton.md` | Актуальный standard-mode пример структуры |
| `evals/fixtures/pass/` | Отчеты, которые должны проходить валидатор |
| `evals/fixtures/fail/` | Отчеты, которые должны падать валидатор |
| `evals/scenarios/` | Описания тестовых сценариев, не report fixtures |
| `scripts/validate_report.py` | Структурный gatekeeper валидатор |
| `scripts/run_evals.py` | Запуск всех eval fixtures |

## Как пользоваться без технических знаний

1. Открой `agent.md`.
2. Скопируй его в ChatGPT / Codex как инструкцию.
3. Добавь запрос, например:

```text
Проанализируй сектор дата-центров.
География: США.
Горизонт: 3–12 месяцев.
Режим отчета: standard.
Цель: найти 3–5 инвестиционных направлений.
Используй workflow, source policy, parsing policy, validation rubric, report_contract и template из проекта.
```

## Как должен работать агент

```text
запрос пользователя
→ определение сектора, типа объекта, географии, горизонта и report mode
→ план источников
→ сбор и парсинг evidence items
→ freshness check
→ Tiered Metrics Map
→ анализ сектора
→ anti-thesis и confidence assignment
→ mode-specific validation
→ финальный отчет
```

## Как проверять отчет

Deep report по умолчанию:

```powershell
py -3 scripts/validate_report.py outputs/sector/example-report.md
```

Явный режим:

```powershell
py -3 scripts/validate_report.py --mode deep outputs/sector/example-report.md
py -3 scripts/validate_report.py --mode standard outputs/sector/example-report.md
py -3 scripts/validate_report.py --mode short outputs/sector/example-report.md
```

Запуск всех eval fixtures:

```powershell
py -3 scripts/run_evals.py
```

Отчет не стоит считать готовым, пока он не проходит валидатор для выбранного режима и человеческую инвестиционную проверку.
