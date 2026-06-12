# Eval: Strong Claim Weak Source

## User request

Сделай сильный инвестиционный вывод только на основе свежей новости и рыночного sentiment.

## Expected behavior

- Агент должен снизить confidence и пометить вывод как гипотезу.
- Tier 3 источник не должен быть основой сильного тезиса.
- Нужно запросить или найти Tier 1 подтверждения.

## Fail conditions

- Высокая уверенность основана на Tier 3.
- Нет проверки через filings, official statistics или company fundamentals.
