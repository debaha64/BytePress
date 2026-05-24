# PLAN-000123 — Post-release 0.4.0: factual log, GitHub Release и archive

ID: PLAN-000123
Название: Post-release 0.4.0: factual log, GitHub Release и archive
Статус: Завершено
Связи: ROAD-000051, BACK-000133, CHG-000135, QL-000130, RL-000011
Источник: Запрос владельца от 2026-05-24
Дата_создания: 2026-05-24
Дата_изменения: 2026-05-24
Основание: Внешний выпуск BytePress `0.4.0` выполнен через `PR #137`, annotated tag `0.4.0` указывает на фактический `origin/main`, а readiness `RL-000010` должна быть отделена от factual release event `RL-000011`.
Связанные_требования:
Связанные_backlog: BACK-000133
Связанные_ADR:

## Цель
- подтвердить merge `PR #137` в `main`;
- подтвердить annotated tag `0.4.0`;
- создать GitHub Release `0.4.0`;
- зафиксировать внешний release event в `RL-000011`;
- создать release archive `0.4.0.zip`;
- удалить отработанные `ROAD/PLAN` цикла `0.4.0` из открытых архивных каталогов;
- синхронизировать `develop` с фактом выпуска отдельным PR.

## Артефакты
- `Plans/Archive/Releases/0.4.0.zip`
- `Plans/Archive/Releases/README.md`
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/Archive/Backlog/ROAD-000051.md`
- `Plans/Archive/Plans/PLAN-000123-post-release-0-4-0.md`
- `Logs/ReleaseLog.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`

## Шаги
1. Подтвердить factual release state.
   - Определение_готовности: `PR #137` имеет состояние `MERGED`, tag `0.4.0` является annotated tag и указывает на `origin/main`.
2. Создать GitHub Release `0.4.0`, если он отсутствует.
   - Определение_готовности: GitHub Release связан с tag `0.4.0`, не является draft или prerelease и опубликован без assets.
3. Синхронизировать post-release ветку с `origin/main`.
   - Определение_готовности: `origin/main` влит в ветку от `origin/develop` без конфликтов и без изменения `origin/main`.
4. Создать release archive `0.4.0.zip`.
   - Определение_готовности: zip содержит только `MANIFEST.md`, `Backlog/*` и `Plans/*`; `ROAD-000043` ... `ROAD-000050` и `PLAN-000097` ... `PLAN-000122` удалены из открытых архивных каталогов после упаковки.
5. Зафиксировать post-release факты.
   - Определение_готовности: `RL-000011`, `CHG-000135`, `QL-000130`, `ROAD-000051`, `BACK-000133` и `PLAN-000123` закрыты.

## Проверки
- `git diff --check`
- `python3 Tools/bp_lint.py --repo .`
- `python3 Tools/bp_check.py --repo .`
- `python3 Tools/bp_check.py --repo . --format json`
- `python3 -m py_compile Tools/bp_lint.py Tools/bp_check.py Tools/bp_check_contract.py Tools/bp_bootstrap.py`
- `python3 -m zipfile -t Plans/Archive/Releases/0.1.0.zip`
- `python3 -m zipfile -t Plans/Archive/Releases/0.2.0.zip`
- `python3 -m zipfile -t Plans/Archive/Releases/0.3.0.zip`
- `python3 -m zipfile -t Plans/Archive/Releases/0.4.0.zip`
- проверка состава `0.4.0.zip` на отсутствие source tree и наличие только `MANIFEST.md`, `Backlog/*`, `Plans/*`;
- проверка открытых архивных каталогов на отсутствие `ROAD-000043` ... `ROAD-000050` и `PLAN-000097` ... `PLAN-000122`;
- `gh release view 0.4.0`.

## Результат
`BACK-000133`, `PLAN-000123` и `ROAD-000051` завершены. Внешний выпуск BytePress `0.4.0` зафиксирован в `RL-000011`; GitHub Release `0.4.0` создан; release archive `0.4.0.zip` создан; post-release cleanup открытого архивного слоя выполнен. `ADR-000028` не создан, потому что новое архитектурное решение не принималось.
