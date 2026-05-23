# PLAN-000017 — Discovery and sync contract

ID: PLAN-000017
Название: Проявить Discovery layer и закрепить sync-contract артефактов
Статус: Завершено
Связи: BACK-000029, ADR-000017, CHG-000029
Источник: Discovery/sync-contract pass после выравнивания продуктового и bootstrap-layer contracts
Дата_создания: 2026-03-28
Дата_изменения: 2026-03-28
Основание: В системе отсутствует явный аналитический слой `Docs/Discovery/`, интервью не закреплено как current truth, `Roadmap` содержит слишком детальный уровень проходов, а pipeline contract не фиксирует обязательную проверку связанных артефактов после изменения интервью, шаблонов и ключевых документов.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000029
Связанные_ADR:
- ADR-000017

## Шаги
1. Зафиксировать управляемый контур прохода.
   - Описание: Добавить один backlog-item текущей задачи и отдельный plan-file для discovery/sync-contract pass.
   - DoD: `Plans/Backlog.md` содержит `BACK-000029`, а `Plans/Archive/Plans/PLAN-000017-discovery-and-sync-contract.md` фиксирует scope и ограничения прохода.
2. Проявить discovery-domain и current-truth interview.
   - Описание: Создать `Docs/Discovery/README.md`, `Templates/Interview.md` и `Docs/Discovery/Interview.md`, где интервью описывает текущую истину, а не журнал сессий.
   - DoD: `Docs/Discovery/` существует, `Interview.md` фиксирует краткие актуальные ответы по BytePress, а `Docs/README.md` отражает новый слой.
3. Синхронизировать roadmap и pipeline contract.
   - Описание: Привести `Plans/Roadmap.md` к уровню крупных этапов системы и добавить в `Docs/Technical/Pipeline.md` минимальную sync-matrix по обязательной проверке связанных артефактов.
   - DoD: roadmap не дублирует backlog, а pipeline contract фиксирует полезный минимальный набор правил синхронизации после изменения интервью, шаблонов, product docs и инструментов.
4. Синхронизировать lint и архитектурную фиксацию.
   - Описание: Обновить `Tools/bp_lint.py` под новый discovery-contract и создать ADR только если existing ADR не покрывают новый аналитический домен, current-truth модель интервью и sync-matrix.
   - DoD: lint валидирует `Docs/Discovery/README.md`, `Docs/Discovery/Interview.md` и `Templates/Interview.md`; история изменений закреплена в `Roadmap`, `Backlog`, `Plan`, `Logs`, а при необходимости и `ADR`.

## Риски
- перенос interview в current-truth модель без явной фиксации истории в `Roadmap`, `Backlog`, `Plan` и `Logs` создаст двусмысленность;
- детализация roadmap до уровня отдельных проходов сохранит смешение roadmap и backlog;
- отсутствие обновления `bp_lint.py` оставит discovery-contract декларацией без проверки.

## Артефакты
- `Plans/Backlog.md`
- `Plans/Archive/Plans/PLAN-000017-discovery-and-sync-contract.md`
- `Docs/Discovery/README.md`
- `Docs/Discovery/Interview.md`
- `Docs/README.md`
- `Templates/Interview.md`
- `Templates/README.md`
- `Docs/Technical/Pipeline.md`
- `Plans/Roadmap.md`
- `Plans/README.md`
- `Docs/Technical/Architecture.md`
- `Docs/Technical/Model.md`
- `Docs/Technical/README.md`
- `Tools/bp_lint.py`
- `Logs/ADRlog.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`

## DoD
- существует `Docs/Discovery/README.md`.
- существует `Docs/Discovery/Interview.md`.
- существует `Templates/Interview.md`.
- интервью фиксируется как current truth, а не журнал сессий; история изменений живёт в `Roadmap`, `Backlog`, `Plan`, `Logs` и при необходимости `ADR`.
- `Plans/Roadmap.md` отражает только крупные этапы уровня системы.
- `Docs/Technical/Pipeline.md` содержит минимальный полезный sync-contract артефактов.
- `bp_lint.py` валидирует discovery-contract.
- scope ограничен `Docs/Discovery/*`, `Templates/Interview.md`, `Docs/Technical/Pipeline.md`, `Plans/Roadmap.md`, минимально нужными `Docs/Technical/*`, `Docs/README.md`, `Templates/README.md`, `Plans/README.md`, `Tools/bp_lint.py` и журналами; `Rules/*`, `Standards/*`, `Schemas/*`, process-docs и `Tools/bp_bootstrap.py` не меняются без прямого blocker.
