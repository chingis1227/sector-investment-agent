# Scenario: Stale Sources

## User request

Сделай standard-анализ сектора дата-центров, где ключевой market size источник старше релевантного цикла.

## Expected behavior

- Агент помечает источник как stale или potentially stale.
- Агент не ставит high confidence, если stale data поддерживают ключевой тезис.
- Агент указывает, какие свежие данные нужны для повышения уверенности.

## Fail conditions

- Stale data подаются как fresh.
- Итоговый вывод звучит уверенно без freshness limitation.
- Валидатор не ловит high confidence при stale / unknown data.
