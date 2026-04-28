# Domain Model Migration Plan

## Назначение
`Docs/Technical/Domain_Model_Migration_Plan.md` фиксирует безопасный план перехода от разросшейся доменной модели `BytePress` к профильной фабрике самодостаточных продуктовых каркасов.

Этот document не удаляет домены сам по себе. Он задаёт порядок, зависимости, проверки и риски будущих refactoring passes.

## Целевое состояние BytePress
`BytePress` становится фабрикой профилей продукта.

Целевые домены фабрики:
- `AGENTS.md`, `README.md`, `Setup_Guide.md` — входные карты человека и агента;
- `Docs/*` — knowledge, product, user, terms и сокращённые technical contracts фабрики;
- `Pipeline/*` — process model и workflows, включая процедуры, перенесённые из `Skills/*`;
- `Plans/*` — planning contour самой фабрики;
- `Logs/*` — factual closure, ADR и quality evidence фабрики;
- `Rules/*` — короткий набор обязательных проектно-специфичных правил;
- `Schemas/*` — схемы только для проверяемых фабрикой артефактов;
- `Templates/*` — шаблоны только для артефактов, которые фабрика реально materialize;
- `Tools/*` — генерация профильных каркасов и проверка самой фабрики.

Целевые retired domains:
- `Adapters/*` — удалить до появления реального adapter mechanism;
- `Memory/*` — удалить до появления реального memory mechanism;
- `MCP/*` — удалить до появления реального connector mechanism;
- `Runtime/*` — удалить как отдельный домен до появления реального execution mechanism;
- `Roles/*` — удалить до появления реального role execution mechanism;
- `Skills/*` — перенести смысловые процедуры в `Pipeline/*`, затем удалить домен;
- `Standards/*` — обязательные нормы перенести в `Rules/*`, остальное удалить.

## Целевое состояние создаваемого продукта
Создаваемый продукт получает профильный самодостаточный каркас.

Обязательный минимум:
- root entry files;
- `Docs/Discovery/*`, `Docs/Product/*`, `Docs/User/*`, `Docs/Terms/*`, сокращённый `Docs/Technical/*`;
- `Plans/*`;
- `Logs/*`;
- лёгкий локальный `Pipeline/*`;
- локальный `Tools/*`;
- `Templates/*` только для включённых артефактов;
- `Schemas/*` только для артефактов, которые локальный `Tools/*` проверяет.

Продукт не получает `Adapters/*`, `Memory/*`, `MCP/*`, `Runtime/*`, `Roles/*`, `Skills/*` и отдельный `Standards/*` в baseline.

## Что удалить
Удалять только после tool-gate pass, в котором `bp_lint.py` перестанет требовать наличие домена и появится replacement contract.

Кандидаты на удаление:
- `Adapters/*` после удаления adapter requirements из bootstrap/lint/contracts;
- `Memory/*` после фиксации отсутствия active memory mechanism;
- `MCP/*` после удаления connector placeholder contracts;
- `Runtime/*` после переноса временных outputs в ignored tool-output paths;
- `Roles/*` после удаления role references из profiles/interfaces/model;
- `Skills/*` после переноса процедур в `Pipeline/*`;
- `Standards/*` после переноса обязательных норм в `Rules/*`.

## Что перенести
- `Skills/Interview.md`, `Skills/Planning.md`, `Skills/Review.md`, `Skills/Quality.md`, `Skills/Release.md`, `Skills/Support.md`, `Skills/Research.md`, `Skills/Requirements.md`, `Skills/Discussion.md`, `Skills/Implementation.md` перенести в `Pipeline/Workflows.md` или отдельные workflow files.
- Обязательные нормы из `Standards/Naming.md`, `Standards/Planning.md`, `Standards/Quality.md`, `Standards/Traceability.md`, `Standards/Documentation.md`, `Standards/Terminology.md`, `Standards/Coding.md`, `Standards/Release.md` перенести в сокращённые project-specific `Rules/*` только если они являются запретом или обязательным условием.
- Generated `scripts/*` перенести в product-local `Tools/*`; shell scripts оставить только как optional aliases, если профиль требует shell entrypoints.
- Runtime smoke reports перенести из `Runtime/*` в ignored path продукта, принадлежащий `Tools/*`.

## Что объединить
- Повторяющиеся verification/validation/evidence documents объединить в сокращённый technical verification contract.
- `Docs/Technical/Pipeline.md` оставить только как краткий technical pointer или удалить после усиления `Pipeline/README.md`.
- Product bootstrap contract и profile package matrix синхронизировать так, чтобы contract описывал artifact obligations, а matrix — package composition.
- `Rules/*` сократить до проектно-специфичных обязательных правил; meta-rules оставить только если они реально проверяются или нужны агентному gate.

## Какие проверки обновить
- `Tools/bp_lint.py` должен получить transitional mode: старый BytePress layout допустим до удаления, новый target layout обязателен после migration flag или версии.
- Product checks должны перейти с `scripts/*` и `BYTEPRESS_ROOT` на local product `Tools/*`.
- Bootstrap checks должны проверять profile packages: `Core`, selected `Rules`, selected `Templates`, selected `Schemas`.
- Negative checks должны падать на placeholder domains `Adapters`, `Memory`, `MCP`, `Runtime`, `Roles` в создаваемом продукте.
- Repo checks должны перестать требовать retired domains только в том pass, где удаляются соответствующие files.

## Риски
- Одновременное удаление доменов и изменение tools может сломать lint без ясного replacement contract.
- Перенос `scripts/*` в product `Tools/*` меняет operational model уже созданных продуктов и требует отдельного service update route.
- Сокращение `Standards/*` может потерять полезные нормы, если не отделить обязательное от рекомендательного.
- Перенос `Skills/*` в `Pipeline/*` может раздуть process-domain, если workflows станут вторым technical-layer.
- Локальные product tools могут начать расходиться между продуктами без profile versioning.
- Сокращение `Docs/Technical/*` может удалить owner-documents, на которые ещё ссылаются `Plans`, `Logs`, `Tools` или generated docs.

## Последовательность passes
1. Зафиксировать ADR, target matrix и этот migration plan без удаления доменов.
2. Добавить profile package contract и версионирование product profiles.
3. Обновить `bp_bootstrap.py` для генерации local product `Tools/*`, lightweight `Pipeline/*`, profile-bound `Templates/*` и `Schemas/*`. Статус: начато в `PLAN-000080`.
4. Обновить `bp_lint.py` под transitional checks. Статус: начато в `PLAN-000080`.
5. Перенести procedures из `Skills/*` в `Pipeline/*`.
6. Перенести обязательные norms из `Standards/*` в `Rules/*` и сократить ruleset.
7. Удалить retired domains после прохождения updated checks.
8. Сократить `Docs/Technical/*` и убрать повторяющиеся verification/validation documents.

## Граница документа
Этот план не является разрешением на массовое удаление файлов. Удаление каждого домена требует отдельного pass, updated checks и фактического log closure.
