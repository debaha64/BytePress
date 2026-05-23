# PLAN-000038 — Audit and close ROAD-000009

ID: PLAN-000038
Название: Провести финальный audit-pass и закрыть ROAD-000009
Статус: Завершено
Связи: BACK-000050
Источник: Final audit-pass inside `ROAD-000009`
Дата_создания: 2026-04-07
Дата_изменения: 2026-04-07
Основание: После закрытия planning-contour, unified `ID scheme`, log-layer и remaining governance/supporting tail в active слое остался только один candidate про hard-close contour. Нужен финальный audit-pass, который проверит активный governance-layer на реальные противоречия и либо переведёт `ROAD-000009` в `Завершено`, либо оставит ровно один доказанный gap без расширения этапа.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000050
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать audit-pass как единственную реальную задачу этапа.
   - Описание: Добавить одну узкую backlog-задачу и один текущий `Plan` только для финальной проверки `ROAD-000009`.
   - DoD: `BACK-000050` и `PLAN-000038` отражают только audit/closure scope без нового redesign.
2. Провести audit active governance-layer и planning-contour.
   - Описание: Проверить `Roadmap`, `Backlog`, active contracts, lint и candidate tail на наличие реально незакрытого дефекта.
   - DoD: audit даёт один из двух формальных исходов: stage closure или один доказанный gap.
3. Синхронизировать только необходимый closure-state.
   - Описание: Обновить только те документы, которые нужны для фиксации результата audit-pass.
   - DoD: active layer больше не держит неподтверждённый candidate tail и не спорит о статусе этапа.
4. Подтвердить tooling contract.
   - Описание: Проверить, требуется ли изменение `bp_lint.py`.
   - DoD: `bp_lint.py` меняется только при доказанном contract impact.
5. Закрыть pass governance-сверкой.
   - Описание: Перевести backlog-задачу и `Plan` в финальные статусы только после согласования индекса, `ROAD-*`, текущего `Plan` и self-check.
   - DoD: `BACK-000050`, индекс backlog, `ROAD-000009`, `PLAN-000038` и self-check полностью согласованы.

## Ограничения
- без нового redesign `ROAD-000009`;
- без открытия `ROAD-000010`;
- без migration новых доменов и без больших structural moves;
- без широкого переписывания `Docs/Technical/*`, `AGENTS.md` и `Docs/User/*`.

## Риски
- если принять historical или cosmetic след за реальный gap, audit-pass искусственно продлит уже закрытый этап;
- если закрыть этап без проверки candidate tail, в backlog останется неподтверждённый residual scope;
- если затронуть contracts или lint без фактической необходимости, pass потеряет узкий closure-характер.

## Артефакты
- `Plans/Backlog.md`
- `Plans/Roadmap.md`
- `Plans/Archive/Plans/PLAN-000038-audit-and-close-road-000009.md`
- `Plans/README.md`
- `Standards/Planning.md`
- `Standards/Naming.md`
- `Tools/bp_lint.py`

## DoD
- создана одна узкая backlog-задача только для audit/closure pass.
- создан новый текущий `Plan` только под этот pass.
- выполнен явный audit активного governance/supporting layer.
- `ROAD-000009` либо переведён в `Завершено`, либо оставлен ровно один доказанный gap.
- `python3 Tools/bp_lint.py --repo .` проходит.

## Результат
- Audit активного governance-layer и planning-contour не подтвердил реального residual gap: candidate про hard-close contour не опирался на активное рассогласование и снят как неподтверждённый.
- `ROAD-000009` переведён в `Завершено`; `ROAD-000010` не активирован автоматически и остаётся следующим черновым горизонтом без новой backlog-задачи.
- `Plans/Backlog.md`, `Plans/Roadmap.md` и текущий `Plan` синхронизированы на closure-state без открытия нового redesign.

bp_lint contract unaffected
