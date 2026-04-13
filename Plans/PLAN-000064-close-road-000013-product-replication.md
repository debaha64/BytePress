# PLAN-000064 — Close ROAD-000013 product replication

ID: PLAN-000064
Название: Закрыть `ROAD-000013` и довести bootstrap до first-usable replicated product repo
Статус: В_работе
Связи: BACK-000076
Источник: Новый stage-closing pass этапа `ROAD-000013`
Дата_создания: 2026-04-13
Дата_изменения: 2026-04-13
Основание: `ROAD-000013` должен быть закрыт одним pass: bootstrap/replication contract всё ещё materialize лишь minimal skeleton, а не first-usable replicated product repo, активный baseline `BytePress` ещё несёт operational references на `0.1.0`, а workflow продолжает шуметь из-за `.codex`, не игнорируемого `.gitignore`. Нужен один stage-closing pass, который активирует и затем, при clean audit, закрывает `ROAD-000013` без открытия `ROAD-000014`.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000076
Связанные_ADR:
- отсутствуют

## Шаги
1. Активировать `ROAD-000013` как текущий этап.
   - Описание: Обновить `Roadmap` и `Backlog`, создать одну новую backlog-задачу и один current `Plan`, а завершённый `PLAN-000063` вывести в archive-layer.
   - DoD: `ROAD-000013`, `BACK-000076` и `PLAN-000064` согласованы как текущий stage/task/pass.
2. Довести bootstrap/replication contract до first-usable outcome.
   - Описание: Обновить `Product_Bootstrap_Contract.md`, `Product_Bootstrap_Validation.md`, `Tools/README.md`, `Tools/bp_bootstrap.py` и при необходимости `Tools/bp_lint.py`, чтобы bootstrap materialize replicated product repo с minimal human/agent entry contour, first current stage/task/pass и usable project scripts без превращения продукта в копию `BytePress`.
   - DoD: contract, materializer и structural checks не спорят о target outcome.
3. Синхронизировать active non-log baseline `0.2.0`.
   - Описание: Обновить только те active non-log owner-documents, где `0.1.0` ещё означает текущий operational contract, а также закрыть `.codex` noise, если `.gitignore` действительно имел gap.
   - DoD: active baseline references и workflow noise больше не спорят с текущим stage scope.
4. Выполнить реальный smoke bootstrap и structural validation replicated repo.
   - Описание: Materialize product repo во временный target path вне дерева `BytePress`, затем выполнить `python3 Tools/bp_lint.py --repo <generated-product-repo>`.
   - DoD: generated product repo проходит updated structural contract.
5. Провести финальный audit и закрыть stage.
   - Описание: Проверить active contracts, planning sync, smoke bootstrap result и residual workflow defects; если residual gap не подтверждён, перевести `ROAD-000013` в `Завершено` и вывести stage backlog в archive-layer без активации `ROAD-000014`.
   - DoD: planning-layer, bootstrap tooling и replicated repo outcome не спорят о состоянии `ROAD-000013`.
