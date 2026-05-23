# Release Manifest 0.3.0

ID: RELEASE-MANIFEST-0.3.0
Версия: 0.3.0
Статус: Проверено
Дата_создания: 2026-05-24
Дата_изменения: 2026-05-24

## Git-факты
- Tag: `0.3.0`
- Тип_tag: `commit`
- Release_commit: `56767aaa8208ebfb125afd00ac0b6d57e0fa0a98`
- Release_PR: `PR #108`
- Post_release_sync_PR: `PR #109`

## Плановый контур
- ROAD: `ROAD-000042`
- BACK: `BACK-000107`
- PLAN: `PLAN-000096`

## Журнальный контур
- ReleaseLog: `RL-000009`
- ChangeLog: `CHG-000108`
- QualityLog: `QL-000103`
- Manifest_creation: `CHG-000126`, `QL-000121`

## Проверки
- Выполненные_проверки:
  - `git cat-file -t 0.3.0`
  - `git rev-list -n 1 0.3.0`
  - `git show -s --format='%H%n%s%n%b' 56767aaa8208ebfb125afd00ac0b6d57e0fa0a98`
  - `git ls-tree -d --name-only 0.3.0`
  - `git archive --format=zip --output=Plans/Archive/Releases/0.3.0/BytePress-0.3.0.zip 0.3.0`
  - `python3 -m zipfile -t Plans/Archive/Releases/0.3.0/BytePress-0.3.0.zip`
  - сверка списка файлов zip со списком `git ls-tree -r --name-only 0.3.0`: `OK`, `git_files 258`, `zip_files 258`, `missing 0`, `extra 0`
  - сверка `Logs/ReleaseLog.md`, `Logs/ChangeLog.md`, `Logs/QualityLog.md`, `Plans/Archive/Backlog/ROAD-000042.md` и `Plans/Archive/Plans/PLAN-000096-post-release-0-3-0-factual-log-and-release-route.md`
- Непроверенные_зоны:
  - нет

## Состав release package
- Включено:
  - `.editorconfig`, `.gitattributes`, `.gitignore`, `AGENTS.md`, `README.md`, `Setup_Guide.md`
  - `Docs/`, `Logs/`, `Pipeline/`, `Plans/`, `Profiles/`, `Rules/`, `Schemas/`, `Templates/`, `Tools/`
- Исключено:
  - `не подтверждено`
- Проверка_состава:
  - `git ls-tree -d --name-only 0.3.0`
  - `git ls-tree -r --name-only 0.3.0`

## Zip
- Решение: `создан как исторический пакет`
- Путь: `Plans/Archive/Releases/0.3.0/BytePress-0.3.0.zip`
- Размер_байт: `510585`
- Проверка_состава_zip: `python3 -m zipfile -t Plans/Archive/Releases/0.3.0/BytePress-0.3.0.zip`; сверка списка файлов zip со списком `git ls-tree -r --name-only 0.3.0`: `OK`, `git_files 258`, `zip_files 258`, `missing 0`, `extra 0`
- Решение_владельца_для_крупного_бинарного_архива: `неприменимо`

## Границы
Manifest не заменяет `Logs/ReleaseLog.md`, `Logs/ChangeLog.md`, `Logs/QualityLog.md` и tag. Zip является только проверяемым историческим пакетом и не становится текущим источником истины.
