# PLAN-000074 — Product lint lifecycle modes

ID: PLAN-000074
Название: Product lint lifecycle modes
Статус: Завершено
Связи: BACK-000086
Источник: Corrective pass after first evolving product repository check
Дата_создания: 2026-04-26
Дата_изменения: 2026-04-26
Основание: Первый развивающийся product repo после подтверждения current truth показал, что current `bp_lint.py` всё ещё проверяет только fresh bootstrap baseline и ошибочно считает нормальный lifecycle transition defect.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000086
Связанные_ADR:
- отсутствуют

## Шаги
1. Открыть corrective planning-contour и подтвердить scope.
   - DoD: `ROAD-000021`, `BACK-000086` и `PLAN-000074` согласованы.
2. Разделить fresh и developed product repo checks в `Tools/bp_lint.py`.
   - DoD: fresh bootstrap strict gate сохранён, developed gate принимает подтверждённую current truth и закрытый first pass.
3. Синхронизировать generated `scripts/dev-test.sh` и technical documents.
   - DoD: docs и script route явно показывают, какой режим проверки запускается.
4. Подтвердить оба режима на временном generated product repo и negative scenario.
   - DoD: fresh repo проходит fresh gate, developed repo проходит developed gate, contradictory statuses падают.
5. Закрыть planning/log contour и подготовить PR в `develop`.
   - DoD: checks выполнены, logs зафиксированы, branch pushed, PR подготовлен.

## Ограничения
- не менять `Minesweeper`;
- не добавлять Roles, Schemas, Templates, Rules, Standards или Skills в product bootstrap;
- не расширять проверку до semantic auditor;
- не ослаблять branch gate и first product-start gate;
- не ломать fresh bootstrap contract.

## Артефакты
- `Tools/bp_lint.py`
- `Tools/bp_bootstrap.py`
- `Docs/Technical/Product_Bootstrap_Contract.md`
- `Docs/Technical/Product_Bootstrap_Validation.md`
- `Docs/Technical/Artifact_Lifecycle.md`
- `Tools/README.md`
- `Plans/*`
- `Logs/*`

## DoD
- `bp_lint.py` различает fresh и developed product repo modes;
- `scripts/dev-test.sh` generated product repo запускает explicit auto mode;
- bootstrap fresh state остаётся строгим;
- developed state после first pass проверяется по согласованности `Docs/Discovery/Interview.md`, `Plans/*` и `Logs/*`;
- contradiction scenario падает deterministic check.

## Результат
- `bp_lint.py` получил режимы `product-fresh`, `product-developed` и `auto`; fresh mode сохраняет strict bootstrap expectations, developed mode принимает подтверждённую current truth только при закрытых `ROAD-000001`, `BACK-000001`, `PLAN-000001`, наличии следующего active/completed plan и log closure.
- Generated `scripts/dev-test.sh` запускает `python3 "$LINT_SCRIPT" --repo "$ROOT_DIR" --mode auto`, а `Tools/README.md`, bootstrap contract, validation contract и lifecycle contract описывают различие fresh/developed checks.
- Временный product repo `/tmp/bytepress-lint-lifecycle-q7DZ8V/product` подтвердил fresh check, auto check, generated `dev-test.sh`, integration smoke, developed check и expected fail на contradictory `PLAN-000001`.
- `ROAD-000021` и `BACK-000086` закрыты без активации нового `ROAD-*`.
