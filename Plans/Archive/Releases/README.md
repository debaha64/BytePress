# Release Archive

`Plans/Archive/Releases/` хранит проверяемый архив release-пакетов `BytePress`.

## Назначение
- отделять release archive от архива завершённых планов и архива этапов;
- хранить release zip как проверяемый исторический пакет архивного plan/backlog;
- связывать manifest с `Logs/ReleaseLog.md`, `Logs/ChangeLog.md`, `Logs/QualityLog.md`, `Plans/Roadmap.md`, `Plans/Backlog.md` и архивными `PLAN-*`;
- готовить post-release очистку без потери проверяемости.

## Manifest
Release manifest описывает проверяемый состав конкретного release archive zip и связывает package с уже подтверждёнными фактами. Шаблон manifest хранится в `Templates/Release_Manifest.md`.

Manifest размещается внутри zip как `MANIFEST.md`. Отдельный внешний `MANIFEST.md` рядом с zip не хранится.

Manifest не заменяет `Logs/ReleaseLog.md`, `Logs/ChangeLog.md`, `Logs/QualityLog.md` и tag. `ReleaseLog` остаётся источником factual release event, `ChangeLog` — фактов изменения, `QualityLog` — фактов проверки, а tag — Git-указателем на выпуск.

## Zip-архивация
Исторические zip-пакеты созданы для выпусков `0.1.0`, `0.2.0` и `0.3.0` в корне release archive:
- `0.1.0.zip`;
- `0.2.0.zip`;
- `0.3.0.zip`.

Zip допустим только как проверяемый исторический release package:
- zip не является текущим source of truth и не заменяет активные `Plans`, `Logs`, `Templates` или Git tag;
- zip содержит только `MANIFEST.md`, `Backlog/<ROAD-файл>` и `Plans/<PLAN-файл>`;
- zip не содержит source tree BytePress: `AGENTS.md`, `Docs/`, `Rules/`, `Pipeline/`, `Tools/`, `Templates/`, `Schemas/` и другие файлы текущего дерева не включаются;
- состав zip должен быть проверен по manifest и списку файлов zip;
- zip не создаётся автоматически release route и не требуется для обычного рабочего прохода.

Состав каждого zip сверяется по списку файлов внутри архива. Zip остаётся историческим пакетом архивного планового контура, а не текущим источником истины.

## Границы
- `Plans/Archive/Plans/` хранит завершённые `PLAN-*.md`.
- `Plans/Archive/Backlog/` хранит завершённые реестры задач этапов.
- `Plans/Archive/Releases/` хранит release zip-пакеты.
- `Templates/Release_Manifest.md` хранит шаблон manifest для release archive zip.
- `Logs/*` остаются источником фактов изменений, проверок, решений, выпуска и поддержки.
