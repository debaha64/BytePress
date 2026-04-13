# PLAN-000064 — Close ROAD-000013 product replication

ID: PLAN-000064
Название: Закрыть `ROAD-000013` и довести bootstrap до first-usable replicated product repo
Статус: Завершено
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

## Риски
- если first-usable replicated repo начнёт накапливать новые governance domains без отдельного контракта, product bootstrap снова превратится в partial copy `BytePress`;
- если baseline `0.2.0` расширять в future integration layer без отдельного stage, active non-log docs снова начнут спорить о текущем operational contract;
- если structural check перестанет покрывать human/agent entry contour replicated repo, smoke bootstrap снова станет проходить формально, но не по реальному usable outcome.

## Артефакты
- `.gitignore`
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/PLAN-000064-close-road-000013-product-replication.md`
- `Plans/Archive/PLAN-000063-close-road-000012-user-entry.md`
- `Plans/Archive/Backlog/ROAD-000013.md`
- `Docs/Technical/Product_Bootstrap_Contract.md`
- `Docs/Technical/Product_Bootstrap_Validation.md`
- `Tools/README.md`
- `Tools/bp_bootstrap.py`
- `Tools/bp_lint.py`
- `Adapters/*`
- `Pipeline/*`
- `Standards/README.md`
- `Standards/Naming.md`
- `Setup_Guide.md`

## DoD
- создана одна новая backlog-задача и один новый current `Plan` для полного stage-closing pass `ROAD-000013`.
- `ROAD-000013` переведён в `В_работе`, затем в `Завершено` в пределах этого же pass.
- bootstrap/replication contract доведён до first-usable replicated product repo outcome.
- `Tools/bp_bootstrap.py` materialize outcome, согласованный с active contracts.
- `Tools/bp_lint.py` проверяет updated bootstrap-result, включая entry contour, initial planning state и `.gitignore` для `.codex`.
- выполнен реальный smoke bootstrap вне дерева `BytePress`, и structural check generated repo проходит.
- active non-log baseline `BytePress` синхронизирован с `0.2.0` только там, где `0.1.0` обозначал текущий operational contract.
- residual workflow defect с `.codex` закрыт как реальный `.gitignore` gap.
- `ROAD-000014` не активирован автоматически.

## Результат
- `bp_bootstrap.py` больше не materialize лишь minimal skeleton: generated repo получает `README.md`, `AGENTS.md`, `Setup_Guide.md`, полный минимальный `Docs/User/*` contour, adapter policy/registry, executable scripts и initial current stage/task/pass.
- `bp_lint.py` расширен до structural contract first-usable replicated repo и подтверждает не только product skeleton, но и human/agent entry contour, `.gitignore` для `.codex`, executable scripts и initial planning state.
- Реальный smoke bootstrap на отдельном target path materialize product repo, который проходит `python3 Tools/bp_lint.py --repo <generated-product-repo>` и `scripts/dev-test.sh` через `BYTEPRESS_ROOT`.
- Active non-log baseline `BytePress` синхронизирован с `0.2.0` только в owner-documents, где `0.1.0` ещё обозначал текущий operational contract.
- Финальный audit не подтвердил residual gap в scope `ROAD-000013`, поэтому stage закрыт, active backlog очищен и backlog этапа выведен в `Plans/Archive/Backlog/ROAD-000013.md`.
- `ROAD-000014` не активирован автоматически.
- `.gitignore` теперь закрывает и `.codex`, и `.codex/`.
