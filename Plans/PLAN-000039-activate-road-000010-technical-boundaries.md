# PLAN-000039 — Activate ROAD-000010 technical boundaries

ID: PLAN-000039
Название: Зафиксировать границы и минимальный состав technical-layer
Статус: Завершено
Связи: BACK-000051
Источник: Первый узкий pass этапа `ROAD-000010`
Дата_создания: 2026-04-07
Дата_изменения: 2026-04-07
Основание: После закрытия `ROAD-000009` следующий этап должен стартовать без широкого технического рефакторинга. Нужен отдельный pass, который активирует `ROAD-000010`, определит назначение и границы `Docs/Technical/*`, зафиксирует минимальный required состав слоя и разведёт technical-layer с `Pipeline/*` и planning/governance доменами без создания нового избыточного объёма работ.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000051
Связанные_ADR:
- отсутствуют

## Шаги
1. Перевести active planning-layer на `ROAD-000010`.
   - Описание: Сделать `ROAD-000010` текущим этапом, завести одну реальную backlog-задачу и один новый `Plan`.
   - DoD: `ROAD-000010`, `BACK-000051` и `PLAN-000039` согласованы как текущий stage/task/pass.
2. Зафиксировать границы technical-layer.
   - Описание: Определить назначение `Docs/Technical/*`, его включения, исключения и отношение к `Pipeline/*`, `Plans/*`, `Runtime/*` и `Logs/*`.
   - DoD: entrypoint technical-layer больше не создаёт двусмысленность между knowledge-layer и process-layer.
3. Зафиксировать минимальный состав `Docs/Technical/*`.
   - Описание: Определить минимальное required ядро technical-documents на базе уже существующих имён файлов без создания лишних сущностей.
   - DoD: `Docs/Technical/README.md` даёт короткую карту слоя и объясняет роль каждого минимально обязательного technical-document.
4. Синхронизировать только реально затронутые прямые ссылки.
   - Описание: Исправить только те документы, где текущий contract технического слоя явно спорит с новым boundary-pass.
   - DoD: прямые references не спорят о роли `Docs/Technical/*` и `Pipeline/*`.
5. Закрыть pass governance-сверкой.
   - Описание: Перевести backlog-задачу и `Plan` в финальные статусы только после согласования индекса backlog, `ROAD-000010`, текущего `Plan` и self-check.
   - DoD: `BACK-000051`, индекс backlog, `ROAD-000010`, `PLAN-000039` и self-check полностью согласованы.

## Ограничения
- без широкого рефакторинга `Docs/Technical/*`;
- без migration новых доменов;
- без изменения active/archive layout для `Plans` и backlog archive-layer;
- без открытия `ROAD-000011` и без автоматической активации следующих этапов.

## Риски
- если смешать technical-layer с process-layer, pass превратится в скрытый redesign `Pipeline/*` и planning-контура;
- если не зафиксировать минимальный состав technical-documents, следующий pass снова будет спорить о ядре слоя;
- если исправлять historical content ради косметики, pass потеряет узкий boundary-scope.

## Артефакты
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/PLAN-000039-activate-road-000010-technical-boundaries.md`
- `Docs/Technical/README.md`
- `Docs/Technical/Pipeline.md`
- `Pipeline/*`
- `Tools/bp_lint.py`

## DoD
- `ROAD-000010` переведён в `В_работе`.
- создана одна узкая backlog-задача только для старта technical-layer boundary pass.
- создан новый текущий `Plan` только под этот pass.
- `Docs/Technical/README.md` фиксирует границы и минимальный состав слоя.
- `python3 Tools/bp_lint.py --repo .` проходит.

## Результат
- `ROAD-000010` активирован как текущий этап без переоткрытия `ROAD-000009`.
- `Docs/Technical/README.md` зафиксировал назначение technical-layer, его включения, исключения, отношение к `Pipeline/*`, `Plans/*`, `Runtime/*` и `Logs/*`, а также минимальный required состав слоя.
- `Pipeline/Artifacts.md` синхронизирован с уже реализованным plan filename-contract и больше не ссылается на legacy `Plan_<ID>.md`.
- Дополнительные contracts, `Plans/README.md`, `Standards/Planning.md`, `Standards/Naming.md` и `bp_lint.py` не потребовали изменения в этом pass.

bp_lint contract unaffected
