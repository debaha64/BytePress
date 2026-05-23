# PLAN-000065 — Activate ROAD-000014 integration contour

ID: PLAN-000065
Название: Активировать `ROAD-000014` и собрать controlled integration contour
Статус: Завершено
Связи: BACK-000077
Источник: Новый крупный activation pass этапа `ROAD-000014`
Дата_создания: 2026-04-13
Дата_изменения: 2026-04-13
Основание: После закрытия `ROAD-000013` у `BytePress` появился first-usable replicated product repo, но integration contour всё ещё определён неполно: `MCP/*` остаётся в режиме future-only, controlled handoff между `Adapters/*`, `MCP/*`, `Tools/*`, generated product repo и `scripts/*` не зафиксирован канонически, а generated repo не materialize отдельный minimal integration smoke route. Нужен activation pass, который вводит управляемый integration-layer без реальных внешних подключений и оставляет `ROAD-000014` активным.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000077
Связанные_ADR:
- отсутствуют

## Шаги
1. Активировать `ROAD-000014` как текущий stage.
   - Описание: Обновить `Roadmap` и `Backlog`, создать одну новую backlog-задачу и один current `Plan`, а завершённый `PLAN-000064` вывести в archive-layer.
   - DoD: `ROAD-000014`, `BACK-000077` и `PLAN-000065` согласованы как текущий stage/task/pass.
2. Зафиксировать канонический controlled integration contour.
   - Описание: Уточнить границы между `Adapters/*`, `MCP/*`, generated product repo, `scripts/*` и `Tools/*` в owner-documents technical и integration layers.
   - DoD: integration contour описан как активный и ограниченный system contract без открытия реальных внешних интеграций.
3. Materialize minimal integration smoke route для generated product repo.
   - Описание: Обновить bootstrap materialization и при необходимости tooling checks, чтобы generated repo получал отдельный integration smoke route без реальных connector runtimes.
   - DoD: generated product repo имеет deterministic route для smoke handoff к `BytePress`, а `bp_lint.py` и tooling contracts не спорят о required outcome.
4. Выполнить smoke bootstrap и audit результата.
   - Описание: Materialize product repo во временный path, затем выполнить structural lint и integration smoke route.
   - DoD: generated repo проходит `bp_lint.py` и минимальный integration smoke без сетевых зависимостей.
5. Закрыть backlog-задачу pass, не закрывая stage.
   - Описание: Провести финальный audit active contracts, завершить `BACK-000077` и `PLAN-000065`, но оставить `ROAD-000014` активным с узко сформулированным следующим фронтом.
   - DoD: planning-layer, tooling и technical contracts согласованы, а stage остаётся `В_работе`.

## Риски
- если integration contour описать слишком широко, stage превратится в future wishlist вместо управляемого active layer;
- если product repo начнёт materialize `MCP/*` или реальный connector runtime, bootstrap снова смешает source-of-truth и external integration layers;
- если smoke route останется неотличимым от обычного structural lint, integration handoff снова будет формальным, а не проверяемым.

## Артефакты
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/PLAN-000065-activate-road-000014-integration-contour.md`
- `Plans/Archive/Plans/PLAN-000064-close-road-000013-product-replication.md`
- `Docs/Technical/Architecture.md`
- `Docs/Technical/Interfaces.md`
- `Docs/Technical/Platform_Contracts.md`
- `Docs/Technical/Product_Bootstrap_Contract.md`
- `Docs/Technical/Product_Bootstrap_Validation.md`
- `MCP/*`
- `Adapters/*`
- `Tools/README.md`
- `Tools/bp_bootstrap.py`
- `Tools/bp_lint.py`
- `Tools/bp_integration_smoke.py`

## DoD
- создана одна новая backlog-задача и один новый current `Plan` для activation pass `ROAD-000014`.
- `ROAD-000014` переведён в `В_работе`.
- integration contour зафиксирован как controlled и ограниченный system contract, а не как future wishlist.
- границы между `Adapters/*`, `MCP/*`, generated product repo, `scripts/*` и `Tools/*` описаны явно.
- bootstrap materialize minimal integration smoke route без реальных внешних подключений.
- smoke bootstrap, `bp_lint.py` и integration smoke route проходят на generated repo.
- `ROAD-000014` остаётся `В_работе` после pass с узко сформулированным residual front.

## Результат
- `ROAD-000014` активирован и оставлен в статусе `В_работе` как текущий stage.
- `Docs/Technical/*`, `MCP/*`, `Adapters/*` и `Tools/README.md` теперь согласованно фиксируют controlled integration contour, границы `Adapters/*` и `MCP/*`, product-side handoff через `scripts/*` и отсутствие реальных внешних подключений в active scope.
- `Tools/bp_bootstrap.py` materialize `scripts/integration-smoke.sh`, а `Tools/bp_integration_smoke.py` и `Tools/bp_lint.py` подтверждают minimal integration smoke contour generated product repo.
- Реальный smoke bootstrap на отдельном target path подтвердил, что generated repo проходит и structural lint, и integration smoke route.
