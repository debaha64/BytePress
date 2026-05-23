# PLAN-000032 — Migrate plan history to archive

ID: PLAN-000032
Название: Перевести historical plan-files в archive layer и оставить один текущий Plan
Статус: Завершено
Связи: BACK-000044
Источник: Narrow plan-layer migration pass inside `ROAD-000009`
Дата_создания: 2026-04-06
Дата_изменения: 2026-04-06
Основание: После фиксации unified `ID scheme` planning-contour всё ещё остаётся в переходном состоянии: historical `BP-*` и завершённые `PLAN-*` лежат в активном `Plans/`, хотя target model уже требует `Plans/Archive/` для завершённых `Plan` и одного текущего `Plan` в active layer. Нужен отдельный pass, который физически приведёт только plan-layer к этому состоянию без migration backlog, logs и других доменов.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000044
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать текущий migration scope внутри `ROAD-000009`.
   - Описание: Добавить одну реальную backlog-задачу и один новый текущий `Plan` только для migration plan-files и archive policy.
   - DoD: `BACK-000044` и `PLAN-000032` описывают только plan-layer migration без открытия migration других доменов.
2. Ввести active/archive layout для plan-layer.
   - Описание: Создать `Plans/Archive/`, перевести historical `BP-*` и завершённые `PLAN-*` в `Plans/Archive/Plans/PLAN-*`, а в активном `Plans/` оставить только текущий `Plan`.
   - DoD: активный слой содержит только singleton files и `PLAN-000032`, а завершённые `Plan` живут в `Plans/Archive/`.
3. Синхронизировать прямые ссылки и plan-contract.
   - Описание: Обновить path-ссылки, затронутые migration, а также `Standards/Naming.md`, `Standards/Planning.md` и `Plans/README.md` только в пределах реально изменённого plan-layer.
   - DoD: прямые ссылки на plan-files не указывают на несуществующие legacy paths, а contract описывает уже реализованное состояние.
4. Подтвердить границы contract checks.
   - Описание: Оценить, требует ли новое состояние plan-layer обновления `bp_lint.py`, и внести только минимально необходимое изменение.
   - DoD: `bp_lint.py` синхронизирован только там, где это требуется для нового archive layout, либо зафиксирован вывод `bp_lint contract unaffected`.

## Ограничения
- без migration `ID` для backlog, logs, rules, standards, templates, schemas и остальных доменов;
- без архивирования historical backlog прошлых этапов;
- без удаления `Runtime/Plan.md`;
- без широкого переписывания `Docs/Technical/*`, `AGENTS.md` и `Docs/User/*`;
- без structural moves вне plan-files и реально затронутых ссылок.

## Риски
- если historical plan-files не перевести в `Plans/Archive/`, active layer продолжит спорить с уже принятым plan-contract;
- если path-ссылки на old `BP-*` не синхронизировать, migration сломает traceability и навигацию по журналам и ролям;
- если archive policy не синхронизировать в `bp_lint.py`, обязательная проверка репозитория начнёт спорить с реализованным layout.

## Артефакты
- `Plans/Backlog.md`
- `Plans/Roadmap.md`
- `Plans/Archive/Plans/PLAN-000032-migrate-plan-history-to-archive.md`
- `Plans/Archive/*`
- `Standards/Naming.md`
- `Standards/Planning.md`
- `Plans/README.md`
- `Tools/bp_lint.py`

## DoD
- создана одна узкая backlog-задача только для migration plan-files и archive policy.
- создан новый текущий `Plan` только под этот pass.
- historical `BP-*` plan-files migrated в `Plans/Archive/Plans/PLAN-*`.
- завершённые `Plan` перемещены в `Plans/Archive/`.
- в активном `Plans/` остался только текущий `Plan` плюс singleton files.
- все затронутые ссылки на plan-files синхронизированы.
- `python3 Tools/bp_lint.py --repo .` проходит.

## Фактический результат
- `BACK-000044` и `PLAN-000032` зафиксировали только pass на migration plan-files и archive policy.
- historical `BP-*` и завершённые `PLAN-*` перемещены в `Plans/Archive/` и приведены к `PLAN-*` filename-contract.
- active `Plans/` на момент закрытия pass оставил только singleton files и текущий `PLAN-000032`, после чего сам план стал частью historical archive-layer.
- `Standards/Naming.md`, `Standards/Planning.md`, `Plans/README.md` и `bp_lint.py` синхронизированы под фактически реализованный active/archive plan-layer.
