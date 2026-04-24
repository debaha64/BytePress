# Discovery

`Docs/Discovery/` хранит аналитическое долговременное знание о продукте и системе до перехода в плановый и исполнительный контур.

## Current-truth owner
- `Interview.md` — owner текущей аналитической истины.

## Активный состав BytePress
- `Discussion.md` — канонический документ входной аналитической фазы до `Interview`, `Research` и `Requirements`.
- `Interview.md` — канонический текущий документ с вопросами и актуальными ответами.
- `Research.md` — канонический документ фазы проверки фактов, ограничений, вариантов и зависимостей после `Discussion`.
- `Requirements.md` — канонический документ перевода результатов `Discussion` и `Research` в обязательные требования и границы следующего этапа.

## Bootstrap minimum для generated product repo
- В раннем product-start contour bootstrap materialize только `Docs/Discovery/README.md` и `Docs/Discovery/Interview.md`.
- Это не противоречит active discovery-layer самого `BytePress`: generated repo получает только minimum current-truth route до отдельного открытия `Discussion`, `Research` и `Requirements`.
- Bootstrap-created product interview стартует в состоянии `Статус_текущей_истины: Не_подтверждена`.
- Пока пользователь не дал явные ответы и current truth не подтверждена, generated repo остаётся в discovery-only contour: это не разрешает переход к `Docs/Product/*`, `Docs/Technical/*`, `Runtime/*`, `scripts/*` или предметной реализации.
- Даже в discovery-only contour первый writable action generated product repo допускается только после открытия рабочей ветки; это относится и к `Docs/Discovery/*`, `Plans/*` и `Logs/*`.
- Failed product-start закрывается через product-side reset/cleanup route, а не через молчаливую трактовку bootstrap placeholders как утверждённого scope.

## Interview protocol
- owner протокола интервью один: `Docs/Discovery/Interview.md`;
- `README.md`, `Skills/Interview.md` и `Templates/Interview.md` дают только короткие выдержки и ссылки, но не дублируют весь протокол;
- вопросы первого прохода собираются в пять смысловых классов: `Контекст`, `Граница`, `Ограничение`, `Владение`, `Переход`;
- если вопрос из соседнего рабочего потока блокирует следующий шаг, он задаётся сразу в интервью;
- если вопрос не блокирует ранний проход, он накапливается для следующей фазы, а не раздувает стартовое интервью.

## Будущее расширение
В следующих проходах сюда могут входить дополнительные discovery-артефакты, если они будут отдельно зафиксированы в системе, обеспечены шаблоном и введены отдельным pass.

В рамках текущего состояния `Discussion.md`, `Research.md` и `Requirements.md` уже введены как рабочие discovery-документы.
