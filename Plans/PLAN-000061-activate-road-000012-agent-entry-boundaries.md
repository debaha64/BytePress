# PLAN-000061 — Activate ROAD-000012 agent entry boundaries

ID: PLAN-000061
Название: Активировать `ROAD-000012` и зафиксировать `AGENTS.md` как canonical agent entry point
Статус: Завершено
Связи: BACK-000073
Источник: Новый узкий pass этапа `ROAD-000012`
Дата_создания: 2026-04-11
Дата_изменения: 2026-04-11
Основание: После закрытия `ROAD-000011` verification/validation contour больше не спорит о planning-state, поэтому `ROAD-000012` можно активировать узким boundary-pass без широкого user-layer. Нужен pass, который переведёт следующий этап в `В_работе`, определит `AGENTS.md` как каноническую entry point карту агента и зафиксирует source-of-truth hierarchy, operating loop и границы между `AGENTS.md`, `Docs/User/*`, `Docs/Technical/*`, `Plans/*`, `Logs/*` и `Tools/*` без открытия `ROAD-000013`.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000073
Связанные_ADR:
- отсутствуют

## Шаги
1. Активировать `ROAD-000012` как текущий этап.
   - Описание: Обновить `Roadmap` и `Backlog`, завести одну реальную backlog-задачу и один новый current `Plan`, а завершённый `PLAN-000060` вывести в archive-layer.
   - DoD: `ROAD-000012`, `BACK-000073` и `PLAN-000061` согласованы как текущий stage/task/pass.
2. Провести audit active contracts вокруг agent entry point.
   - Описание: Проверить `AGENTS.md`, `README.md`, `Docs/User/README.md`, `Docs/Technical/README.md`, `Standards/Planning.md`, `Plans/*` и `Tools/README.md` только на реальные boundary contradictions.
   - DoD: определено, что `AGENTS.md` должен быть entrypoint и routing-document агента, а не дубль user-layer, technical-layer, planning-layer или tooling-layer.
3. Пересобрать `AGENTS.md` как каноническую entry point карту агента.
   - Описание: Зафиксировать роль агента в системе, source-of-truth hierarchy, task entry, domain routing, operating loop, обязательные checks, reporting contract, defect criteria и одну improvement expectation без длинного ручного operational script.
   - DoD: `AGENTS.md` направляет агента в owner-domains и не подменяет репозиторные contracts.
4. Синхронизировать только реально затронутые прямые references.
   - Описание: Менять `README.md`, `Docs/User/README.md`, `Docs/Technical/README.md`, `Standards/Planning.md`, `Tools/README.md` и `Tools/bp_lint.py` только если без этого остаётся доказанное противоречие.
   - DoD: boundary-sync минимален; широкий user-layer и tool refactor не открываются.
5. Закрыть pass governance-сверкой и self-check.
   - Описание: Перевести backlog-задачу и `Plan` в финальные статусы только после согласования индекса backlog, `ROAD-000012`, текущего `Plan` и self-check.
   - DoD: `BACK-000073`, индекс backlog, `ROAD-000012`, `PLAN-000061` и self-check полностью согласованы.

## Ограничения
- без открытия `ROAD-000013`;
- без широкого рефакторинга `Docs/User/*`;
- без переписывания всего `Docs/Technical/*`;
- без рефакторинга всего `Tools/*`;
- без превращения `AGENTS.md` в дубль всех repo contracts;
- без изменения `Tools/bp_lint.py`, если audit не доказал реальный contract gap.

## Риски
- если оставить `AGENTS.md` короткой сводкой без hierarchy и operating loop, агент продолжит зависеть от длинных ручных промптов;
- если смешать `AGENTS.md` с `Docs/User/*` или `Docs/Technical/*`, новый entrypoint создаст ещё одну двусмысленную копию owner-contracts;
- если активировать `ROAD-000013` автоматически, planning-layer снова начнёт спорить о текущем горизонте;
- если менять tooling без доказанного противоречия, boundary-pass превратится в лишний tool refactor.

## Артефакты
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/PLAN-000061-activate-road-000012-agent-entry-boundaries.md`
- `Plans/Archive/PLAN-000060-audit-and-close-road-000011.md`
- `AGENTS.md`
- `README.md`
- `Docs/User/README.md`
- `Docs/Technical/README.md`
- `Standards/Planning.md`
- `Tools/README.md`
- `Tools/bp_lint.py`

## DoD
- `ROAD-000012` переведён в `В_работе`.
- создана одна узкая задача этого pass.
- создан один current `Plan`.
- `AGENTS.md` фиксирует каноническую entry point роль агента в `BytePress`.
- `AGENTS.md` направляет агента в repo contracts, а не дублирует их.
- границы между `AGENTS.md`, `Docs/User/*`, `Docs/Technical/*`, `Plans/*`, `Logs/*` и `Tools/*` разведены без двусмысленности.
- `python3 Tools/bp_lint.py --repo .` проходит.

## Результат
- `ROAD-000012` активирован без автоматической активации `ROAD-000013`.
- `Plans/Backlog.md` переведён на `ROAD-000012` и содержит одну завершённую задачу `BACK-000073` этого узкого pass.
- завершённый `PLAN-000060` выведен в `Plans/Archive/`, а `PLAN-000061` оформлен как новый current `Plan`.
- `AGENTS.md` пересобран как каноническая entry point карта агента и routing-document: зафиксированы роль агента, source-of-truth hierarchy, task entry, domain routing, operating loop, обязательные checks, reporting contract, defect criteria и improvement expectation без дублирования repo contracts.
- `README.md`, `Docs/User/README.md`, `Docs/Technical/README.md`, `Standards/Planning.md`, `Tools/README.md` и `Tools/bp_lint.py` не менялись, потому что audit не подтвердил реального boundary contradiction.
- `bp_lint contract unaffected`
