# Platform_Contracts

## Назначение
`Docs/Technical/Platform_Contracts.md` является каноническим platform-contract текущего `BytePress`.

Этот document отвечает на вопросы:
- в какой рабочей платформе `BytePress` считается поддерживаемым;
- какие execution assumptions обязательны;
- какой tool perimeter считается поддерживаемым;
- какую роль играет каждый ключевой инструмент;
- какие режимы platform usage допустимы, а какие считаются отклонением.

## Место документа в technical-layer
`Platform_Contracts.md` является supporting technical-document, а не частью required core.

Его роль:
- фиксировать platform assumptions, execution boundaries и supported tool perimeter;
- удерживать границу между system contracts и фактической рабочей средой, где эти contracts materialize и проверяются;
- не дублировать `README.md` как карту technical-layer;
- не дублировать `Architecture.md` как карту доменов и слоёв;
- не дублировать `Model.md` как ownership-модель;
- не дублировать `Artifact_Lifecycle.md` как source-of-truth matrix и sync-loop;
- не дублировать `Interfaces.md` как карту touchpoints;
- не дублировать `System_Invariants.md` как список ненарушаемых свойств;
- не дублировать `Pipeline/*` как process-canon.

## Чем platform-contract отличается от соседних документов
- `README.md` отвечает за границы technical-layer и required/supporting split.
- `Architecture.md` отвечает за карту доменов, слоёв и архитектурные запреты подмены.
- `Model.md` отвечает за сущности, ownership состояния и основные связи.
- `Artifact_Lifecycle.md` отвечает за источники истины, обязательные sync-loop и layer transitions.
- `Interfaces.md` отвечает за допустимые touchpoints и классы интерфейсов.
- `System_Invariants.md` отвечает за ненарушаемые свойства системы.
- `Platform_Contracts.md` отвечает за рабочую платформу, execution constraints и supported tool perimeter, в котором эти contracts исполняются.
- `Pipeline/*` отвечает за process-canon, а не за platform assumptions.

## Поддерживаемая среда исполнения
### Каноническая рабочая среда
- Linux считается канонической рабочей платформой `BytePress`.
- WSL допускается как эквивалентный режим, если поведение shell, Git и Python остаётся совместимым с Linux-контуром.
- Windows-native execution без Linux/WSL не считается каноническим режимом для active work.

### Рабочий execution context
- основным execution interface считается локальный shell-контур внутри репозитория;
- рабочая директория должна оставаться файловым деревом Git-репозитория, а не ad hoc export или временной копией без `.git`;
- основной путь репозитория может отличаться от `~/code/BytePress`, но среда должна сохранять тот же filesystem-first и Git-first contract.

### Минимальные средовые допущения
- доступна файловая система с обычными path operations;
- доступен Git-контур веток, коммитов, diff и PR-подготовки;
- доступен `python3` для запуска project tooling;
- доступен shell уровня `bash` или совместимого Linux-shell;
- UTF-8 текст и line-based diff считаются нормой для активных артефактов.

## Обязательные platform assumptions
### Repository-first contract
- активное состояние системы читается из репозитория и его canonical files;
- tool output, shell history, chat context и runtime notes не считаются source of truth без фиксации в репозитории;
- archive artifacts остаются history/reference layer и не становятся active source of truth.

### Controlled execution contract
- активная работа идёт только через task-ветку от `develop`;
- локальные коммиты и self-check выполняются до final push;
- `main` и `develop` не редактируются напрямую;
- PR в `develop` остаётся каноническим delivery interface для task work.

### Tooling-follows-documents contract
- инструменты используют уже утверждённые documents и contracts;
- изменение обязательного tooling behavior без документной синхронизации считается platform drift;
- ad hoc local scripts вне `Tools/*` не становятся частью supported platform perimeter только по факту использования.

### External isolation contract
- продуктовые репозитории и их runtime не являются execution substrate самого `BytePress`;
- model adapters, memory и MCP остаются отдельными extension domains и не подменяют ядро знания и governance;
- secrets, credentials и внешние service tokens не попадают в Git и не становятся частью canonical platform state.

## Supported tool perimeter
### Обязательные инструменты
- `git` — delivery и history perimeter репозитория;
- `python3` — execution substrate для project tooling;
- Linux/WSL shell — основной interactive execution interface;
- `Tools/bp_lint.py` — обязательная структурная проверка `BytePress` и product bootstrap contract.

### Поддерживаемые repo-native инструменты
- `Tools/bp_bootstrap.py` — materialization минимального product skeleton по contract `BytePress`;
- `Tools/bp_integration_smoke.py` — deterministic integration smoke handoff для generated product repo без реальных внешних подключений;
- `Tools/bp_normalize_terms.py` — нормализация карточек терминов и пересборка индекса терминов.

### Поддерживаемые служебные инструменты
- `gh` — допустимый service interface для проверки existing PR и создания нового PR, если доступен и авторизован;
- `rg`, `sed`, `find` и совместимые shell utilities — допустимые inspection helpers для локальной навигации и чтения active layer;
- стандартные Git subcommands — допустимый operational interface для branch lifecycle и review prep.

### Что не входит в supported perimeter
- произвольные GUI-only workflows как обязательный execution path;
- tool-specific hidden state вне репозитория как единственный носитель contract;
- Windows-native shell path как primary active platform;
- случайные одноразовые scripts вне `Tools/*` как часть канонического platform contract.

## Роль ключевых инструментов
### `git`
Роль:
- держит task-branch workflow, diff, commit history, push и merge contour.

Не роль:
- не владеет доменным source of truth вместо документов репозитория.

### `python3`
Роль:
- даёт execution substrate для deterministic project tools.

Не роль:
- не заменяет document contracts и не превращает scripts в primary owner system state.

### `Tools/bp_lint.py`
Роль:
- проверяет минимальные structural contracts active `BytePress` и product bootstrap.

Не роль:
- не определяет system contracts в одиночку и не заменяет technical documents.

### `Tools/bp_bootstrap.py`
Роль:
- materialize first-usable replicated product repo и его controlled integration smoke route по уже утверждённому bootstrap contract.

Не роль:
- не определяет product governance или technical contracts без синхронизации документов.

### `Tools/bp_normalize_terms.py`
Роль:
- обслуживает serial term cards и индекс `Base_Terms.md`.

Не роль:
- не является owner'ом терминологического слоя.

### `Tools/bp_integration_smoke.py`
Роль:
- проверяет minimal controlled connector handoff generated product repo против active integration contracts `BytePress`;
- при repo-native report route materialize deterministic integration evidence artifact без обращения к внешней сети.

Не роль:
- не открывает реальные внешние подключения;
- не становится vendor runtime engine;
- не подменяет `bp_lint.py`, `MCP/*` или procedural audit integration-layer.

### `gh`
Роль:
- автоматизирует PR contour после final push, если среда и аутентификация это позволяют;
- является единственным основным маршрутом создания PR в `develop`.

Не роль:
- не является обязательным execution substrate для локальной подготовки pass;
- не должен переавторизовываться автоматически при первой ошибке.

## Допустимые режимы platform usage
- работать внутри Git-репозитория `BytePress` или product repo, созданного по bootstrap contract;
- синхронизироваться от `origin/develop` перед началом task pass;
- выполнять project tooling через `python3 Tools/...`;
- выполнять integration smoke только через repo-native tool route, а не через прямые внешние connector calls;
- использовать shell utilities для чтения, diff и навигации по active layer;
- использовать `gh` только после final push и после проверки отсутствия existing PR для head-ветки;
- не использовать GitHub connector для создания PR;
- если `gh` недоступен или не авторизован, выполнить push и вернуть ссылку или точные параметры для ручного PR;
- хранить runtime context только как временный execution helper, не превращая его в source of truth.

## Недопустимые отклонения и anti-patterns
- считать shell output, chat transcript или память исполнителя каноническим contract без фиксации в репозитории;
- менять active system contract только через tooling behavior без документной синхронизации;
- выполнять active work напрямую в `develop`, `main` или повторно использовать уже merged head-ветку;
- считать Windows-native execution без Linux/WSL равноправным каноническим режимом;
- использовать ignored tool-output paths как substitute для planning-state, archive или facts;
- использовать `Pipeline/*` как justification для переписывания platform constraints, ownership или planning rules;
- вносить secrets в Git или считать внешние сервисы частью обязательного execution substrate;
- подменять supported tool perimeter случайными локальными скриптами, о которых не знает active documentation.

## Отношение platform-layer к соседним контурам
### К `Plans/*`
`Plans/*` задаёт stage/task/pass и branch-delivery contour. `Platform_Contracts.md` фиксирует, в какой среде и какими инструментами этот contour поддерживается, но не владеет planning-state.

### К ignored tool-output paths
ignored tool-output paths остаётся временным execution context. `Platform_Contracts.md` задаёт ограничения среды, в которой runtime допускается, но не делает runtime источником истины.

### К `Tools/*`
`Tools/*` являются materialization and check perimeter текущей платформы. `Platform_Contracts.md` фиксирует их роли и границы, но не переносит в них ownership системных contracts.

### К `Pipeline/*`
`Pipeline/*` остаётся process-canon. `Platform_Contracts.md` фиксирует его как потребителя platform/tool perimeter, но не повторяет phase canon, gates и process IO как primary source.

## Граница документа
`Platform_Contracts.md` не является:
- картой technical-layer как каталога;
- картой доменов и слоёв;
- ownership-моделью сущностей;
- lifecycle-checklist и source-of-truth matrix;
- картой интерфейсов;
- process-canon document.

Он остаётся каноническим contract рабочей платформы, среды исполнения и tool perimeter текущего `BytePress`.

## Связи
- `ADR-000001`
- `ADR-000005`
- `ADR-000007`
- `ADR-000009`
- `RULE-000002`
- `RULE-000003`
- `RULE-000010`
