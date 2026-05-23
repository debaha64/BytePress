# Release Archive

`Plans/Archive/Releases/` хранит проверяемый архив release-пакетов `BytePress`.

## Назначение
- отделять release archive от архива завершённых планов и архива этапов;
- хранить release manifest как проверяемое описание состава выпуска;
- связывать manifest с `Logs/ReleaseLog.md`, `Logs/ChangeLog.md`, `Logs/QualityLog.md`, `Plans/Roadmap.md`, `Plans/Backlog.md` и архивными `PLAN-*`;
- готовить post-release очистку без потери проверяемости.

## Manifest
Release manifest описывает проверяемый состав конкретного выпуска и связывает release package с уже подтверждёнными фактами.

Обязательный состав manifest:
- версия выпуска;
- tag выпуска и тип tag, если тип проверялся;
- release commit, на который указывает tag или фактический release route;
- release PR в `main`;
- post-release sync PR в `develop`, если он выполнялся;
- связанные `ROAD/BACK/PLAN`;
- связанные записи `CHG`, `QL` и `RL`;
- выполненные проверки и их команды;
- непроверенные зоны и ограничения среды;
- состав release package: включённые owner-documents, tools, schemas, templates и явные исключения;
- решение по zip: `не создавался`, `создан как исторический пакет` или `запрещён до отдельного решения владельца`;
- проверка состава release package и, если zip создан, проверка состава zip.

Manifest не заменяет `Logs/ReleaseLog.md`, `Logs/ChangeLog.md`, `Logs/QualityLog.md` и tag. `ReleaseLog` остаётся источником factual release event, `ChangeLog` — фактов изменения, `QualityLog` — фактов проверки, а tag — Git-указателем на выпуск. Manifest не является журналом фактов, не закрывает release gate сам по себе и не становится текущим источником истины вместо активных owner-documents. Он служит проверяемым мостом между плановым контуром, журналами, Git-фактами и release package.

Manifest для исторического выпуска допустимо создавать только после сверки с соответствующими `RL`, `CHG`, `QL`, архивными `ROAD/BACK/PLAN`, tag и commit. Если release PR или post-release sync PR отсутствует у раннего выпуска, manifest обязан явно указать отсутствие такого факта как непроверенную или неприменимую зону, а не выводить его догадкой.

## Zip-архивация
Исторические zip-пакеты созданы для выпусков `0.1.0`, `0.2.0` и `0.3.0` внутри соответствующих каталогов release archive.

Zip допустим только как проверяемый исторический release package:
- zip не является текущим source of truth и не заменяет активные `Docs`, `Rules`, `Pipeline`, `Logs`, `Templates`, `Schemas`, `Tools` или Git tag;
- zip должен иметь release manifest;
- состав zip должен быть проверен по manifest;
- manifest должен фиксировать команду или способ проверки состава;
- крупные бинарные архивы не добавляются в репозиторий без отдельного решения владельца;
- zip не создаётся автоматически release route и не требуется для обычного рабочего прохода.

Состав каждого zip сверяется с соответствующим tag и фиксируется в manifest выпуска. Zip остаётся историческим пакетом, а не текущим источником истины.

## Границы
- `Plans/Archive/Plans/` хранит завершённые `PLAN-*.md`.
- `Plans/Archive/Backlog/` хранит завершённые реестры задач этапов.
- `Plans/Archive/Releases/` хранит release manifest, manifest template и будущие release package references.
- `Logs/*` остаются источником фактов изменений, проверок, решений, выпуска и поддержки.
