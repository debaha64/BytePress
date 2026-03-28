# PLAN-000020 — Artifact lifecycle contract

ID: PLAN-000020
Название: Зафиксировать technical-contract жизненного цикла артефактов
Статус: Завершено
Связи: BACK-000030, CHG-000032, QL-000027
Источник: Technical cleanup pass после закрепления discovery, sync-contract и branch/PR process contract
Дата_создания: 2026-03-29
Дата_изменения: 2026-03-29
Основание: Источники истины и порядок обязательной синхронизации артефактов сейчас распределены между `Docs/Discovery/`, `Docs/Technical/Pipeline.md`, `Plans/Roadmap.md`, активными `Plans/*` и `Logs/*`. Нужно собрать их в один короткий technical-contract, оставить `Pipeline.md` кратким и минимально обновить lint под новый обязательный technical artifact.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000030
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать управляемый контур прохода.
   - Описание: Добавить backlog-item текущей задачи и отдельный plan-file для lifecycle-pass.
   - DoD: `Plans/Backlog.md` и `Plans/BP-000020-artifact-lifecycle-contract.md` отражают scope без расширения области.
2. Добавить канонический lifecycle contract.
   - Описание: Создать `Docs/Technical/Artifact_Lifecycle.md` как короткий практический документ про источники истины, производные артефакты, порядок синхронизации и task-close checklist.
   - DoD: lifecycle contract не дублирует целиком `Pipeline.md`, а собирает в одном месте обязательный порядок обновления артефактов.
3. Синхронизировать technical docs и lint.
   - Описание: Обновить только нужные `Docs/Technical/*`, `Docs/README.md` и `Tools/bp_lint.py`, чтобы новый technical artifact стал частью обязательного контракта `BytePress`.
   - DoD: `Pipeline.md` остаётся кратким и ссылается на `Artifact_Lifecycle.md`, а lint требует новый документ.
4. Закрыть pass в плановом и журнальном контуре.
   - Описание: Перевести backlog и plan в финальный статус, обновить `ChangeLog` и `QualityLog`, а `ADR` создавать только при появлении нового устойчивого решения.
   - DoD: `python3 Tools/bp_lint.py --repo .` проходит, `BACK-000030` закрыт по факту, а `ADRlog` не меняется без реальной необходимости.

## Риски
- попытка превратить lifecycle contract в большой регламент смешает technical contract с process-doc rewrite;
- дублирование `Pipeline.md` создаст ещё один источник process-noise вместо его удаления;
- лишние правки в `Model.md`, `System_Invariants.md` и соседних доменах выведут задачу за пределы согласованного scope.

## Артефакты
- `Plans/Backlog.md`
- `Plans/BP-000020-artifact-lifecycle-contract.md`
- `Docs/Technical/Artifact_Lifecycle.md`
- `Docs/Technical/README.md`
- `Docs/Technical/Pipeline.md`
- `Docs/README.md`
- `Tools/bp_lint.py`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`

## DoD
- существует `Docs/Technical/Artifact_Lifecycle.md`.
- lifecycle contract короткий, практический и не дублирует целиком `Pipeline.md`.
- `Pipeline.md` и `Docs/Technical/README.md` синхронизированы с новым документом.
- `Tools/bp_lint.py` требует новый обязательный technical artifact.
- `python3 Tools/bp_lint.py --repo .` проходит.
- новый `ADR` создаётся только при реальной необходимости.

## Фактический результат
- Создан `Docs/Technical/Artifact_Lifecycle.md` как единая точка для источников истины, производных артефактов, порядка обязательной синхронизации и минимального task-close checklist.
- `Docs/Technical/Pipeline.md` сокращён до краткой роли конвейера и ссылки на `Artifact_Lifecycle.md` как на точку детализации lifecycle-порядка.
- `Docs/Technical/README.md` и `Docs/README.md` синхронизированы с новым technical artifact без побочного рефакторинга `Model.md` и `System_Invariants.md`.
- `Tools/bp_lint.py` минимально расширен и теперь требует `Docs/Technical/Artifact_Lifecycle.md` как обязательный technical artifact репозитория `BytePress`.
- `ADRlog` не менялся, потому что проход только собрал уже принятый канон в один technical-contract без нового устойчивого архитектурного решения.
