# SYSTEM.md

## Назначение

Системный реестр архитектурных границ и постоянных правил статической поставки BytePress Harness. Текущая работа, планы, журналы и внутренние свидетельства принадлежат внешнему `WS_<Slug>/`, а не корню продукта.

## Домены и границы слоёв

| ID | Путь | Каноническая роль |
|---|---|---|
| `domain:agent-map` | `AGENTS.md` | короткая карта агента; машинный источник состава и SoT — Project Profile |
| `domain:human-entry` | `README.md` | вход пользователя, быстрый старт и навигация |
| `domain:system-registry` | `SYSTEM.md` | архитектурные границы и постоянные правила |
| `domain:docs` | `docs/` | объяснения и устойчивый смысл |
| `domain:sops` | `sops/` | нормативные процедуры |
| `domain:roles` | `roles/` | ответственность и полномочия основных ролей фаз SDLC |
| `domain:skills` | `skills/` | переносимые Agent Skills без расширения полномочий |
| `domain:templates` | `templates/` | статические заготовки и формы будущих записей Workspace |
| `domain:tests` | `tests/` | принадлежащие продукту исполняемые модули технической и регрессионной проверки Harness |
| `domain:tools` | `tools/` | принадлежащие продукту исполняемые возможности Harness |

Полное правило хранится в каноническом слое. Другие слои дают только необходимое краткое пояснение и ссылку.

## Инварианты

| ID | Формулировка |
|---|---|
| `invariant:human-control` | Человек управляет, агенты исполняют. |
| `invariant:workspace-product` | Workspace `<Slug>` делает продукт `<Slug>`; продукт не управляет Workspace. |
| `invariant:workspace-plan` | Развёрнутый Workspace хранит `WROAD -> WBACK -> WPLAN`; поставка BytePress не содержит текущего маршрута. |
| `invariant:no-current-workspace-route` | Product Unit не хранит текущий маршрут Workspace. |
| `invariant:technical-check-boundary` | Технический PASS не является продуктовой приёмкой. |
| `invariant:executable-code-layers` | Рабочие инструменты находятся в `tools/`; тестовые модули находятся в `tests/`, механически доказывают Markdown-контракты и не имеют собственного пользовательского CLI или нормативного смысла. Вне этих слоёв исполняемая поверхность требует отдельного решения владельца. |
| `invariant:profile-composition` | После Project Start единственный корневой `<Slug>.profile` задаёт состав Workspace и его `sot_mode`; Slug и производные пути не дублируются полями. |
| `invariant:static-distribution` | Поставка не содержит локальных планов, журналов, подставного исследовательского каталога, синтетической контрольной отметки или обязательного универсального `src/`. |
| `invariant:product-delivery` | Корень продукта и граница поставки совпадают с `<Slug>/` непосредственно в Workspace; Product Unit после поставки не зависит от Project Profile. |
| `invariant:native-checks-declarative` | Разбор Project Profile, проверка Workspace и проверка состава продукта не исполняют `product_native_checks`; запуск принадлежит только явному режиму `check_product.py`. |
| `invariant:sot-single-source` | Корневой Project Profile — единственный машинный источник состава и SoT Workspace; статическая поставка не содержит конфигурации развёрнутой среды. |
| `invariant:sot-files-isolation` | `sot_files` не читает `.git` и не вызывает Git CLI. |
| `invariant:sot-git-current` | `sot_git` требует валидные `HEAD` и ветвь, чистое дерево и отсутствие удалённого репозитория. |
| `invariant:sot-github-current` | `sot_github` проверяет только подготовленный локальный репозиторий, один `origin`, совпадающую идентичность, отслеживаемую ветвь и `origin/HEAD`. |
| `invariant:canonical-product-identity` | Идентичность продукта принадлежит его документации и README; WPLAN Workspace может ссылаться на неё, но не дублирует владельца смысла. |
| `invariant:typed-acceptance` | Продуктовая приёмка фиксируется только записью `product_acceptance` с ID `PA-*`. |
| `invariant:protected-surfaces` | Системные поверхности не меняются в `product-work` вне точного разрешённого исключения. |
| `invariant:harness-blocker` | При дефекте Harness агент выводит `HARNESS_BLOCKER: <краткое описание>` и прекращает изменения. |
| `invariant:sdlc-21` | Канонический SDLC содержит фазы `01–21`; `21 Вывод из эксплуатации` переводит продукт в конечное состояние `retired`. |
| `invariant:role-coverage` | Каждая каноническая фаза имеет одну самостоятельную основную роль в `roles/`; один исполнитель может последовательно принимать несколько ролей. |
| `invariant:skills-authority` | Agent Skill не расширяет полномочия WPLAN, SYSTEM или SOP; поставка BytePress содержит `0` собственных встроенных навыков. |
| `invariant:sdd-tdd-rails` | `S0/S1/S2`, владение спецификацией, проверка DDD, `REQ/INV/SCN`, предварительное написание тестов, Impact Scan и Consistency Closure следуют `docs/technical/task-flow.md`; тесты и заготовки не создают полномочий владельца. |
| `invariant:product-version` | `VERSION` — единственный машинный источник версии продукта BytePress; версия развёрнутого Harness, снимок, тег и Release имеют других владельцев смысла. |
| `invariant:project-start-v1` | `tools/new_project.py` выполняет `preview` без записи и `apply` только с разрешением по контрольной сумме: создаёт отдельный `WS_<Slug>/`, минимальный профиль из четырёх полей, пустой либо только скопированный корень продукта и только `WROAD-000001`; исходная поставка и источник существующего продукта неизменны. |

## Машинная проекция фаз SDLC (`registry:sdlc-phases`)

Канонический полный каталог и смысл фаз принадлежат [docs/technical/sdlc.md](docs/technical/sdlc.md). Таблица системного реестра ниже является его машинной проекцией для прямых потребителей и не создаёт второго владельца модели.

| № | ID | Фаза | Граница |
|---|---|---|---|
| `01` | `intent` | Замысел | не открывает реализацию |
| `02` | `discussion` | Обсуждение | не подменяет решение владельца |
| `03` | `interview` | Интервью | требует ответа владельца |
| `04` | `research` | Исследование | вывод не является решением владельца |
| `05` | `requirements` | Требования | черновик не разрешает код |
| `06` | `basis` | Основание | использует только подтверждённые входы |
| `07` | `architecture` | Архитектура | смысловые развилки решает владелец |
| `08` | `design` | Проектирование | не является разрешением реализации |
| `09` | `planning` | Планирование | требует управляемой границы |
| `10` | `approval` | Утверждение | утверждение молчанием запрещено |
| `11` | `implementation` | Реализация | требует решения о реализации |
| `12` | `verification` | Проверка | PASS не равен приёмке |
| `13` | `owner-review` | Обзор владельцем | не является приёмкой |
| `14` | `product-acceptance` | Продуктовая приёмка | только отдельное решение владельца |
| `15` | `release-readiness` | Готовность к выпуску | не создаёт тег или выпуск |
| `16` | `release` | Выпуск | только отдельный маршрут |
| `17` | `handoff` | Передача | требует проверяемого получателя |
| `18` | `operation` | Эксплуатация | действует в утверждённых границах |
| `19` | `maintenance` | Сопровождение | смысловое изменение возвращается в SDLC |
| `20` | `retrospective` | Ретроспектива | вывод не становится правилом автоматически |
| `21` | `decommissioning` | Вывод из эксплуатации | только отдельное решение; конечное состояние `retired` |

`discovery` и `product discovery` являются совместимыми именами стартового прохода фазы `04 Исследование` и нормализуются в `research`; отдельной канонической фазой они не являются. Процедурные проекции находятся в `sops/sdlc.md` и `sops/project-management.md`.

## Операционные режимы (`registry:operational-modes`)

| ID | Назначение | Граница |
|---|---|---|
| `product-work` | обычная продуктовая работа | следует активному WPLAN Workspace и фазе SDLC |
| `system-editing` | изменение системных файлов | только активный WPLAN, открытый владельцем |

Агент в режиме `product-work` сам не открывает `system-editing`. Эти режимы являются состоянием Workspace и не созданы в статической поставке.

## Режимы SoT (`registry:sot-modes`)

Поддерживаются ровно три режима:

| ID | Локальный контракт |
|---|---|
| `sot_files` | файловая поверхность; Git полностью вне проверки |
| `sot_git` | действительный локальный репозиторий без удалённого подключения |
| `sot_github` | подготовленные локальные `origin`, идентичность, отслеживаемая ветвь, удалённые ссылки и `origin/HEAD`; сеть вне проверки |

После развёртывания `sot_mode` принадлежит корневому Project Profile; идентичность репозитория GitHub остаётся отдельной настройкой Workspace. Универсальный `check_workspace.py` читает режим только из профиля и отвергает прежнее машинное поле в `AGENTS.md`; `check_product.py` SoT не интерпретирует. Режим не разрешает переход, `fetch`, `push`, PR, слияние, тег, выпуск или изменяющее действие GitHub.

## Типизированные записи

| Запись | Хранилище | Назначение |
|---|---|---|
| `interview_evidence`, `IE-*` | `WS_<Slug>/logs/sessions.md` | фактический ответ интервью |
| `owner_decision`, `OD-*` | `WS_<Slug>/logs/decisions.md` | отдельное решение владельца |
| `product_acceptance`, `PA-*` | `WS_<Slug>/logs/decisions.md` | отдельная продуктовая приёмка |

Активный WPLAN Workspace хранит ссылки на записи, но не копирует их содержимое. Канонический локальный источник использует конечный диапазон `codexlog:.codex/<actual-log-file>#lines=<start>-<end>`.

## Состояние и поставка

Текущее состояние определяется WPLAN и журналами Workspace без реконструкции истории. Поставка не хранит `initial-idle`, синтетический список задач или стартовую контрольную отметку. Наличие кода и каталогов продукта не определяет фазу, Product Part или разрешение на изменение.

## Защищённые поверхности (`registry:protected-surfaces`)

| ID | Путь |
|---|---|
| `protected:agent-map` | `AGENTS.md` |
| `protected:system-registry` | `SYSTEM.md` |
| `protected:sops` | `sops/` |
| `protected:roles` | `roles/` |
| `protected:skills` | `skills/` |
| `protected:templates` | `templates/` |
| `protected:tools` | `tools/` |

WPLAN Workspace перечисляет точные разрешённые поверхности. Исключения допустимы только в переходе, утверждённом владельцем; внешняя граница всегда имеет приоритет.

## Точки контроля (`registry:gates`)

| ID | Назначение |
|---|---|
| `owner-decision-required` | требуется решение владельца |
| `interview-complete` | обязательное интервью закрыто |
| `implementation-approved` | владелец открыл реализацию |
| `verification-pass` | техническая проверка прошла |
| `ready-for-owner-review` | результат можно передать владельцу |
| `product-acceptance` | отдельная продуктовая приёмка |
| `release-readiness` | отдельная готовность к выпуску |
| `release/tag` | отдельное решение о выпуске и теге |

## Системные связи

| Смысл | Канонический владелец | Процедура или проверка |
|---|---|---|
| решения и плановый контур | `WS_<Slug>/plans/`, `WS_<Slug>/logs/` | `sops/project-management.md` |
| Схема и создание Project Profile | `docs/architecture/project-profile.md` | `tools/project_profile.py`, `tests/test_project_profile.py` |
| Slug, корень продукта, Product Parts и граница поставки | `docs/architecture/domain-model.md` | `tools/project_profile.py` |
| режим источника истины | корневой Project Profile после развёртывания; статическая поставка не имеет текущего SoT | `sops/sot.md` |
| защищённые поверхности | этот реестр | `sops/project-management.md`, `sops/verify-work.md` |
| основные роли фаз | `roles/` | `roles/README.md` |
| переносимые Agent Skills | `skills/` | `skills/README.md` |
| продуктовая приёмка | `WS_<Slug>/logs/decisions.md` | `sops/verify-work.md` |
| терминология | `docs/terminology/glossary.md` | `sops/terminology.md` |
| Создание Workspace через Project Start | `docs/technical/project-start.md` | `tools/new_project.py`, `tests/test_new_project.py` |
| рабочие инструменты | `tools/README.md` | `tools/check_workspace.py`, `tools/check_product.py`, `tools/bp_clean.py`, `tools/project_profile.py`, `tools/new_project.py` |
| нормативные контракты проверки | соответствующие Markdown-владельцы | `tests/README.md`, `tests/test_harness.py`, `tests/test_project_profile.py`, `tests/test_new_project.py` |
| SDD/TDD и владение спецификацией | `docs/technical/task-flow.md` | `templates/specification.md`, `docs/technical/testing.md`, `tests/test_harness.py` |
| Версия продукта | `VERSION`, `docs/product/product-passport.md` | `tests/test_harness.py` |

README продукта прежде всего описывает сам продукт. Пользовательские документы продукта не хранят внутренние WROAD/WBACK/WPLAN, решения владельца или динамический статус Harness. Универсальный каталог исходного кода не предписывается.

## Исполнимый SDLC-инвариант

После Project Start активный WPLAN хранит одну компактную запись `SDLC_TRANSITION: v1`: исходную и целевую фазы и роли, завершённость, ссылки на свидетельства, контрольную отметку, передачу результата, полномочия обеих ролей и независимые статусы точки решения владельца, Verification, Validation, Product Acceptance и Release Authorization. Универсальный инструмент Workspace сверяет запись с [phase-gates](docs/technical/phase-gates.md) и фактическими изменениями файловой системы; он не создаёт полномочия или решения.

`ALLOWED_SURFACES` задаются точными `CREATE/UPDATE/REMOVE` с разрешёнными изменениями типа, режима доступа и содержимого; `PROTECTED_SURFACES` — `PRESERVE`. Полная исходная база, переданная вызывающей стороной, является входом проверки, а не новым владельцем смысла. Любое незаявленное изменение или изменение защищённой поверхности даёт FAIL без исправления.
