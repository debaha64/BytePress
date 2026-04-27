# PLAN-000075 — Product service update path

ID: PLAN-000075
Название: Product service update path
Статус: Завершено
Связи: BACK-000087
Источник: Corrective pass after developed product service-layer update need
Дата_создания: 2026-04-27
Дата_изменения: 2026-04-27
Основание: После разделения fresh/developed product lint нужен короткий канонический путь обновления служебных файлов уже созданного product repo, чтобы `scripts/dev-test.sh` и `scripts/README.md` обновлялись без пересоздания продукта и без потери предметных артефактов.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000087
Связанные_ADR:
- отсутствуют

## Шаги
1. Открыть минимальный planning-contour для corrective pass.
   - DoD: `ROAD-000022`, `BACK-000087` и `PLAN-000075` согласованы.
2. Зафиксировать canonical service-layer update path.
   - DoD: technical/tooling documents и generated service files показывают, как обновлять `scripts/dev-test.sh` и `scripts/README.md` без fresh bootstrap reset.
3. Добавить короткий пример developed product state после первого pass.
   - DoD: fresh bootstrap gate и developed product check остаются разведены и не ослаблены.
4. Уточнить commit discipline.
   - DoD: verification contract фиксирует, что основание, документы, код, проверки и журналы лучше коммитить отдельными смысловыми commits.
5. Выполнить required checks и закрыть planning/log contour.
   - DoD: repo checks, bootstrap fresh check, modeled developed check, logs и archive planning-layer согласованы.

## Ограничения
- не менять `Minesweeper`;
- не добавлять новые домены в product bootstrap;
- не делать широкую языковую чистку;
- не усложнять процесс обновления;
- не ослаблять fresh bootstrap gate и product-developed check.

## Артефакты
- `Docs/Technical/Product_Bootstrap_Contract.md`
- `Docs/Technical/Product_Bootstrap_Validation.md`
- `Docs/Technical/Artifact_Lifecycle.md`
- `Docs/Technical/Verification.md`
- `Tools/README.md`
- `Tools/bp_bootstrap.py`
- `Plans/*`
- `Logs/*`

## DoD
- canonical update path for `scripts/dev-test.sh` and `scripts/README.md` documented;
- developed product example after first pass documented;
- commit discipline clarified;
- fresh bootstrap and developed product checks pass on temporary product repo;
- `bp_lint.py` contract remains unaffected unless a real check change is required.

## Результат
- `Product_Bootstrap_Contract.md` фиксирует минимальный product-side route обновления `scripts/dev-test.sh` и `scripts/README.md` без повторного bootstrap и без переписывания `Docs/Product/*`, `Docs/Discovery/*`, `Plans/*`, `Logs/*` или предметного кода вне scope.
- `Product_Bootstrap_Validation.md`, `Artifact_Lifecycle.md`, `Verification.md`, `Tools/README.md` и generated `scripts/README.md` синхронизированы вокруг точечного service-layer update path, developed state example и commit discipline.
- Временный product repo `/tmp/bytepress-service-update-YpTbG9/product` подтвердил fresh bootstrap check, generated `scripts/dev-test.sh`, modeled developed product check и generated service guidance.
- `bp_lint.py` не менялся; fresh bootstrap gate и product-developed check не ослаблялись.
