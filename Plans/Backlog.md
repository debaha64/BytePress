# Backlog

## Индекс
- ROAD-000011 — Контур проверок и верификации (Verification and Validation Contour) | Активные: BACK-000065 | Завершённые: BACK-000062, BACK-000063, BACK-000064 | Кандидаты задач этапа

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

## ROAD-000011 — Контур проверок и верификации (Verification and Validation Contour)

### Активные

#### BACK-000065 — Зафиксировать tooling boundary verification-контура
ID: BACK-000065
Название: Зафиксировать tooling boundary verification-контура
Тип: Документация
Приоритет: Критический
Статус: В_работе
Связи: ROAD-000011, PLAN-000053
Источник: Следующий узкий pass этапа `ROAD-000011`
Дата_создания: 2026-04-07
Дата_изменения: 2026-04-07

##### Описание
Пересобрать `Tools/README.md` как boundary-document tooling verification contour: развести роль `bp_lint`, target role будущего `bp_check`, target role будущего `bp_verify`, structural checks, contract/verification checks и procedural verification без реализации новых инструментов.

### Завершённые

#### BACK-000062 — Зафиксировать границы verification-layer
ID: BACK-000062
Название: Зафиксировать границы verification-layer
Тип: Документация
Приоритет: Критический
Статус: Завершено
Связи: ROAD-000011, PLAN-000050
Источник: Первый узкий pass этапа `ROAD-000011`
Дата_создания: 2026-04-07
Дата_изменения: 2026-04-07

##### Описание
Активировать `ROAD-000011`, определить место verification/checks contour в системе и пересобрать `Docs/Technical/Verification.md` как boundary-document, который явно разводит verification-layer, automatic checks, procedural checks, `Pipeline` gates и tool implementation без рефакторинга toolchain.

#### BACK-000063 — Пересобрать contract map verification-layer
ID: BACK-000063
Название: Пересобрать contract map verification-layer
Тип: Документация
Приоритет: Критический
Статус: Завершено
Связи: ROAD-000011, PLAN-000051
Источник: Следующий узкий pass этапа `ROAD-000011`
Дата_создания: 2026-04-07
Дата_изменения: 2026-04-07

##### Описание
Пересобрать `Docs/Technical/Verification.md` из boundary-document в contract map verification-layer: зафиксировать классы checks, verification inputs/outputs, evidence формы, ownership интерпретации результата и явную границу между automatic checks, procedural checks и process gates без рефакторинга toolchain.

#### BACK-000064 — Зафиксировать verification levels и target automation split
ID: BACK-000064
Название: Зафиксировать verification levels и target automation split
Тип: Документация
Приоритет: Критический
Статус: Завершено
Связи: ROAD-000011, PLAN-000052
Источник: Следующий узкий pass этапа `ROAD-000011`
Дата_создания: 2026-04-07
Дата_изменения: 2026-04-07

##### Описание
Создать `Docs/Technical/Verification_Levels.md` и зафиксировать уровни verification-контура, evidence, ownership результата и target contract будущих `bp_check / bp_verify` без реализации нового toolchain.

### Кандидаты задач этапа
- нет
