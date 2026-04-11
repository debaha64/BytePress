# PLAN-000059 — Define validation tooling boundary

ID: PLAN-000059
Название: Зафиксировать tooling boundary validation-контура
Статус: Завершено
Связи: BACK-000071
Источник: Следующий узкий pass этапа `ROAD-000011`
Дата_создания: 2026-04-11
Дата_изменения: 2026-04-11
Основание: `Validation.md`, `Validation_Levels.md` и `Validation_Evidence.md` уже развели validation-layer, его уровни и evidence contract, но `Tools/README.md` пока описывает tooling boundary только для verification contour. Нужен узкий pass, который зафиксирует роль tooling в validation, разведёт validation tooling, verification tooling и procedural validation, а также удержит границу между validation result и gate decision без реализации нового validation toolchain.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000071
Связанные_ADR:
- отсутствуют

## Шаги
1. Синхронизировать planning-contour под новый validation-tooling pass.
   - Описание: Оставить `ROAD-000011` активным, создать одну реальную backlog-задачу и один новый current `Plan`, а предыдущий завершённый `Plan` вывести в archive.
   - DoD: `ROAD-000011`, `BACK-000071` и `PLAN-000059` согласованы как текущий stage/task/pass.
2. Провести audit validation tooling perimeter.
   - Описание: Проверить `Validation.md`, `Validation_Levels.md`, `Validation_Evidence.md`, `Verification_Levels.md`, `Pipeline/Phase_Gates.md`, `Tools/README.md` и `bp_lint.py` только на реальные противоречия по границам между validation tooling support, verification tooling, procedural validation и gate contour.
   - DoD: зафиксировано, какие roles должны быть описаны в tooling boundary, а какие остаются в `Docs/Technical/*`, `Pipeline/*` и governance practice.
3. Пересобрать `Tools/README.md` как boundary-document verification + validation tooling contour.
   - Описание: Явно описать роль текущего `bp_lint`, target role будущего `bp_check`, target role будущего `bp_verify`, допустимый future validation tooling horizon, запреты на automation и границы между tooling support, procedural validation и gate decision.
   - DoD: читателю ясно, что automation может только поддерживать validation contour, а verdict interpretation и gate decision остаются вне tool ownership.
4. Подтвердить минимальный contract impact.
   - Описание: Проверить, нужны ли точечные updates в `Validation.md`, `Validation_Levels.md`, `Validation_Evidence.md`, `Verification_Levels.md`, `Docs/Technical/README.md`, `Pipeline/Phase_Gates.md` или `bp_lint.py`.
   - DoD: меняются только реально противоречащие линии; новые tools не реализуются.
5. Закрыть pass через governance-сверку и self-check.
   - Описание: Перевести backlog-задачу и `Plan` в финальные статусы только после согласования индекса backlog, `ROAD-000011`, текущего `Plan` и self-check.
   - DoD: `BACK-000071`, индекс backlog, `ROAD-000011`, `PLAN-000059` и self-check полностью согласованы.

## Ограничения
- без реализации `bp_check / bp_verify` и любого validation toolchain;
- без рефакторинга всего `Tools/*`;
- без открытия `ROAD-000012`;
- без широкого переписывания `Docs/Technical/*`.

## Риски
- если tooling boundary validation-контура останется неявным, future automation снова смешает evidence support, verdict interpretation и gate decision;
- если future validation tooling будет описан как approval engine, validation result начнёт подменять procedural validation и process gates;
- если расширить `bp_lint.py` без доказанной необходимости, boundary-pass снова превратится в изменение behavior вместо contract clarification.

## Артефакты
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/PLAN-000059-define-validation-tooling-boundary.md`
- `Plans/Archive/PLAN-000058-define-validation-evidence-contract.md`
- `Tools/README.md`
- `Docs/Technical/Validation.md`
- `Docs/Technical/Validation_Levels.md`
- `Docs/Technical/Validation_Evidence.md`
- `Docs/Technical/Verification_Levels.md`
- `Docs/Technical/README.md`
- `Pipeline/Phase_Gates.md`
- `Tools/bp_lint.py`

## DoD
- `ROAD-000011` остаётся в `В_работе`.
- создана одна узкая задача этого pass.
- создан один current `Plan`.
- `Tools/README.md` фиксирует tooling boundary validation-контура без двусмысленности.
- `python3 Tools/bp_lint.py --repo .` проходит.

## Результат
- `Tools/README.md` пересобран как boundary-document verification + validation tooling contour с явным разделением роли `bp_lint`, target role будущих `bp_check / bp_verify`, допустимого future validation tooling и procedural validation.
- `Docs/Technical/Validation.md`, `Validation_Levels.md`, `Validation_Evidence.md`, `Verification_Levels.md`, `Docs/Technical/README.md`, `Pipeline/Phase_Gates.md` и `Tools/bp_lint.py` не менялись, потому что audit не подтвердил реального противоречия или contract impact.
- `bp_lint contract unaffected`
