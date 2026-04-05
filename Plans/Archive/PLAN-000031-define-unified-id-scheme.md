# PLAN-000031 — Define unified ID scheme

ID: PLAN-000031
Название: Зафиксировать единую схему идентификаторов и порядок будущей migration
Статус: Завершено
Связи: BACK-000043
Источник: Narrow governance-pass inside `ROAD-000009`
Дата_создания: 2026-04-06
Дата_изменения: 2026-04-06
Основание: После выравнивания planning transition `ROAD-000009` всё ещё требует отдельного pass, который зафиксирует целевую единую `ID scheme` для всего репозитория: классы артефактов по модели идентификации, правила filename и внутренних ссылок, а также порядок будущей migration по доменам. Этот pass не делает саму migration и не меняет physical layout репозитория.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000043
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать текущий corrective scope внутри `ROAD-000009`.
   - Описание: Добавить одну реальную backlog-задачу и один новый текущий `Plan` только для unified `ID scheme`.
   - DoD: `BACK-000043` и `PLAN-000031` описывают только определение целевой схемы и порядка migration без запуска migration.
2. Определить целевую модель идентификации артефактов.
   - Описание: Зафиксировать classes `serial / hybrid / singleton`, обязательность внутреннего `ID`, обязательность `ID` в filename и filename-contract для serial domains.
   - DoD: `Standards/Naming.md` явно различает target `ID scheme` и transitional legacy-state.
3. Зафиксировать правила ссылок и порядок будущей migration.
   - Описание: Определить, когда достаточно внутреннего `ID`, когда нужен filename/path, и в каком порядке future migration должна проходить по доменам.
   - DoD: правила ссылок и migration-order зафиксированы, но migration не запущена.
4. Синхронизировать минимально необходимые planning-зависимости.
   - Описание: Обновить `Standards/Planning.md` и связанные документы только там, где это реально необходимо для согласования с unified `ID scheme`.
   - DoD: planning-contract не спорит с новым naming-contract, а `bp_lint.py` меняется только при доказанной необходимости.

## Ограничения
- без physical migration `ID`;
- без массового переименования файлов;
- без переноса historical `BP-*` plan-files;
- без архивирования historical backlog;
- без удаления `Runtime/Plan.md`;
- без широкого переписывания `Docs/Technical/*`, `AGENTS.md` и `Docs/User/*`.

## Риски
- если не зафиксировать классы доменов и правила ссылок явно, будущая migration снова размоется по разным локальным исключениям;
- преждевременная physical migration выйдет за scope и сломает проверяемость governance-pass;
- если transition-state не будет явно отделён от target `ID scheme`, naming-contract снова начнёт спорить с фактическим деревом.

## Артефакты
- `Plans/Backlog.md`
- `Plans/Roadmap.md`
- `Plans/PLAN-000031-define-unified-id-scheme.md`
- `Standards/Naming.md`
- `Standards/Planning.md`
- `Plans/README.md`

## DoD
- создана одна узкая backlog-задача только для unified `ID scheme`.
- создан новый текущий `Plan` только под этот pass.
- в `Standards/Naming.md` зафиксированы classes `serial / hybrid / singleton`, filename-contract, правила ссылок и migration-order.
- target `ID scheme` и transitional legacy-state явно разведены.
- `python3 Tools/bp_lint.py --repo .` проходит.

## Фактический результат
- `BACK-000043` и `PLAN-000031` зафиксировали только pass на unified `ID scheme` без запуска migration.
- `Standards/Naming.md` зафиксировал target `ID scheme` для serial / hybrid / singleton domains, правила filename и внутренних ссылок, а также future migration-order по доменам.
- `Standards/Planning.md` и `Plans/README.md` синхронизированы только в минимально необходимой части.
- `bp_lint.py` не менялся, потому что pass уточняет policy и naming-contract, но не меняет обязательный набор путей или текущую файловую структуру; `bp_lint contract unaffected`.
