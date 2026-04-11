# PLAN-000063 — Close ROAD-000012 user entry

ID: PLAN-000063
Название: Провести closure-pass и закрыть `ROAD-000012`
Статус: В_работе
Связи: BACK-000075
Источник: Новый завершающий pass этапа `ROAD-000012`
Дата_создания: 2026-04-11
Дата_изменения: 2026-04-11
Основание: `ROAD-000012` уже получил agent entry point и минимальный user-layer, но перед закрытием этапа нужен завершающий pass: добрать один обязательный user-facing contract о формулировании pass человеком, исправить доказанный direct contradiction в `Docs/User/*` вокруг запуска `bp_lint.py` из корня репозитория и провести финальный audit agent-entry/user-layer contour. Если residual gap не подтвердится, этап должен быть закрыт и выведен из active backlog без активации `ROAD-000013`.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000075
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать closure-pass внутри активного `ROAD-000012`.
   - Описание: Обновить `Roadmap` и `Backlog`, создать одну новую backlog-задачу и один новый current `Plan`, а завершённый `PLAN-000062` вывести в archive-layer.
   - DoD: `ROAD-000012`, `BACK-000075` и `PLAN-000063` согласованы как текущий stage/task/pass.
2. Исправить доказанный direct contradiction в `Docs/User/*`.
   - Описание: Привести user-facing references к запуску `bp_lint.py` в согласованное состояние: команда должна соответствовать запуску из корня репозитория.
   - DoD: в `Docs/User/*` больше нет противоречия между stated location и actual command path.
3. Добрать последний обязательный user-facing contract.
   - Описание: Добавить один минимальный document, который объясняет человеку, как формулировать pass для агента через repo contracts без дублирования agent operating loop.
   - DoD: user-layer покрывает human operating mode, first start, pass request и basic usage scenarios.
4. Провести финальный audit `ROAD-000012`.
   - Описание: Проверить `AGENTS.md`, `Docs/User/*`, `README.md`, `Setup_Guide.md`, `Plans/*`, `Standards/Planning.md` и определить, остался ли ровно один доказанный residual gap или contour можно закрыть полностью.
   - DoD: есть явное audit-решение о closure или о ровно одном residual gap.
5. Закрыть pass governance-сверкой и self-check.
   - Описание: Перевести backlog-задачу и `Plan` в финальные статусы после согласования индекса backlog, `ROAD-000012`, текущего `Plan` и self-check; если gap не найден, закрыть stage и вывести stage backlog в archive-layer.
   - DoD: planning-layer и user-layer не спорят о состоянии `ROAD-000012`.

## Ограничения
- без открытия `ROAD-000013`;
- без изменений `AGENTS.md`, если audit не доказал прямое противоречие;
- без изменений `Docs/Technical/*`;
- без изменений `Tools/*`, кроме доказанного contract gap;
- без широкого переписывания `README.md` и `Setup_Guide.md`;
- без превращения `Docs/User/*` в широкий manual.

## Риски
- если оставить contradiction вокруг `bp_lint.py`, user-layer будет давать неверный first-start route;
- если pass request document начнёт дублировать agent operating loop, `Docs/User/*` снова смешается с `AGENTS.md`;
- если закрыть этап без явного audit-решения, planning-layer может потерять прозрачность о том, почему `ROAD-000012` завершён.

## Артефакты
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/PLAN-000063-close-road-000012-user-entry.md`
- `Plans/Archive/PLAN-000062-minimal-user-boundary.md`
- `Docs/User/*`
- `README.md`
- `Setup_Guide.md`
- `Plans/README.md`
- `Standards/Planning.md`
- `Tools/bp_lint.py`
