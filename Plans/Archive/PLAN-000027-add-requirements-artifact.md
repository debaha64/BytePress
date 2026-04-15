# PLAN-000027 — Add requirements artifact

ID: PLAN-000027
Название: Ввести Requirements как следующий канонический артефакт ROAD-000008
Статус: Завершено
Связи: BACK-000039, CHG-000039, QL-000034
Источник: Next real artifact pass after Research introduction
Дата_создания: 2026-04-01
Дата_изменения: 2026-04-01
Основание: `Discussion` и `Research` уже введены как реальные discovery-артефакты, место `Requirements` в системе уже зафиксировано, а шаблон `Templates/Requirements.md` уже существует. Следующий согласованный шаг — ввести `Docs/Discovery/Requirements.md` и синхронизировать planning-контур этапа `ROAD-000008`, не ломая уже введённые discovery-артефакты.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000039
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать управляемый контур прохода.
   - Описание: Закрыть `BACK-000038` как завершённый pass по `Research`, завести новый backlog-item для `Requirements` и создать отдельный plan-file.
   - DoD: `BACK-000038`, `BACK-000039` и `PLAN-000027` отражают фактическое состояние этапа `ROAD-000008`.
2. Ввести канонический артефакт `Requirements`.
   - Описание: Создать `Docs/Discovery/Requirements.md` по существующему шаблону и зафиксировать его роль как перевода результатов `Discussion` и `Research` в обязательные требования.
   - DoD: `Requirements.md` существует, остаётся кратким и не дублирует `Discussion` или `Research`.
3. Согласовать discovery и planning-контур.
   - Описание: Минимально обновить `Docs/Discovery/README.md`, `Docs/Technical/Pipeline.md`, `Plans/Roadmap.md`, `Plans/Backlog.md` и связанные discovery-документы только там, где это реально нужно для текущего этапа.
   - DoD: `ROAD-000008` остаётся согласованным между `Roadmap`, `Backlog` и текущим `Plan`, а `Discussion` и `Research` остаются предыдущими артефактами без лишней переписи.
4. Закрыть pass в журнале и governance-контуре.
   - Описание: Обновить `ChangeLog` и `QualityLog`, а `ADR` и `bp_lint.py` менять только при доказанной необходимости.
   - DoD: обязательная финальная governance-сверка пройдена, `python3 Tools/bp_lint.py --repo .` проходит, а `BACK-000039` и `PLAN-000027` имеют корректный финальный статус по факту результата.

## Риски
- сохранение двусмысленного `BACK-000038` сломает управление этапом `ROAD-000008`;
- преждевременное расширение прохода за пределы `Requirements` выведет задачу за согласованный scope;
- избыточная перепись `Discussion` и `Research` создаст ненужный noise в discovery-layer.

## Артефакты
- `Docs/Discovery/Requirements.md`
- `Docs/Discovery/README.md`
- `Docs/Discovery/Discussion.md`
- `Docs/Discovery/Research.md`
- `Docs/Discovery/Interview.md`
- `Docs/Technical/Pipeline.md`
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Tools/bp_lint.py`
- `Plans/Archive/PLAN-000027-add-requirements-artifact.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`

## Фактический результат
- `BACK-000038` закрыт как завершённый pass по `Research` без двусмысленного residual scope.
- `Docs/Discovery/Requirements.md` введён как следующий канонический discovery-артефакт и выровнен с `Docs/Discovery/README.md`.
- `Plans/Roadmap.md` и `Plans/Backlog.md` синхронизированы под фактическое состояние `ROAD-000008`.
- `Tools/bp_lint.py` теперь требует `Docs/Discovery/Requirements.md` как обязательный discovery-артефакт BytePress repo.
- Финальная governance-сверка пройдена: `BACK-000039`, его секция, индекс backlog, статус `ROAD-000008`, его `Связанные_backlog` и статус `PLAN-000027` согласованы.

## DoD
- рассогласование по `BACK-000038` устранено.
- `BACK-000038` не остаётся двусмысленным контейнером.
- существует `Docs/Discovery/Requirements.md`.
- `Requirements` введён как канонический артефакт и использует свой шаблон.
- `Discussion` и `Research` не сломаны и не переписаны без необходимости.
- `ROAD-000008` остаётся согласованным между `Roadmap`, `Backlog` и текущим `Plan`.
- правило по шаблонам не нарушено.
- `python3 Tools/bp_lint.py --repo .` проходит.
- новый `ADR` создаётся только если реально нужен.
- `bp_lint.py` меняется только если обязательный contract действительно изменяется.
