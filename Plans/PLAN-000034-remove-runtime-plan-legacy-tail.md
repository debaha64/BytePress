# PLAN-000034 — Remove runtime plan legacy tail

ID: PLAN-000034
Название: Удалить `Runtime/Plan.md` и закрыть legacy-tail planning-контура
Статус: В_работе
Связи: BACK-000046
Источник: Narrow planning cleanup pass inside `ROAD-000009`
Дата_создания: 2026-04-06
Дата_изменения: 2026-04-06
Основание: Planning-contour уже приведён к active/archive layout для `Plan` и `Backlog`, но в рабочем дереве ещё остаётся `Runtime/Plan.md`, а active-layer документы по-прежнему описывают его как допустимый legacy artifact. Нужен отдельный pass, который физически удалит этот файл, выведет его из active contract и оставит planning-layer без legacy runtime plan.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000046
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать scope cleanup-pass внутри `ROAD-000009`.
   - Описание: Добавить одну реальную backlog-задачу и один новый текущий `Plan` только для удаления runtime plan legacy-tail.
   - DoD: `BACK-000046` и `PLAN-000034` описывают только cleanup planning legacy-tail и не открывают другие домены.
2. Удалить legacy runtime plan из рабочего дерева.
   - Описание: Удалить `Runtime/Plan.md` и, если нужно для правила одного текущего `Plan`, перевести предыдущий завершённый current `Plan` в `Plans/Archive/`.
   - DoD: `Runtime/Plan.md` физически отсутствует, а active `Plans/` по-прежнему содержит только один текущий `Plan`.
3. Убрать active-layer двусмысленности.
   - Описание: Обновить только те active документы и инструменты, которые ещё опираются на существование `Runtime/Plan.md` как допустимого legacy artifact.
   - DoD: active-layer больше не содержит правил, path-patterns или bootstrap-поведения, предполагающих существование `Runtime/Plan.md`.
4. Синхронизировать planning-contract с завершённым состоянием.
   - Описание: Обновить `Standards/Planning.md`, `Plans/README.md`, при необходимости `Standards/Naming.md` и минимально необходимый терминологический слой.
   - DoD: planning-contour описан как завершённый active/archive layer без legacy runtime plan.
5. Подтвердить границы contract checks.
   - Описание: Оценить влияние на `bp_lint.py` и менять его только при доказанной необходимости.
   - DoD: `bp_lint.py` синхронизирован только если реально нужен новый structural check, либо зафиксирован вывод `bp_lint contract unaffected`.

## Ограничения
- без migration `ID` для logs, rules, standards, templates, schemas и остальных доменов;
- без изменения plan archive layout;
- без изменения backlog archive layout;
- без широкого переписывания `Docs/Technical/*`, `AGENTS.md` и `Docs/User/*`;
- без больших structural moves вне planning legacy-tail.

## Риски
- если удалить `Runtime/Plan.md` без синхронизации bootstrap и active contract, репозиторий начнёт заново материализовать уже закрытый legacy-tail;
- если оставить в active docs transitional policy про `Runtime/Plan.md`, planning-layer сохранит двусмысленную модель состояния;
- если не вывести предыдущий current `Plan` в archive при создании нового плана, active `Plans/` снова нарушит правило одного текущего `Plan`.

## Артефакты
- `Plans/Backlog.md`
- `Plans/Roadmap.md`
- `Plans/PLAN-000034-remove-runtime-plan-legacy-tail.md`
- `Runtime/Plan.md`
- `Standards/Planning.md`
- `Plans/README.md`
- `Standards/Naming.md`
- `Tools/bp_bootstrap.py`

## DoD
- создана одна узкая backlog-задача только для удаления `Runtime/Plan.md` и закрытия legacy-tail.
- создан новый текущий `Plan` только под этот pass.
- `Runtime/Plan.md` удалён из рабочего дерева.
- active-layer больше не содержит рабочих правил и зависимостей, завязанных на legacy runtime plan.
- `python3 Tools/bp_lint.py --repo .` проходит.
