# PLAN-000062 — Minimal user boundary

ID: PLAN-000062
Название: Проявить минимальный user-facing layer в `Docs/User/*`
Статус: Завершено
Связи: BACK-000074
Источник: Новый узкий pass этапа `ROAD-000012`
Дата_создания: 2026-04-11
Дата_изменения: 2026-04-11
Основание: После activation-pass `ROAD-000012` уже получил agent entry point через `AGENTS.md`, но `Docs/User/*` остаётся слишком кратким и не закрывает минимальный human-facing слой. Нужен отдельный pass, который проявит canonical user-layer entrypoint, human operating mode, первый маршрут старта и базовые сценарии использования без дублирования `AGENTS.md`, `Setup_Guide.md` и `Docs/Technical/*`, без открытия широкого user-layer и без активации `ROAD-000013`.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000074
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать новый pass внутри активного `ROAD-000012`.
   - Описание: Обновить `Roadmap` и `Backlog`, создать одну новую backlog-задачу и один новый current `Plan`, а завершённый `PLAN-000061` вывести в archive-layer.
   - DoD: `ROAD-000012`, `BACK-000074` и `PLAN-000062` согласованы как текущий stage/task/pass.
2. Провести audit minimal user-layer boundary.
   - Описание: Проверить `Docs/User/README.md`, `README.md`, `Setup_Guide.md`, `AGENTS.md`, `Plans/*` и только определить, чего не хватает для minimal human-facing layer.
   - DoD: подтверждено, что user-layer должен маршрутизировать к owner-documents, а не дублировать setup, technical и agent contracts.
3. Собрать минимальный `Docs/User/*`.
   - Описание: Пересобрать `Docs/User/README.md` как карту user-layer и добавить только минимально необходимые user-documents для operating mode, first start и basic usage scenarios.
   - DoD: human operating mode, first start и basic usage scenarios покрыты явным минимальным набором user-documents.
4. Синхронизировать только прямые references при доказанном конфликте.
   - Описание: Менять `README.md` и `Setup_Guide.md` только если без этого остаётся прямое противоречие.
   - DoD: direct-reference layer не спорит, а лишние rewrites отсутствуют.
5. Закрыть pass governance-сверкой и self-check.
   - Описание: Перевести backlog-задачу и `Plan` в финальные статусы только после согласования индекса backlog, `ROAD-000012`, текущего `Plan` и self-check.
   - DoD: `BACK-000074`, индекс backlog, `ROAD-000012`, `PLAN-000062` и self-check полностью согласованы.

## Ограничения
- без изменений `AGENTS.md`, если audit не доказал прямое противоречие;
- без изменений `Docs/Technical/*`;
- без изменений `Tools/*`, кроме доказанного contract gap;
- без открытия `ROAD-000013`;
- без широкого переписывания `README.md` и `Setup_Guide.md`;
- без создания лишних user-documents вне минимально необходимого набора.

## Риски
- если user-layer повторит setup, technical или agent contracts, появится ещё один competing summary вместо routing-layer;
- если не проявить human operating mode явно, `Docs/User/*` останется декоративным каталогом без реального first-usable value;
- если начать расширять user-layer beyond minimum, pass потеряет узкий boundary-scope внутри `ROAD-000012`.

## Артефакты
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/PLAN-000062-minimal-user-boundary.md`
- `Plans/Archive/PLAN-000061-activate-road-000012-agent-entry-boundaries.md`
- `Docs/User/README.md`
- `Docs/User/Operating_Mode.md`
- `Docs/User/First_Start.md`
- `Docs/User/Usage_Scenarios.md`
- `README.md`
- `Setup_Guide.md`
- `Tools/bp_lint.py`

## DoD
- `ROAD-000012` остаётся активным и не открывает `ROAD-000013`.
- создана одна новая backlog-задача и один новый current `Plan` для этого pass.
- `Docs/User/README.md` оформлен как каноническая карта user-layer.
- в `Docs/User/*` появился минимальный user-facing набор для human operating mode, first start и basic usage scenarios.
- user-layer не дублирует `AGENTS.md`, `Setup_Guide.md` и `Docs/Technical/*`, а направляет к ним.
- `python3 Tools/bp_lint.py --repo .` проходит.

## Результат
- `ROAD-000012` остался активным, а `ROAD-000013` не активирован.
- `PLAN-000061` выведен в archive-layer, `PLAN-000062` оформлен как новый current `Plan`.
- `Docs/User/README.md` пересобран как каноническая карта user-layer и routing-document для человека.
- Добавлены `Operating_Mode.md`, `First_Start.md` и `Usage_Scenarios.md` как минимальный user-facing набор без дублирования setup-, technical- и agent-contracts.
- `README.md`, `Setup_Guide.md` и `Tools/bp_lint.py` не менялись, потому что audit не подтвердил прямого contradiction или tooling gap.
- `bp_lint contract unaffected`
