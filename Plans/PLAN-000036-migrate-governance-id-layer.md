# PLAN-000036 — Migrate governance ID layer

ID: PLAN-000036
Название: Привести `Rules/*`, `Standards/*`, `Templates/*` и `Schemas/*` к unified `ID scheme`
Статус: Завершено
Связи: BACK-000048
Источник: Narrow governance/supporting migration pass inside `ROAD-000009`
Дата_создания: 2026-04-06
Дата_изменения: 2026-04-06
Основание: Planning-contour и log-layer уже синхронизированы с unified `ID scheme`, но active governance/supporting domains всё ещё расходятся по фактической модели идентификации: часть active standards не имеет явных `STD-*`, а `Templates/*` и `Schemas/*` не несут устойчивый внутренний artifact-level `ID`, хотя naming-contract уже относит их к hybrid domains. Нужен отдельный pass, который доведёт `Rules/*`, `Standards/*`, `Templates/*` и `Schemas/*` до уже утверждённого contract без redesign остальных доменов.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000048
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать scope governance/supporting migration pass внутри `ROAD-000009`.
   - Описание: Добавить одну реальную backlog-задачу и один новый текущий `Plan` только для migration `ID` и ссылочного слоя `Rules/*`, `Standards/*`, `Templates/*`, `Schemas/*`.
   - DoD: `BACK-000048` и `PLAN-000036` описывают только этот domain-scoped migration без открытия других доменов.
2. Определить минимальную migration model для целевых доменов.
   - Описание: Оставить singleton domains singleton-артефактами, а hybrid domains довести до обязательного внутреннего `ID` без искусственной сериализации filename.
   - DoD: для каждого затронутого домена явно определено, где `ID` живёт и что реально требует изменения.
3. Применить migration к active artifacts и прямым зависимостям.
   - Описание: Обновить только реально несогласованные `Rules/*`, `Standards/*`, `Templates/*`, `Schemas/*` и синхронизировать только те path/reference места, которые реально ломаются или противоречат migrated contract.
   - DoD: active governance/supporting layer не содержит broken path-references и не спорит с unified `ID scheme`.
4. Синхронизировать минимально необходимые contracts и tooling.
   - Описание: Обновить `Standards/Naming.md`, а также только реально затронутые active docs, `bp_bootstrap.py` и `bp_lint.py`, если path-contract или contract checks этого требуют.
   - DoD: active-layer contracts и инструменты описывают фактически реализованное состояние migrated domains без лишнего redesign.
5. Подтвердить hard-close pass.
   - Описание: Провести финальную governance-сверку, закрыть backlog-задачу и перевести `Plan` в финальный статус только после согласования статусов, ссылок и обязательных проверок.
   - DoD: `BACK-000048`, индекс backlog, `ROAD-000009`, текущий `Plan` и локальные проверки согласованы.

## Ограничения
- без migration `ID` для `Docs/Product/*`, `Docs/Discovery/*`, `Docs/Technical/*`, `Docs/User/*`, `Roles/*`, `Profiles/*`, `Adapters/*`, `Memory/*`, `Pipeline/*`, `MCP/*` и остальных доменов;
- без изменения active/archive layout для `Plans` и backlog archive-layer;
- без широкого переписывания `Docs/Technical/*`, `AGENTS.md` и `Docs/User/*`;
- без создания новой модели `ID` сверх уже утверждённой unified `ID scheme`.

## Риски
- если не различить singleton и hybrid domains по фактическому contract, migration либо останется декларативной, либо начнёт искусственно сериализовать semantic filenames;
- если добавить artifact-level `ID` в шаблоны и схемы без согласования domain-native формы, supporting layer останется двусмысленным для ссылок и проверок;
- если не обновить только реально затронутые references и tools, репозиторий сохранит скрытые противоречия между naming-contract и фактическим состоянием active domains.

## Артефакты
- `Plans/Backlog.md`
- `Plans/Roadmap.md`
- `Plans/PLAN-000036-migrate-governance-id-layer.md`
- `Rules/*`
- `Standards/*`
- `Templates/*`
- `Schemas/*`
- `Tools/bp_bootstrap.py`
- `Tools/bp_lint.py`

## DoD
- создана одна узкая backlog-задача только для migration active governance/supporting domains.
- создан новый текущий `Plan` только под этот pass.
- `Rules/*`, `Standards/*`, `Templates/*`, `Schemas/*` приведены к unified `ID scheme` в реально необходимом объёме.
- все реально затронутые ссылки на migrated domains синхронизированы.
- `python3 Tools/bp_lint.py --repo .` проходит.

## Фактический результат
- `BACK-000048` и `PLAN-000036` зафиксировали только узкий pass по active governance/supporting domains без открытия других доменов.
- `Rules/*` подтвердили singleton contract без filename-migration; `Standards/Naming.md`, `Standards/Quality.md` и `Standards/Traceability.md` доведены до явных `STD-*`.
- `Templates/*` приведены к hybrid artifact-ID contract через внутренние `TPL-*` markers, а `Schemas/*` — через top-level `SCH-*` в `$id`, при сохранении semantic filenames.
- `Plans/Archive/PLAN-000035-migrate-log-id-layer.md` выведен в archive, поэтому active `Plans/` снова содержит только singleton files и текущий `PLAN-000036`.
- `bp_bootstrap.py` не менялся, потому что filename/path-contract bootstrap не затронут; `bp_lint.py` минимально расширен под новые обязательные IDs active governance/supporting layer.
