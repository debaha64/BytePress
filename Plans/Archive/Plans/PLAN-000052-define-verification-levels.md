# PLAN-000052 — Define verification levels

ID: PLAN-000052
Название: Зафиксировать verification levels и target automation split
Статус: Завершено
Связи: BACK-000064
Источник: Следующий узкий pass этапа `ROAD-000011`
Дата_создания: 2026-04-07
Дата_изменения: 2026-04-07
Основание: `Verification.md` уже держит boundaries и contract map verification-layer, но уровни verification-контура и target split будущих `bp_check / bp_verify` ещё не выделены в отдельный supporting document. Нужен узкий pass, который введёт `Docs/Technical/Verification_Levels.md` и разведёт уровни checks, evidence и automation boundaries без реализации toolchain.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000064
Связанные_ADR:
- отсутствуют

## Шаги
1. Синхронизировать planning-contour под новый verification pass.
   - Описание: Оставить `ROAD-000011` активным, создать одну реальную backlog-задачу и один новый current `Plan`, а предыдущий завершённый `Plan` вывести в archive.
   - DoD: `ROAD-000011`, `BACK-000064` и `PLAN-000052` согласованы как текущий stage/task/pass.
2. Провести audit verification levels perimeter.
   - Описание: Проверить `Verification.md`, `Platform_Contracts.md`, `Artifact_Lifecycle.md`, `Pipeline/Phase_Gates.md`, `Tools/README.md` и `bp_lint.py` только на реальные противоречия между уровнями verification и target automation split.
   - DoD: зафиксировано, какие части verification contour должны войти в новый документ, а какие остаются в `Pipeline/*` и `Tools/*`.
3. Ввести `Docs/Technical/Verification_Levels.md`.
   - Описание: Создать singleton technical document на базе `Templates/Document.md` и описать уровни verification, evidence, ownership результата и target split будущих `bp_check / bp_verify`.
   - DoD: читателю ясно, что автоматизируется в будущем, что остаётся procedural, а что не должно автоматизироваться.
4. Подтвердить минимальный contract impact.
   - Описание: Проверить, нужны ли точечные updates в `Verification.md`, `Artifact_Lifecycle.md`, `Pipeline/Phase_Gates.md`, `Docs/Technical/README.md`, `Tools/README.md` или `bp_lint.py`.
   - DoD: меняются только реально противоречащие линии; tooling не реализуется.
5. Закрыть pass governance-сверкой.
   - Описание: Перевести backlog-задачу и `Plan` в финальные статусы только после согласования индекса backlog, `ROAD-000011`, текущего `Plan` и self-check.
   - DoD: `BACK-000064`, индекс backlog, `ROAD-000011`, `PLAN-000052` и self-check полностью согласованы.

## Ограничения
- без реализации `bp_check / bp_verify`;
- без рефакторинга всего `Tools/*`;
- без открытия `ROAD-000012`;
- без широкого переписывания `Docs/Technical/*`.

## Риски
- если уровни verification останутся неявными, future tooling снова смешает structural checks, procedural review и gate input;
- если target split `bp_check / bp_verify` будет зафиксирован как implementation вместо contract, pass откроет преждевременный redesign `Tools/*`;
- если расширить `bp_lint.py` без доказанной необходимости, pass превратится в toolchain change вместо contract pass.

## Артефакты
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/PLAN-000052-define-verification-levels.md`
- `Plans/Archive/Plans/PLAN-000051-clarify-verification-contract-map.md`
- `Docs/Technical/Verification.md`
- `Docs/Technical/Verification_Levels.md`
- `Docs/Technical/Platform_Contracts.md`
- `Docs/Technical/Artifact_Lifecycle.md`
- `Pipeline/Phase_Gates.md`
- `Tools/README.md`
- `Tools/bp_lint.py`

## DoD
- `ROAD-000011` остаётся в `В_работе`.
- создана одна узкая задача этого pass.
- создан один current `Plan`.
- `Verification_Levels.md` фиксирует уровни verification-контура и target contract будущих `bp_check / bp_verify`.
- `python3 Tools/bp_lint.py --repo .` проходит.

## Результат
- `Docs/Technical/Verification_Levels.md` создан как supporting technical document уровней verification-контура и target split будущих `bp_check / bp_verify`.
- `Docs/Technical/Verification.md` минимально синхронизирован ссылкой на level-specific document, а `Docs/Technical/README.md` обновлён в карте supporting documents.
- `Artifact_Lifecycle.md`, `Pipeline/Phase_Gates.md`, `Tools/README.md` и `bp_lint.py` не менялись, потому что audit не подтвердил реального противоречия или contract impact.
- `bp_lint contract unaffected`
