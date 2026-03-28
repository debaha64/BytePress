# ChangeLog

## Индекс
- CHG-000031 — Branch and PR process contract finalized and residual process noise removed
- CHG-000030 — Repo-wide active layer audit aligned maps, roles, skills and technical references
- CHG-000029 — Discovery layer, interview current truth and sync contract surfaced
- CHG-000028 — Delivery template, bootstrap, and lint contracts synchronized with product layer canon
- CHG-000027 — Product layer aligned with canonical templates and minimal document scope
- CHG-000026 — Release branch example aligned with canonical branch naming
- CHG-000025 — Release governance and README product value formalized before main preparation
- CHG-000024 — Planning truth aligned with logs truth for release preparation
- CHG-000023 — Orphan IDs removed from active plans and approval rule without new namespaces
- CHG-000022 — Semver operationalized for active BytePress documents at baseline 0.1.0
- CHG-000021 — Historical logs migrated to six-digit IDs and active references synced
- CHG-000020 — Active non-log ID layer переведён на 6-значный формат без переписывания historical logs
- CHG-000019 — Tool contract sync завершил приведение bootstrap и lint к текущим contracts
- CHG-000018 — Terms layer мигрирован на канонические filenames и 6-значные TERM ID
- CHG-000017 — Синхронизированы схемы, шаблоны, профили и language contract Git/PR
- CHG-000016 — Зафиксирована repo-wide policy фазной ID migration без запуска rewrite-pass
- CHG-000015 — Remaining plan layer приведён к каноническим именам и 6-значным plan ID
- CHG-000014 — Нормализован foundation-план BytePress и удалён legacy-дубль
- CHG-000013 — Зафиксирован контракт 6-значных ID, naming plan-file и модель профилей
- CHG-000012 — Зафиксированы branch lifecycle, целевой Auto-PR процесс и следующий плановый проход
- CHG-000011 — Добавлены корневые карты README.md и AGENTS.md и обновлены минимальные контракты агентной работы
- CHG-000010 — Подтверждён рабочий цикл agent push -> agent PR -> human approve -> human merge в GitHub
- CHG-000009 — Усилен bootstrap продукта и подтверждён тестовой генерацией
- CHG-000008 — Оформлен интеграционный каркас Adapters, Memory и MCP
- CHG-000007 — Замкнут исполнительный контур ролей, навыков и инструментов BytePress
- CHG-000006 — Усилен технический слой и контур правил BytePress
- CHG-000005 — Введён рабочий журнальный контур решений и изменений
- CHG-000004 — Заполнены короткие стандарты BytePress полезными практиками
- CHG-000003 — Заполнена базовая терминология BytePress и политика её изменений
- CHG-000002 — Уточнены схемы и шаблоны ключевых сущностей
- CHG-000001 — Создан первичный каркас BytePress v1

---

## CHG-000031 — Branch and PR process contract finalized and residual process noise removed
ID: CHG-000031
Дата: 2026-03-28
Тип_изменения: Документация
Источник: Branch/PR process cleanup pass after repo-wide active layer audit
Связи: PLAN-000019, BACK-000027, QL-000026
Дата_создания: 2026-03-28
Дата_изменения: 2026-03-28

### Описание
Завершён process-contract для task-branch, local commits, self-check, final push, проверки существующего PR и создания PR в `develop`. `AGENTS.md`, `Setup_Guide.md` и `Docs/Technical/Platform_Contracts.md` синхронизированы по правилу не использовать `--dry-run`, если текущий `gh` его не поддерживает, и по fallback без автоматической переавторизации `gh` при ошибке команды PR. `Plans/README.md` очищен от устаревшей привязки к раннему диапазону plan-files, а в `Roles/Developer.md`, `Roles/QA.md` и `Roles/Release.md` заменены остаточные ссылки `Plans/PLAN-*.md` на `Plans/BP-*.md`. `bp_lint.py` и `ADRlog` не менялись, так как обязательный contract и архитектурные решения в этом проходе не изменились.

### Эффект
Process-facing слой BytePress теперь описывает один и тот же практический branch/PR workflow без двусмысленностей по моменту `push`, созданию PR, `gh` fallback и повторному использованию head-ветки после merge.

---

## CHG-000030 — Repo-wide active layer audit aligned maps, roles, skills and technical references
ID: CHG-000030
Дата: 2026-03-28
Тип_изменения: Документация
Источник: Repo-wide audit pass after product, discovery and sync-contract canon alignment
Связи: PLAN-000018, BACK-000019, QL-000025
Дата_создания: 2026-03-28
Дата_изменения: 2026-03-28

### Описание
Проведён repo-wide аудит активного слоя `BytePress` после отдельных проходов по product-layer, discovery-layer и pipeline sync-contract. В `README.md`, `AGENTS.md` и `Tools/README.md` устранены устаревшие формулировки и закреплена текущая модель discovery-layer, крупноэтапного `Roadmap` и lint-checks. В `Docs/Technical/Product_Bootstrap_Validation.md` выровнена фактическая формулировка validation-контракта, в `Roles/Business_Analyst.md`, `Roles/System_Analyst.md`, `Roles/Architect.md`, `Skills/Interview.md` и `Skills/Planning.md` исправлены реальные рассогласования по `Docs/Discovery/`, current-truth интервью и каноническому виду `Plans/BP-*.md`. В `Plans/BP-000017-discovery-and-sync-contract.md` удалён дублирующийся артефакт `Logs/ADRlog.md`; `bp_lint.py` не менялся, потому что обязательный contract в этом audit-pass не изменился.

### Эффект
Активный слой BytePress снова согласован repo-wide: карты, validation-контракт, роли, навыки и активные планы используют один и тот же текущий канон product/discovery/pipeline без большого рефакторинга и без переписывания historical layer.

---

## CHG-000029 — Discovery layer, interview current truth and sync contract surfaced
ID: CHG-000029
Дата: 2026-03-28
Тип_изменения: Контракт
Источник: Discovery/sync-contract pass after delivery/bootstrap/lint alignment
Связи: PLAN-000017, BACK-000029, ADR-000017, QL-000024
Дата_создания: 2026-03-28
Дата_изменения: 2026-03-28

### Описание
Добавлен новый аналитический слой `Docs/Discovery/` с `README.md` и каноническим `Interview.md`, а также создан `Templates/Interview.md` как минимальный шаблон current-truth интервью. `Plans/Roadmap.md` приведён к уровню крупных этапов системы, `Docs/Technical/Pipeline.md` дополнен минимальной sync-matrix обязательной проверки связанных артефактов, `Docs/README.md`, `Plans/README.md`, `Docs/Technical/Architecture.md`, `Docs/Technical/Model.md`, `Docs/Technical/README.md` и `Templates/README.md` синхронизированы с новой моделью. `bp_lint.py` расширен так, чтобы валидировать `Docs/Discovery/README.md`, `Docs/Discovery/Interview.md` и `Templates/Interview.md`. В `ADR-000017` зафиксированы discovery-domain, current-truth модель интервью и sync-contract pipeline.

### Эффект
Аналитический слой BytePress стал явной частью `Docs/`, интервью закреплено как текущая истина, roadmap перестал дублировать backlog мелкими проходами, а pipeline contract получил обязательные правила синхронизации после изменения ключевых артефактов.

---

## CHG-000028 — Delivery template, bootstrap, and lint contracts synchronized with product layer canon
ID: CHG-000028
Дата: 2026-03-28
Тип_изменения: Контракт
Источник: Delivery/bootstrap/lint sync pass after product-layer normalization
Связи: PLAN-000016, BACK-000028, QL-000023
Дата_создания: 2026-03-28
Дата_изменения: 2026-03-28

### Описание
Добавлен `Templates/Delivery.md`, а `Templates/README.md` и `Docs/Product/Delivery.md` приведены к новому минимальному шаблону поставки. `Docs/Technical/Product_Bootstrap_Contract.md` и `Docs/Technical/Product_Bootstrap_Validation.md` синхронизированы с каноническим продуктовым набором `Docs/Product/README.md`, `Docs/Product/JTBD.md`, `Docs/Product/PRD.md`, `Docs/Product/Delivery.md`. `bp_bootstrap.py` теперь материализует весь этот набор в product repo, а `bp_lint.py` требует `Templates/Delivery.md` в `BytePress` и проверяет наличие полного минимального `Docs/Product/*` слоя в bootstrap-продукте. Краткая синхронизация добавлена в `Tools/README.md`.

### Эффект
Шаблоны, bootstrap-documentation, генерация продукта и lint используют один и тот же минимальный contract продуктового слоя; bootstrap smoke-check подтверждает, что этот contract действительно материализуется и валидируется.

---

## CHG-000027 — Product layer aligned with canonical templates and minimal document scope
ID: CHG-000027
Дата: 2026-03-27
Тип_изменения: Документация
Источник: Product-layer normalization pass after accepted JTBD and PRD templates
Связи: PLAN-000015, BACK-000026, QL-000022
Дата_создания: 2026-03-27
Дата_изменения: 2026-03-27

### Описание
`Docs/Product/PRD.md` и `Docs/Product/JTBD.md` приведены к каноническим шаблонам с сохранением продуктового смысла и без смешения с внутренними техническими слоями. `Docs/Product/README.md` и `Docs/Product/Delivery.md` сокращены до минимального продуктового канона, а `Docs/Product/Implementation_Plan.md` и `Docs/Product/Profiles.md` удалены как дубли или документы вне продуктовой границы. Технические документы bootstrap перенесены в `Docs/Technical/Product_Bootstrap_Contract.md` и `Docs/Technical/Product_Bootstrap_Validation.md`, после чего прямые ссылки в активных `Plans/*` и текущих журналах синхронизированы.

### Эффект
Продуктовый слой BytePress больше не смешивает продуктовые требования с внутренними системными описаниями и содержит только канонический минимальный набор документов, а технический bootstrap knowledge живёт в профильном слое `Docs/Technical/`.

---

## CHG-000026 — Release branch example aligned with canonical branch naming
ID: CHG-000026
Дата: 2026-03-19
Тип_изменения: Документация
Источник: Release-readiness cleanup before recreating the 0.1.0 release branch
Связи: CHG-000025, QL-000021
Дата_создания: 2026-03-19
Дата_изменения: 2026-03-19

### Описание
В `Setup_Guide.md` пример release-ветки приведён к каноническому формату `<type>/<NNNNNN>-<slug>` и заменён с `release/0.1.0` на `release/000019-0.1.0-rc2` в командах создания, открытия PR и удаления ветки.

### Эффект
Практический release workflow больше не противоречит принятому branch naming contract перед пересозданием release branch `0.1.0`.

---

## CHG-000025 — Release governance and README product value formalized before main preparation
ID: CHG-000025
Дата: 2026-03-18
Тип_изменения: Документация
Источник: Release branch workflow formalization before main preparation
Связи: STD-000004, CHG-000024, QL-000020
Дата_создания: 2026-03-18
Дата_изменения: 2026-03-18

### Описание
В `README.md` кратко усилено описание ценности `BytePress` как системы, которая формирует устойчивый контекст вокруг продукта, удерживает агента в управляемом контуре и снижает недетерминированность в SDLC. В `AGENTS.md`, `Setup_Guide.md`, `Docs/Technical/Platform_Contracts.md` и `Standards/Release.md` зафиксирован release-branch workflow для `release/*` как временной стабилизационной ветки от `develop` с PR только в `main`, без feature-work и с возвратом release-only fixes в `develop` при необходимости.

### Эффект
Release governance и краткое product value message формализованы до подготовки первого выхода `BytePress` в `main`.

---

## CHG-000024 — Planning truth aligned with logs truth for release preparation
ID: CHG-000024
Дата: 2026-03-18
Тип_изменения: Контракт
Источник: Release-readiness alignment pass for planning truth
Связи: PLAN-000006, BACK-000017, BACK-000018
Дата_создания: 2026-03-18
Дата_изменения: 2026-03-18

### Описание
В `Plans/Backlog.md` статусы `BACK-000017` и `BACK-000018` выровнены до `Завершено`, чтобы planning truth соответствовал уже зафиксированным `PLAN-000006`, `CHG-000012` и `QL-000007` перед подготовкой release branch `0.1.0`.

### Эффект
Planning truth и logs truth больше не расходятся по закрытию branch lifecycle и Auto-PR preparation pass.

---

## CHG-000023 — Orphan IDs removed from active plans and approval rule without new namespaces
ID: CHG-000023
Дата: 2026-03-18
Тип_изменения: Контракт
Источник: Orphan ID cleanup after semver operationalization
Связи: PLAN-000014, BACK-000019
Дата_создания: 2026-03-18
Дата_изменения: 2026-03-18

### Описание
Из `Plans/BP-000001-foundation.md` и `Plans/BP-000002-seed-docs-and-standards.md` удалён orphan ID `BP-REQ-0001` без введения нового requirement namespace и без замены его новой сущностью требований. Из `Rules/Approval_Strictness.md` удалён orphan ID `PIPE-0001`; смысл зависимости от конвейерных фаз сохраняется в текстовом описании и проверке правила без нового pipeline namespace.

### Эффект
Активный non-log слой BytePress больше не содержит оставшихся orphan ID `BP-REQ-0001` и `PIPE-0001`; ссылки и смысл документов сохранены без расширения модели и без добавления новых registry-доменов.

---

## CHG-000022 — Semver operationalized for active BytePress documents at baseline 0.1.0
ID: CHG-000022
Дата: 2026-03-18
Тип_изменения: Контракт
Источник: Semver operationalization pass after historical log migration
Связи: PLAN-000013, BACK-000019
Дата_создания: 2026-03-18
Дата_изменения: 2026-03-18

### Описание
В `Standards/Naming.md` и `Docs/Technical/Platform_Contracts.md` зафиксирован current operational baseline `BytePress` как `0.1.0`, а активные non-log документы переведены с использования `v1` на semver-метку `0.1.0` там, где `v1` обозначал текущий baseline-состояние системы. Historical logs намеренно не переписывались.

### Эффект
Текущий operational contract `BytePress` теперь маркируется через semver, а не через размытое обозначение `v1`, что снимает двусмысленность между baseline системы и историческими фазами её развития.

---

## CHG-000021 — Historical logs migrated to six-digit IDs and active references synced
ID: CHG-000021
Дата: 2026-03-18
Тип_изменения: Контракт
Источник: Late-phase historical logs migration after active non-log ID normalization
Связи: PLAN-000012, BACK-000024, ADR-000015
Дата_создания: 2026-03-18
Дата_изменения: 2026-03-18

### Описание
`Logs/ADRlog.md`, `Logs/ChangeLog.md` и `Logs/QualityLog.md` приведены к 6-значному формату исторических `ADR`, `CHG` и `QL ID` без изменения смысла записей, порядка, дат и текста истории. Прямые ссылки на historical log IDs в `Plans/*`, `Docs/Technical/*`, `Docs/Product/*`, `Rules/*`, `Standards/*`, `Adapters/*`, `Tools/README.md` и `Plans/Backlog.md` синхронизированы с новым форматом. Однозначные ссылки на старые `BACK` и `ROAD` в самих historical logs также приведены к уже действующему 6-значному формату, а `BP-REQ-0001` и `PIPE-0001` оставлены без изменений.

### Эффект
Журнальный исторический слой больше не смешивает 4- и 6-значный формат идентификаторов, а активные non-log документы ссылаются на historical logs по одному каноническому виду ID.

---

## CHG-000020 — Active non-log ID layer переведён на 6-значный формат без переписывания historical logs
ID: CHG-000020
Дата: 2026-03-18
Тип_изменения: Контракт
Источник: Следующая фаза repo-wide migration после term и tool sync-проходов
Связи: PLAN-000011, BACK-000019, ADR-000015, ADR-000016
Дата_создания: 2026-03-18
Дата_изменения: 2026-03-18

### Описание
Активные non-log internal ID в `Plans/Backlog.md`, `Plans/Roadmap.md`, `Profiles/*`, `Rules/*`, `Standards/*`, `Roles/*`, `Skills/*`, `Adapters/*`, `Memory/Registry.md`, `MCP/Registry.md`, `Docs/Technical/*` и `Docs/Technical/Product_Bootstrap_Contract.md` приведены к 6-значному формату для `BACK`, `ROAD`, `PROF`, `RULE`, `STD`, `ROLE`, `SKILL`, `ADP`, `MEM` и `MCP`. Прямые ссылки на старые 4-значные active ID синхронизированы, создан `Plans/BP-000011-migrate-active-nonlog-ids.md`, а historical logs намеренно не переписывались.

### Эффект
Активный non-log слой BytePress перестал смешивать 4- и 6-значный формат внутренних ID; текущие рабочие связи по singleton- и registry-доменам согласованы с repo-wide naming migration policy без запуска historical log rewrite-pass.

---

## CHG-000019 — Tool contract sync завершил приведение bootstrap и lint к текущим contracts
ID: CHG-000019
Дата: 2026-03-18
Тип_изменения: Инструмент
Источник: Исполнение tool contract sync после naming/profile/language migration passes
Связи: PLAN-000010, BACK-000022, ADR-000015, ADR-000016
Дата_создания: 2026-03-18
Дата_изменения: 2026-03-18

### Описание
`bp_bootstrap.py` переведён на обязательные параметры `--name`, `--product-code`, `--brand-profile`, `--target`; bootstrap теперь валидирует brand profile в `BytePress`, использует текущую дату выполнения, создаёт `Profiles/Product.md`, initial plan file `Plans/<PRODUCT_CODE>-000001-product-initialization.md` и 6-значные ID. `bp_lint.py` минимально обновлён под новый product bootstrap output contract, а `Tools/README.md`, `Docs/Technical/Product_Bootstrap_Contract.md`, `Docs/Technical/Product_Bootstrap_Validation.md` и `Profiles/README.md` синхронизированы с фактическим поведением инструментов; позднее contract дополнительно расширен каноническим `Delivery` template и полным минимальным `Docs/Product/*` набором.

### Эффект
Инструментальный контур больше не расходится с принятыми naming/profile/language contracts: bootstrap и lint работают по одному минимальному product bootstrap contract без большого рефакторинга tools.

---

## CHG-000018 — Terms layer мигрирован на канонические filenames и 6-значные TERM ID
ID: CHG-000018
Дата: 2026-03-17
Тип_изменения: Документация
Источник: Исполнение term migration phase из repo-wide naming policy
Связи: PLAN-000009, BACK-000023, ADR-000015
Дата_создания: 2026-03-17
Дата_изменения: 2026-03-17

### Описание
`Docs/Terms/*` приведены к каноническим filenames `TERM-<NNNNNN>-<slug>.md`, внутренние `TERM ID` выровнены до `TERM-000001`...`TERM-000016`, `Base_Terms.md` и прямые term-ссылки в `Docs/Technical/Model.md`, `Plans/BP-000003-fill-technical-and-rules.md`, `Plans/BP-000004-fill-skills-and-tools.md`, `Standards/*`, `Rules/Terms_Governance.md` и `Logs/ADRlog.md` синхронизированы. `bp_normalize_terms.py` минимально обновлён под новый filename pattern, а `Docs/Terms/README.md` и `Plans/Backlog.md` приведены к фактическому состоянию migration-pass.

### Эффект
Term layer перестал смешивать legacy filenames и 4-значные `TERM ID`; индекс словаря и прямые ссылки по репозиторию теперь согласованы с принятым naming contract без запуска migration для `Schemas/*`, `Templates/*`, `Profiles/*`, semver и historical logs.

---

## CHG-000017 — Синхронизированы схемы, шаблоны, профили и language contract Git/PR
ID: CHG-000017
Дата: 2026-03-17
Тип_изменения: Контракт
Источник: Первый migration-pass после фиксации repo-wide policy
Связи: ADR-000016, PLAN-000008, BACK-000021, BACK-000022, BACK-000025
Дата_создания: 2026-03-17
Дата_изменения: 2026-03-17

### Описание
`Schemas/*` и `Templates/*` переведены на 6-значную числовую часть `ID`, `Schemas/README.md` и `Templates/README.md` синхронизированы с новым контрактом, а `profile.schema.json` и `Templates/Profile.md` расширены полями `Тип_профиля`, `Код_продукта` и `Язык_взаимодействия`. `Profiles/README.md`, `Profiles/Default.md` и `Profiles/Speculorg.md` приведены к актуальной модели brand profiles с semantic filename и 6-значными внутренними `PROF ID`. В `AGENTS.md`, `Docs/Technical/Platform_Contracts.md` и `Standards/Documentation.md` зафиксировано правило английского языка для commit/PR artifacts и `branch slug`. Создан `Plans/BP-000008-schemas-templates-profiles-and-language-sync.md`.

### Эффект
Первый repo-wide migration-pass замкнул контракт между схемами, шаблонами, профилями и Git/PR-языком без запуска миграции `Terms/*`, `Tools/*`, semver и historical logs.

---

## CHG-000016 — Зафиксирована repo-wide policy фазной ID migration без запуска rewrite-pass
ID: CHG-000016
Дата: 2026-03-17
Тип_изменения: Контракт
Источник: Policy-проход после нормализации current plan layer
Связи: ADR-000015, PLAN-000007, BACK-000021, BACK-000022, BACK-000023, BACK-000024
Дата_создания: 2026-03-17
Дата_изменения: 2026-03-17

### Описание
Уточнены `Standards/Naming.md`, `Docs/Technical/Model.md`, `Docs/Terms/README.md`, `Profiles/README.md` и `Plans/Backlog.md`: зафиксирована repo-wide policy фазной миграции ID и правил filename по доменам, различены serial-, hybrid- и singleton-домены, зафиксирован целевой контракт для `Docs/Terms/*`, подтверждено semantic-filename правило для brand profiles в `BytePress`, а historical logs вынесены в отдельную позднюю фазу миграции. Создан `Plans/BP-000007-id-migration-policy-and-phase-plan.md` как план policy-прохода без запуска самой миграции.

### Эффект
Репозиторий получил явный phase plan для remaining ID migration: новые артефакты создаются только по новому контракту, а legacy-слои переходят на него управляемыми отдельными проходами.

---

## CHG-000015 — Remaining plan layer приведён к каноническим именам и 6-значным plan ID
ID: CHG-000015
Дата: 2026-03-17
Тип_изменения: Документация
Источник: Исполнение принятого naming contract для remaining plan layer
Связи: ADR-000014, PLAN-000002, PLAN-000003, PLAN-000004, PLAN-000005, PLAN-000006, BACK-000021, BACK-000022
Дата_создания: 2026-03-17
Дата_изменения: 2026-03-17

### Описание
Remaining plan-files приведены к каноническим именам `Plans/BP-000002-seed-docs-and-standards.md`, `Plans/BP-000003-fill-technical-and-rules.md`, `Plans/BP-000004-fill-skills-and-tools.md`, `Plans/BP-000005-adapters-memory-mcp-and-bootstrap.md` и `Plans/BP-000006-branch-lifecycle-auto-pr-and-audit-preparation.md`. Их внутренние `ID` выровнены до `PLAN-000002`...`PLAN-000006`, прямые ссылки в `Plans/Roadmap.md`, `Plans/Backlog.md`, `Logs/ADRlog.md`, `Logs/ChangeLog.md`, `Logs/QualityLog.md`, `Docs/Technical/Product_Bootstrap_Validation.md` и минимально в `Tools/bp_lint.py` обновлены под новый канон. `PLAN-000006` переведён в `Завершено` по фактически закрытому DoD.

### Эффект
Весь текущий plan layer BytePress теперь использует один naming contract и 6-значные plan ID без смешения 4- и 6-значного формата в актуальных плановых артефактах.

---

## CHG-000014 — Нормализован foundation-план BytePress и удалён legacy-дубль
ID: CHG-000014
Дата: 2026-03-17
Тип_изменения: Документация
Источник: Исполнение принятого naming contract для слоя `Plans/`
Связи: ADR-000014, PLAN-000001, BACK-000020
Дата_создания: 2026-03-17
Дата_изменения: 2026-03-17

### Описание
Foundation-план BytePress приведён к каноническому имени `Plans/BP-000001-foundation.md`, его внутренний `ID` выровнен до `PLAN-000001`, статус приведён к фактическому состоянию `Завершено`, legacy-дубль `Plans/Plan_BP-0001_BytePress_V1.md` удалён, а `Plans/README.md` и продуктовый слой перепривязаны к актуальному plan-layer без отдельного дубля плана. Прямые ссылки в `Roadmap`, `Backlog` и связанных журнальных записях обновлены на новый `ID`.

### Эффект
В слое `Plans/` устранён параллельный канон для foundation-плана BytePress: остался один актуальный файл, один актуальный `ID` и одна рабочая точка ссылок для связанных документов.

---

## CHG-000013 — Зафиксирован контракт 6-значных ID, naming plan-file и модель профилей
ID: CHG-000013
Дата: 2026-03-17
Тип_изменения: Контракт
Источник: Контрактный проход перед нормализацией legacy-слоя `Plans/*`
Связи: ADR-000014, BACK-000019, BACK-000020, BACK-000021, BACK-000022
Дата_создания: 2026-03-17
Дата_изменения: 2026-03-17

### Описание
Уточнены `Standards/Naming.md`, `Docs/Technical/Model.md`, `Profiles/README.md`, `Plans/README.md` и `Plans/Backlog.md`: зафиксированы 6-значная числовая часть ID, каноническое имя plan-file `Plans/<PRODUCT_CODE>-<NNNNNN>-<slug>.md`, правила `PRODUCT_CODE`, граница `brand profile` / `product profile` и статус текущего слоя `Plans/*` как legacy до отдельного PR нормализации. В backlog добавлены отдельные задачи на нормализацию `Plans/*` и последующее приведение `Schemas/*`, `Templates/*` и `Tools/*` к новому контракту.

### Эффект
Система получила явный контракт именования и профилей до переименования legacy-планов, что снимает двусмысленность для следующих проходов и разделяет текущий контрактный шаг от будущей миграции исторического слоя.

---

## CHG-000012 — Зафиксированы branch lifecycle, целевой Auto-PR процесс и следующий плановый проход
ID: CHG-000012
Дата: 2026-03-14
Тип_изменения: Процесс
Источник: Уточнение управляемого Git/PR-контура BytePress
Связи: ADR-000013, PLAN-000006, BACK-000017, BACK-000018, BACK-000019
Дата_создания: 2026-03-14
Дата_изменения: 2026-03-14

### Описание
Уточнены `AGENTS.md`, `Docs/Technical/Platform_Contracts.md` и `Setup_Guide.md`: зафиксирован полный жизненный цикл ветки, целевой порядок Auto-PR после `push`, правило закрытия head-ветки после merge и минимальная подготовка `gh`. В `Backlog` и новом `Plan` добавлен следующий проход под branch lifecycle, Auto-PR process и подготовку к большому аудиту.

### Эффект
Процесс веток и PR стал управляемым и навигационно закреплённым, а следующий шаг по развитию локального агентного контура вынесен в плановый контур без запуска большого рефакторинга.

---

## CHG-000011 — Добавлены корневые карты README.md и AGENTS.md и обновлены минимальные контракты агентной работы
ID: CHG-000011
Дата: 2026-03-14
Тип_изменения: Документация
Источник: Синхронизация канона BytePress с фактической агентной работой
Связи: ADR-000010, ADR-000012
Дата_создания: 2026-03-14
Дата_изменения: 2026-03-14

### Описание
Добавлен корневой `AGENTS.md` как карта для агента, обновлён корневой `README.md` как карта для человека, минимально уточнены `Standards/Naming.md` и `Docs/Technical/Platform_Contracts.md` для фиксации веточного и PR-контура.

### Эффект
Навигация для человека и агента разведена, а минимальный канон текущего рабочего режима зафиксирован в постоянных артефактах.

---

## CHG-000010 — Подтверждён рабочий цикл agent push -> agent PR -> human approve -> human merge в GitHub
ID: CHG-000010
Дата: 2026-03-14
Тип_изменения: Процесс
Источник: Публикация BytePress в GitHub и фактические эпизоды агентной работы
Связи: ADR-000010, ADR-000011, ADR-000012
Дата_создания: 2026-03-14
Дата_изменения: 2026-03-14

### Описание
Подтверждён рабочий контур: агент работает в task-ветке, выполняет `push`, готовит PR, человек утверждает направление и выполняет merge в `develop`/`main`.

### Эффект
GitHub-процесс BytePress стал явным и воспроизводимым для следующих проходов агентной работы.

---

## CHG-000009 — Усилен bootstrap продукта и подтверждён тестовой генерацией
ID: CHG-000009
Дата: 2026-03-10
Тип_изменения: Инструмент
Источник: PLAN-000005
Связи: BACK-000016, ADR-000009, ROAD-000007
Дата_создания: 2026-03-10
Дата_изменения: 2026-03-10

### Описание
`bp_bootstrap.py` усилен до продуктового полезного минимума: теперь он создаёт не только папки, но и минимальные документы, журналы, один стартовый `Plan`, один стартовый backlog-элемент и управляемые скрипты продукта. Выполнена отдельная тестовая генерация каркаса `Speculorg.Terminal`.

### Эффект
Bootstrap продукта перестал быть декларативной заготовкой и стал подтверждённой функцией `BytePress v1`.

---

## CHG-000008 — Оформлен интеграционный каркас Adapters, Memory и MCP
ID: CHG-000008
Дата: 2026-03-10
Тип_изменения: Архитектура
Источник: PLAN-000005
Связи: BACK-000013, BACK-000014, BACK-000015, ADR-000008, ROAD-000007
Дата_создания: 2026-03-10
Дата_изменения: 2026-03-10

### Описание
Домены `Adapters/`, `Memory/` и `MCP/` переведены из пустых заготовок в согласованный каркас: добавлены политика, реестры, интерфейсы и явные границы применения.

### Эффект
`BytePress` получил управляемый интеграционный контур расширения без внедрения лишней сложности в ядро знания.


---

## CHG-000007 — Замкнут исполнительный контур ролей, навыков и инструментов BytePress
ID: CHG-000007
Дата: 2026-03-10
Тип_изменения: Исполнение
Источник: PLAN-000004
Связи: BACK-000011, BACK-000012, ADR-000007, ROAD-000003, ROAD-000006
Дата_создания: 2026-03-10
Дата_изменения: 2026-03-10

### Описание
Библиотека навыков BytePress усилена до полного набора фаз золотого пути, добавлены `Implementation` и `Quality`, существующие навыки приведены к единому формату. Инструменты `bp_bootstrap.py` и `bp_normalize_terms.py` переведены из заглушек в полезный минимум `v1`, а `bp_lint.py` согласован с исполнительным контуром. Роли и профили обновлены под актуальные навыки и стандарты.

### Эффект
BytePress получил рабочий исполнительный контур: роли, навыки, инструменты и профиль теперь поддерживают один и тот же порядок работы и перестали расходиться между собой.

---

## CHG-000006 — Усилен технический слой и контур правил BytePress
ID: CHG-000006
Дата: 2026-03-10
Тип_изменения: Архитектура
Источник: PLAN-000003
Связи: BACK-000009, BACK-000010, ADR-000005, ADR-000006
Дата_создания: 2026-03-10
Дата_изменения: 2026-03-10

### Описание
`Docs/Technical/*` заполнены до уровня рабочего технического контура `v1`, а `Rules/` дополнен правилами о доменных границах, планах, журналах и порядке массового наполнения.

### Эффект
BytePress получил не только каркас, но и явное техническое объяснение своего устройства и достаточный набор обязательных ограничений для системной работы.

---

## CHG-000005 — Введён рабочий журнальный контур решений и изменений
ID: CHG-000005
Дата: 2026-03-10
Тип_изменения: Процесс
Источник: PLAN-000002
Связи: BACK-000008, ADR-000002, ADR-000003, ADR-000004
Дата_создания: 2026-03-10
Дата_изменения: 2026-03-10

### Описание
В `ADRlog` и `ChangeLog` добавлены пропущенные записи по уже принятым архитектурным решениям и значимым изменениям. Плановый и журнальный контуры приведены к рабочему режиму.

### Эффект
Журналы перестали быть пустой формальностью и стали системным контуром фиксации решений и значимых изменений.

---

## CHG-000004 — Заполнены короткие стандарты BytePress полезными практиками
ID: CHG-000004
Дата: 2026-03-10
Тип_изменения: Стандарт
Источник: PLAN-000002
Связи: BACK-000007, ADR-000003, ADR-000004
Дата_создания: 2026-03-10
Дата_изменения: 2026-03-10

### Описание
Стандарты `Documentation`, `Terminology`, `Planning`, `Coding` и `Release` усилены только теми практиками из Speculorg, которые полезны на текущем этапе.

### Эффект
BytePress получил рабочие короткие нормативы вместо пустых или слишком абстрактных заготовок.

---

## CHG-000003 — Заполнена базовая терминология BytePress и политика её изменений
ID: CHG-000003
Дата: 2026-03-10
Тип_изменения: Документация
Источник: PLAN-000002
Связи: BACK-000006, ADR-000002, ADR-000004
Дата_создания: 2026-03-10
Дата_изменения: 2026-03-10

### Описание
Созданы отдельные карточки базовых терминов BytePress, индекс словаря и политика изменения терминов.

### Эффект
Терминологическая база стала управляемой: определения вынесены в отдельные сущности, а ввод новых терминов теперь подчинён явной процедуре.

---

## CHG-000002 — Уточнены схемы и шаблоны ключевых сущностей
ID: CHG-000002
Дата: 2026-03-10
Тип_изменения: Стандарт
Источник: PLAN-000001
Связи: BACK-000004, ADR-000004
Дата_создания: 2026-03-10
Дата_изменения: 2026-03-10

### Описание
Уточнены `Schemas/` и `Templates/` для `Term`, `Roadmap`, `Backlog`, `Plan`, `ADRlog`, `ChangeLog`, `Profile`, `Role`, `Rule`, `Standard`.

### Эффект
Контракты данных стали пригодны для системного заполнения документов и дальнейшей автоматической проверки.

---

## CHG-000001 — Создан первичный каркас BytePress v1
ID: CHG-000001
Дата: 2026-03-09
Тип_изменения: Структура
Источник: PLAN-000001
Связи: ADR-000001, BACK-000003
Дата_создания: 2026-03-09
Дата_изменения: 2026-03-10

### Описание
Создан первичный каркас `BytePress v1` с доменным корнем, базовыми документами, журналами, профилями, ролями, правилами и стандартами.

### Эффект
Появилась переносимая основа системы, пригодная для дальнейшего уточнения контрактов данных.
