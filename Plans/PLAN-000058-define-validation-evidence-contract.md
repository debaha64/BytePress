# PLAN-000058 — Define validation evidence contract

ID: PLAN-000058
Название: Зафиксировать contract validation evidence
Статус: В_работе
Связи: BACK-000070
Источник: Следующий узкий pass этапа `ROAD-000011`
Дата_создания: 2026-04-11
Дата_изменения: 2026-04-11
Основание: `Validation.md` и `Validation_Levels.md` уже развели validation-layer и его уровни, но пока не выделяют отдельный contract validation evidence. Нужен узкий pass, который введёт `Docs/Technical/Validation_Evidence.md` и зафиксирует classes validation evidence, их обязательность, relation к validation levels и pass-close contour без реализации validation toolchain.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000070
Связанные_ADR:
- отсутствуют

## Шаги
1. Синхронизировать planning-contour под новый validation-evidence pass.
   - Описание: Оставить `ROAD-000011` активным, создать одну реальную backlog-задачу и один новый current `Plan`, а предыдущий завершённый `Plan` вывести в archive.
   - DoD: `ROAD-000011`, `BACK-000070` и `PLAN-000058` согласованы как текущий stage/task/pass.
2. Провести audit validation evidence perimeter.
   - Описание: Проверить `Validation.md`, `Validation_Levels.md`, `Verification_Evidence.md`, `Artifact_Lifecycle.md`, `Pipeline/Phase_Gates.md` и `Tools/README.md` только на реальные противоречия по границам между validation evidence, validation levels, verification evidence и gate contour.
   - DoD: зафиксировано, какие evidence-assumptions уже есть в active contracts и какие distinctions нужно сделать явными в отдельном evidence-document.
3. Ввести `Docs/Technical/Validation_Evidence.md`.
   - Описание: Создать singleton technical document и описать classes validation evidence, mandatory/optional evidence, storage expectations, sufficient/insufficient criteria и relation к `Validation.md`, `Validation_Levels.md` и pass-close contour.
   - DoD: читателю ясно, что считается validation evidence, как оно связано с уровнями validation и что не считается evidence.
4. Подтвердить минимальный contract impact.
   - Описание: Проверить, нужны ли точечные updates в `Validation.md`, `Validation_Levels.md`, `Docs/Technical/README.md`, `Pipeline/Phase_Gates.md`, `Tools/README.md` или `bp_lint.py`.
   - DoD: меняются только реально противоречащие документы; при отсутствии противоречий фиксируется `bp_lint contract unaffected`.
5. Закрыть pass через governance-сверку и self-check.
   - Описание: Перевести backlog-задачу и `Plan` в финальные статусы только после согласования индекса backlog, `ROAD-000011`, текущего `Plan` и self-check.
   - DoD: `BACK-000070`, индекс backlog, `ROAD-000011`, `PLAN-000058` и self-check полностью согласованы.

## Ограничения
- без реализации `bp_check / bp_verify` и любого validation toolchain;
- без рефакторинга всего `Tools/*`;
- без открытия `ROAD-000012`;
- без широкого переписывания `Docs/Technical/*`.

## Риски
- если validation evidence останется неявным, relation между validation levels и pass-close contour будет трактоваться ситуативно;
- если validation evidence смешается с verification evidence, подтверждение outcome снова потеряет границу между produced checks basis и interpreted validation basis;
- если pass превратится в tooling design, он выйдет за пределы contract work.

## Артефакты
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/PLAN-000058-define-validation-evidence-contract.md`
- `Plans/Archive/PLAN-000057-define-validation-levels.md`
- `Docs/Technical/Validation_Evidence.md`
- `Docs/Technical/Validation.md`
- `Docs/Technical/Validation_Levels.md`
- `Docs/Technical/README.md`
- `Docs/Technical/Verification_Evidence.md`
- `Pipeline/Phase_Gates.md`
- `Tools/README.md`

## DoD
- `ROAD-000011` остаётся в `В_работе`.
- создана одна узкая задача этого pass.
- создан один current `Plan`.
- `Validation_Evidence.md` фиксирует contract validation evidence.
- `python3 Tools/bp_lint.py --repo .` проходит.

## Результат
- в работе
