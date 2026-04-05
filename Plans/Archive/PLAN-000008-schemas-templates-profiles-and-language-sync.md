# PLAN-000008 — Schemas, templates, profiles and language contract sync

ID: PLAN-000008
Название: Синхронизировать Schemas, Templates, Profiles и language contract
Статус: Завершено
Связи: BACK-000021, BACK-000022, BACK-000025, ADR-000016, CHG-000017
Источник: Следующая фаза после фиксации repo-wide ID migration policy
Дата_создания: 2026-03-17
Дата_изменения: 2026-03-17
Основание: После фиксации naming migration policy нужно выполнить первый ограниченный migration-pass для `Schemas/*`, `Templates/*` и `Profiles/*`, не заходя в `Tools/*`, `Docs/Terms/TERM-*` и historical logs.
Связанные_требования:
Связанные_backlog:
- BACK-000021
- BACK-000022
- BACK-000025
Связанные_ADR:
- ADR-000016

## Шаги
1. Привести `Schemas/*` к 6-значным ID.
   - DoD: schema-patterns и примеры используют 6-значную числовую часть для внутренних `ID` и ссылок.
2. Привести `Templates/*` к 6-значным ID и согласовать их со схемами.
   - DoD: шаблоны используют `ADR-000001`, `BACK-000001`, `PLAN-000001`, `CHG-000001`, `ROAD-000001`, `PROF-000001`, `TERM-000001` и аналогичные примеры.
3. Синхронизировать profile model и language contract.
   - DoD: `profile.schema.json`, `Templates/Profile.md`, `Profiles/README.md`, `Profiles/Default.md` и `Profiles/Speculorg.md` согласованно описывают `Тип_профиля`, `Код_продукта`, `Язык_взаимодействия` и semantic filename для brand profiles.
4. Зафиксировать language contract для Git/PR артефактов.
   - DoD: `AGENTS.md`, `Standards/Documentation.md` и `Docs/Technical/Platform_Contracts.md` фиксируют английский язык для commit/PR artifacts и English `kebab-case` для `branch slug`.
5. Обновить плановый и журнальный контуры.
   - DoD: `Plans/Backlog.md`, `Logs/ADRlog.md`, `Logs/ChangeLog.md` и `Logs/QualityLog.md` отражают только факты этого прохода.

## Риски
- преждевременное обновление `Tools/*` смешает schema/template/profile pass с инструментальным;
- language contract может быть ошибочно принят как требование к user-facing ответам вместо Git/PR-артефактов;
- profile model может начать дрейфовать между `README`, schema и реальными brand profile файлами.

## Артефакты
- `Standards/Naming.md`
- `Standards/Documentation.md`
- `Docs/Technical/Model.md`
- `Docs/Technical/Platform_Contracts.md`
- `AGENTS.md`
- `Schemas/README.md`
- `Schemas/*.json`
- `Templates/README.md`
- `Templates/*.md`
- `Profiles/README.md`
- `Profiles/Default.md`
- `Profiles/Speculorg.md`
- `Plans/Backlog.md`
- `Plans/BP-000008-schemas-templates-profiles-and-language-sync.md`
- `Logs/ADRlog.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`

## DoD
`Schemas/*`, `Templates/*` и `Profiles/*` синхронизированы с 6-значным ID contract и language contract, при этом `Tools/*`, `Docs/Terms/TERM-*`, historical logs и semver остаются вне scope текущего прохода.
