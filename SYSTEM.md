# SYSTEM.md

## Назначение

Системный реестр архитектурных границ и постоянных правил BytePress Harness. Процедуры находятся в `sops/`, текущая работа — только в `plans/`.

## Домены и границы слоёв

| ID | Путь | Каноническая роль |
|---|---|---|
| `domain:agent-map` | `AGENTS.md` | короткая карта агента и машиночитаемое объявление SoT |
| `domain:human-entry` | `README.md` | вход пользователя, быстрый старт и навигация |
| `domain:system-registry` | `SYSTEM.md` | архитектурные границы и постоянные правила |
| `domain:docs` | `docs/` | объяснения и устойчивый смысл |
| `domain:sops` | `sops/` | нормативные процедуры |
| `domain:roles` | `roles/` | ответственность и полномочия основных ролей фаз SDLC |
| `domain:skills` | `skills/` | переносимые Agent Skills без расширения полномочий |
| `domain:templates` | `templates/` | формы создаваемых записей |
| `domain:plans` | `plans/` | единственное текущее состояние `ROAD -> BACK -> PLAN` |
| `domain:logs` | `logs/` | факты и свидетельства |
| `domain:research` | `research/` | исследования Product Unit |
| `domain:tests` | `tests/` | единственное специальное место для исполняемых модулей технической и регрессионной проверки |
| `domain:tools` | `tools/` | исполняемые рабочие инструменты Product Unit |
| `domain:src` | `src/` | код продукта; в стартовой обвязке пуст по замыслу |

Полное правило хранится в каноническом слое. Другие слои дают только необходимое краткое пояснение и ссылку.

## Инварианты

| ID | Формулировка |
|---|---|
| `invariant:human-control` | Человек управляет, агенты исполняют. |
| `invariant:workspace-product` | Workspace `<Slug>` делает продукт `<Slug>`; продукт не управляет Workspace. |
| `invariant:local-plan` | В `plans/active/` допускается от нуля до одного активного `PLAN-*.md`. |
| `invariant:no-current-workspace-route` | Product Unit не хранит текущий маршрут Workspace. |
| `invariant:technical-check-boundary` | Технический PASS не является продуктовой приёмкой. |
| `invariant:executable-code-layers` | Рабочие инструменты находятся в `tools/`; тестовые модули находятся в `tests/`, механически доказывают Markdown-контракты и не имеют собственного пользовательского CLI или нормативного смысла. Вне этих слоёв исполняемая поверхность требует отдельного решения владельца. |
| `invariant:sot-single-source` | Текущий `SOT_MODE` объявляется только в `AGENTS.md`. |
| `invariant:sot-files-isolation` | `sot_files` не читает `.git` и не вызывает Git CLI. |
| `invariant:sot-git-current` | `sot_git` требует валидные `HEAD` и ветвь, чистое дерево и отсутствие remote. |
| `invariant:sot-github-current` | `sot_github` проверяет только подготовленный локальный репозиторий, один `origin`, совпадающую идентичность, upstream и `origin/HEAD`. |
| `invariant:canonical-product-identity` | Идентичность продукта согласована между кратким описанием, активным PLAN и README с приоритетом продукта. |
| `invariant:typed-acceptance` | Продуктовая приёмка фиксируется только записью `product_acceptance` с ID `PA-*`. |
| `invariant:protected-surfaces` | Системные поверхности не меняются в `product-work` вне точного разрешённого исключения. |
| `invariant:harness-blocker` | При дефекте Harness агент выводит `HARNESS_BLOCKER: <краткое описание>` и прекращает изменения. |
| `invariant:sdlc-21` | Канонический SDLC содержит фазы `01–21`; `21 Вывод из эксплуатации` переводит продукт в terminal state `retired`. |
| `invariant:role-coverage` | Каждая каноническая фаза имеет одну самостоятельную основную роль в `roles/`; один исполнитель может последовательно принимать несколько ролей. |
| `invariant:skills-authority` | Agent Skill не расширяет полномочия PLAN, SYSTEM или SOP; основа Product Unit поставляет `0` собственных встроенных навыков. |

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
| `15` | `release-readiness` | Готовность к выпуску | не создаёт tag или release |
| `16` | `release` | Выпуск | только отдельный маршрут |
| `17` | `handoff` | Передача | требует проверяемого получателя |
| `18` | `operation` | Эксплуатация | действует в утверждённых границах |
| `19` | `maintenance` | Сопровождение | смысловое изменение возвращается в SDLC |
| `20` | `retrospective` | Ретроспектива | вывод не становится правилом автоматически |
| `21` | `decommissioning` | Вывод из эксплуатации | только отдельное решение; terminal state `retired` |

`discovery` и `product discovery` являются совместимыми именами стартового прохода фазы `04 Исследование` и нормализуются в `research`; отдельной канонической фазой они не являются. Процедурные проекции находятся в `sops/sdlc.md` и `sops/project-management.md`.

## Операционные режимы (`registry:operational-modes`)

| ID | Назначение | Граница |
|---|---|---|
| `product-work` | обычная продуктовая работа | следует активному PLAN и фазе SDLC |
| `system-editing` | изменение системных файлов | только активный PLAN, открытый владельцем |

Агент в режиме `product-work` сам не открывает `system-editing`.

## Режимы SoT (`registry:sot-modes`)

Поддерживаются ровно три режима:

| ID | Локальный контракт |
|---|---|
| `sot_files` | файловая поверхность; Git полностью вне проверки |
| `sot_git` | валидный локальный репозиторий без remote |
| `sot_github` | подготовленные локальные `origin`, идентичность, upstream, remote refs и `origin/HEAD`; сеть вне проверки |

При `sot_github` в `AGENTS.md` существует ровно одно поле `SOT_GITHUB_REPOSITORY` со значением `owner/repository`; в других режимах поле отсутствует. Кроме технического bootstrap отсутствующей неизменённой Product Unit в уже объявленном `sot_git`, режим не разрешает transition, изменяющую Git-работу, fetch, push, PR, merge, tag, выпуск или GitHub write. Нормативный контракт находится в `sops/sot.md`.

## Типизированные записи

| Запись | Хранилище | Назначение |
|---|---|---|
| `interview_evidence`, `IE-*` | `logs/sessions.md` | фактический ответ интервью |
| `owner_decision`, `OD-*` | `logs/decisions.md` | отдельное решение владельца |
| `product_acceptance`, `PA-*` | `logs/decisions.md` | отдельная продуктовая приёмка |

Активный PLAN хранит ссылки `INTERVIEW_EVIDENCE_REF`, `OWNER_DECISION_REFS` и `PRODUCT_ACCEPTANCE_REF`, но не копирует содержимое записей. Канонический локальный источник использует конечный диапазон `codexlog:.codex/<actual-log-file>#lines=<start>-<end>`.

## Состояние продукта

| Условие | Состояние |
|---|---|
| существует активный PLAN | его текущая фаза |
| активный PLAN отсутствует, есть принятое завершённое основание | `accepted-completed` |
| есть продуктовые файлы без активного PLAN и принятого основания | `idle-product` |
| стартовая обвязка пуста и активный PLAN отсутствует | `initial-idle` |

Состояние определяется по текущим артефактам без реконструкции истории.

`idle-product` и `accepted-completed` могут входить в `discovery` с существующей продуктовой базой. Наличие базового кода само по себе не является свидетельством преждевременной реализации; границу изменений по-прежнему задают активный PLAN и `ALLOWED_SURFACES`.

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

`ALLOWED_SURFACES` принимает точный относительный путь, дерево `path/**`, `none` либо точные исключения `AGENTS.md::SOT_MODE` и `AGENTS.md::SOT_GITHUB_REPOSITORY`. Исключения допустимы только в переходе, утверждённом владельцем; внешняя граница всегда имеет приоритет.

## Гейты (`registry:gates`)

| ID | Назначение |
|---|---|
| `owner-decision-required` | требуется решение владельца |
| `interview-complete` | обязательное интервью закрыто |
| `implementation-approved` | владелец открыл реализацию |
| `verification-pass` | техническая проверка прошла |
| `ready-for-owner-review` | результат можно передать владельцу |
| `product-acceptance` | отдельная продуктовая приёмка |
| `release-readiness` | отдельная готовность к выпуску |
| `release/tag` | отдельное решение о выпуске и tag |

## Системные связи

| Смысл | Канонический владелец | Процедура или проверка |
|---|---|---|
| решения и плановый контур | `plans/`, `logs/` | `sops/project-management.md` |
| режим источника истины | `AGENTS.md`, этот реестр | `sops/sot.md`, `tools/bp_check.py` |
| защищённые поверхности | этот реестр | `sops/project-management.md`, `sops/verify-work.md` |
| основные роли фаз | `roles/` | `roles/README.md` |
| переносимые Agent Skills | `skills/` | `skills/README.md` |
| продуктовая приёмка | `logs/decisions.md` | `sops/verify-work.md` |
| терминология | `docs/terminology/glossary.md` | `sops/terminology.md` |
| рабочие инструменты | `tools/README.md` | `tools/bp_check.py`, `tools/bp_clean.py` |
| нормативные контракты проверки | соответствующие Markdown-владельцы | `tests/README.md`, `tests/test_harness.py` |

После появления продуктового кода root `README.md` становится product-first по `templates/product-readme.md`. Пользовательские документы не хранят внутренние `ROAD`, `BACK`, `PLAN`, решения владельца или динамический статус Harness; публичная SoT configuration остаётся допустимым пользовательским контрактом.
