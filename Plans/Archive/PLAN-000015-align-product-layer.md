# PLAN-000015 — Align product layer

ID: PLAN-000015
Название: Нормализовать продуктовый слой `Docs/Product/` по каноническим шаблонам
Статус: Завершено
Связи: BACK-000026, CHG-000027
Источник: Документный проход после утверждения шаблонов `PRD` и `JTBD`
Дата_создания: 2026-03-27
Дата_изменения: 2026-03-27
Основание: В `Docs/Product/` смешаны продуктовые документы, технические артефакты и прямые дубли plan-layer. Нужно сохранить только минимальный продуктовый слой, привести `PRD` и `JTBD` к принятым шаблонам и синхронизировать ссылки без выхода в большой рефакторинг репозитория.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000026
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать управляемый контур прохода.
   - Описание: Добавить backlog-элемент текущей задачи, capture следующего цикла по Git/PR subsystem и отдельный plan-file для этого прохода.
   - DoD: `Plans/Backlog.md` содержит `BACK-000026` и `BACK-000027`, а `Plans/Archive/PLAN-000015-align-product-layer.md` описывает scope и ограничения текущей задачи.
2. Привести `JTBD` и `PRD` к каноническим шаблонам.
   - Описание: Минимально выровнять `Docs/Product/JTBD.md` по `Templates/JTBD.md`, а основной фокус прохода направить на `Docs/Product/PRD.md`, убрав из него внутренние системно-технические сущности и избыточные дубли.
   - DoD: `JTBD` использует шаблон без лишней переписи, а `PRD` использует шаблон `Templates/PRD.md` и описывает только продуктовый слой первой версии.
3. Очистить `Docs/Product/` до минимального состава.
   - Описание: Оставить только `README.md`, `JTBD.md`, `PRD.md`, `Delivery.md`; удалить дубли plan-layer и вынести технические документы в канонические точки знания.
   - DoD: `Docs/Product/` содержит только четыре целевых файла, а содержимое вынесенных документов либо перенесено в `Docs/Technical/*` и существующие README, либо удалено как дубль.
4. Синхронизировать прямые ссылки и журналы без лишнего выхода за scope.
   - Описание: Обновить только те README, планы, логи и явные ссылки, которые реально зависят от старых путей или состава `Docs/Product/`.
   - DoD: прямые ссылки не ведут на удалённые файлы, `ChangeLog` и `QualityLog` отражают факты прохода, а `Plan` и `Backlog` переведены в финальный статус.

## Риски
- перенос технических документов может породить лишние новые файлы вместо интеграции в существующие точки знания;
- переписывание `JTBD` сверх минимума нарушит ограничение текущего прохода;
- попытка затронуть `Tools/*`, `Schemas/*`, `Rules/*` и `Standards/*` сверх необходимой синхронизации выведет работу за согласованный scope.

## Артефакты
- `Plans/Backlog.md`
- `Plans/Archive/PLAN-000015-align-product-layer.md`
- `Plans/Archive/PLAN-000005-adapters-memory-mcp-and-bootstrap.md`
- `Plans/Archive/PLAN-000010-tools-contract-sync.md`
- `Plans/Archive/PLAN-000011-migrate-active-nonlog-ids.md`
- `Plans/Archive/PLAN-000012-migrate-historical-logs.md`
- `Docs/Product/README.md`
- `Docs/Product/JTBD.md`
- `Docs/Product/PRD.md`
- `Docs/Product/Delivery.md`
- `Docs/Technical/README.md`
- `Docs/Technical/Product_Bootstrap_Contract.md`
- `Docs/Technical/Product_Bootstrap_Validation.md`
- `Profiles/README.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`

## DoD
- `Docs/Product/` содержит только `README.md`, `JTBD.md`, `PRD.md`, `Delivery.md`.
- `PRD` и `JTBD` приведены к каноническим шаблонам без смешения продуктового и технического слоёв.
- дубли и технические артефакты вынесены из `Docs/Product/`, а прямые ссылки синхронизированы.
- `Tools/*`, `Schemas/*`, `Rules/*` и `Standards/*` не меняются, кроме строго необходимой синхронизации ссылок.
- `Backlog`, `Plan`, `ChangeLog` и `QualityLog` отражают фактическое завершение прохода.
