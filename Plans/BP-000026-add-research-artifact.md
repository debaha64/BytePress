# PLAN-000026 — Add research artifact

ID: PLAN-000026
Название: Ввести Research как следующий канонический артефакт ROAD-000008
Статус: Черновик
Связи: BACK-000038
Источник: Next real artifact pass after Discussion introduction
Дата_создания: 2026-04-01
Дата_изменения: 2026-04-01
Основание: `Discussion` уже введён как первый реальный discovery-артефакт, место `Research` в системе уже зафиксировано, а шаблон `Templates/Research.md` уже существует. Следующий согласованный шаг — ввести `Docs/Discovery/Research.md` и синхронизировать planning-контур этапа `ROAD-000008`, не вводя в этом pass `Requirements.md`.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000038
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать управляемый контур прохода.
   - Описание: Обновить `BACK-000038` под фактический смысл текущего pass и создать отдельный plan-file для `Research`.
   - DoD: backlog-item и plan отражают текущую цель, ограничения и связь с `ROAD-000008`.
2. Ввести канонический артефакт `Research`.
   - Описание: Создать `Docs/Discovery/Research.md` по существующему шаблону и зафиксировать его роль как фазы проверки фактов, ограничений, вариантов и внешних зависимостей после `Discussion`.
   - DoD: `Research.md` существует, остаётся кратким и не дублирует `Discussion` или `Interview`.
3. Согласовать discovery и planning-контур.
   - Описание: Минимально обновить `Docs/Discovery/README.md`, `Docs/Technical/Pipeline.md`, `Plans/Roadmap.md`, `Plans/Backlog.md` и связанные discovery-документы только там, где это реально нужно для текущего этапа.
   - DoD: `ROAD-000008` остаётся согласованным между `Roadmap`, `Backlog` и текущим `Plan`, а `Requirements` остаётся будущим шагом.
4. Закрыть pass в журнале и governance-контуре.
   - Описание: Обновить `ChangeLog` и `QualityLog`, а `ADR` и `bp_lint.py` менять только при доказанной необходимости.
   - DoD: обязательная финальная governance-сверка пройдена, `python3 Tools/bp_lint.py --repo .` проходит, а `BACK-000038` и `PLAN-000026` имеют корректный финальный статус по факту результата.

## Риски
- избыточная перепись `Discussion` или `Interview` выведет задачу за пределы согласованного scope;
- преждевременное введение `Requirements.md` нарушит порядок `место -> шаблон -> артефакт`;
- несогласованное обновление backlog и roadmap создаст шум в активном этапе `ROAD-000008`.

## Артефакты
- `Docs/Discovery/Research.md`
- `Docs/Discovery/README.md`
- `Docs/Discovery/Discussion.md`
- `Docs/Discovery/Interview.md`
- `Docs/Technical/Pipeline.md`
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Tools/bp_lint.py`
- `Plans/BP-000026-add-research-artifact.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`

## DoD
- существует `Docs/Discovery/Research.md`.
- `Research` введён как канонический артефакт и использует свой шаблон.
- `Discussion` не сломан и не переписан без необходимости.
- `Requirements` не введены преждевременно.
- `ROAD-000008` остаётся согласованным между `Roadmap`, `Backlog` и текущим `Plan`.
- правило по шаблонам не нарушено.
- `python3 Tools/bp_lint.py --repo .` проходит.
- новый `ADR` создаётся только если реально нужен.
- `bp_lint.py` меняется только если обязательный contract действительно изменяется.
