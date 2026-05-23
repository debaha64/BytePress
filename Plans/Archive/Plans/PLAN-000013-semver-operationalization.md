# PLAN-000013 — Semver operationalization

ID: PLAN-000013
Название: Операционализировать semver в активных non-log документах BytePress
Статус: Завершено
Связи: BACK-000019, CHG-000022
Источник: Следующий проход после late-phase migration historical logs
Дата_создания: 2026-03-18
Дата_изменения: 2026-03-18
Основание: После нормализации ID и historical logs текущий operational baseline `BytePress` всё ещё обозначался как `v1` в активных non-log документах, что размывало связь между состоянием системы и semver contract.
Связанные_требования:
Связанные_backlog:
- BACK-000019
Связанные_ADR:
- ADR-000014
- ADR-000015

## Шаги
1. Зафиксировать semver baseline в контрактном слое.
   - DoD: `Standards/Naming.md` и `Docs/Technical/Platform_Contracts.md` явно фиксируют `0.1.0` как current operational baseline и правило использования semver вместо `vN`.
2. Синхронизировать active non-log документы.
   - DoD: `Docs/Technical/*`, `Docs/Product/*`, `Adapters/*`, `Memory/*`, `MCP/*`, `Pipeline/*`, `Plans/Backlog.md`, `Plans/Roadmap.md`, релевантные `Plans/BP-*`, `Tools/README.md`, `Rules/README.md`, `Standards/README.md` и `Skills/README.md` используют `0.1.0` там, где раньше `v1` обозначал текущий baseline.
3. Не переписывать историю и не трогать вне-scope артефакты.
   - DoD: `Logs/*`, orphan requirement и orphan pipeline reference, `Schemas/*`, `Templates/*` и `Tools/*.py` остаются вне содержательного rewrite.

## Риски
- механическая замена `v1` может затронуть текст, где semver не является operational label;
- частичная синхронизация оставит смешение `v1` и `0.1.0` в активном non-log слое;
- попытка затронуть historical logs или release automation выведет проход за утверждённый scope.

## Артефакты
- `Standards/Naming.md`
- `Docs/Technical/*.md`
- `Docs/Product/*.md`
- `Adapters/*.md`
- `Adapters/*/README.md`
- `Memory/*.md`
- `MCP/*.md`
- `Pipeline/*.md`
- `Plans/Backlog.md`
- `Plans/Roadmap.md`
- `Plans/Archive/Plans/PLAN-000003-fill-technical-and-rules.md`
- `Plans/Archive/Plans/PLAN-000004-fill-skills-and-tools.md`
- `Plans/Archive/Plans/PLAN-000005-adapters-memory-mcp-and-bootstrap.md`
- `Plans/Archive/Plans/PLAN-000013-semver-operationalization.md`
- `Tools/README.md`
- `Rules/README.md`
- `Standards/README.md`
- `Skills/README.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`

## DoD
Текущий operational contract `BytePress` маркируется baseline-version `0.1.0`, активные non-log документы используют semver вместо `v1`, а historical logs и вне-scope артефакты остаются без содержательных изменений.
