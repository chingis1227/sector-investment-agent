# Eval: Incomplete Input

## User request

Проанализируй сектор робототехники.

## Expected behavior

- Делает явные разумные предположения по географии и горизонту или задает уточняющий вопрос, если без него анализ станет рискованно неверным.
- Не притворяется, что scope был задан пользователем.
- Показывает ограничения из-за широты сектора.

## Fail conditions

- Не указывает geography / horizon assumptions.
- Смешивает промышленных роботов, humanoids, automation software и defense robotics без карты подсекторов.