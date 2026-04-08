# PLAN-000057 — Define validation levels

ID: PLAN-000057
Название: Зафиксировать уровни validation-контура
Статус: В_работе
Связи: BACK-000069
Источник: Следующий узкий pass этапа `ROAD-000011`
Дата_создания: 2026-04-08
Дата_изменения: 2026-04-08
Основание: `Validation.md` уже удерживает contract map validation-layer, но уровни validation пока не выделены как отдельный contract. Нужен узкий pass, который введёт `Docs/Technical/Validation_Levels.md` и зафиксирует уровни validation, их цель, required inputs, expected outputs, relation к evidence package и к pass-close contour без реализации validation toolchain.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000069
Связанные_ADR:
- отсутствуют

## Шаги
1. Синхронизировать planning-contour под новый validation-levels pass.
   - Описание: Оставить `ROAD-000011` активным, создать одну реальную backlog-задачу и один новый current `Plan`, а предыдущий завершённый `Plan` вывести в archive.
   - DoD: `ROAD-000011`, `BACK-000069` и `PLAN-000057` согласованы как текущий stage/task/pass.
2. Провести audit validation levels perimeter.
   - Описание: Проверить `Validation.md`, `Verification_Evidence.md`, `Artifact_Lifecycle.md`, `Docs/Technical/README.md` и `Tools/README.md` только на реальные противоречия между validation levels, evidence package, pass-close contour и verification levels.
   - DoD: зафиксировано, какие distinctions уже подразумеваются contracts и что нужно сделать явным в новом level-document.
3. Ввести `Docs/Technical/Validation_Levels.md`.
   - Описание: Создать singleton technical document на базе `Templates/Document.md` и описать уровни validation, их назначение, required inputs, expected outputs, связь с `Validation.md`, `Verification_Evidence.md` и pass-close contour.
   - DoD: читателю ясно, как validation contour раскладывается по уровням и что в нём не должно автоматизироваться.
4. Подтвердить минимальный contract impact.
   - Описание: Проверить, нужны ли точечные updates в `Validation.md`, `Docs/Technical/README.md`, `Verification_Evidence.md`, `Tools/README.md` или `bp_lint.py`.
   - DoD: меняются только реально противоречащие линии; tooling не реализуется.
5. Закрыть pass governance-сверкой.
   - Описание: Перевести backlog-задачу и `Plan` в финальные статусы только после согласования индекса backlog, `ROAD-000011`, текущего `Plan` и self-check.
   - DoD: `BACK-000069`, индекс backlog, `ROAD-000011`, `PLAN-000057` и self-check полностью согласованы.

## Ограничения
- без реализации `bp_check / bp_verify`;
- без рефакторинга всего `Tools/*`;
- без открытия `ROAD-000012`;
- без широкого переписывания `Docs/Technical/*`.

## Риски
- если validation levels останутся неявными, outcome confirmation и pass-close relation будут трактоваться ситуативно;
- если validation levels будут смешаны с verification levels, система потеряет ясную границу между evidence reading и outcome confirmation;
- если pass превратится в tooling design, он выйдет за границы contract work.

## Артефакты
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/PLAN-000057-define-validation-levels.md`
- `Plans/Archive/PLAN-000056-clarify-validation-contract-map.md`
- `Docs/Technical/Validation_Levels.md`
- `Docs/Technical/Validation.md`
- `Docs/Technical/README.md`
- `Docs/Technical/Verification_Evidence.md`
- `Tools/README.md`

## DoD
- `ROAD-000011` остаётся в `В_работе`.
- создана одна узкая задача этого pass.
- создан один current `Plan`.
- `Validation_Levels.md` фиксирует уровни validation-контура.
- `python3 Tools/bp_lint.py --repo .` проходит.

## Результат
- В работе.
