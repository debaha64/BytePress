# PLAN-000011 — Migrate active non-log IDs

ID: PLAN-000011
Название: Перевести активные non-log internal ID и прямые ссылки на 6-значный формат
Статус: Завершено
Связи: BACK-000019, CHG-000020
Источник: Следующая фаза repo-wide migration после sync-проходов по plans, terms и tools
Дата_создания: 2026-03-18
Дата_изменения: 2026-03-18
Основание: После миграции `Plans/`, `Terms/`, `Schemas/`, `Templates/` и tool contract остаётся активный слой singleton- и registry-доменов, который всё ещё смешивает 4- и 6-значные internal ID.
Связанные_требования:
- PROF-000001
- ROAD-000001
- BACK-000019
Связанные_backlog:
- BACK-000019
Связанные_ADR:
- ADR-000015
- ADR-000016

## Шаги
1. Перевести active non-log ID в singleton- и registry-доменах на 6-значный формат.
   - DoD: `Profiles/`, `Rules/`, `Standards/`, `Roles/`, `Skills/`, `Adapters/`, `Memory/` и `MCP/` используют 6-значные internal ID без переименования singleton filenames.
2. Синхронизировать прямые ссылки в плановом и техническом слоях.
   - DoD: `Plans/Backlog.md`, `Plans/Roadmap.md`, `Plans/BP-*`, `Docs/Technical/*` и `Docs/Product/Bootstrap_Contract.md` больше не ссылаются на 4-значные active non-log ID.
3. Не затрагивать historical logs и инструментальный код.
   - DoD: `Logs/ADRlog.md`, существующие sections `Logs/ChangeLog.md` и `Logs/QualityLog.md`, `Schemas/*`, `Templates/*`, `Docs/Terms/*` и `Tools/*.py` остаются вне rewrite-pass, кроме новых фактических записей текущего прохода.

## Риски
- частичная миграция active ID оставит смешение 4- и 6-значного формата в связях между singleton-доменами и plan layer;
- переписывание historical logs в этом проходе смешает активную миграцию с поздней исторической фазой;
- случайное изменение `Tools/*.py`, `Schemas/*`, `Templates/*` или `Docs/Terms/*` выведет проход за утверждённый scope.

## Артефакты
- `Profiles/*.md`
- `Rules/*.md`
- `Standards/*.md`
- `Roles/*.md`
- `Skills/*.md`
- `Adapters/*`
- `Memory/Registry.md`
- `MCP/Registry.md`
- `Plans/Backlog.md`
- `Plans/Roadmap.md`
- `Plans/BP-000001-foundation.md`
- `Plans/BP-000002-seed-docs-and-standards.md`
- `Plans/BP-000003-fill-technical-and-rules.md`
- `Plans/BP-000004-fill-skills-and-tools.md`
- `Plans/BP-000005-adapters-memory-mcp-and-bootstrap.md`
- `Plans/BP-000006-branch-lifecycle-auto-pr-and-audit-preparation.md`
- `Plans/BP-000011-migrate-active-nonlog-ids.md`
- `Docs/Technical/*.md`
- `Docs/Product/Bootstrap_Contract.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`

## DoD
Активный non-log слой BytePress использует только 6-значные internal ID для `Backlog`, `Roadmap`, brand profiles, rules, standards, roles, skills, adapters, memory и MCP; прямые ссылки в активных non-log артефактах синхронизированы, а historical logs не переписаны.
