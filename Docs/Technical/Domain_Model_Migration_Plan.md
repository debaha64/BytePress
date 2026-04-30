# Domain Model Migration Plan

## Назначение
`Docs/Technical/Domain_Model_Migration_Plan.md` фиксирует безопасный план перехода от разросшейся доменной модели `BytePress` к профильной фабрике самодостаточных продуктовых каркасов.

Этот document фиксирует план и итог прохода сокращения доменной модели. Удаление выполнено только после переноса смысла, обновления contracts, tools и checks.

## Целевое состояние BytePress
`BytePress` становится фабрикой профилей продукта.

Целевые домены фабрики:
- `AGENTS.md`, `README.md`, `Setup_Guide.md` — входные карты человека и агента;
- `Docs/*` — knowledge, product, user, terms и сокращённые technical contracts фабрики;
- `Pipeline/*` — process model и workflows;
- `Plans/*` — planning contour самой фабрики;
- `Logs/*` — factual closure, ADR и quality evidence фабрики;
- `Rules/*` — короткий набор обязательных проектно-специфичных правил;
- `Schemas/*` — схемы только для проверяемых фабрикой артефактов;
- `Templates/*` — шаблоны только для артефактов, которые фабрика реально materialize;
- `Tools/*` — генерация профильных каркасов и проверка самой фабрики.

Retired domains зафиксированы как неактивные: бывшие extension, execution, role, procedure и standards layers не возвращаются до появления реального механизма, владельца смысла, потребителя и проверки.

Статус на 2026-04-30: retired domains удалены из active layer. Рабочие процедуры живут в `Pipeline/Workflows.md`. Обязательные нормы выбора зависимостей, PR-маршрута, смысловых коммитов и semantic naming живут в `Rules/*`.

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

Продукт не получает retired domains в baseline.

## Что удалено
- бывшие extension domains — active mechanism отсутствовал.
- ignored tool-output paths — временные outputs перенесены в ignored tool-output paths продукта.
- бывший role catalog — role execution mechanism отсутствовал, profiles очищены от ссылок.
- бывший procedural domain — процедуры перенесены в `Pipeline/Workflows.md`.
- бывший standards layer — обязательные нормы перенесены в `Rules/*`.

## Что перенести
- Рабочие процедуры перенесены в `Pipeline/Workflows.md`.
- Обязательные нормы перенесены в `Rules/Dependencies.md`, `Rules/Git.md`, `Rules/Domains.md`, `Rules/Workflow.md`, `Rules/Logs.md`, `Rules/Terms.md`, `Rules/Security.md`, `Rules/Source.md` и `Rules/Naming.md`. Рекомендательные формулировки не перенесены.
- Generated `scripts/*` перенести в product-local `Tools/*`; shell scripts оставить только как optional aliases, если профиль требует shell entrypoints.
- Runtime smoke reports перенесены из прежнего `Runtime/*` в ignored path продукта, принадлежащий `Tools/*`.

## Что объединить
- Повторяющиеся документы проверки, подтверждения результата и доказательств объединить в сокращённый technical verification contract.
- `Docs/Technical/Pipeline.md` оставить только как краткий technical pointer или удалить после усиления `Pipeline/README.md`.
- Product bootstrap contract и profile package matrix синхронизировать так, чтобы contract описывал artifact obligations, а matrix — package composition.
- `Rules/*` сократить до проектно-специфичных обязательных правил; meta-rules оставить только если они реально проверяются или нужны агентному gate.

## Какие проверки обновить
- `Tools/bp_lint.py` больше не требует retired domains в самом `BytePress`.
- Product checks должны перейти с `scripts/*` и `BYTEPRESS_ROOT` на local product `Tools/*`.
- Bootstrap checks должны проверять profile packages: `Core`, selected `Rules`, selected `Templates`, selected `Schemas`.
- Negative checks должны падать на retired placeholder domains в создаваемом продукте.
- Repo checks должны перестать требовать retired domains только в том pass, где удаляются соответствующие files.

## Риски
- Одновременное удаление доменов и изменение tools может сломать lint без ясного replacement contract.
- Перенос `scripts/*` в product `Tools/*` меняет operational model уже созданных продуктов и требует отдельного service update route.
- Сокращение `Rules/*` может потерять полезные нормы, если не отделить обязательное от рекомендательного.
- Перенос процедур в `Pipeline/*` может раздуть process-domain, если workflows станут вторым technical-layer.
- Локальные product tools могут начать расходиться между продуктами без profile versioning.
- Сокращение `Docs/Technical/*` может удалить owner-documents, на которые ещё ссылаются `Plans`, `Logs`, `Tools` или generated docs.

## Последовательность passes
1. Зафиксировать ADR, target matrix и этот migration plan без удаления доменов.
2. Добавить profile package contract и версионирование product profiles.
3. Обновить `bp_bootstrap.py` для генерации local product `Tools/*`, lightweight `Pipeline/*`, profile-bound `Templates/*` и `Schemas/*`. Статус: начато в `PLAN-000080`.
4. Обновить `bp_lint.py` под transitional checks. Статус: начато в `PLAN-000080`.
5. Перенести procedures в `Pipeline/*`. Статус: выполнено в `PLAN-000082`.
6. Перенести обязательные norms в предметные файлы `Rules/*` и сократить ruleset. Статус: выполнено в `PLAN-000084`.
7. Удалить retired domains после прохождения updated checks. Статус: выполнено в `PLAN-000082`.
8. Сократить `Docs/Technical/*` и убрать повторяющиеся проверочные документы. Статус: выполнено в `PLAN-000085`.

## Граница документа
Этот план не является разрешением на массовое удаление файлов. Удаление каждого домена требует отдельного pass, updated checks и фактического log closure.
