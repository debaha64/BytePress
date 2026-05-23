# Release Archive

`Plans/Archive/Releases/` хранит проверяемый архив release-пакетов `BytePress`.

## Назначение
- отделять release archive от архива завершённых планов и архива этапов;
- хранить release manifest как проверяемое описание состава выпуска;
- связывать manifest с `Logs/ReleaseLog.md`, `Logs/ChangeLog.md`, `Logs/QualityLog.md`, `Plans/Roadmap.md`, `Plans/Backlog.md` и архивными `PLAN-*`;
- готовить post-release очистку без потери проверяемости.

## Manifest
Release manifest описывает состав конкретного выпуска:
- версия выпуска;
- commit или tag выпуска после подтверждения release route;
- связанные `ROAD/BACK/PLAN`;
- связанные `CHG/QL` и запись `ReleaseLog`;
- список включённых owner-documents и инструментальных проверок;
- явные исключения, непроверенные зоны и post-release действия.

Manifest не заменяет `Logs/ReleaseLog.md`, не является журналом фактов и не закрывает release gate сам по себе. Он служит проверяемым мостом между плановым контуром, журналами и будущим release package.

## Zip-архивация
Zip-файлы в текущем проходе не создаются. Если zip-архивация потребуется для post-release очистки, она должна быть отдельным следующим шагом внутри `ROAD-000047` с явным manifest-договором: что упаковывается, как проверяется состав, как связаны manifest, logs, tag и архивный пакет.

## Границы
- `Plans/Archive/Plans/` хранит завершённые `PLAN-*.md`.
- `Plans/Archive/Backlog/` хранит завершённые реестры задач этапов.
- `Plans/Archive/Releases/` хранит release manifest и будущие release package references.
- `Logs/*` остаются источником фактов изменений, проверок, решений, выпуска и поддержки.
