# Roadmap

## Индекс
- ROAD-000032 — Verification contract reduction and language cleanup
- ROAD-000031 — Semantic cleanup after retired domain removal
- ROAD-000030 — Already-created product service update route ID correction
- ROAD-000029 — Product pipeline control and retired domain cleanup
- ROAD-000028 — Синхронизация терминов и проверок нового product skeleton
- ROAD-000027 — Локальный Tools создаваемого продукта и переходный product lint
- ROAD-000026 — Профильная фабрика продуктовых каркасов и сокращение доменной модели
- ROAD-000025 — Русские проверочные маркеры lint-договора
- ROAD-000024 — Договор карт доменов и ADR-журнала
- ROAD-000023 — Языковая и картографическая чистка активного и создаваемого слоя
- ROAD-000022 — Канонический путь обновления service-layer created product repo
- ROAD-000021 — Разделить product lint для свежего bootstrap и развивающегося продукта
- ROAD-000020 — Семантическая чистка стартового контура после повторного полевого теста
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
- ROAD-000015 — Release readiness и factual log closure (Release Readiness and Factual Log Closure)
- ROAD-000016 — Post-release sync после `0.2.0` (Post-release Sync After `0.2.0`)
- ROAD-000017 — Discovery minimum bootstrap и startup-handshake агента (Bootstrap Discovery Minimum and Agent Startup Handshake)
- ROAD-000018 — Product-start control gaps after first field test (Product-Start Control Gaps After First Field Test)
- ROAD-000019 — Domain bootstrap strategy and early product-start gate

## Легенда статусов
- Черновик
- Готово_к_утверждению
- Утверждено
- В_работе
- Завершено
- Отменено

---

## ROAD-000032 — Verification contract reduction and language cleanup
ID: ROAD-000032
Этап: Verification contract reduction and language cleanup
Статус: Завершено
Связи: BACK-000097, PLAN-000085, ADR-000025, CHG-000097
Источник: Запрос владельца от 2026-04-30
Дата_создания: 2026-04-30
Дата_изменения: 2026-04-30
Цель: Сократить повторяющиеся technical documents проверочного контура и синхронизировать язык проверок после удаления преждевременных доменов.
Зависимости: ROAD-000031
Связанные_backlog: BACK-000097

### Описание
Этап закрыт узким pass `PLAN-000085`. Проверочный договор сокращён до одного владельца `Docs/Technical/Verification.md`; дублирующие документы уровней, доказательств и подтверждения результата удалены; `Pipeline/*`, `Rules/README.md`, `Tools/README.md`, `bp_lint.py` и `bp_bootstrap.py` синхронизированы. `Minesweeper`, новые домены, состав создаваемого продукта и широкая языковая чистка не выполнялись.

---

## ROAD-000031 — Semantic cleanup after retired domain removal
ID: ROAD-000031
Этап: Semantic cleanup after retired domain removal
Статус: Завершено
Связи: BACK-000096, PLAN-000084, ADR-000024, CHG-000096
Источник: Запрос владельца от 2026-04-30
Дата_создания: 2026-04-30
Дата_изменения: 2026-04-30
Цель: Навести семантический порядок после удаления преждевременных доменов: исправить остатки retired domains, упорядочить `Rules/*`, закрепить правило именования путей и файлов, устранить дубли планового контура и синхронизировать tools/checks.
Зависимости: ROAD-000029, ROAD-000030
Связанные_backlog: BACK-000096

### Описание
Этап закрыт одним широким системным pass `PLAN-000084`. Дублирование `PLAN-000082` исправлено через отдельный исторический контур `PLAN-000083`; `Rules/*` сгруппирован по предметным областям; semantic path/file naming закреплён в `Rules/Naming.md`; active references на retired domains заменены owner-доменами или оставлены только как forbidden/history context; `bp_lint.py` синхронизирован с новым ruleset. `Minesweeper`, новые домены и полная языковая чистка архивов не выполнялись.

---

## ROAD-000030 — Already-created product service update route ID correction
ID: ROAD-000030
Этап: Already-created product service update route ID correction
Статус: Завершено
Связи: BACK-000095, PLAN-000083, CHG-000095, QL-000090
Источник: Идентификационная коррекция архива от 2026-04-30
Дата_создания: 2026-04-28
Дата_изменения: 2026-04-30
Цель: Выделить архивный проход про маршрут обновления already-created product repo на local tools baseline из ошибочного дублирования `PLAN-000082`.
Зависимости: ROAD-000027, ROAD-000028
Связанные_backlog: BACK-000095

### Описание
Исторический смысл прохода сохранён: он описывает service update route для уже созданного product repo после перехода product skeleton на local `Tools/*`. Исправлена только идентификация: архивный план получает `PLAN-000083`, собственные `ROAD/BACK/CHG/QL` связи и перестаёт ссылаться на `ROAD-000029 / BACK-000094 / CHG-000094 / QL-000089`, которые принадлежат product pipeline cleanup.

---

## ROAD-000029 — Product pipeline control and retired domain cleanup
ID: ROAD-000029
Этап: Product pipeline control and retired domain cleanup
Статус: Завершено
Связи: BACK-000094, PLAN-000082, ADR-000023, CHG-000094
Источник: Запрос владельца от 2026-04-29
Дата_создания: 2026-04-29
Дата_изменения: 2026-04-29
Цель: Закрыть проблемы нового полевого теста `Minesweeper`, усилить создаваемый product Pipeline и завершить удаление retired domains `BytePress` после переноса полезного смысла.
Зависимости: ROAD-000028
Связанные_backlog: BACK-000094

### Описание
Этап закрыт одним широким корректирующим pass `PLAN-000082`. Рабочие процедуры перенесены в `Pipeline/Workflows.md`, обязательные нормы перенесены в `Rules/*`, retired domains удалены из active layer. `bp_bootstrap.py` создаёт усиленный `Pipeline/*`, `AGENTS.md` направляет агента в generated Pipeline, interview protocol запрещает подтверждать текущую истину догадками, а `bp_lint.py` больше не требует удалённые домены в самом `BytePress`.

---

## ROAD-000028 — Синхронизация терминов и проверок нового product skeleton
ID: ROAD-000028
Этап: Синхронизация терминов и проверок нового product skeleton
Статус: Завершено
Связи: BACK-000093, PLAN-000081, CHG-000093
Источник: Запрос владельца от 2026-04-28
Дата_создания: 2026-04-28
Дата_изменения: 2026-04-28
Цель: Исправить противоречия после перехода к local product `Tools/*`: термины, интервью, паспорт каркаса, template IDs и forbidden-domain error path.
Зависимости: ROAD-000027
Связанные_backlog: BACK-000093

### Описание
Этап закрыт одним корректирующим pass `PLAN-000081`. Термины `Каркас репозитория` и `Профиль продукта`, active interview, bootstrap/validation matrix и generated product skeleton синхронизированы с моделью `Docs`, `Plans`, `Logs`, `Pipeline`, `Tools`, `Templates`, `Schemas` и transition `scripts/*`. `bp_lint.py` теперь возвращает нормальную ошибку для forbidden product domains, а generated `Templates/*` получают уникальные `TPL-*` IDs.

---

## ROAD-000027 — Локальный Tools создаваемого продукта и переходный product lint
ID: ROAD-000027
Этап: Локальный Tools создаваемого продукта и переходный product lint
Статус: Завершено
Связи: BACK-000092, PLAN-000080, CHG-000092
Источник: Запрос владельца от 2026-04-28
Дата_создания: 2026-04-28
Дата_изменения: 2026-04-28
Цель: Начать инструментальную реализацию профильного самодостаточного product skeleton: local product `Tools/*`, lightweight `Pipeline/*`, bounded `Templates/*` и `Schemas/*`, без удаления legacy domains `BytePress`.
Зависимости: ROAD-000026
Связанные_backlog: BACK-000092

### Описание
Этап закрыт одним pass `PLAN-000080`. `bp_bootstrap.py` теперь materialize product-local `Tools/*` как основной service layer, lightweight `Pipeline/*`, bounded `Templates/*` и `Schemas/*`, не создаёт retired domains в новом продукте, а `scripts/*` оставляет transition wrappers. `bp_lint.py` проверяет новый product skeleton через local tools contract.

---

## ROAD-000026 — Профильная фабрика продуктовых каркасов и сокращение доменной модели
ID: ROAD-000026
Этап: Профильная фабрика продуктовых каркасов и сокращение доменной модели
Статус: Завершено
Связи: BACK-000091, PLAN-000079, ADR-000022, CHG-000091
Источник: Решение владельца от 2026-04-28
Дата_создания: 2026-04-28
Дата_изменения: 2026-04-28
Цель: Зафиксировать переход `BytePress` от разросшейся доменной модели к профильной фабрике самодостаточных продуктовых каркасов и подготовить безопасный план рефакторинга без массового удаления файлов.
Зависимости: ROAD-000025
Связанные_backlog: BACK-000091

### Описание
Этап закрыт одним архитектурным pass `PLAN-000079`. Добавлены `ADR-000022`, целевая профильная матрица пакетов продукта, migration plan сокращения доменной модели и правило удаления преждевременных доменов. Документы-владельцы синхронизированы вокруг решения: продукт зависит от профиля, получает lightweight `Pipeline/*`, local `Tools/*`, profile-bound `Templates/*` и `Schemas/*`, а retired domains выводятся в миграционный контур без удаления в этом pass.

---

## ROAD-000025 — Русские проверочные маркеры lint-договора
ID: ROAD-000025
Этап: Русские проверочные маркеры lint-договора
Статус: Завершено
Связи: BACK-000090, PLAN-000078, ADR-000021, CHG-000090
Источник: Запрос владельца от 2026-04-27
Дата_создания: 2026-04-27
Дата_изменения: 2026-04-27
Цель: Обновить `bp_lint.py`, чтобы активный и создаваемый слой могли использовать русские проверочные маркеры без обязательной англоязычной формы и без ослабления структурных проверок.
Зависимости: ROAD-000024
Связанные_backlog: BACK-000090

### Описание
Этап закрыт одним узким проходом `PLAN-000078`. `bp_lint.py` теперь принимает русские эквиваленты проверочных маркеров для стартового отчёта, аналитического гейта, текущей истины, документов-владельцев, доменов-владельцев и записываемых действий. Active/generated layer синхронизирован без изменения `Minesweeper`, без новых доменов создаваемого продукта и без широкой языковой чистки архивов.

---

## ROAD-000024 — Договор карт доменов и ADR-журнала
ID: ROAD-000024
Этап: Договор карт доменов и ADR-журнала
Статус: Завершено
Связи: BACK-000089, PLAN-000077, ADR-000018, ADR-000019, ADR-000020, CHG-000089
Источник: Запрос владельца от 2026-04-27
Дата_создания: 2026-04-27
Дата_изменения: 2026-04-27
Цель: Закрепить краткий README.md домена как карту домена и закрыть доказанный пропуск ADR для значимых архитектурных, процессных и продуктово-договорных решений последних product-start проходов.
Зависимости: ROAD-000023
Связанные_backlog: BACK-000089

### Описание
Этап закрыт одним узким проходом `PLAN-000077`. Добавлен шаблон карты домена, стандарт документации закрепил `README.md` домена как краткую карту, правило ADR уточнено для значимых архитектурных, процессных и продуктово-договорных решений, а `Logs/ADRlog.md` закрывает три ретро-решения по product-start contour, fresh/developed checks, картам доменов и service-layer update route. Проверки repo/product lifecycle пройдены без изменения `Minesweeper`, без новых доменов создаваемого продукта и без изменения `bp_lint.py`.

---

## ROAD-000023 — Языковая и картографическая чистка активного и создаваемого слоя
ID: ROAD-000023
Этап: Языковая и картографическая чистка активного и создаваемого слоя
Статус: Завершено
Связи: BACK-000088, PLAN-000076
Источник: Запрос владельца от 2026-04-27
Дата_создания: 2026-04-27
Дата_изменения: 2026-04-27
Цель: Привести активные артефакты `BytePress` и создаваемый продуктовый слой к чистому русскому языку, единой инженерной стилистике, установленной терминологии и единому формату карт доменов без изменения предметного смысла и bootstrap-гейтов.
Зависимости: ROAD-000022
Связанные_backlog: BACK-000088

### Описание
Этап закрыт одним широким проходом `PLAN-000076`. Активные карты доменов, README доменов, `AGENTS.md`, `Setup_Guide.md`, `Tools/README.md` и текстовый слой `Tools/bp_bootstrap.py` приведены к краткому русскому инженерному формату. `bp_lint.py` не изменялся: проверочный договор сохранён, а требуемые repo/product checks подтвердили fresh, auto и developed lifecycle created product repo.

---

## ROAD-000022 — Канонический путь обновления service-layer created product repo
ID: ROAD-000022
Этап: Канонический путь обновления service-layer created product repo
Статус: Завершено
Связи: BACK-000087, PLAN-000075
Источник: Corrective pass after developed product service-layer update need
Дата_создания: 2026-04-27
Дата_изменения: 2026-04-27
Цель: Зафиксировать минимальный путь обновления служебных файлов уже созданного product repo без пересоздания продукта, потери предметных артефактов, расширения bootstrap-доменов или ослабления fresh/developed product checks.
Зависимости: ROAD-000021
Связанные_backlog: BACK-000087

### Описание
Этап закрыт одним узким pass `PLAN-000075`. Bootstrap contract, validation contract, lifecycle, verification и tooling map теперь фиксируют canonical product-side route обновления `scripts/dev-test.sh` и `scripts/README.md` в уже созданном product repo: точечный service-layer delta, без fresh bootstrap reset, без переписывания предметных артефактов и с подтверждением через `scripts/dev-test.sh` / `bp_lint.py --mode auto`. Временный product repo подтвердил fresh state, generated service guidance и modeled developed state.

---

## ROAD-000021 — Разделить product lint для свежего bootstrap и развивающегося продукта
ID: ROAD-000021
Этап: Разделить product lint для свежего bootstrap и развивающегося продукта
Статус: Завершено
Связи: BACK-000086, PLAN-000074
Источник: Corrective pass after first evolving product repository check
Дата_создания: 2026-04-26
Дата_изменения: 2026-04-26
Цель: Развести automatic check свежего bootstrap-состояния и развивающегося product repo после подтверждения current truth, чтобы `bp_lint.py` выявлял реальные contradictions lifecycle, а не нормальный переход после первого прохода.
Зависимости: ROAD-000020
Связанные_backlog: BACK-000086

### Описание
Этап закрыт одним corrective pass `PLAN-000074`. `bp_lint.py` теперь различает fresh bootstrap product repo и developed product repo после подтверждения current truth; generated `scripts/dev-test.sh` запускает explicit `--mode auto`; technical contracts и tooling map синхронизированы с двумя structural gates. Проверки на временном generated product repo подтвердили fresh pass, developed pass и expected fail для contradiction scenario.

---

## ROAD-000020 — Семантическая чистка стартового контура после повторного полевого теста
ID: ROAD-000020
Этап: Семантическая чистка стартового контура после повторного полевого теста
Статус: Завершено
Связи: BACK-000085, PLAN-000073, CHG-000085
Источник: Corrective pass after repeated `Minesweeper` field test
Дата_создания: 2026-04-24
Дата_изменения: 2026-04-24
Цель: Снять остаточные смысловые противоречия стартового контура `BytePress` между терминологией, матрицей начального развёртывания, интервью, агентной картой, картой жизненного цикла, bootstrap и lint перед следующим полевым тестом.
Зависимости: ROAD-000019
Связанные_backlog: BACK-000085

### Описание
Этап закрыт одним corrective pass `PLAN-000073`. Термин `Каркас репозитория`, матрица начального развёртывания и фактический `bp_bootstrap.py` теперь одинаково разводят bootstrap-default, будущие product-side расширения и BytePress-only domains. Generated product repo получает минимальный стартовый пакет терминов, `AGENTS.md` снова стал короткой картой входа, интервью сосредоточено в одном owner-document с пятью смысловыми классами вопросов, а compact lifecycle/handoff map закреплена в `Pipeline/Inputs_Outputs.md`. Финальный repo lint, bootstrap smoke, generated repo lint на `develop` и task-ветке, а также product-side script checks не подтвердили residual contradiction в scope этапа.

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
Дата_изменения: 2026-04-08
Цель: Зафиксировать новую операционную модель `BytePress`, planning-contour и единую схему идентификаторов на уровне governance-contract, включая терминологию `этап / задача / проход`, ownership состояния, lifecycle `Plan`, завершённый active/archive planning-layer и hard-close contour без полной migration всех остальных historical доменов.
Зависимости: ROAD-000008
Связанные_backlog: BACK-000041, BACK-000042, BACK-000043, BACK-000044, BACK-000045, BACK-000046, BACK-000047, BACK-000048, BACK-000049, BACK-000050

### Описание
Этап завершён: `Roadmap` владеет стадиями, `Backlog` владеет задачами текущего этапа, `Plan` описывает только один текущий проход, единая `ID scheme` и порядок её migration зафиксированы отдельными governance-pass, active/archive layout planning-layer реализован, log-layer приведён к утверждённому serial-entry contract, active governance/supporting singleton-hybrid tail закрыт, а финальный audit-pass не подтвердил реального residual gap внутри `ROAD-000009`.

---

## ROAD-000010 — Технический слой и карта системных контрактов (Technical Layer and System Contract Map)
ID: ROAD-000010
Этап: Технический слой и карта системных контрактов (Technical Layer and System Contract Map)
Статус: Завершено
Связи: BACK-000051, BACK-000052, BACK-000053, BACK-000054, BACK-000055, BACK-000056, BACK-000057, BACK-000058, BACK-000059, BACK-000060, BACK-000061, PLAN-000039, PLAN-000040, PLAN-000041, PLAN-000042, PLAN-000043, PLAN-000044, PLAN-000045, PLAN-000046, PLAN-000047, PLAN-000048, PLAN-000049
Источник: PLAN-000039, PLAN-000040, PLAN-000041, PLAN-000042, PLAN-000043, PLAN-000044, PLAN-000045, PLAN-000046, PLAN-000047, PLAN-000048, PLAN-000049
Дата_создания: 2026-03-31
Дата_изменения: 2026-04-08
Цель: Определить границы `Docs/Technical/*`, минимальный состав technical-layer и карту системных контрактов без смешения technical knowledge-layer с `Pipeline/*` и planning/governance контуром.
Зависимости: ROAD-000009
Связанные_backlog: BACK-000051, BACK-000052, BACK-000053, BACK-000054, BACK-000055, BACK-000056, BACK-000057, BACK-000058, BACK-000059, BACK-000060, BACK-000061

### Описание
Этап завершён: boundary-pass зафиксировал назначение `Docs/Technical/*`, его минимальное ядро и границы относительно `Pipeline/*`, `Plans/*`, `Runtime/*` и `Logs/*`, после чего contract-map pass подтвердил required core и supporting technical-documents. Отдельные passes пересобрали `Architecture.md`, `Model.md`, `Artifact_Lifecycle.md`, `Interfaces.md`, `System_Invariants.md`, `Platform_Contracts.md`, `Product_Bootstrap_Contract.md` и `Product_Bootstrap_Validation.md` как согласованную карту системных контрактов; финальный audit-pass не подтвердил реального residual gap в active technical layer, bootstrap/lint perimeter или planning sync, поэтому `ROAD-000010` закрыт без candidate tail и без автоматической активации `ROAD-000011`.

---

## ROAD-000011 — Контур проверок и верификации (Verification and Validation Contour)
ID: ROAD-000011
Этап: Контур проверок и верификации (Verification and Validation Contour)
Статус: Завершено
Связи: BACK-000062, BACK-000063, BACK-000064, BACK-000065, BACK-000066, BACK-000067, BACK-000068, BACK-000069, BACK-000070, BACK-000071, BACK-000072, PLAN-000050, PLAN-000051, PLAN-000052, PLAN-000053, PLAN-000054, PLAN-000055, PLAN-000056, PLAN-000057, PLAN-000058, PLAN-000059, PLAN-000060
Источник: PLAN-000050, PLAN-000051, PLAN-000052, PLAN-000053, PLAN-000054, PLAN-000055, PLAN-000056, PLAN-000057, PLAN-000058, PLAN-000059, PLAN-000060
Дата_создания: 2026-03-31
Дата_изменения: 2026-04-11
Цель: Собрать контур проверок и верификации поверх обновлённой operating model и технической карты системы без смешения verification-work с самой нормализацией техслоя.
Зависимости: ROAD-000010
Связанные_backlog: BACK-000062, BACK-000063, BACK-000064, BACK-000065, BACK-000066, BACK-000067, BACK-000068, BACK-000069, BACK-000070, BACK-000071, BACK-000072

### Описание
Этап завершён: boundary-pass для verification contour зафиксировал место verification-layer в системе и границы между automatic checks, procedural checks, process gates и tool implementation, после чего contract-map pass собрал verification-layer с checks, inputs, outputs, evidence и ownership результата. Следующие завершённые passes ввели `Verification_Levels.md`, tooling boundary verification-контура и `Verification_Evidence.md`, чтобы развести automatic verification, future `bp_check / bp_verify`, evidence package и pass-close contour без реализации нового toolchain. Затем отдельные passes ввели `Validation.md`, `Validation_Levels.md`, `Validation_Evidence.md` и tooling boundary validation-контура в `Tools/README.md`, чтобы развести validation и verification, outcome confirmation, evidence sufficiency, procedural validation, tooling support и границу между validation result и gate decision без открытия `ROAD-000012`. Финальный audit-pass не подтвердил реального residual gap в active verification/validation contour, planning sync, gate boundary или lint perimeter, поэтому `ROAD-000011` закрыт без candidate tail и без автоматической активации `ROAD-000012`.

---

## ROAD-000012 — Точка входа агента и пользовательский слой (Agent Entry Point and User Layer)
ID: ROAD-000012
Этап: Точка входа агента и пользовательский слой (Agent Entry Point and User Layer)
Статус: Завершено
Связи: BACK-000073, BACK-000074, BACK-000075
Источник: PLAN-000061, PLAN-000062, PLAN-000063
Дата_создания: 2026-03-31
Дата_изменения: 2026-04-11
Цель: Проявить устойчивую точку входа агента и согласованный пользовательский слой после того, как planning и verification-контуры перестанут противоречить друг другу.
Зависимости: ROAD-000011
Связанные_backlog: BACK-000073, BACK-000074, BACK-000075

### Описание
Этап завершён: первый pass зафиксировал `AGENTS.md` как каноническую agent entry point и routing-document для Codex внутри `BytePress`, source-of-truth hierarchy, operating loop и границы между `AGENTS.md`, `Docs/User/*`, `Docs/Technical/*`, `Plans/*`, `Logs/*` и `Tools/*`. Следующий pass проявил минимальный human-facing `Docs/User/*` с human operating mode, порядком первого старта и базовыми сценариями использования без широкого user-layer. Финальный closure-pass добавил последний обязательный user-facing contract для формулирования pass человеком, исправил доказанный direct contradiction вокруг запуска `bp_lint.py` из корня репозитория и не подтвердил residual gap в active agent-entry/user-layer contour, поэтому `ROAD-000012` закрыт и не активирует `ROAD-000013` автоматически.

---

## ROAD-000013 — Тиражирование product repo и baseline `0.2.0` (Product Repository Replication and Baseline `0.2.0`)
ID: ROAD-000013
Этап: Тиражирование product repo и baseline `0.2.0` (Product Repository Replication and Baseline `0.2.0`)
Статус: Завершено
Связи: BACK-000076
Источник: PLAN-000064
Дата_создания: 2026-03-31
Дата_изменения: 2026-04-13
Цель: Подготовить повторяемое тиражирование product repo и следующий baseline `0.2.0` как отдельный управляемый этап после проявления точки входа агента и пользовательского слоя.
Зависимости: ROAD-000012
Связанные_backlog: BACK-000076

### Описание
Этап завершён одним stage-closing pass: bootstrap/replication contract доведён от minimal skeleton до first-usable replicated product repo, materialized outcome синхронизирован с current agent/user entry contracts, active non-log baseline `BytePress` переведён на `0.2.0` только в реально operational contracts, а `.codex` workflow noise закрыт как доказанный `.gitignore` gap. Финальный audit не подтвердил residual gap в bootstrap/replication contour, поэтому `ROAD-000013` закрыт и не активирует `ROAD-000014` автоматически.

---

## ROAD-000014 — Интеграционный контур и будущие расширения (Integration Layer and Future Extensions)
ID: ROAD-000014
Этап: Интеграционный контур и будущие расширения (Integration Layer and Future Extensions)
Статус: Завершено
Связи: BACK-000077, BACK-000078, PLAN-000065, PLAN-000066
Источник: PLAN-000065, PLAN-000066
Дата_создания: 2026-03-31
Дата_изменения: 2026-04-13
Цель: Собрать управляемый integration contour `BytePress` после replication-stage и baseline `0.2.0`, не открывая реальные внешние интеграции и не смешивая integration-layer с source-of-truth моделью репозитория.
Зависимости: ROAD-000013
Связанные_backlog: BACK-000077, BACK-000078

### Описание
Activation pass перевёл stage из черновика в рабочее состояние и зафиксировал controlled connector handoff между `Adapters/*`, `MCP/*`, `Tools/*`, bootstrap-generated product repo и `scripts/*`. Stage-closing pass усилил существующий `integration-smoke` route до deterministic repo-native evidence handoff: generated product repo теперь materialize report artifact `Runtime/Integration_Smoke_Report.json`, а verdict этого artifact согласован со smoke result без открытия реальных внешних подключений, network runtime, secrets или vendor-specific execution. Финальный audit не подтвердил residual gap в active integration contour, bootstrap/validation sync или evidence handoff boundary, поэтому `ROAD-000014` закрыт и backlog этапа выведен в archive-layer без автоматической активации нового `ROAD-*`.

---

## ROAD-000015 — Release readiness и factual log closure (Release Readiness and Factual Log Closure)
ID: ROAD-000015
Этап: Release readiness и factual log closure (Release Readiness and Factual Log Closure)
Статус: Завершено
Связи: BACK-000079, PLAN-000067, CHG-000079
Источник: PLAN-000067
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15
Цель: Закрыть release-readiness и journaling gaps после завершения `ROAD-000014`, довести канонический workflow выпуска `0.2.0` до `main` и восстановить factual history-fact closure в журналах без открытия нового roadmap-stage.
Зависимости: ROAD-000014
Связанные_backlog: BACK-000079

### Описание
Этап закрыт одним corrective pass: `Setup_Guide.md`, release workflow contract, `Artifact_Lifecycle.md`, evidence contracts и `Logs/*` теперь согласованно фиксируют полный release workflow `release/* -> main -> tag -> cleanup -> develop sync -> factual release logging` без подмены release event gate-approval или прогнозом. Одновременно `ChangeLog.md` и `QualityLog.md` дозаполнены для ранее завершённых pass, а `ReleaseLog.md` получил factual запись о release event `0.1.0`, подтверждённом tag/history. Финальный audit не подтвердил residual release-blocker для подготовки `0.2.0`, поэтому `ROAD-000015` закрыт и не активирует новый `ROAD-*` автоматически.

---

## ROAD-000016 — Post-release sync после `0.2.0` (Post-release Sync After `0.2.0`)
ID: ROAD-000016
Этап: Post-release sync после `0.2.0` (Post-release Sync After `0.2.0`)
Статус: Завершено
Связи: BACK-000080, PLAN-000068, CHG-000080
Источник: PLAN-000068
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15
Цель: Завершить post-release closure после merge/tag `0.2.0`: зафиксировать factual release event в `ReleaseLog.md`, подтвердить отсутствие release-only back-sync fixes и закрыть минимальный planning/log contour в `develop`.
Зависимости: ROAD-000015
Связанные_backlog: BACK-000080

### Описание
Этап закрыт одним узким operational sync-pass после подтверждённого merge `PR #77` и annotated tag `0.2.0` на commit `68824d0646fc3e68992bbd1d6a3e6b7f5dcf3b83` в `main`. Remote release-ветка уже отсутствовала, local release-ветка удалена, factual запись о выпуске `0.2.0` добавлена в `ReleaseLog.md`, а сравнение `origin/main` и `origin/develop` не подтвердило release-only tree fixes для back-sync. Минимальный planning/log closure завершён без открытия нового product-development scope.

## ROAD-000017 — Discovery minimum bootstrap и startup-handshake агента (Bootstrap Discovery Minimum and Agent Startup Handshake)
ID: ROAD-000017
Этап: Discovery minimum bootstrap и startup-handshake агента (Bootstrap Discovery Minimum and Agent Startup Handshake)
Статус: Завершено
Связи: BACK-000081, PLAN-000069, CHG-000081
Источник: PLAN-000069
Дата_создания: 2026-04-19
Дата_изменения: 2026-04-19
Цель: Закрыть ранние control gaps после первого полевого запуска generated product repo: materialize minimal discovery-layer, сделать startup mode агента наблюдаемым и закрепить канонический interview format без открытия нового широкого stage.
Зависимости: ROAD-000016
Связанные_backlog: BACK-000081

### Описание
Этап закрыт одним corrective pass: generated product repo теперь materialize `Docs/Discovery/README.md` и `Docs/Discovery/Interview.md`, product `AGENTS.md` явно включает discovery-layer в source-of-truth hierarchy и routing, а `AGENTS.md` самого `BytePress` фиксирует observable startup-handshake первого ответа. Одновременно `Skills/Interview.md`, `Templates/Interview.md`, active discovery-layer, bootstrap/validation contracts и `bp_lint.py` синхронизированы вокруг канонического interview format и нового bootstrap minimum. Smoke bootstrap и lint generated repo подтвердили отсутствие residual contradiction в этом scope.

---

## ROAD-000018 — Product-start control gaps after first field test (Product-Start Control Gaps After First Field Test)
ID: ROAD-000018
Этап: Product-start control gaps after first field test (Product-Start Control Gaps After First Field Test)
Статус: Завершено
Связи: BACK-000082, PLAN-000070, CHG-000082
Источник: PLAN-000070
Дата_создания: 2026-04-20
Дата_изменения: 2026-04-20
Цель: Полностью закрыть end-to-end gaps раннего product-start contour после теста `Minesweeper`: довести startup-handshake, interview current-truth, discovery minimum и runtime artifact hygiene до согласованного поведения между core contracts, bootstrap, generated product repo и lint без открытия release contour.
Зависимости: ROAD-000017
Связанные_backlog: BACK-000082

### Описание
Этап закрыт одним corrective pass после фактического smoke bootstrap во временный target path вне дерева `BytePress`. Core `AGENTS.md`, bootstrap/validation contracts, active discovery-layer, `Skills/Interview.md`, `Templates/Interview.md`, `Tools/bp_bootstrap.py` и `Tools/bp_lint.py` теперь одинаково требуют observable startup-handshake первого ответа, исполнимый first interview из 8–10 ключевых вопросов и явный current-truth ownership `Docs/Discovery/Interview.md`. Одновременно принят канон runtime artifact hygiene: `Runtime/Integration_Smoke_Report.json` не входит в bootstrap baseline commit, materialize только после фактического smoke run и остаётся runtime-local artifact по умолчанию. Smoke bootstrap, generated repo lint и smoke report hygiene не подтвердили residual contradiction в этом scope.

---

## ROAD-000019 — Domain bootstrap strategy and early product-start gate
ID: ROAD-000019
Этап: Domain bootstrap strategy and early product-start gate
Статус: Завершено
Связи: BACK-000083, BACK-000084, PLAN-000071, PLAN-000072, CHG-000083, CHG-000084
Источник: PLAN-000071, PLAN-000072
Дата_создания: 2026-04-21
Дата_изменения: 2026-04-22
Цель: Закрыть системные разрывы раннего product-start contour после полевых тестов `Minesweeper`: сначала классифицировать top-level домены `BytePress` для product bootstrap и ввести canonical reset/cleanup route, затем довести live execution discipline branch gate и structured interview format до согласованного поведения bootstrap, generated repo и lint.
Зависимости: ROAD-000018
Связанные_backlog: BACK-000083, BACK-000084

### Описание
Этап закрыт двумя узкими corrective passes после повторных полевых тестов `Minesweeper`. Первый pass `PLAN-000071` зафиксировал каноническую replication matrix top-level доменов, удержал generated repo в discovery-only contour до ответов пользователя и оформил canonical reset/cleanup route `scripts/reset-product-start.sh`. Второй pass `PLAN-000072` довёл live execution discipline до наблюдаемого branch gate и жёсткого structured interview contract: generated repo теперь требует task-ветку до любого writable action, startup-handshake сообщает branch status и branch action, а full interview и допустимый delta-интервью одинаково удерживают numbered / lettered / recommended format. Финальный repo lint, smoke bootstrap, generated repo lint на `develop` и task-ветке, а также negative smoke свободноформатного delta-интервью не подтвердили residual contradiction между core contracts, bootstrap, generated repo и lint.
