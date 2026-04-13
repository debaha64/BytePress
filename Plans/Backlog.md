# Backlog

## Индекс
- ROAD-000014 — Интеграционный контур и будущие расширения

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

## Архив
Historical backlog завершённых этапов хранится в `Plans/Archive/Backlog/ROAD-<NNNNNN>.md`.

---

## ROAD-000014 — Интеграционный контур и будущие расширения

### Активные

#### BACK-000077 — Активировать controlled integration contour
ID: BACK-000077
Название: Активировать controlled integration contour
Тип: Инфраструктура
Приоритет: Высокий
Статус: В_работе
Связи: ROAD-000014, PLAN-000065
Источник: Activation pass этапа `ROAD-000014`
Дата_создания: 2026-04-13
Дата_изменения: 2026-04-13

##### Описание
Зафиксировать канонический integration contour `BytePress`, controlled connector handoff между `Adapters/*`, `MCP/*`, `Tools/*`, bootstrap-generated product repo и `scripts/*`, materialize minimal integration smoke route без открытия реальных внешних подключений и оставить stage в управляемом активном состоянии.

### Завершённые
- отсутствуют

### Кандидаты задач этапа
- Следующий узкий фронт: оформить repo-native integration evidence handoff для generated product repo без открытия реальных connector runtimes и без расширения bootstrap-stage.
