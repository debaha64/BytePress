# Product Service Update Route

## Назначение
`Docs/Technical/Product_Service_Update_Route.md` фиксирует канонический маршрут обновления служебного слоя уже созданного product repo.

Этот document отвечает на вопросы:
- как обновлять product repo, созданный старым bootstrap, без повторного bootstrap;
- какие файлы переносить из нового baseline;
- какие product artifacts защищены от переписывания;
- какие legacy domains допускается удалить при переходе к local `Tools/*`;
- какие проверки подтверждают корректность миграции.

## Scope
Route применяется к product repo, который уже создан и может содержать старый служебный слой: `Runtime/*`, `Adapters/*`, `Profiles/Product.md`, прежние `scripts/*` и зависимость проверок от `BYTEPRESS_ROOT`.

Новый продуктовый каркас больше не создаёт `scripts/*`. Этот route сохраняет описание `scripts/*` только как наследия старых продуктов и как временной совместимой поверхности при их миграции к локальному `Tools/*`.

Route не является product-start reset, fresh bootstrap или предметной миграцией продукта. Он обновляет только service layer и minimal process/check contour, нужный для текущей профильной модели.

## Канонический маршрут
1. Открыть рабочую ветку внутри product repo.
2. Создать временный product repo актуальным `Tools/bp_bootstrap.py` с тем же или эквивалентным `product-code` и brand profile.
3. Сравнить временный baseline с текущим product repo и выделить только service delta.
4. Перенести add/replace/delete наборы ниже вручную или детерминированным product-side patch.
5. Не переписывать подтверждённую текущую истину, product docs, planning history, logs и предметный код.
6. Запустить local checks продукта и внешнюю проверку `BytePress` в режиме `auto` или `product-developed`.
7. Закрыть product-side planning/log facts внутри самого product repo.

## Add Set
Если отсутствуют, добавить из актуального generated baseline:
- `Tools/README.md`;
- `Tools/product_check.py`;
- `Tools/product_bootstrap_smoke.py`;
- `Pipeline/README.md`;
- `Pipeline/Phases.md`;
- `Pipeline/Workflows.md`;
- `Pipeline/Gates.md`;
- `Templates/README.md` и bounded templates для materialized artifacts;
- `Schemas/README.md` и bounded schemas, которые проверяет local `Tools/*`;
- `Docs/Product/Product_Passport.md`, если в продукте нет другого явного паспорта созданного каркаса.

`Docs/Product/Product_Passport.md` добавляется как skeleton metadata. Он не должен заменить `Docs/Product/JTBD.md`, `PRD.md`, `Delivery.md` или фактическую product truth.

## Replace Set
Заменять можно только служебные wrappers старых продуктов и карты service layer:
- `scripts/README.md`;
- `scripts/dev-test.sh`;
- `scripts/integration-smoke.sh`;
- `scripts/reset-product-start.sh`;
- `.gitignore` только в части ignored tool reports, если `Tools/.reports/` ещё не исключён;
- `Setup_Guide.md` только в точечных строках запуска проверок, если он всё ещё требует primary `BYTEPRESS_ROOT` route.

Wrappers старого продукта должны вызывать local `Tools/*`. `BYTEPRESS_ROOT` допустим только для внешней проверки `BytePress` tooling, а не как обычная product-local dependency. Для нового каркаса wrappers не создаются.

## Delete Set
После успешного переноса local `Tools/*` допускается удалить только placeholder service domains старого каркаса:
- `Runtime/*`, если он содержит только bootstrap smoke reports или временный service output;
- `Adapters/*`, если это placeholder domain без реального adapter mechanism продукта;
- `Profiles/Product.md`, если его единственная роль — старый bootstrap passport, заменённый на `Docs/Product/Product_Passport.md`;
- устаревшие generated scripts, если они не являются временными compatibility wrappers к local `Tools/*`.

Нельзя удалять эти пути механически, если продукт уже наполнил их предметным смыслом. В таком случае нужен отдельный product-side decision и отдельная миграция содержимого.

## Protected Artifacts
Route не должен переписывать:
- `Docs/Discovery/Interview.md` и подтверждённую current truth;
- `Docs/Product/JTBD.md`, `Docs/Product/PRD.md`, `Docs/Product/Delivery.md` и другие product-owned docs;
- `Plans/Roadmap.md`, `Plans/Backlog.md`, существующие plans и archive history, кроме product-side closure текущего update pass;
- `Logs/*` history, кроме новых factual entries update pass;
- предметный код, данные, конфигурацию продукта и runtime artifacts, которые уже являются реальной частью продукта.

## Verification Route
Минимальная проверка migrated product repo:
- `python3 Tools/product_check.py --repo . --mode auto` внутри product repo;
- `python3 Tools/product_bootstrap_smoke.py` внутри product repo;
- `python3 <BytePress>/Tools/bp_lint.py --repo <product-repo> --mode auto` из `BytePress`;
- если product repo уже developed, explicit `--mode product-developed` должен проходить, а `product-fresh` может падать на expected fresh markers;
- для старого продукта, где временно сохранены compatibility wrappers, `scripts/dev-test.sh` и `scripts/integration-smoke.sh` должны вызывать local `Tools/*`, а smoke report должен выпускаться в ignored `Tools/.reports/`, а не в `Runtime/*`.

## Migration Smoke Scenario
Для проверки route без изменения реального продукта используется временный сценарий:
1. bootstrap fresh product актуальным `Tools/bp_bootstrap.py`;
2. смоделировать старый product repo: убрать local `Tools/*`, вернуть placeholder `Runtime/*`, `Adapters/*`, `Profiles/Product.md` и legacy `scripts/*`;
3. применить service update route: добавить local `Tools/*`, lightweight `Pipeline/*`, bounded `Templates/*`/`Schemas/*`, заменить или удалить wrappers старого продукта и удалить placeholder legacy domains;
4. смоделировать developed state: подтвердить `Docs/Discovery/Interview.md`, закрыть `ROAD-000001`, `BACK-000001`, `PLAN-000001`, добавить следующий plan и closure facts в `Logs/*`;
5. подтвердить checks из раздела `Verification Route`.

## Boundaries
Этот route не расширяет bootstrap obligations и не разрешает удаление legacy domains самого `BytePress`. Он описывает product-side service update уже созданного продукта.

Если service update требует предметного изменения продукта, этот route должен остановиться на service delta, а предметное изменение должно получить отдельный product-side pass.

## Связи
- `ADR-000022`
- `Product_Bootstrap_Contract.md`
- `Product_Bootstrap_Validation.md`
- `Domain_Model_Migration_Plan.md`
