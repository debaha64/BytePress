# PLAN-000050 — Activate ROAD-000011 verification boundaries

ID: PLAN-000050
Название: Зафиксировать границы verification-layer
Статус: В_работе
Связи: BACK-000062
Источник: Первый узкий pass этапа `ROAD-000011`
Дата_создания: 2026-04-07
Дата_изменения: 2026-04-07
Основание: После закрытия `ROAD-000010` technical-layer уже фиксирует системные контракты, но verification contour ещё не выделен как отдельный слой. Нужен boundary-pass, который активирует `ROAD-000011`, введёт `Docs/Technical/Verification.md` и разведёт verification-layer, `bp_lint.py`, procedural checks, `Pipeline` gates и tool implementation без рефакторинга инструментов.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000062
Связанные_ADR:
- отсутствуют

## Шаги
1. Активировать `ROAD-000011` как текущий этап.
   - Описание: Перевести roadmap и backlog на verification contour, создав одну реальную задачу и один новый current `Plan`.
   - DoD: `ROAD-000011`, `BACK-000062` и `PLAN-000050` согласованы как текущий stage/task/pass.
2. Провести audit verification perimeter.
   - Описание: Проверить `Artifact_Lifecycle`, `Platform_Contracts`, `Pipeline/Phase_Gates.md`, `bp_lint.py` и active planning-state только на реальные boundary contradictions.
   - DoD: зафиксировано, что verification-layer должен владеть границами checks contour, но не process gates и не tool implementation.
3. Ввести `Docs/Technical/Verification.md` как boundary-document.
   - Описание: Создать singleton technical document на базе `Templates/Document.md` и описать verification-layer, automatic/procedural checks, границы с `Pipeline` и `Tools`, а также minimal target-state для будущего `bp_check / bp_verify`.
   - DoD: читателю ясно, что verification-layer не подменяет process gates, lint implementation и planning-state.
4. Подтвердить минимальный contract impact.
   - Описание: Проверить, нужны ли updates в `Docs/Technical/README.md`, `Artifact_Lifecycle.md`, `Pipeline/Phase_Gates.md`, `Standards/Planning.md` и `bp_lint.py`.
   - DoD: меняются только реально противоречащие boundary lines; tooling не рефакторится.
5. Закрыть pass governance-сверкой.
   - Описание: Перевести backlog-задачу и `Plan` в финальные статусы только после согласования индекса backlog, `ROAD-000011`, текущего `Plan` и self-check.
   - DoD: `BACK-000062`, индекс backlog, `ROAD-000011`, `PLAN-000050` и self-check полностью согласованы.

## Ограничения
- без `bp_check / bp_verify`;
- без рефакторинга всего `Tools/*`;
- без широкого переписывания `Docs/Technical/*`;
- без открытия `ROAD-000012`.

## Риски
- если verification-layer останется неявным, future verification work снова смешает checks contour, process gates и tool implementation;
- если перенести в новый document process-canon или lifecycle ownership, pass создаст новое пересечение с `Pipeline/*` и `Artifact_Lifecycle.md`;
- если расширить `bp_lint.py` без доказанной необходимости, boundary-pass превратится в toolchain redesign.

## Артефакты
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/PLAN-000050-activate-road-000011-verification-boundaries.md`
- `Plans/Archive/PLAN-000049-audit-and-close-road-000010.md`
- `Plans/Archive/Backlog/ROAD-000010.md`
- `Docs/Technical/Verification.md`
- `Docs/Technical/README.md`
- `Docs/Technical/Artifact_Lifecycle.md`
- `Docs/Technical/Platform_Contracts.md`
- `Pipeline/Phase_Gates.md`
- `Tools/bp_lint.py`

## DoD
- `ROAD-000011` переведён в `В_работе`.
- создана одна узкая задача этого pass.
- создан один current `Plan`.
- verification-layer получил ясные границы.
- `python3 Tools/bp_lint.py --repo .` проходит.

## Результат
- в работе
