# PLAN-000014 — Cleanup orphan IDs

ID: PLAN-000014
Название: Убрать оставшиеся orphan references из активного non-log слоя
Статус: Завершено
Связи: BACK-000019, CHG-000023
Источник: Следующий точечный cleanup-проход после semver operationalization
Дата_создания: 2026-03-18
Дата_изменения: 2026-03-18
Основание: После migration и semver-проходов в активном non-log слое оставались две orphan reference: orphan requirement в ранних plan-файлах и orphan pipeline reference в правиле строгости утверждений.
Связанные_требования:
Связанные_backlog:
- BACK-000019
Связанные_ADR:
- ADR-000014

## Шаги
1. Убрать orphan requirement reference из ранних plan-файлов.
   - DoD: `Plans/Archive/PLAN-000001-foundation.md` и `Plans/Archive/PLAN-000002-seed-docs-and-standards.md` больше не содержат orphan requirement reference, при этом смысл оснований и связей сохранён через существующие поля плана.
2. Убрать orphan pipeline reference из правила строгости утверждений.
   - DoD: `Rules/Approval_Strictness.md` больше не содержит orphan pipeline reference, а зависимость от фаз конвейера описана только текстом правила.
3. Зафиксировать cleanup-pass без расширения модели.
   - DoD: добавлены только `Plan`, `ChangeLog` и `QualityLog` текущего прохода; новые ID namespaces, requirement registry и pipeline registry не создаются.

## Риски
- попытка заменить orphan reference новой сущностью нарушит ограничение на отсутствие новых namespace и registry;
- частичный cleanup оставит orphan references в активном non-log слое и сохранит двусмысленность;
- избыточные правки за пределами трёх целевых файлов выведут проход за утверждённый scope.

## Артефакты
- `Plans/Archive/PLAN-000001-foundation.md`
- `Plans/Archive/PLAN-000002-seed-docs-and-standards.md`
- `Rules/Approval_Strictness.md`
- `Plans/Archive/PLAN-000014-cleanup-orphan-ids.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`

## DoD
Оставшиеся orphan requirement и orphan pipeline reference удалены из активного non-log слоя без введения новых сущностей, новых namespace и нового registry-контура.
