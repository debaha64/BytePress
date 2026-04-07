# PLAN-000051 — Clarify verification contract map

ID: PLAN-000051
Название: Пересобрать contract map verification-layer
Статус: В_работе
Связи: BACK-000063
Источник: Следующий узкий pass этапа `ROAD-000011`
Дата_создания: 2026-04-07
Дата_изменения: 2026-04-07
Основание: Boundary-pass уже активировал `ROAD-000011` и ввёл `Docs/Technical/Verification.md`, но verification-layer пока описан только как слой границ. Нужен следующий узкий pass, который превратит document в contract map с явными классами checks, inputs/outputs, evidence и ownership результата без создания нового toolchain.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000063
Связанные_ADR:
- отсутствуют

## Шаги
1. Синхронизировать planning-contour под новый verification pass.
   - Описание: Оставить `ROAD-000011` активным, создать одну реальную backlog-задачу и один новый current `Plan`, а предыдущий завершённый `Plan` вывести в archive.
   - DoD: `ROAD-000011`, `BACK-000063` и `PLAN-000051` согласованы как текущий stage/task/pass.
2. Провести audit verification contract perimeter.
   - Описание: Проверить `Verification.md`, `Artifact_Lifecycle.md`, `Platform_Contracts.md`, `Pipeline/Phase_Gates.md` и `bp_lint.py` только на реальные противоречия между checks contour, evidence и ownership результата.
   - DoD: зафиксировано, какие части verification-layer должны быть описаны в contract map, а какие остаются в `Pipeline/*` и `Tools/*`.
3. Пересобрать `Docs/Technical/Verification.md` как contract map.
   - Описание: Явно описать классы checks, verification inputs/outputs, evidence формы, ownership интерпретации результата и место verification result в pass-close contour.
   - DoD: читателю ясно, где verification заканчивается и начинается gate, а также кто владеет evidence и решением по результату.
4. Подтвердить минимальный contract impact.
   - Описание: Проверить, нужны ли точечные updates в `Artifact_Lifecycle.md`, `Pipeline/Phase_Gates.md`, `Docs/Technical/README.md` или `bp_lint.py`.
   - DoD: меняются только реально противоречащие линии; tooling не рефакторится.
5. Закрыть pass governance-сверкой.
   - Описание: Перевести backlog-задачу и `Plan` в финальные статусы только после согласования индекса backlog, `ROAD-000011`, текущего `Plan` и self-check.
   - DoD: `BACK-000063`, индекс backlog, `ROAD-000011`, `PLAN-000051` и self-check полностью согласованы.

## Ограничения
- без `bp_check / bp_verify`;
- без рефакторинга всего `Tools/*`;
- без открытия `ROAD-000012`;
- без широкого переписывания `Docs/Technical/*`.

## Риски
- если verification contract map останется неполным, future checks work снова смешает evidence, ownership результата и process approval;
- если перенести в `Verification.md` gate policy или tooling implementation, pass создаст новое пересечение с `Pipeline/*` и `Tools/*`;
- если расширить `bp_lint.py` без доказанной необходимости, verification pass превратится в toolchain redesign.

## Артефакты
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/PLAN-000051-clarify-verification-contract-map.md`
- `Plans/Archive/PLAN-000050-activate-road-000011-verification-boundaries.md`
- `Docs/Technical/Verification.md`
- `Docs/Technical/Artifact_Lifecycle.md`
- `Docs/Technical/Platform_Contracts.md`
- `Pipeline/Phase_Gates.md`
- `Tools/bp_lint.py`

## DoD
- `ROAD-000011` остаётся в `В_работе`.
- создана одна узкая задача этого pass.
- создан один current `Plan`.
- `Verification.md` фиксирует contract map verification-layer.
- `python3 Tools/bp_lint.py --repo .` проходит.

## Результат
- В работе.
