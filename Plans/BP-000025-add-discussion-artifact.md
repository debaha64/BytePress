# PLAN-000025 — Add discussion artifact

ID: PLAN-000025
Название: Ввести Discussion как канонический артефакт ROAD-000008
Статус: Завершено
Связи: BACK-000038, CHG-000037, QL-000032
Источник: First real artifact pass after ROAD-000008 activation
Дата_создания: 2026-04-01
Дата_изменения: 2026-04-01
Основание: Место `Discussion` в системе уже зафиксировано, шаблон `Templates/Discussion.md` уже добавлен, поэтому следующий согласованный шаг — ввести `Docs/Discovery/Discussion.md` как первый реальный discovery-артефакт этапа `ROAD-000008`, не расширяя проход на `Research` и `Requirements`.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000038
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать управляемый контур прохода.
   - Описание: Добавить новый backlog-item для pass по `Discussion` и отдельный plan-file с жёстким ограничением scope.
   - DoD: `BACK-000038` и `PLAN-000025` отражают цель pass, ограничения и связь с `ROAD-000008`.
2. Ввести канонический артефакт `Discussion`.
   - Описание: Создать `Docs/Discovery/Discussion.md` по существующему шаблону и зафиксировать его роль как входной аналитической фазы до `Interview`, `Research` и `Requirements`.
   - DoD: `Discussion.md` существует, остаётся кратким и не дублирует `Interview`.
3. Согласовать discovery и planning-контур.
   - Описание: Минимально обновить `Docs/Discovery/README.md`, `Plans/Roadmap.md`, `Plans/Backlog.md` и `Docs/Technical/Pipeline.md` только если это реально нужно для синхронизации текущего этапа.
   - DoD: `ROAD-000008` имеет реальную текущую или завершённую задачу без рассогласования backlog и roadmap, а `Research` и `Requirements` остаются будущими задачами.
4. Закрыть pass в журнале и governance-контуре.
   - Описание: Обновить `ChangeLog` и `QualityLog`, а `ADR` и `bp_lint.py` менять только при доказанной необходимости.
   - DoD: обязательная финальная governance-сверка пройдена, `python3 Tools/bp_lint.py --repo .` проходит, `BACK-000038` и `PLAN-000025` имеют корректный финальный статус.

## Риски
- попытка превратить `Discussion.md` в стенограмму разрушит его каноническую роль входной аналитической фазы;
- преждевременное введение `Research.md` или `Requirements.md` выведет задачу за пределы согласованного scope;
- несогласованные правки `Roadmap` и `Backlog` снова сломают governance-контур текущего этапа.

## Артефакты
- `Docs/Discovery/Discussion.md`
- `Docs/Discovery/README.md`
- `Docs/Technical/Pipeline.md`
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Tools/bp_lint.py`
- `Plans/BP-000025-add-discussion-artifact.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`

## DoD
- существует `Docs/Discovery/Discussion.md`.
- `Discussion` введён как канонический артефакт и использует свой шаблон.
- `ROAD-000008` имеет реальную активную или завершённую текущую задачу без рассогласования backlog и roadmap.
- `Research` и `Requirements` не введены преждевременно.
- правило по шаблонам не нарушено.
- `python3 Tools/bp_lint.py --repo .` проходит.
- новый `ADR` создаётся только если реально нужен.
- `bp_lint.py` меняется только если обязательный contract действительно изменяется.

## Фактический результат
- `Docs/Discovery/Discussion.md` введён как первый реальный discovery-артефакт этапа `ROAD-000008` и использует существующий шаблон `Templates/Discussion.md`.
- `Docs/Discovery/README.md` синхронизирован с фактическим минимальным составом discovery-layer: `Discussion.md` и `Interview.md`.
- `Plans/Roadmap.md` и `Plans/Backlog.md` теперь отражают, что `Discussion` уже введён, а `Research` и `Requirements` остаются следующими задачами этапа без преждевременного ввода.
- `Tools/bp_lint.py` минимально расширен и теперь требует `Docs/Discovery/Discussion.md` как обязательный discovery-артефакт BytePress repo.
- `BACK-000038` оставлен в статусе `В_работе` как текущая активная задача этапа `ROAD-000008`; остаточный scope ограничен следующими проходами по `Research` и `Requirements`.
