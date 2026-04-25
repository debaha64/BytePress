# Backlog

## Индекс
- ROAD-000021 — Разделить product lint для свежего bootstrap и развивающегося продукта

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

## ROAD-000021 — Разделить product lint для свежего bootstrap и развивающегося продукта

### Активные

#### BACK-000086 — Разделить fresh и developed проверки product repo
ID: BACK-000086
Название: Разделить fresh и developed проверки product repo
Тип: Инструмент
Приоритет: Критический
Статус: В_работе
Связи: ROAD-000021, PLAN-000074
Источник: Corrective pass after first evolving product repository check
Дата_создания: 2026-04-26
Дата_изменения: 2026-04-26

##### Описание
`bp_lint.py` должен сохранить строгий fresh bootstrap gate и добавить отдельный developed product gate для состояния после подтверждения current truth и закрытия первого product-start pass. Generated `scripts/dev-test.sh`, validation docs и lifecycle references должны явно показывать выбранный режим проверки.

### Завершённые
- отсутствуют

### Кандидаты задач этапа
- нет

---
