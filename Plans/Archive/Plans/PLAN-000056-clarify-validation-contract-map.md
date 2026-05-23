# PLAN-000056 — Clarify validation contract map

ID: PLAN-000056
Название: Пересобрать contract map validation-layer
Статус: Завершено
Связи: BACK-000068
Источник: Следующий узкий pass этапа `ROAD-000011`
Дата_создания: 2026-04-08
Дата_изменения: 2026-04-08
Основание: `Validation.md` уже ввёл границы validation-layer, но пока остаётся boundary-document. Нужен отдельный узкий pass, который пересоберёт его в contract map validation-layer: зафиксирует inputs, outputs, classes validation result, ownership интерпретации, отношение к evidence package, место в pass-close contour и границу между validation result и gate decision без запуска нового toolchain.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000068
Связанные_ADR:
- отсутствуют

## Шаги
1. Синхронизировать planning-contour под новый validation pass.
   - Описание: Оставить `ROAD-000011` активным, создать одну реальную backlog-задачу и один новый current `Plan`, а предыдущий завершённый `Plan` вывести в archive.
   - DoD: `ROAD-000011`, `BACK-000068` и `PLAN-000056` согласованы как текущий stage/task/pass.
2. Провести audit validation contract perimeter.
   - Описание: Проверить `Validation.md`, `Verification.md`, `Verification_Evidence.md`, `Artifact_Lifecycle.md`, `Pipeline/Phase_Gates.md` и `Tools/README.md` только на реальные противоречия по границам между validation, verification, evidence и gate contour.
   - DoD: зафиксировано, какие validation assumptions уже есть в системе и какие линии нужно сделать явными в contract map.
3. Пересобрать `Docs/Technical/Validation.md` как contract map validation-layer.
   - Описание: Явно описать validation inputs/outputs, classes validation result, ownership интерпретации, отношение к evidence package, место в pass-close contour и границу с gate decision.
   - DoD: читателю ясно, как validation работает как системный contract и что он не подменяет.
4. Подтвердить минимальный contract impact.
   - Описание: Проверить, нужны ли точечные updates в `Verification.md`, `Verification_Evidence.md`, `Docs/Technical/README.md`, `Pipeline/Phase_Gates.md`, `Tools/README.md` или `bp_lint.py`.
   - DoD: меняются только реально противоречащие линии; tooling не реализуется.
5. Закрыть pass governance-сверкой.
   - Описание: Перевести backlog-задачу и `Plan` в финальные статусы только после согласования индекса backlog, `ROAD-000011`, текущего `Plan` и self-check.
   - DoD: `BACK-000068`, индекс backlog, `ROAD-000011`, `PLAN-000056` и self-check полностью согласованы.

## Ограничения
- без реализации `bp_check / bp_verify`;
- без рефакторинга всего `Tools/*`;
- без открытия `ROAD-000012`;
- без широкого переписывания `Docs/Technical/*`.

## Риски
- если validation останется только boundary-doc, следующий pass снова смешает validation result, evidence sufficiency и gate input;
- если validation result classes останутся неявными, локальный close и gate handoff будут трактоваться по-разному;
- если расширить scope до нового toolchain, pass потеряет узость и превратится в tooling redesign.

## Артефакты
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/Archive/Plans/PLAN-000056-clarify-validation-contract-map.md`
- `Plans/Archive/Plans/PLAN-000055-define-validation-boundaries.md`
- `Docs/Technical/Validation.md`
- `Docs/Technical/Verification.md`
- `Docs/Technical/Verification_Evidence.md`
- `Docs/Technical/README.md`
- `Docs/Technical/Artifact_Lifecycle.md`
- `Pipeline/Phase_Gates.md`
- `Tools/README.md`

## DoD
- `ROAD-000011` остаётся в `В_работе`.
- создана одна узкая задача этого pass.
- создан один current `Plan`.
- `Validation.md` фиксирует contract map validation-layer.
- `python3 Tools/bp_lint.py --repo .` проходит.

## Результат
- `Docs/Technical/Validation.md` пересобран из boundary-doc в contract map validation-layer: document теперь явно фиксирует validation inputs, outputs, verdict classes, ownership интерпретации, отношение к evidence package и место в pass-close contour.
- `Docs/Technical/Verification.md` минимально синхронизирован, чтобы развести verification contract map и validation contract map.
- `Docs/Technical/README.md` минимально синхронизирован, чтобы описывать `Validation.md` уже как contract map, а не как boundary-only document.
- `Verification_Evidence.md`, `Artifact_Lifecycle.md`, `Pipeline/Phase_Gates.md`, `Tools/README.md` и `bp_lint.py` не менялись, потому что audit не подтвердил реального противоречия или contract impact.
- `bp_lint contract unaffected`
