# PLAN-000024 — Start ROAD-000008 and add discovery templates

ID: PLAN-000024
Название: Запустить ROAD-000008 и добавить discovery templates
Статус: Завершено
Связи: BACK-000037, CHG-000036, QL-000031
Источник: Transition pass after analytical-product-planning contour alignment
Дата_создания: 2026-04-01
Дата_изменения: 2026-04-01
Основание: После выравнивания `Interview`, product-layer и planning-контуров нужно корректно закрыть `ROAD-000007`, сделать `ROAD-000008` текущим этапом, зафиксировать место `Discussion`, `Research`, `Requirements` в системе и добавить для них канонические шаблоны без преждевременного введения самих discovery-артефактов.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000037
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать управляемый контур переходного pass.
   - Описание: Добавить новый backlog-item для старта `ROAD-000008` и отдельный plan-file с жёстким ограничением scope.
   - DoD: `BACK-000037` и `PLAN-000024` отражают цель pass, ограничения и переход между `ROAD-000007` и `ROAD-000008`.
2. Закрыть `ROAD-000007` и активировать `ROAD-000008`.
   - Описание: Исправить остаточные рассогласования по статусам, секциям и связям текущих этапов в `Roadmap` и `Backlog`.
   - DoD: `ROAD-000007` корректно закрыт без активных задач, а `ROAD-000008` переведён в `В_работе` с актуальным backlog-item.
3. Зафиксировать место discovery-stage artifacts и добавить шаблоны.
   - Описание: Обновить `Pipeline`, добавить шаблоны `Discussion`, `Research`, `Requirements` и синхронизировать template layer без создания самих discovery-документов.
   - DoD: место новых артефактов зафиксировано в системе, шаблоны существуют и не нарушают текущий канон.
4. Закрыть pass в журнале и governance-контуре.
   - Описание: Обновить `ChangeLog` и `QualityLog`, а `ADR` и `bp_lint.py` менять только при доказанной необходимости.
   - DoD: обязательная финальная governance-сверка пройдена, `python3 Tools/bp_lint.py --repo .` проходит, `BACK-000037` и `PLAN-000024` имеют корректный финальный статус.

## Риски
- раннее введение `Docs/Discovery/Discussion.md`, `Research.md` или `Requirements.md` нарушит прямое ограничение pass;
- несогласованное закрытие `ROAD-000007` и запуск `ROAD-000008` снова сломает governance-контур;
- избыточные правки в `Pipeline` или template layer могут превратить переходный pass в большой discovery refactor.

## Артефакты
- `Plans/Backlog.md`
- `Plans/Roadmap.md`
- `Docs/Technical/Pipeline.md`
- `Templates/Discussion.md`
- `Templates/Research.md`
- `Templates/Requirements.md`
- `Templates/README.md`
- `Tools/bp_lint.py`
- `Plans/Archive/PLAN-000024-start-road-000008-and-add-discovery-templates.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`

## DoD
- `ROAD-000007` закрыт без остаточного рассогласования.
- `ROAD-000008` активирован.
- место `Discussion`, `Research`, `Requirements` зафиксировано в `Pipeline`.
- существуют `Templates/Discussion.md`, `Templates/Research.md`, `Templates/Requirements.md`.
- правило по шаблонам не нарушено.
- у `ROAD-000008` есть текущая задача с `BACK-ID` и кандидаты задач без `BACK-ID`.
- `python3 Tools/bp_lint.py --repo .` проходит.
- новый `ADR` создаётся только если реально нужен.
- `bp_lint.py` меняется только если обязательный contract действительно изменяется.

## Фактический результат
- `ROAD-000007` закрыт без остаточного governance-рассогласования: активных задач не осталось, а `Roadmap` и `Backlog` используют согласованный набор завершённых задач этапа.
- `ROAD-000008` переведён в `В_работе` как текущий этап `Research and Requirements`, а `BACK-000037` зафиксировал стартовый transition pass этого этапа.
- `Docs/Technical/Pipeline.md` теперь явно фиксирует выходы фаз `Discussion`, `Research`, `Requirements` и правило последовательного ввода новых типов артефактов: место -> шаблон -> сам артефакт.
- Добавлены канонические шаблоны `Templates/Discussion.md`, `Templates/Research.md`, `Templates/Requirements.md`; сами discovery-артефакты в `Docs/Discovery/` не вводились.
- `Tools/bp_lint.py` расширен минимально и теперь требует новые обязательные discovery-stage templates как часть BytePress repo contract.
