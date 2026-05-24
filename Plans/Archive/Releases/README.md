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

Release archive распределяет исторический плановый слой по подтверждённым ID-интервалам:
- `0.1.0.zip`: `ROAD-000001` ... `ROAD-000015`, `PLAN-000001` ... `PLAN-000067`;
- `0.2.0.zip`: `ROAD-000016`, `PLAN-000068`;
- `0.3.0.zip`: `ROAD-000017` ... `ROAD-000042`, `PLAN-000069` ... `PLAN-000096`.

Zip допустим только как проверяемый исторический release package:
- zip не является текущим source of truth и не заменяет активные `Plans`, `Logs`, `Templates` или Git tag;
- zip содержит только `MANIFEST.md`, `Backlog/<ROAD-файлы>` и `Plans/<PLAN-файлы>`;
- zip не содержит source tree BytePress: `AGENTS.md`, `Docs/`, `Rules/`, `Pipeline/`, `Tools/`, `Templates/`, `Schemas/` и другие файлы текущего дерева не включаются;
- состав zip должен быть проверен по manifest и списку файлов zip;
- zip не создаётся автоматически release route и не требуется для обычного рабочего прохода.

Состав каждого zip сверяется по списку файлов внутри архива. Zip остаётся историческим пакетом архивного планового контура, а не текущим источником истины.

После упаковки исторических интервалов открытые архивные каталоги хранят только текущий релизный цикл `0.4.0`: `Plans/Archive/Backlog/ROAD-000043.md` и далее, `Plans/Archive/Plans/PLAN-000097-*.md` и далее.

## Границы
- `Plans/Archive/Plans/` хранит завершённые `PLAN-*.md`.
- `Plans/Archive/Backlog/` хранит завершённые реестры задач этапов.
- `Plans/Archive/Releases/` хранит release zip-пакеты.
- `Templates/Release_Manifest.md` хранит шаблон manifest для release archive zip.
- `Logs/*` остаются источником фактов изменений, проверок, решений, выпуска и поддержки.
