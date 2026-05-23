# PLAN-000028 — Fix ROAD-000008 governance state

ID: PLAN-000028
Название: Зафиксировать переход Discussion -> Research -> Requirements -> Roadmap
Статус: Завершено
Связи: BACK-000040, CHG-000040, QL-000035
Источник: Transition governance repair pass after Requirements introduction
Дата_создания: 2026-04-02
Дата_изменения: 2026-04-02
Основание: `Discussion`, `Research` и `Requirements` уже введены как реальные discovery-артефакты этапа `ROAD-000008`, но backlog-layer всё ещё держит следующий переход только как candidate-level хвост. Нужен короткий pass, который превратит этот переход в реальную текущую backlog-задачу, синхронизирует `Pipeline`, `Roadmap` и `Backlog` и уберёт остаточное governance-рассогласование этапа.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000040
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать управляемый контур переходного pass.
   - Описание: Создать новый backlog-item и отдельный plan-file для ремонта governance-state `ROAD-000008` без расширения discovery-scope.
   - DoD: `BACK-000040` и `PLAN-000028` отражают текущую активную задачу, ограничения и связь с этапом `ROAD-000008`.
2. Синхронизировать planning-контур этапа.
   - Описание: Минимально обновить `Docs/Technical/Pipeline.md`, `Plans/Roadmap.md` и `Plans/Backlog.md` только там, где это реально нужно для перехода `Discussion -> Research -> Requirements -> Roadmap`.
   - DoD: `ROAD-000008` не остаётся активным без активной задачи, а candidate-level хвост превращён в реальную текущую или завершённую backlog-задачу.
3. Оценить, закрывается ли этап этим pass.
   - Описание: После синхронизации проверить, может ли `ROAD-000008` быть завершён без остаточного governance-noise, либо должен остаться `В_работе` с активным `BACK-000040`.
   - DoD: финальный статус `ROAD-000008` согласован с фактическим статусом и секцией `BACK-000040`.
4. Закрыть pass в журналах и governance-контуре.
   - Описание: Обновить `Logs/ChangeLog.md` и `Logs/QualityLog.md`, а `ADR` и `bp_lint.py` менять только при доказанной необходимости.
   - DoD: обязательная финальная governance-сверка пройдена, `python3 Tools/bp_lint.py --repo .` проходит, `PLAN-000028` и `BACK-000040` имеют корректный статус по факту результата.

## Риски
- сохранение `ROAD-000008` в статусе `В_работе` без активной backlog-задачи оставит governance-контур в неконсистентном состоянии;
- избыточная перепись `Discussion`, `Research`, `Requirements` или добавление новых discovery-артефактов выведет pass за пределы согласованного scope;
- преждевременное закрытие `ROAD-000008` без полной сверки `Backlog`, `Roadmap` и текущего `Plan` закрепит новую форму рассогласования.

## Артефакты
- `Docs/Technical/Pipeline.md`
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/Archive/Plans/PLAN-000028-fix-road-000008-governance-state.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`
- `Tools/bp_lint.py`

## DoD
- переход `Discussion -> Research -> Requirements -> Roadmap` больше не существует только как candidate-level хвост.
- у `ROAD-000008` есть реальная текущая или завершённая backlog-задача с `BACK-ID`.
- `Roadmap.md` и `Backlog.md` согласованы по текущему этапу.
- обязательная финальная governance-сверка пройдена.
- правило по шаблонам не нарушено.
- `python3 Tools/bp_lint.py --repo .` проходит.
- новый `ADR` создаётся только если реально нужен.
- `bp_lint.py` меняется только если обязательный contract действительно изменяется.

## Фактический результат
- `BACK-000040` перевёл оставшийся переход `Discussion -> Research -> Requirements -> Roadmap` из candidate-level хвоста в реальный pass и затем закрыл его как завершённую задачу.
- `Docs/Technical/Pipeline.md`, `Plans/Roadmap.md` и `Plans/Backlog.md` синхронизированы под правило, что активный этап roadmap не может оставаться без активной backlog-задачи.
- `ROAD-000008` закрыт как завершённый этап без остаточного governance-рассогласования по статусу, `Связанные_backlog` и секциям backlog.
- `bp_lint.py` не менялся, потому что обязательный contract путей, шаблонов и доменов не изменился; `bp_lint contract unaffected`.
- Новый `ADR` не создавался, потому что pass не вводил нового устойчивого архитектурного решения.
