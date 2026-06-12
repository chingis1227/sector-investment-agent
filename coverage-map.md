# Coverage Map

Карта показывает, где требования исходного промпта отражены в структуре агента.

| Требование исходного промпта | Где отражено | Статус |
|---|---|---|
| Анализ должен помогать инвестиционному решению | `AGENTS.md`, `docs/workflow.md` | Покрыто |
| Принцип Парето: фокус на 20% факторов | `AGENTS.md`, `docs/validation-rubric.md` | Покрыто |
| 8 обязательных вопросов | `AGENTS.md` | Покрыто |
| Короткий вердикт по сектору | `AGENTS.md`, `templates/sector-analysis-template.md` | Покрыто |
| Описание бизнес-модели и сегментов | `AGENTS.md`, `templates/sector-analysis-template.md` | Покрыто |
| Размер рынка, TAM / SAM / SOM и рост | `AGENTS.md`, `templates/sector-analysis-template.md`, `docs/source-policy.md` | Покрыто |
| Разделение роста на структурный, циклический и временный | `AGENTS.md`, `templates/sector-analysis-template.md` | Покрыто |
| 3–5 ключевых драйверов | `AGENTS.md`, `docs/validation-rubric.md` | Покрыто |
| Цепочка поставок и цепочка создания стоимости | `AGENTS.md`, `templates/sector-analysis-template.md` | Покрыто |
| Profit pool | `AGENTS.md`, `docs/workflow.md`, `templates/sector-analysis-template.md` | Покрыто |
| Конкурентная среда и ключевые игроки | `AGENTS.md`, `templates/sector-analysis-template.md` | Покрыто |
| Экономика сектора и релевантные метрики | `AGENTS.md`, `templates/sector-analysis-template.md` | Покрыто |
| Контекст оценки сектора | `AGENTS.md`, `templates/sector-analysis-template.md` | Покрыто |
| Что уже заложено в цену | `AGENTS.md`, `templates/sector-analysis-template.md` | Покрыто |
| Бенефициары, зависимости, эффекты второго порядка | `AGENTS.md`, `templates/sector-analysis-template.md` | Покрыто |
| Возможности, риски и катализаторы | `AGENTS.md`, `templates/sector-analysis-template.md` | Покрыто |
| Карта подсекторов | `AGENTS.md`, `templates/sector-analysis-template.md` | Покрыто |
| Инвестиционная карта сектора | `AGENTS.md`, `templates/sector-analysis-template.md` | Покрыто |
| Ранжирование инвестиционных возможностей | `AGENTS.md`, `templates/sector-analysis-template.md` | Покрыто |
| Анти-тезис | `AGENTS.md`, `docs/validation-rubric.md` | Покрыто |
| Метрики мониторинга | `AGENTS.md`, `templates/sector-analysis-template.md`, `scripts/validate_report.py` | Покрыто |
| Финальный вывод ровно в 8 предложениях | `AGENTS.md`, `docs/validation-rubric.md`, `scripts/validate_report.py` | Покрыто |
| Сильные вопросы в конце | `AGENTS.md`, `templates/sector-analysis-template.md` | Покрыто |
| Требования к данным и источникам | `docs/source-policy.md`, `docs/parsing-policy.md` | Покрыто |
| Указывать дату анализа | `AGENTS.md`, `templates/sector-analysis-template.md`, `scripts/validate_report.py` | Покрыто |
| Не писать отчет на 100 страниц | `AGENTS.md`, `docs/validation-rubric.md` | Покрыто |
| Каждый блок заканчивать мини-выводом | `AGENTS.md`, `templates/sector-analysis-template.md` | Покрыто |

## Что нужно проверить вручную

## Дополнительное покрытие после усиления агента

| Требование | Где отражено | Статус |
|---|---|---|
| Роль: секторный аналитик + инвестор + риск-менеджер | `AGENTS.md` | Покрыто |
| Тип объекта анализа | `AGENTS.md`, `templates/sector-analysis-template.md`, `scripts/validate_report.py` | Покрыто |
| Горизонты 1–3 месяца / 3–12 месяцев / 1–5 лет | `AGENTS.md`, `docs/workflow.md`, `templates/sector-analysis-template.md`, `scripts/validate_report.py` | Покрыто |
| Data-first evidence table | `AGENTS.md`, `docs/workflow.md`, `templates/sector-analysis-template.md`, `scripts/validate_report.py` | Покрыто |
| Свежесть данных и даты публикации / доступа | `docs/source-policy.md`, `docs/reviewer-checklist.md`, `scripts/validate_report.py` | Покрыто |
| Tier 1 / Tier 2 / Tier 3 метрики | `AGENTS.md`, `templates/sector-analysis-template.md`, `docs/validation-rubric.md`, `scripts/validate_report.py` | Покрыто |
| Факт / Интерпретация / Допущение | `AGENTS.md`, `docs/reviewer-checklist.md`, `scripts/validate_report.py` | Покрыто |
| Confidence level | `AGENTS.md`, `templates/sector-analysis-template.md`, `docs/validation-rubric.md`, `scripts/validate_report.py` | Покрыто |
| Anti-hallucination gate | `AGENTS.md`, `docs/reviewer-checklist.md`, `docs/validation-rubric.md` | Покрыто |

После вставки полного текста в `original_prompt.md` желательно пройтись по нему и добавить сюда любые требования, которые не попали в карту.
## v1 stabilization coverage

| Требование | Где отражено | Статус |
|---|---|---|
| Единый контракт отчета | `configs/report_contract.yaml`, `scripts/validate_report.py` | Покрыто |
| Режимы short / standard / deep | `configs/report_contract.yaml`, `AGENTS.md`, `README.md`, `docs/workflow.md` | Покрыто |
| Mode-specific validation | `scripts/validate_report.py`, `docs/validation-rubric.md`, `docs/reviewer-checklist.md` | Покрыто |
| Актуальный standard skeleton | `examples/example-output-skeleton.md` | Покрыто |
| Исполняемые pass/fail evals | `evals/fixtures/`, `scripts/run_evals.py` | Покрыто |
| Сценарии отдельно от fixtures | `evals/scenarios/` | Покрыто |
| Canonical evidence schema | `configs/report_contract.yaml`, `docs/parsing-policy.md` | Покрыто |

