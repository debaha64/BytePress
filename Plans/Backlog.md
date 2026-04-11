# Backlog

## Индекс
- ROAD-000011 — Контур проверок и верификации (Verification and Validation Contour) | Активные: нет | Завершённые: BACK-000062, BACK-000063, BACK-000064, BACK-000065, BACK-000066, BACK-000067, BACK-000068, BACK-000069, BACK-000070, BACK-000071 | Кандидаты задач этапа

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

- нет

### Завершённые

#### BACK-000071 — Зафиксировать tooling boundary validation-контура
ID: BACK-000071
Название: Зафиксировать tooling boundary validation-контура
Тип: Документация
Приоритет: Критический
Статус: Завершено
Связи: ROAD-000011, PLAN-000059
Источник: Следующий узкий pass этапа `ROAD-000011`
Дата_создания: 2026-04-11
Дата_изменения: 2026-04-11

##### Описание
Пересобрать `Tools/README.md` так, чтобы tooling boundary явно покрывал не только verification contour, но и validation contour: развести validation tooling support, verification tooling, procedural validation, границу между validation result и gate decision, а также не вводить новый validation toolchain.

#### BACK-000070 — Зафиксировать contract validation evidence
ID: BACK-000070
Название: Зафиксировать contract validation evidence
Тип: Документация
Приоритет: Критический
Статус: Завершено
Связи: ROAD-000011, PLAN-000058
Источник: Следующий узкий pass этапа `ROAD-000011`
Дата_создания: 2026-04-11
Дата_изменения: 2026-04-11

##### Описание
Создать `Docs/Technical/Validation_Evidence.md` и зафиксировать contract validation evidence: classes validation evidence, mandatory/optional evidence, relation к validation levels, storage expectations, sufficient/insufficient evidence и связь с pass-close contour без реализации validation toolchain.

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

#### BACK-000065 — Зафиксировать tooling boundary verification-контура
ID: BACK-000065
Название: Зафиксировать tooling boundary verification-контура
Тип: Документация
Приоритет: Критический
Статус: Завершено
Связи: ROAD-000011, PLAN-000053
Источник: Следующий узкий pass этапа `ROAD-000011`
Дата_создания: 2026-04-07
Дата_изменения: 2026-04-07

##### Описание
Пересобрать `Tools/README.md` как boundary-document tooling verification contour: развести роль `bp_lint`, target role будущего `bp_check`, target role будущего `bp_verify`, structural checks, contract/verification checks и procedural verification без реализации новых инструментов.

#### BACK-000066 — Зафиксировать contract verification evidence
ID: BACK-000066
Название: Зафиксировать contract verification evidence
Тип: Документация
Приоритет: Критический
Статус: Завершено
Связи: ROAD-000011, PLAN-000054
Источник: Следующий узкий pass этапа `ROAD-000011`
Дата_создания: 2026-04-08
Дата_изменения: 2026-04-08

##### Описание
Создать `Docs/Technical/Verification_Evidence.md` и зафиксировать contract verification evidence: виды evidence, mandatory/optional по классам checks, место хранения evidence и связи с pass-close contour без реализации нового toolchain.

#### BACK-000067 — Зафиксировать границы validation-layer
ID: BACK-000067
Название: Зафиксировать границы validation-layer
Тип: Документация
Приоритет: Критический
Статус: Завершено
Связи: ROAD-000011, PLAN-000055
Источник: Следующий узкий pass этапа `ROAD-000011`
Дата_создания: 2026-04-08
Дата_изменения: 2026-04-08

##### Описание
Создать `Docs/Technical/Validation.md` и зафиксировать место validation-layer в системе: развести validation и verification, определить inputs/outputs, связь с evidence, phase gates и pass-close contour без реализации нового toolchain.

#### BACK-000068 — Пересобрать contract map validation-layer
ID: BACK-000068
Название: Пересобрать contract map validation-layer
Тип: Документация
Приоритет: Критический
Статус: Завершено
Связи: ROAD-000011, PLAN-000056
Источник: Следующий узкий pass этапа `ROAD-000011`
Дата_создания: 2026-04-08
Дата_изменения: 2026-04-08

##### Описание
Пересобрать `Docs/Technical/Validation.md` из boundary-doc в contract map validation-layer: явно зафиксировать validation inputs/outputs, classes validation result, ownership интерпретации результата, отношение к evidence package, место в pass-close contour и границу между validation result и gate decision без реализации нового toolchain.

#### BACK-000069 — Зафиксировать уровни validation-контура
ID: BACK-000069
Название: Зафиксировать уровни validation-контура
Тип: Документация
Приоритет: Критический
Статус: Завершено
Связи: ROAD-000011, PLAN-000057
Источник: Следующий узкий pass этапа `ROAD-000011`
Дата_создания: 2026-04-08
Дата_изменения: 2026-04-08

##### Описание
Создать `Docs/Technical/Validation_Levels.md` и зафиксировать уровни validation-контура: назначение каждого уровня, required inputs, expected outputs, relation к `Validation.md`, relation к `Verification_Evidence.md`, relation к pass-close contour и границы того, что не должно автоматизироваться и смешиваться с verification levels.

### Кандидаты задач этапа
- нет
