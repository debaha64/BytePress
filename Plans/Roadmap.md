# Roadmap

## Индекс
- ROAD-000001 — Каркас репозитория и доменная структура (Repository Scaffold and Domain Structure)
- ROAD-000002 — Термины, идентификаторы и шаблоны (Terms, IDs, and Templates)
- ROAD-000003 — Инструменты и baseline `0.1.0` (Tools and Baseline `0.1.0`)
- ROAD-000004 — Продуктовый слой и product bootstrap (Product Layer and Product Bootstrap)
- ROAD-000005 — Discovery-слой и текущая истина (Discovery Layer and Current Truth)
- ROAD-000006 — Process contract и жизненный цикл артефактов (Process Contract and Artifact Lifecycle)
- ROAD-000007 — Управление развитием: Pipeline, Roadmap, Backlog и Plan (Development Governance: Pipeline, Roadmap, Backlog, and Plan)
- ROAD-000008 — Исследование и требования (Research and Requirements)
- ROAD-000009 — Операционная модель и governance-контур (Operating Model and Governance Contour)
- ROAD-000010 — Технический слой и карта системных контрактов (Technical Layer and System Contract Map)
- ROAD-000011 — Контур проверок и верификации (Verification and Validation Contour)
- ROAD-000012 — Точка входа агента и пользовательский слой (Agent Entry Point and User Layer)
- ROAD-000013 — Тиражирование product repo и baseline `0.2.0` (Product Repository Replication and Baseline `0.2.0`)
- ROAD-000014 — Интеграционный контур и будущие расширения (Integration Layer and Future Extensions)

## Легенда статусов
- Черновик
- Готово_к_утверждению
- Утверждено
- В_работе
- Завершено
- Отменено

---

## ROAD-000001 — Каркас репозитория и доменная структура (Repository Scaffold and Domain Structure)
ID: ROAD-000001
Этап: Каркас репозитория и доменная структура (Repository Scaffold and Domain Structure)
Статус: Завершено
Связи: BACK-000001, BACK-000002, BACK-000003, CHG-000001
Источник: PLAN-000001
Дата_создания: 2026-03-09
Дата_изменения: 2026-03-31
Цель: Собрать каркас `BytePress` как файловой системы доменов и закрепить базовую структуру репозитория.
Зависимости:
Связанные_backlog: BACK-000001, BACK-000002, BACK-000003

### Описание
Этап закрыл пересборку репозитория как доменной системы: домены разведены, каркас каталогов собран и базовая структура стала устойчивой.

---

## ROAD-000002 — Термины, идентификаторы и шаблоны (Terms, IDs, and Templates)
ID: ROAD-000002
Этап: Термины, идентификаторы и шаблоны (Terms, IDs, and Templates)
Статус: Завершено
Связи: BACK-000004, BACK-000006, BACK-000021, BACK-000023, BACK-000024, BACK-000025, CHG-000017, CHG-000018
Источник: PLAN-000002, PLAN-000007, PLAN-000008, PLAN-000009, PLAN-000012
Дата_создания: 2026-03-10
Дата_изменения: 2026-03-31
Цель: Нормализовать термины, внутренние ID и шаблонный слой так, чтобы последующие проходы опирались на единый contract именования и представления.
Зависимости: ROAD-000001
Связанные_backlog: BACK-000004, BACK-000006, BACK-000021, BACK-000023, BACK-000024, BACK-000025

### Описание
Этап закрыл term-layer, ID migration policy и шаблонный contract, на котором затем строятся документы, планы и журналы.

---

## ROAD-000003 — Инструменты и baseline `0.1.0` (Tools and Baseline `0.1.0`)
ID: ROAD-000003
Этап: Инструменты и baseline `0.1.0` (Tools and Baseline `0.1.0`)
Статус: Завершено
Связи: BACK-000005, BACK-000009, BACK-000010, BACK-000011, BACK-000012, BACK-000022, CHG-000019, CHG-000022
Источник: PLAN-000003, PLAN-000004, PLAN-000010, PLAN-000013
Дата_создания: 2026-03-10
Дата_изменения: 2026-03-31
Цель: Довести `Docs/Technical`, `Rules`, `Skills` и `Tools` до согласованного baseline `0.1.0`.
Зависимости: ROAD-000002
Связанные_backlog: BACK-000005, BACK-000009, BACK-000010, BACK-000011, BACK-000012, BACK-000022

### Описание
Этап закрыл усиление технического слоя, правил, навыков и инструментов, чтобы у BytePress появился рабочий baseline `0.1.0`.

---

## ROAD-000004 — Продуктовый слой и product bootstrap (Product Layer and Product Bootstrap)
ID: ROAD-000004
Этап: Продуктовый слой и product bootstrap (Product Layer and Product Bootstrap)
Статус: Завершено
Связи: BACK-000016, BACK-000026, BACK-000028, CHG-000009, CHG-000027, CHG-000028
Источник: PLAN-000015, PLAN-000016
Дата_создания: 2026-03-27
Дата_изменения: 2026-03-31
Цель: Нормализовать product-layer и подтвердить, что product bootstrap материализует минимальный продуктовый contract.
Зависимости: ROAD-000003
Связанные_backlog: BACK-000016, BACK-000026, BACK-000028

### Описание
Этап закрыл выравнивание `Docs/Product/*`, `Delivery` contract и product bootstrap/lint под минимальный продуктовый набор.

---

## ROAD-000005 — Discovery-слой и текущая истина (Discovery Layer and Current Truth)
ID: ROAD-000005
Этап: Discovery-слой и текущая истина (Discovery Layer and Current Truth)
Статус: Завершено
Связи: BACK-000029, ADR-000017, CHG-000029
Источник: PLAN-000017
Дата_создания: 2026-03-28
Дата_изменения: 2026-03-31
Цель: Выделить discovery-layer, закрепить current-truth интервью и привязать аналитический слой к плановому и журнальному контуру.
Зависимости: ROAD-000004
Связанные_backlog: BACK-000029

### Описание
Этап закрыл проявление `Docs/Discovery/`, current-truth модели интервью и нового аналитического слоя как части системы.

---

## ROAD-000006 — Process contract и жизненный цикл артефактов (Process Contract and Artifact Lifecycle)
ID: ROAD-000006
Этап: Process contract и жизненный цикл артефактов (Process Contract and Artifact Lifecycle)
Статус: Завершено
Связи: BACK-000017, BACK-000018, BACK-000019, BACK-000020, BACK-000027, BACK-000030, BACK-000031, CHG-000030, CHG-000031, CHG-000032, CHG-000033
Источник: PLAN-000006, PLAN-000018, PLAN-000019, PLAN-000020, PLAN-000021
Дата_создания: 2026-03-28
Дата_изменения: 2026-03-31
Цель: Закрепить process-contract task-ветки и PR, lifecycle артефактов и участие ключевых доменов в системе без двусмысленности.
Зависимости: ROAD-000005
Связанные_backlog: BACK-000017, BACK-000018, BACK-000019, BACK-000020, BACK-000027, BACK-000030, BACK-000031

### Описание
Этап закрыл branch/PR process, artifact lifecycle contract и participation contract доменов исполнения и расширения.

---

## ROAD-000007 — Управление развитием: Pipeline, Roadmap, Backlog и Plan (Development Governance: Pipeline, Roadmap, Backlog, and Plan)
ID: ROAD-000007
Этап: Управление развитием: Pipeline, Roadmap, Backlog и Plan (Development Governance: Pipeline, Roadmap, Backlog, and Plan)
Статус: Завершено
Связи: BACK-000032, BACK-000033, BACK-000034, BACK-000035, BACK-000036, CHG-000034, CHG-000035
Источник: PLAN-000022, PLAN-000023
Дата_создания: 2026-03-31
Дата_изменения: 2026-04-01
Цель: Построить управленческий контур, в котором развитие `BytePress` идёт по системе `Roadmap -> Backlog -> Plan`.
Зависимости: ROAD-000006
Связанные_backlog: BACK-000032, BACK-000033, BACK-000034, BACK-000035, BACK-000036

### Описание
Этап фокусируется на полном каноне `Pipeline`, непрерывном дальнем пути `Roadmap`, производном `Backlog`, который строго следует этапам roadmap, и на выравнивании связей между analytical, product и planning-контурами текущей стадии.

---

## ROAD-000008 — Исследование и требования (Research and Requirements)
ID: ROAD-000008
Этап: Исследование и требования (Research and Requirements)
Статус: Завершено
Связи: BACK-000037, BACK-000038, BACK-000039, BACK-000040, CHG-000040
Источник: PLAN-000024, PLAN-000025, PLAN-000026, PLAN-000027, PLAN-000028
Дата_создания: 2026-03-31
Дата_изменения: 2026-04-02
Цель: Ввести устойчивый исследовательский и требовательный контур до планирования новых типов проходов.
Зависимости: ROAD-000007
Связанные_backlog: BACK-000037, BACK-000038, BACK-000039, BACK-000040

### Описание
Этап закрыт: после фиксации места и шаблонов введены `Discussion`, `Research` и `Requirements` как реальные discovery-артефакты, а `BACK-000040` завершил переход `Discussion -> Research -> Requirements -> Roadmap`, синхронизировал governance-контур и снял остаточный шум этапа без расширения discovery-layer.

---

## ROAD-000009 — Операционная модель и governance-контур (Operating Model and Governance Contour)
ID: ROAD-000009
Этап: Операционная модель и governance-контур (Operating Model and Governance Contour)
Статус: Завершено
Связи: BACK-000041, BACK-000042, BACK-000043, BACK-000044, BACK-000045, BACK-000046, BACK-000047, BACK-000048, BACK-000049, BACK-000050, PLAN-000029, PLAN-000030, PLAN-000031, PLAN-000032, PLAN-000033, PLAN-000034, PLAN-000035, PLAN-000036, PLAN-000037, PLAN-000038
Источник: PLAN-000029, PLAN-000030, PLAN-000031, PLAN-000032, PLAN-000033, PLAN-000034, PLAN-000035, PLAN-000036, PLAN-000037, PLAN-000038
Дата_создания: 2026-03-31
Дата_изменения: 2026-04-07
Цель: Зафиксировать новую операционную модель `BytePress`, planning-contour и единую схему идентификаторов на уровне governance-contract, включая терминологию `этап / задача / проход`, ownership состояния, lifecycle `Plan`, завершённый active/archive planning-layer и hard-close contour без полной migration всех остальных historical доменов.
Зависимости: ROAD-000008
Связанные_backlog: BACK-000041, BACK-000042, BACK-000043, BACK-000044, BACK-000045, BACK-000046, BACK-000047, BACK-000048, BACK-000049, BACK-000050

### Описание
Этап завершён: `Roadmap` владеет стадиями, `Backlog` владеет задачами текущего этапа, `Plan` описывает только один текущий проход, единая `ID scheme` и порядок её migration зафиксированы отдельными governance-pass, active/archive layout planning-layer реализован, log-layer приведён к утверждённому serial-entry contract, active governance/supporting singleton-hybrid tail закрыт, а финальный audit-pass не подтвердил реального residual gap внутри `ROAD-000009`.

---

## ROAD-000010 — Технический слой и карта системных контрактов (Technical Layer and System Contract Map)
ID: ROAD-000010
Этап: Технический слой и карта системных контрактов (Technical Layer and System Contract Map)
Статус: В_работе
Связи: BACK-000051, PLAN-000039
Источник: PLAN-000039
Дата_создания: 2026-03-31
Дата_изменения: 2026-04-07
Цель: Определить границы `Docs/Technical/*`, минимальный состав technical-layer и карту системных контрактов без смешения technical knowledge-layer с `Pipeline/*` и planning/governance контуром.
Зависимости: ROAD-000009
Связанные_backlog: BACK-000051

### Описание
Этап стартует с boundary-pass: сначала фиксируются назначение `Docs/Technical/*`, его минимальное ядро и границы относительно `Pipeline/*`, `Plans/*`, `Runtime/*` и `Logs/*`, а уже затем возможны более узкие technical contract passes без широкого рефакторинга всего слоя.

---

## ROAD-000011 — Контур проверок и верификации (Verification and Validation Contour)
ID: ROAD-000011
Этап: Контур проверок и верификации (Verification and Validation Contour)
Статус: Черновик
Связи: отсутствуют
Источник: Следующий этап после technical layer and system contracts
Дата_создания: 2026-03-31
Дата_изменения: 2026-04-06
Цель: Собрать контур проверок и верификации поверх обновлённой operating model и технической карты системы без смешения verification-work с самой нормализацией техслоя.
Зависимости: ROAD-000010
Связанные_backlog: отсутствуют

### Описание
Этап подготавливает verification-layer, contract checks и модель верификации как отдельный следующий горизонт после фиксации системных контрактов.

---

## ROAD-000012 — Точка входа агента и пользовательский слой (Agent Entry Point and User Layer)
ID: ROAD-000012
Этап: Точка входа агента и пользовательский слой (Agent Entry Point and User Layer)
Статус: Черновик
Связи: отсутствуют
Источник: Следующий этап после verification contour
Дата_создания: 2026-03-31
Дата_изменения: 2026-04-06
Цель: Проявить устойчивую точку входа агента и согласованный пользовательский слой после того, как planning и verification-контуры перестанут противоречить друг другу.
Зависимости: ROAD-000011
Связанные_backlog: отсутствуют

### Описание
Этап объединяет agent entry point и `Docs/User/*` в один следующий продуктовый горизонт, не раскрывая его здесь в список мелких задач.

---

## ROAD-000013 — Тиражирование product repo и baseline `0.2.0` (Product Repository Replication and Baseline `0.2.0`)
ID: ROAD-000013
Этап: Тиражирование product repo и baseline `0.2.0` (Product Repository Replication and Baseline `0.2.0`)
Статус: Черновик
Связи: отсутствуют
Источник: Следующий этап после agent entry and user layer
Дата_создания: 2026-03-31
Дата_изменения: 2026-04-06
Цель: Подготовить повторяемое тиражирование product repo и следующий baseline `0.2.0` как отдельный управляемый этап после проявления точки входа агента и пользовательского слоя.
Зависимости: ROAD-000012
Связанные_backlog: отсутствуют

### Описание
Этап связывает replication-path и подготовку к `0.2.0`, не смешивая это с последующим интеграционным контуром и будущими расширениями.

---

## ROAD-000014 — Интеграционный контур и будущие расширения (Integration Layer and Future Extensions)
ID: ROAD-000014
Этап: Интеграционный контур и будущие расширения (Integration Layer and Future Extensions)
Статус: Черновик
Связи: отсутствуют
Источник: Дальний стратегический этап
Дата_создания: 2026-03-31
Дата_изменения: 2026-04-06
Цель: Развить интеграционный контур, будущие расширения и дальний growth-horizon `BytePress` после replication-stage и baseline `0.2.0`.
Зависимости: ROAD-000013
Связанные_backlog: отсутствуют

### Описание
Дальний этап, в котором интеграции, расширения и последующее масштабирование сходятся в следующий горизонт развития без дополнительной детализации текущим corrective pass.
