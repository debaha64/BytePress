# Backlog

## Индекс
- ROAD-000009 — Операционная модель и governance-контур (Operating Model and Governance Contour) | Активные: нет | Завершённые: BACK-000041, BACK-000042, BACK-000043, BACK-000044, BACK-000045, BACK-000046, BACK-000047, BACK-000048 | Кандидаты задач этапа

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

## ROAD-000009 — Операционная модель и governance-контур (Operating Model and Governance Contour)

### Активные

- нет

### Завершённые

#### BACK-000048 — Привести governance/supporting domains к unified ID scheme
ID: BACK-000048
Название: Привести governance/supporting domains к unified ID scheme
Тип: Стандарт
Приоритет: Критический
Статус: Завершено
Связи: ROAD-000009, PLAN-000036
Источник: Следующий узкий pass внутри `ROAD-000009` после log-layer migration
Дата_создания: 2026-04-06
Дата_изменения: 2026-04-06

##### Описание
Привести `Rules/*`, `Standards/*`, `Templates/*` и `Schemas/*` к уже утверждённой unified `ID scheme` в реально необходимом объёме, не меняя лишние filename/path-contract и синхронизируя только тот ссылочный слой, который действительно затрагивается этим migration-pass.

#### BACK-000047 — Привести log-layer к unified ID scheme
ID: BACK-000047
Название: Привести log-layer к unified ID scheme
Тип: Стандарт
Приоритет: Критический
Статус: Завершено
Связи: ROAD-000009, PLAN-000035
Источник: Следующий узкий pass внутри `ROAD-000009` после cleanup planning legacy-tail
Дата_создания: 2026-04-06
Дата_изменения: 2026-04-06

##### Описание
Привести `Logs/*` к уже утверждённой unified `ID scheme` в пределах фактически существующего log-layer, убрать рассогласование между singleton log-files и serial log entries, а также синхронизировать реально затронутый ссылочный слой без открытия других доменов.

#### BACK-000046 — Удалить runtime plan legacy-tail из planning-контура
ID: BACK-000046
Название: Удалить runtime plan legacy-tail из planning-контура
Тип: Стандарт
Приоритет: Критический
Статус: Завершено
Связи: ROAD-000009, PLAN-000034
Источник: Следующий узкий pass внутри `ROAD-000009` после backlog archive migration
Дата_создания: 2026-04-06
Дата_изменения: 2026-04-06

##### Описание
Удалить `Runtime/Plan.md` из рабочего дерева, убрать active-layer правила и transitional policy, завязанные на его существование, и зафиксировать planning-contour в состоянии без legacy runtime plan и без двусмысленности в активной модели.

#### BACK-000045 — Вывести backlog history-layer в stage archive
ID: BACK-000045
Название: Вывести backlog history-layer в stage archive
Тип: Стандарт
Приоритет: Критический
Статус: Завершено
Связи: ROAD-000009, PLAN-000033
Источник: Следующий узкий pass внутри `ROAD-000009` после migration plan-layer
Дата_создания: 2026-04-06
Дата_изменения: 2026-04-06

##### Описание
Выполнить archive migration historical backlog прошлых этапов: вывести их из активного `Plans/Backlog.md`, ввести поэтапный archive layout в `Plans/Archive/Backlog/` и оставить в активном backlog только текущий этап `ROAD-000009` без изменения plan archive-layer и без migration других доменов.

#### BACK-000041 — Зафиксировать operating model pass для ROAD-000009
ID: BACK-000041
Название: Зафиксировать operating model pass для ROAD-000009
Тип: Стандарт
Приоритет: Критический
Статус: Завершено
Связи: ROAD-000009, PLAN-000029
Источник: Первый governance-pass новой operating model `BytePress`
Дата_создания: 2026-04-06
Дата_изменения: 2026-04-06

##### Описание
Закрепить терминологию `этап / задача / проход`, ownership состояния, lifecycle `Plan`, правило неканоничности `Runtime/Plan.md` и hard-close contour задачи на уровне planning-contract без полной ID migration, без массового архива и без переписывания `AGENTS.md`.

#### BACK-000042 — Снять противоречия planning transition внутри ROAD-000009
ID: BACK-000042
Название: Снять противоречия planning transition внутри ROAD-000009
Тип: Стандарт
Приоритет: Критический
Статус: Завершено
Связи: ROAD-000009, PLAN-000030
Источник: Corrective pass после merge `docs/000034-activate-road-000009-operating-model`
Дата_создания: 2026-04-06
Дата_изменения: 2026-04-06

##### Описание
Согласовать `Roadmap` с утверждённым горизонтом `ROAD-000009`–`ROAD-000014`, снять противоречия между целевой planning-моделью и текущим переходным состоянием дерева, а также явно зафиксировать transitional policy для historical backlog-записей, `BP-*` plan-files и legacy-артефакта `Runtime/Plan.md`.

#### BACK-000043 — Определить unified ID scheme для репозитория
ID: BACK-000043
Название: Определить unified ID scheme для репозитория
Тип: Стандарт
Приоритет: Критический
Статус: Завершено
Связи: ROAD-000009, PLAN-000031
Источник: Следующий узкий pass внутри `ROAD-000009` после выравнивания planning transition
Дата_создания: 2026-04-06
Дата_изменения: 2026-04-06

##### Описание
Зафиксировать целевую единую схему идентификаторов для всего репозитория: классы артефактов по модели идентификации, правила `ID` и filename для serial / hybrid / singleton domains, правила внутренних ссылок и порядок будущей migration по доменам без запуска самой migration.

#### BACK-000044 — Перевести history plan-files в archive layer
ID: BACK-000044
Название: Перевести history plan-files в archive layer
Тип: Стандарт
Приоритет: Критический
Статус: Завершено
Связи: ROAD-000009, PLAN-000032
Источник: Следующий узкий pass внутри `ROAD-000009` после фиксации unified `ID scheme`
Дата_создания: 2026-04-06
Дата_изменения: 2026-04-06

##### Описание
Выполнить migration plan-files внутри planning-contour: перевести historical legacy `BP-*` в целевой `PLAN-*` filename-contract, ввести archive policy через `Plans/Archive/`, переместить туда завершённые `Plan` и оставить в активном слое только один текущий `Plan`.

### Кандидаты задач этапа
- Уточнить контур hard-close для следующих governance-pass этапа
