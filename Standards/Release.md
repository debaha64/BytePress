# Release

ID: STD-000004
Название: Release
Статус: Активно
Связи: RULE-000002, RULE-000003, RULE-000004, TERM-000009
Источник: BytePress + полезные практики Speculorg
Дата_создания: 2026-03-09
Дата_изменения: 2026-04-15

## Назначение
Единообразие выпуска, передачи и сопровождения без скрытого контекста.

## Обязательные_требования
- В `ChangeLog` фиксируются только значимые утверждённые изменения.
- Архитектурно значимые решения фиксируются в `ADRlog`.
- Выпуск опирается на подтверждённые результаты проверки и обновлённые журналы.
- Передача и поддержка опираются на явные документы и журналы, а не на память участника.
- Источник изменения в журнале указывается через связанный `Plan`, `Backlog` или другой утверждённый артефакт.
- `release/*` создаётся только после того, как `develop` признан release candidate для текущего semver baseline.
- В `release/*` допустимы только stabilizing fixes, release-readiness правки и явная синхронизация журналов.
- Release-переход выполняется как `release/* -> main -> tag`.
- Перед merge release-ветки в `main` повторно выполняются финальные validation checks текущего release candidate.
- Tag создаётся и отправляется только после подтверждённого merge release-ветки в `main`.
- После merge/tag release-ветка удаляется, а `develop` синхронизируется от подтверждённого `main` через отдельную task-ветку и PR, если release принёс release-only fixes.
- Если в `release/*` появились release-only fixes, они должны быть возвращены в `develop`.
- `ReleaseLog.md` хранит только factual release events, подтверждённые tag/history; candidate, прогноз или намерение не считаются release log fact.
- Если factual release logging невозможен до merge/tag, канон обязан явно требовать отдельный post-release sync-pass для closure `ReleaseLog.md`.

## Критерии_соблюдения
- У значимого изменения есть запись в `ChangeLog`.
- У архитектурного решения есть запись в `ADRlog`.
- Выпуск не пропускает журнальный контур.
- Поддержка использует `SupportLog`, а не неформальные заметки.
- Release branch создаётся только после закрытия blocker-рисков для целевого baseline.
- В `release/*` отсутствует feature-work.
- Перед merge в `main` финальные release checks повторно пройдены.
- После merge в `main` tag создан и отправлен, release-ветка удаляется.
- После release `develop` синхронизирован от `main` без прямой feature-work в `release/*`.
- factual release event закрыт в `ReleaseLog.md` либо явно назначен в отдельный post-release sync-pass.

## Связанные_правила
- RULE-000002
- RULE-000003
- RULE-000004
