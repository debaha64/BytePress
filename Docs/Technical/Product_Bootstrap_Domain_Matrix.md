# Product Bootstrap Domain Matrix

## Назначение
`Docs/Technical/Product_Bootstrap_Domain_Matrix.md` фиксирует целевую матрицу профильных пакетов каркаса продукта.

Этот document отвечает на вопросы:
- какие пакеты каркаса собирает продуктовый профиль;
- какие домены создаваемого продукта являются базовыми для всех профилей;
- какие пакеты включаются только по profile decision;
- какие домены прежней модели не должны materialize без реального механизма;
- какие части текущего `BytePress` остаются фабричными и не копируются как operational clone.

## Статус реализации
Матрица ниже является целевым договором после решения `ADR-000022` и переходным implemented baseline после `PLAN-000080`.

Текущие `Tools/bp_bootstrap.py` и `Tools/bp_lint.py` уже materialize и проверяют `Core` package subset: local product `Tools/*`, lightweight `Pipeline/*`, bounded `Templates/*` и `Schemas/*`. Optional `Profile` packages beyond this subset требуют отдельных passes.

## Категории пакетов
- `Core` — materialize каждым product profile.
- `Profile` — materialize только если выбранный product profile включает пакет.
- `Factory-only` — остаётся в `BytePress` как фабричный слой и не копируется в продукт.
- `Retired-before-mechanism` — не materialize и подлежит удалению или переносу до появления реального механизма.

## Принцип профильного каркаса
Каркас продукта зависит от профиля продукта. Профиль выбирает состав пакетов, но каждый созданный продукт должен быть самодостаточным после создания: локальные `Tools/*` продукта выполняют проверки и служебные сценарии без зависимости от `BYTEPRESS_ROOT`.

`BytePress` остаётся фабрикой, которая описывает пакеты, генерирует начальный продукт и проверяет миграционный contract самой фабрики. Продукт после создания не должен быть operational child процесса `BytePress`.

## Целевая матрица пакетов продукта
| Package | Категория | Product-side materialization | Обязательные артефакты | Причина |
| --- | --- | --- | --- | --- |
| Repository entry | `Core` | root entry files | `README.md`, `AGENTS.md`, `Setup_Guide.md`, `.gitignore` | продукт должен иметь human/agent entry без чтения фабрики |
| Discovery | `Core` | минимальный current-truth route | `Docs/Discovery/README.md`, `Docs/Discovery/Interview.md` | первый product-start остаётся аналитическим до подтверждения текущей истины |
| Product knowledge | `Core` | стартовые product docs | `Docs/Product/README.md`, `Product_Passport.md`, `JTBD.md`, `PRD.md`, `Delivery.md` | продукт получает место для собственной продуктовой истины и паспорт созданного каркаса без домена `Profiles/*` |
| User docs | `Core` | краткий пользовательский контур | `Docs/User/README.md`, `First_Start.md`, `Operating_Mode.md`, `Pass_Request.md`, `Usage_Scenarios.md` | человек должен понимать запуск и формат pass request внутри продукта |
| Technical docs | `Core` | сокращённый technical subset продукта | `Docs/Technical/README.md`, `Architecture.md`, `Interfaces.md`, `System_Invariants.md` | продукту нужен локальный минимальный technical contract без полного `BytePress` core |
| Terms | `Core` | стартовый словарь продукта | `Docs/Terms/README.md`, `Base_Terms.md` | продукт получает минимальный язык, но не копию полного словаря фабрики |
| Plans | `Core` | локальный planning contour | `Plans/README.md`, `Roadmap.md`, `Backlog.md`, initial plan | продукт сам владеет stage/task/pass после создания |
| Logs | `Core` | локальные fact logs | `Logs/README.md`, `ChangeLog.md`, `ADRlog.md`, `QualityLog.md`, `ReleaseLog.md`, `SupportLog.md` | продукт фиксирует свои факты независимо от `BytePress` |
| Pipeline | `Core` | лёгкий локальный process contour | `Pipeline/README.md`, `Phases.md`, `Workflows.md`, `Gates.md` | каждый продукт получает основной путь, workflows, gates, уровни проверок, журнальное закрытие и PR-маршрут через `gh` без полного pipeline BytePress |
| Tools | `Core` | локальные product tools | `Tools/README.md`, `Tools/product_check.py`, `Tools/product_bootstrap_smoke.py` или profile-equivalent scripts | проверки и служебные маршруты должны быть независимыми после создания |
| Rules | `Profile` | только проектно-специфичные обязательные правила | `Rules/README.md` и выбранные `RULE-*` | правила нужны только там, где профиль вводит реальные обязательства продукта |
| Templates | `Profile` | только шаблоны артефактов, materialized в каркасе | `Templates/README.md` и template files для включённых артефактов | продукт не получает шаблоны сущностей, которых у него нет |
| Schemas | `Profile` | только схемы проверяемых артефактов | `Schemas/README.md` и schema files для реально проверяемых артефактов | schema-layer не должен быть декоративным |
| Former standards layer | `Factory-only` | не materialize как отдельный product domain | нет | обязательные нормы живут в `Rules/*`; остальное остаётся историей решения |
| Former procedure layer | `Factory-only` | не materialize как отдельный product domain | нет | процедуры живут в `Pipeline/*` как workflows |
| Profiles | `Factory-only` | не materialize как отдельный domain продукта | profile data в generated config или `README` пакетов | профиль является входом фабрики, а не отдельным operational layer продукта |
| Adapters | `Retired-before-mechanism` | не materialize | нет | домен удаляется до появления реального adapter mechanism |
| Memory | `Retired-before-mechanism` | не materialize | нет | future memory contour не должен выглядеть активным storage layer |
| MCP | `Retired-before-mechanism` | не materialize | нет | connector domain появится только вместе с реальным controlled mechanism |
| Runtime | `Retired-before-mechanism` | не materialize как домен | временные файлы допустимы только в tool-local ignored paths | runtime-domain удаляется до появления обоснованного execution mechanism |
| Roles | `Retired-before-mechanism` | не materialize | нет | role catalog удаляется до реального role execution mechanism |

## Профильные пакеты
Минимальный product profile должен выбирать только `Core` packages.

Расширенный product profile может добавить:
- `Rules`, если у продукта есть собственные обязательные правила;
- `Templates`, если профиль materialize соответствующие артефакты;
- `Schemas`, если локальный `Tools/*` реально проверяет эти артефакты.

Профиль не может включить `Adapters`, `Memory`, `MCP`, `Runtime` или `Roles` как placeholder. Эти домены возвращаются только после отдельного ADR, владельца механизма, tool support и проверочного договора.

## Модель независимого product Tools
Целевой продукт получает локальный `Tools/*`, а прежние `scripts/*` переносятся в этот домен или становятся тонкими shell aliases к `Tools/*` внутри продукта.

Целевой локальный `Tools/*` продукта обязан:
- запускать structural check продукта без `BYTEPRESS_ROOT`;
- проверять только те schemas и packages, которые есть в профиле;
- хранить deterministic smoke/check reports только в ignored tool-output path;
- не обращаться к `BytePress` после bootstrap как к runtime dependency.

## Early product-start gate и матрица
Переход к профильной фабрике не отменяет first-start gate:
- `Docs/Discovery/Interview.md` стартует в состоянии `Статус_текущей_истины: Не_подтверждена`;
- до явных ответов пользователя продукт остаётся только в аналитическом контуре;
- первое записываемое действие требует рабочую ветку;
- локальные `Tools/*` проверяют этот gate внутри продукта.

## Миграционная граница
В этом pass домены не удаляются и инструменты не переписываются. Целевая матрица требует отдельного refactoring sequence:
1. обновить `bp_bootstrap.py` под profile packages и локальный product `Tools/*`;
2. обновить `bp_lint.py`, чтобы проверять новую модель продукта и сохранить проверку текущего BytePress до удаления доменов;
3. процедуры перенесены в `Pipeline/Workflows.md`;
4. обязательные нормы собраны в сокращённые предметные файлы `Rules/*`;
5. удалить преждевременные домены только после того, как checks перестанут требовать их наличие.

## Граница документа
`Product_Bootstrap_Domain_Matrix.md`:
- не подменяет `Product_Bootstrap_Contract.md` как owner bootstrap obligations;
- не подменяет `Product_Bootstrap_Validation.md` как owner acceptance criteria;
- не подменяет `Docs/Technical/Domain_Model_Migration_Plan.md` как порядок refactoring;
- фиксирует целевую пакетную модель продукта и migration guardrails.
