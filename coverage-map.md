# Coverage Map

Карта показывает, где требования исходного промпта отражены в структуре агента.

| Требование исходного промпта | Где отражено | Статус |
|---|---|---|
| Анализ должен помогать инвестиционному решению | `agent.md`, `docs/workflow.md` | Покрыто |
| Принцип Парето: фокус на 20% факторов | `agent.md`, `docs/validation-rubric.md` | Покрыто |
| 8 обязательных вопросов | `agent.md` | Покрыто |
| Короткий вердикт по сектору | `agent.md`, `templates/sector-analysis-template.md` | Покрыто |
| Описание бизнес-модели и сегментов | `agent.md`, `templates/sector-analysis-template.md` | Покрыто |
| Размер рынка, TAM / SAM / SOM и рост | `agent.md`, `templates/sector-analysis-template.md`, `docs/source-policy.md` | Покрыто |
| Разделение роста на структурный, циклический и временный | `agent.md`, `templates/sector-analysis-template.md` | Покрыто |
| 3–5 ключевых драйверов | `agent.md`, `docs/validation-rubric.md` | Покрыто |
| Цепочка поставок и цепочка создания стоимости | `agent.md`, `templates/sector-analysis-template.md` | Покрыто |
| Profit pool | `agent.md`, `docs/workflow.md`, `templates/sector-analysis-template.md` | Покрыто |
| Конкурентная среда и ключевые игроки | `agent.md`, `templates/sector-analysis-template.md` | Покрыто |
| Экономика сектора и релевантные метрики | `agent.md`, `templates/sector-analysis-template.md` | Покрыто |
| Контекст оценки сектора | `agent.md`, `templates/sector-analysis-template.md` | Покрыто |
| Что уже заложено в цену | `agent.md`, `templates/sector-analysis-template.md` | Покрыто |
| Бенефициары, зависимости, эффекты второго порядка | `agent.md`, `templates/sector-analysis-template.md` | Покрыто |
| Возможности, риски и катализаторы | `agent.md`, `templates/sector-analysis-template.md` | Покрыто |
| Карта подсекторов | `agent.md`, `templates/sector-analysis-template.md` | Покрыто |
| Инвестиционная карта сектора | `agent.md`, `templates/sector-analysis-template.md` | Покрыто |
| Ранжирование инвестиционных возможностей | `agent.md`, `templates/sector-analysis-template.md` | Покрыто |
| Анти-тезис | `agent.md`, `docs/validation-rubric.md` | Покрыто |
| Метрики мониторинга | `agent.md`, `templates/sector-analysis-template.md`, `scripts/validate_report.py` | Покрыто |
| Финальный вывод ровно в 8 предложениях | `agent.md`, `docs/validation-rubric.md`, `scripts/validate_report.py` | Покрыто |
| Сильные вопросы в конце | `agent.md`, `templates/sector-analysis-template.md` | Покрыто |
| Требования к данным и источникам | `docs/source-policy.md`, `docs/parsing-policy.md` | Покрыто |
| Указывать дату анализа | `agent.md`, `templates/sector-analysis-template.md`, `scripts/validate_report.py` | Покрыто |
| Не писать отчет на 100 страниц | `agent.md`, `docs/validation-rubric.md` | Покрыто |
| Каждый блок заканчивать мини-выводом | `agent.md`, `templates/sector-analysis-template.md` | Покрыто |

## Что нужно проверить вручную

## Дополнительное покрытие после усиления агента

| Требование | Где отражено | Статус |
|---|---|---|
| Роль: секторный аналитик + инвестор + риск-менеджер | `agent.md` | Покрыто |
| Тип объекта анализа | `agent.md`, `templates/sector-analysis-template.md`, `scripts/validate_report.py` | Покрыто |
| Горизонты 1–3 месяца / 3–12 месяцев / 1–5 лет | `agent.md`, `docs/workflow.md`, `templates/sector-analysis-template.md`, `scripts/validate_report.py` | Покрыто |
| Data-first evidence table | `agent.md`, `docs/workflow.md`, `templates/sector-analysis-template.md`, `scripts/validate_report.py` | Покрыто |
| Свежесть данных и даты публикации / доступа | `docs/source-policy.md`, `docs/reviewer-checklist.md`, `scripts/validate_report.py` | Покрыто |
| Tier 1 / Tier 2 / Tier 3 метрики | `agent.md`, `templates/sector-analysis-template.md`, `docs/validation-rubric.md`, `scripts/validate_report.py` | Покрыто |
| Факт / Интерпретация / Допущение | `agent.md`, `docs/reviewer-checklist.md`, `scripts/validate_report.py` | Покрыто |
| Confidence level | `agent.md`, `templates/sector-analysis-template.md`, `docs/validation-rubric.md`, `scripts/validate_report.py` | Покрыто |
| Anti-hallucination gate | `agent.md`, `docs/reviewer-checklist.md`, `docs/validation-rubric.md` | Покрыто |

После вставки полного текста в `original_prompt.md` желательно пройтись по нему и добавить сюда любые требования, которые не попали в карту.
## v1 stabilization coverage

| Требование | Где отражено | Статус |
|---|---|---|
| Единый контракт отчета | `configs/report_contract.yaml`, `scripts/validate_report.py` | Покрыто |
| Режимы short / standard / deep | `configs/report_contract.yaml`, `agent.md`, `README.md`, `docs/workflow.md` | Покрыто |
| Mode-specific validation | `scripts/validate_report.py`, `docs/validation-rubric.md`, `docs/reviewer-checklist.md` | Покрыто |
| Актуальный standard skeleton | `examples/example-output-skeleton.md` | Покрыто |
| Исполняемые pass/fail evals | `evals/fixtures/`, `scripts/run_evals.py` | Покрыто |
| Сценарии отдельно от fixtures | `evals/scenarios/` | Покрыто |
| Canonical evidence schema | `configs/report_contract.yaml`, `docs/parsing-policy.md` | Покрыто |

