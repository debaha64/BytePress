# PLAN-000012 — Migrate historical logs

ID: PLAN-000012
Название: Перевести historical logs и прямые ссылки на их ID к 6-значному формату
Статус: Завершено
Связи: BACK-000024, CHG-000021
Источник: Late-phase migration после завершения active non-log ID normalization
Дата_создания: 2026-03-18
Дата_изменения: 2026-03-18
Основание: После нормализации active non-log ID layer historical logs оставались последним legacy-слоем с 4-значными `ADR` и `CHG` и 3-значными `QL ID`.
Связанные_требования:
Связанные_backlog:
- BACK-000024
Связанные_ADR:
- ADR-000015

## Шаги
1. Перевести `Logs/ADRlog.md`, `Logs/ChangeLog.md` и `Logs/QualityLog.md` на 6-значные historical log IDs.
   - DoD: index, section headers, `ID` fields и прямые внутренние журнальные ссылки используют только 6-значный формат `ADR/CHG/QL`.
2. Синхронизировать прямые ссылки на historical log IDs в активных non-log документах.
   - DoD: `Plans/*`, `Docs/Technical/*`, `Docs/Product/*`, `Rules/*`, `Standards/*`, `Adapters/*`, `Tools/README.md` и `Plans/Backlog.md` не ссылаются на старый формат historical log IDs.
3. Не переписывать историю как содержание.
   - DoD: смысл записей, порядок записей, даты и текст history blocks сохранены; orphan requirement и orphan pipeline reference не меняются в рамках этого migration-pass.

## Риски
- механическая замена может затронуть нецелевые идентификаторы вне scope late-phase migration;
- частичная синхронизация ссылок оставит смешение старого и нового формата в активных документах;
- переписывание содержания historical logs разрушит требование на сохранение исторического текста.

## Артефакты
- `Logs/ADRlog.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`
- `Plans/Backlog.md`
- `Plans/Roadmap.md`
- `Plans/Archive/PLAN-000001-foundation.md`
- `Plans/Archive/PLAN-000002-seed-docs-and-standards.md`
- `Plans/Archive/PLAN-000003-fill-technical-and-rules.md`
- `Plans/Archive/PLAN-000004-fill-skills-and-tools.md`
- `Plans/Archive/PLAN-000005-adapters-memory-mcp-and-bootstrap.md`
- `Plans/Archive/PLAN-000006-branch-lifecycle-auto-pr-and-audit-preparation.md`
- `Plans/Archive/PLAN-000007-id-migration-policy-and-phase-plan.md`
- `Plans/Archive/PLAN-000008-schemas-templates-profiles-and-language-sync.md`
- `Plans/Archive/PLAN-000009-migrate-terms-layer.md`
- `Plans/Archive/PLAN-000010-tools-contract-sync.md`
- `Plans/Archive/PLAN-000011-migrate-active-nonlog-ids.md`
- `Plans/Archive/PLAN-000012-migrate-historical-logs.md`
- `Docs/Technical/*.md`
- `Docs/Technical/Product_Bootstrap_Contract.md`
- `Docs/Technical/Product_Bootstrap_Validation.md`
- `Rules/*.md`
- `Standards/*.md`
- `Adapters/*.md`
- `Tools/README.md`

## DoD
Historical logs и прямые ссылки на их ID по активному non-log слою используют только 6-значный формат; содержательная история не переписана, а late-phase migration зафиксирована отдельным планом и фактами в журналах.
