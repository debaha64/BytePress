# PLAN-000007 — ID migration policy and phase plan

ID: PLAN-000007
Название: Зафиксировать repo-wide policy фазной миграции ID и именования
Статус: Завершено
Связи: BACK-000021, BACK-000022, BACK-000023, BACK-000024, ADR-000015, CHG-000016
Источник: Следующий проход после нормализации current plan layer
Дата_создания: 2026-03-17
Дата_изменения: 2026-03-17
Основание: После нормализации `Plans/` нужно зафиксировать repo-wide policy, которая определяет порядок фазной миграции remaining legacy-layer без запуска массового rewrite в этом проходе.
Связанные_требования:
Связанные_backlog:
- BACK-000021
- BACK-000022
- BACK-000023
- BACK-000024
Связанные_ADR:
- ADR-000015

## Шаги
1. Зафиксировать repo-wide policy фазной миграции ID и именования.
   - DoD: `Standards/Naming.md` различает серийные, гибридные и singleton-домены и задаёт фазный порядок миграции.
2. Уточнить модель доменов для `Terms/` и `Profiles/`.
   - DoD: `Docs/Technical/Model.md`, `Docs/Terms/README.md` и `Profiles/README.md` согласованно описывают hybrid- и serial-правила.
3. Подготовить плановый контур следующих миграционных фаз.
   - DoD: в `Plans/Backlog.md` есть явные backlog items для `Schemas/*`, `Templates/*`, `Tools/*`, `Docs/Terms/*` и поздней миграции historical logs.
4. Зафиксировать решение и факт прохода в журналах.
   - DoD: `ADRlog`, `ChangeLog` и `QualityLog` отражают только policy-решения и результаты текущего прохода.

## Риски
- преждевременная массовая миграция смешает policy-pass с rewrite-pass;
- historical logs могут быть переписаны слишком рано и усложнить трассировку перехода;
- гибридные домены могут быть ошибочно переведены на ID в filenames.

## Артефакты
- `Standards/Naming.md`
- `Docs/Technical/Model.md`
- `Docs/Terms/README.md`
- `Profiles/README.md`
- `Plans/Backlog.md`
- `Plans/Archive/PLAN-000007-id-migration-policy-and-phase-plan.md`
- `Logs/ADRlog.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`

## DoD
Repo-wide policy фазной миграции ID и именования зафиксирована без запуска массовой миграции, а backlog и журналы подготовлены к следующим управляемым фазам.
