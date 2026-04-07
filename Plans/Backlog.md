# Backlog

## Индекс
- ROAD-000010 — Технический слой и карта системных контрактов (Technical Layer and System Contract Map) | Активные: BACK-000058 | Завершённые: BACK-000051, BACK-000052, BACK-000053, BACK-000054, BACK-000055, BACK-000056, BACK-000057 | Кандидаты задач этапа

## Легенда типов
- Система
- Документация
- Стандарт
- Инструмент
- Продукт
- Исследование
- Инфраструктура
- Поддержка

## Легенда приоритетов
- Низкий
- Средний
- Высокий
- Критический

## Легенда статусов
- Черновик
- Готово_к_утверждению
- Утверждено
- В_работе
- Завершено
- Отменено

---

## Архив
Historical backlog завершённых этапов хранится в `Plans/Archive/Backlog/ROAD-<NNNNNN>.md`.

---

## ROAD-000010 — Технический слой и карта системных контрактов (Technical Layer and System Contract Map)

### Активные

#### BACK-000058 — Пересобрать Platform_Contracts.md как platform-contract
ID: BACK-000058
Название: Пересобрать Platform_Contracts.md как platform-contract
Тип: Документация
Приоритет: Критический
Статус: В_работе
Связи: ROAD-000010, PLAN-000046
Источник: Следующий узкий pass этапа `ROAD-000010` после system-invariants pass
Дата_создания: 2026-04-07
Дата_изменения: 2026-04-07

##### Описание
Провести audit `Docs/Technical/Platform_Contracts.md`, `Tools/*`, `Pipeline/*`, planning/runtime touchpoints и platform assumptions текущего `BytePress`, затем пересобрать `Platform_Contracts.md` как канонический contract рабочей платформы, среды исполнения, supported tool perimeter, допустимых режимов platform usage и недопустимых отклонений без широкого рефакторинга всего technical-layer.

### Завершённые

#### BACK-000057 — Пересобрать System_Invariants.md как invariant-contract
ID: BACK-000057
Название: Пересобрать System_Invariants.md как invariant-contract
Тип: Документация
Приоритет: Критический
Статус: Завершено
Связи: ROAD-000010, PLAN-000045
Источник: Следующий узкий pass этапа `ROAD-000010` после interfaces-core pass
Дата_создания: 2026-04-07
Дата_изменения: 2026-04-07

##### Описание
Зафиксировать место `Docs/Technical/System_Invariants.md` в required core technical-layer, использовать общий `Templates/Document.md` без создания отдельного шаблона, затем пересобрать `System_Invariants.md` как канонический contract системных инвариантов текущего `BytePress` и синхронизировать только реально необходимые related contracts и tooling.

#### BACK-000056 — Пересобрать Interfaces.md как interface-contract
ID: BACK-000056
Название: Пересобрать Interfaces.md как interface-contract
Тип: Документация
Приоритет: Критический
Статус: Завершено
Связи: ROAD-000010, PLAN-000044
Источник: Следующий узкий pass этапа `ROAD-000010` после artifact-lifecycle pass
Дата_создания: 2026-04-07
Дата_изменения: 2026-04-07

##### Описание
Провести audit `Docs/Technical/Interfaces.md` и его пересечений с `Docs/Technical/README.md`, `Docs/Technical/Architecture.md`, `Docs/Technical/Model.md`, `Docs/Technical/Artifact_Lifecycle.md`, `Docs/Technical/Pipeline.md`, `Pipeline/*`, `Plans/*`, `Runtime/*` и `Logs/*`, затем пересобрать `Interfaces.md` как канонический contract внутренних и внешних интерфейсов, допустимых точек стыка и недопустимых обходов границ без широкого рефакторинга всего technical-layer.

#### BACK-000051 — Зафиксировать границы и минимальный состав Docs/Technical
ID: BACK-000051
Название: Зафиксировать границы и минимальный состав Docs/Technical
Тип: Документация
Приоритет: Критический
Статус: Завершено
Связи: ROAD-000010, PLAN-000039
Источник: Первый узкий pass этапа `ROAD-000010`
Дата_создания: 2026-04-07
Дата_изменения: 2026-04-07

##### Описание
Определить границы `Docs/Technical/*`, минимальный состав technical-layer и ясное разведение с `Pipeline/*`, `Plans/*`, `Runtime/*` и `Logs/*` без широкого рефакторинга technical-documents.

#### BACK-000052 — Уточнить карту системных контрактов technical-layer
ID: BACK-000052
Название: Уточнить карту системных контрактов technical-layer
Тип: Документация
Приоритет: Критический
Статус: Завершено
Связи: ROAD-000010, PLAN-000040
Источник: Следующий узкий pass этапа `ROAD-000010` после фиксации technical boundaries
Дата_создания: 2026-04-07
Дата_изменения: 2026-04-07

##### Описание
Провести audit `Docs/Technical/*` и `Pipeline/*`, зафиксировать карту системных контрактов technical-layer, явно развести обязательные и вспомогательные technical-documents и снять remaining смысловые пересечения между technical-layer и process-layer без широкого рефакторинга всего слоя.

#### BACK-000053 — Пересобрать Architecture.md как карту доменов и слоёв
ID: BACK-000053
Название: Пересобрать Architecture.md как карту доменов и слоёв
Тип: Документация
Приоритет: Критический
Статус: Завершено
Связи: ROAD-000010, PLAN-000041
Источник: Следующий узкий pass этапа `ROAD-000010` после contract-map pass
Дата_создания: 2026-04-07
Дата_изменения: 2026-04-07

##### Описание
Провести audit `Docs/Technical/Architecture.md` и его пересечений с `Docs/Technical/README.md`, `Docs/Technical/Pipeline.md`, `Pipeline/*`, `Plans/*`, `Runtime/*` и `Logs/*`, затем пересобрать `Architecture.md` как каноническую карту доменов, слоёв, границ ответственности и недопустимых подмен без широкого рефакторинга всего technical-layer.

#### BACK-000054 — Пересобрать Model.md как каноническую модель системы
ID: BACK-000054
Название: Пересобрать Model.md как каноническую модель системы
Тип: Документация
Приоритет: Критический
Статус: Завершено
Связи: ROAD-000010, PLAN-000042
Источник: Следующий узкий pass этапа `ROAD-000010` после architecture-core pass
Дата_создания: 2026-04-07
Дата_изменения: 2026-04-07

##### Описание
Провести audit `Docs/Technical/Model.md` и его пересечений с `Docs/Technical/README.md`, `Docs/Technical/Architecture.md`, `Docs/Technical/Artifact_Lifecycle.md`, `Docs/Technical/Pipeline.md`, `Pipeline/*`, `Plans/*`, `Runtime/*` и `Logs/*`, затем пересобрать `Model.md` как каноническую модель ключевых сущностей, ownership состояния, основных связей и недопустимых смешений ответственности без широкого рефакторинга всего technical-layer.

#### BACK-000055 — Пересобрать Artifact_Lifecycle.md как lifecycle-contract
ID: BACK-000055
Название: Пересобрать Artifact_Lifecycle.md как lifecycle-contract
Тип: Документация
Приоритет: Критический
Статус: Завершено
Связи: ROAD-000010, PLAN-000043
Источник: Следующий узкий pass этапа `ROAD-000010` после model-core pass
Дата_создания: 2026-04-07
Дата_изменения: 2026-04-07

##### Описание
Провести audit `Docs/Technical/Artifact_Lifecycle.md` и его пересечений с `Docs/Technical/README.md`, `Docs/Technical/Architecture.md`, `Docs/Technical/Model.md`, `Docs/Technical/Pipeline.md`, `Pipeline/*`, `Plans/*`, `Runtime/*` и `Logs/*`, затем пересобрать `Artifact_Lifecycle.md` как канонический lifecycle-contract артефактов, источников истины, обязательных синхронизаций и недопустимых lifecycle-пропусков без широкого рефакторинга всего technical-layer.

### Кандидаты задач этапа
- нет
