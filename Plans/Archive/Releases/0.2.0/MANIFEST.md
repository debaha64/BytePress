# Release Manifest 0.2.0

ID: RELEASE-MANIFEST-0.2.0
Версия: 0.2.0
Статус: Проверено
Дата_создания: 2026-05-24
Дата_изменения: 2026-05-24

## Git-факты
- Tag: `0.2.0`
- Тип_tag: `tag`
- Release_commit: `68824d0646fc3e68992bbd1d6a3e6b7f5dcf3b83`
- Release_PR: `PR #77`
- Post_release_sync_PR: `PR #78`

## Плановый контур
- ROAD: `ROAD-000016`
- BACK: `BACK-000080`
- PLAN: `PLAN-000068`

## Журнальный контур
- ReleaseLog: `RL-000007`
- ChangeLog: `CHG-000080`
- QualityLog: `QL-000075`
- Manifest_creation: `CHG-000126`, `QL-000121`

## Проверки
- Выполненные_проверки:
  - `git cat-file -t 0.2.0`
  - `git rev-list -n 1 0.2.0`
  - `git show -s --format='%H%n%s%n%b' 68824d0646fc3e68992bbd1d6a3e6b7f5dcf3b83`
  - `git ls-tree -d --name-only 0.2.0`
  - сверка `Logs/ReleaseLog.md`, `Logs/ChangeLog.md`, `Logs/QualityLog.md`, `Plans/Archive/Backlog/ROAD-000016.md` и `Plans/Archive/Plans/PLAN-000068-sync-develop-after-release-0.2.0.md`
- Непроверенные_зоны:
  - отдельный zip-пакет выпуска не создавался и не проверялся

## Состав release package
- Включено:
  - `.editorconfig`, `.gitattributes`, `.gitignore`, `AGENTS.md`, `README.md`, `Setup_Guide.md`
  - `Adapters/`, `Docs/`, `Logs/`, `MCP/`, `Memory/`, `Pipeline/`, `Plans/`, `Profiles/`, `Roles/`, `Rules/`, `Runtime/`, `Schemas/`, `Skills/`, `Standards/`, `Templates/`, `Tools/`
- Исключено:
  - `не подтверждено`
- Проверка_состава:
  - `git ls-tree -d --name-only 0.2.0`
  - `git ls-tree -r --name-only 0.2.0`

## Zip
- Решение: `не создавался`
- Путь: `неприменимо`
- Проверка_состава_zip: `неприменимо`
- Решение_владельца_для_крупного_бинарного_архива: `неприменимо`

## Границы
Manifest не заменяет `Logs/ReleaseLog.md`, `Logs/ChangeLog.md`, `Logs/QualityLog.md` и tag. Zip, если он будет создан отдельным будущим решением, является только проверяемым историческим пакетом и не становится текущим источником истины.
