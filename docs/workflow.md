# Workflow

## Pipeline

```text
Intake
→ Object + Horizon Lock
→ Source Plan
→ Evidence Collection
→ Freshness Check
→ Tiered Metrics Map
→ Analysis
→ Anti-thesis / Counterargument Check
→ Confidence Assignment
→ Validation
→ Final Output
```

Если свежесть данных не проверена, итоговый вывод не может иметь высокий уровень уверенности.


## Report mode lock

На этапе Intake агент должен зафиксировать `report_mode`:

- `deep` — полный 18-секционный отчет;
- `standard` — компактный инвестиционный отчет с evidence, sources, confidence, anti-thesis и monitoring metrics;
- `short` — 6-блочный ответ с источниками, свежестью, confidence и ограничениями.

Правила режимов находятся в `configs/report_contract.yaml`. Validation state должен проверять отчет по выбранному режиму, а не всегда требовать 18 секций.

## 0. Intake

Собрать входные параметры:

- sector;
- object type: sector / subsector / company basket / ETF / theme / catalyst;
- geography;
- horizon;
- report_mode: short / standard / deep;
- target: обзор сектора / поиск идей / сравнение подсекторов / анализ конкретных компаний.

Если сектор, тип объекта, география или горизонт не указаны, сделай разумное предположение и явно напиши его. Задавай уточняющий вопрос только если без него анализ станет рискованно неверным.

## 1. Object + Horizon Lock

Зафиксировать:

- что именно анализируется и что исключено;
- основной горизонт;
- различаются ли выводы на 1–3 месяца, 3–12 месяцев и 1–5 лет;
- какие данные особенно важны для выбранного горизонта.

## 2. Research plan

Составить короткий план источников:

1. filings и отчеты топ-компаний;
2. отраслевые и государственные данные;
3. рыночные оценки и мультипликаторы;
4. новости и катализаторы за последние 3–12 месяцев;
5. дополнительные источники для проверки противоречий.

## 3. Data collection

Собрать только данные, необходимые для инвестиционного решения, в evidence table:

| Метрика | Tier | Значение | Период наблюдения | Дата публикации | Дата доступа | Источник | Свежесть | Надежность |
|---|---|---:|---|---|---|---|---|---|

- market size;
- growth;
- segment mix;
- unit economics;
- margin / ROIC context;
- supply-demand balance;
- valuation multiples;
- revisions / guidance;
- key catalysts.

## 4. Freshness Check

Проверить:

- дата наблюдения соответствует анализируемому периоду;
- дата публикации указана для отчетности, статистики и исследований;
- дата доступа указана для веб-источников;
- рыночные данные, мультипликаторы, новости и ETF holdings являются максимально свежими доступными;
- устаревшие данные помечены как `stale` или `potentially stale`.

Если свежесть ключевого источника неизвестна, снизить confidence и раскрыть ограничение.

## 5. Tiered Metrics Map

Разделить данные на:

- Tier 1 — напрямую влияет на вывод;
- Tier 2 — подтверждает или уточняет Tier 1;
- Tier 3 — контекст, риски, новости и sentiment.

Сильный вывод не должен основываться только на Tier 3. Если это невозможно, пометить вывод как гипотезу / допущение.

## 6. Analysis

Применить фильтр:

`Does this affect growth, margin, ROIC, risk, valuation, moat, catalysts, or investment action?`

Если нет — удалить или перенести в ограничения.

Построить причинную цепочку:

`драйвер → profit pool → компания / подсектор → оценка → риск → инвестиционное действие`.

## 7. Anti-thesis / Counterargument Check

Сформулировать самый сильный контраргумент:

- какой факт или метрика ломает тезис;
- какой риск имеет наибольшую вероятность / impact;
- что рынок может уже учитывать в цене;
- какие условия требуют смены вывода.

## 8. Confidence Assignment

Сделать выводы:

- sector attractiveness;
- primary driver;
- primary risk;
- structural / cyclical / temporary nature;
- profit pool;
- best beneficiaries;
- what is priced in;
- next action.

Присвоить каждому ключевому выводу уверенность:

- высокая — свежие Tier 1 данные и первичные / официальные источники;
- средняя — данные надежные, но есть пробелы или конфликтующие оценки;
- низкая — данные устаревшие, неполные, вторичные или основаны на Tier 3.

## 9. Validation

Проверить результат по `docs/validation-rubric.md`, `docs/reviewer-checklist.md` для глубоких отчетов и `scripts/validate_report.py`, если отчет сохранен в файл.

## 10. Output

Выдать отчет в формате из `AGENTS.md`. Если данных недостаточно, не заполнять пробелы выдумками: явно назвать missing data, уровень уверенности и следующий шаг.

---

# State Machine

## State 1: Intake

- Input: пользовательский запрос.
- Output: sector, object type, geography, horizon, report_mode, target, known tickers / ETFs, assumptions.
- Next step: Object + Horizon Lock.
- Error condition: сектор невозможно определить или запрос требует персональной инвестиционной рекомендации без аналитического контекста.
- Required response: запросить уточнение или переформулировать задачу в аналитический формат.

## State 2: Object + Horizon Lock

- Input: параметры из Intake.
- Output: scope, exclusions, primary horizon, horizon split и ограничения.
- Next step: Source Plan.
- Error condition: горизонт противоречит цели анализа или объект слишком широк без карты подсекторов.
- Required response: раскрыть допущение или сузить scope.

## State 3: Source Plan

- Input: scope и horizon split.
- Output: список нужных типов источников и приоритет поиска по `docs/source-policy.md`.
- Next step: Evidence Collection.
- Error condition: для сектора нет достаточных публичных источников или источники не соответствуют географии / горизонту.
- Required response: указать ограничение данных и предложить, какие источники нужны для продолжения.

## State 4: Evidence Collection

- Input: source plan.
- Output: evidence items с метрикой, Tier, значением, периодом, датой публикации, датой доступа, источником, свежестью, надежностью и ограничением.
- Next step: Freshness Check.
- Error condition: данные устарели, конфликтуют, не имеют даты или основаны на одном слабом источнике.
- Required response: показать диапазон, снизить надежность вывода или пометить утверждение как допущение.

## State 5: Freshness Check

- Input: evidence items.
- Output: статус fresh / stale / potentially stale и ограничение на confidence.
- Next step: Tiered Metrics Map.
- Error condition: свежесть ключевых данных не проверена.
- Required response: запретить высокую уверенность и указать, какие данные нужно обновить.

## State 6: Tiered Metrics Map

- Input: проверенные evidence items.
- Output: Tier 1 / Tier 2 / Tier 3 карта метрик и вес данных.
- Next step: Analysis.
- Error condition: ключевой вывод держится на Tier 3.
- Required response: снизить confidence или переписать тезис как гипотезу.

## State 7: Analysis

- Input: tiered metrics.
- Output: выводы по бизнес-модели, росту, profit pool, конкуренции, unit economics, valuation, рискам и катализаторам.
- Next step: Anti-thesis / Counterargument Check.
- Error condition: вывод не следует из фактов, нет причинной цепочки или valuation оторван от качества бизнеса.
- Required response: переписать анализ через цепочку `драйвер → profit pool → компания / подсектор → оценка → риск → инвестиционное действие`.

## State 8: Anti-thesis / Counterargument Check

- Input: черновой тезис.
- Output: anti-thesis, risk triggers и метрики, которые ломают вывод.
- Next step: Confidence Assignment.
- Error condition: anti-thesis формальный и не атакует главный тезис.
- Required response: усилить контраргумент.

## State 9: Confidence Assignment

- Input: анализ, источники, свежесть и anti-thesis.
- Output: уровень уверенности и причины.
- Next step: Validation.
- Error condition: высокая уверенность при stale / missing data или Tier 3 основе.
- Required response: снизить confidence.

## State 10: Validation

- Input: черновик отчета.
- Output: pass / fail по validation rubric, self-check и reviewer checklist для глубоких отчетов.
- Next step: Final Output, если pass; возврат к Analysis или Evidence Collection, если fail.
- Error condition: отсутствуют источники, даты, Tier-метрики, confidence, anti-thesis, monitoring metrics, 8 предложений итогового вывода или ключевые секции.
- Required response: исправить отчет до финальной выдачи.

## State 11: Final Output

- Input: проверенный отчет.
- Output: финальный ответ в формате `AGENTS.md` или короткий формат, если пользователь явно попросил кратко.
- Next step: завершение.
- Error condition: полная проверка невозможна из-за нехватки данных.
- Required response: явно указать missing data, надежность вывода, confidence и следующий шаг для проверки тезиса.

