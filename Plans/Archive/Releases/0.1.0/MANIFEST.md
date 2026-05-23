# Release Manifest 0.1.0

ID: RELEASE-MANIFEST-0.1.0
Версия: 0.1.0
Статус: Проверено
Дата_создания: 2026-05-24
Дата_изменения: 2026-05-24

## Git-факты
- Tag: `0.1.0`
- Тип_tag: `commit`
- Release_commit: `92891482e9bc88940069700ba93890fb317b5cab`
- Release_PR: `PR #20`
- Post_release_sync_PR: `не подтверждено`

## Плановый контур
- ROAD: `ROAD-000015`
- BACK: `BACK-000079`
- PLAN: `PLAN-000067`

## Журнальный контур
- ReleaseLog: `RL-000006`
- ChangeLog: `CHG-000079`
- QualityLog: `QL-000074`
- Manifest_creation: `CHG-000126`, `QL-000121`

## Проверки
- Выполненные_проверки:
  - `git cat-file -t 0.1.0`
  - `git rev-list -n 1 0.1.0`
  - `git show -s --format='%H%n%s%n%b' 92891482e9bc88940069700ba93890fb317b5cab`
  - `git ls-tree -d --name-only 0.1.0`
  - сверка `Logs/ReleaseLog.md`, `Logs/ChangeLog.md`, `Logs/QualityLog.md`, `Plans/Archive/Backlog/ROAD-000015.md` и `Plans/Archive/Plans/PLAN-000067-release-readiness-and-log-closure.md`
- Непроверенные_зоны:
  - post-release sync PR для `0.1.0` не подтверждён найденными источниками
  - отдельный zip-пакет выпуска не создавался и не проверялся

## Состав release package
- Включено:
  - `.editorconfig`, `.gitattributes`, `.gitignore`, `AGENTS.md`, `README.md`, `Setup_Guide.md`
  - `Adapters/`, `Docs/`, `Logs/`, `MCP/`, `Memory/`, `Pipeline/`, `Plans/`, `Profiles/`, `Roles/`, `Rules/`, `Runtime/`, `Schemas/`, `Skills/`, `Standards/`, `Templates/`, `Tools/`
- Исключено:
  - `не подтверждено`
- Проверка_состава:
  - `git ls-tree -d --name-only 0.1.0`
  - `git ls-tree -r --name-only 0.1.0`

## Zip
- Решение: `не создавался`
- Путь: `неприменимо`
- Проверка_состава_zip: `неприменимо`
- Решение_владельца_для_крупного_бинарного_архива: `неприменимо`

## Границы
Manifest не заменяет `Logs/ReleaseLog.md`, `Logs/ChangeLog.md`, `Logs/QualityLog.md` и tag. Zip, если он будет создан отдельным будущим решением, является только проверяемым историческим пакетом и не становится текущим источником истины.
