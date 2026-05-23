# PLAN-000093 — Tools/* как единственный служебный вход нового каркаса

ID: PLAN-000093
Название: Tools/* как единственный служебный вход нового каркаса
Статус: Завершено
Связи: ROAD-000039, BACK-000104, CHG-000105, QL-000100
Источник: Запрос владельца от 2026-05-11
Дата_создания: 2026-05-11
Дата_изменения: 2026-05-11
Основание: Владелец запросил узкий предрелизный проход: новый создаваемый продукт больше не должен получать `scripts/*`, а `Tools/*` должен остаться единственным служебным входом нового продукта.
Связанные_требования:
Связанные_backlog: BACK-000104
Связанные_ADR: ADR-000027

## Шаги
1. Обновить `Tools/bp_bootstrap.py`, чтобы новый каркас не создавал `scripts/*` и не ссылался на него как на текущий слой.
   - DoD: выполнено; generated `README.md`, `AGENTS.md`, `Setup_Guide.md` и `Docs/Product/Product_Passport.md` не описывают `scripts/*` как текущий слой.
2. Обновить `Tools/bp_lint.py` и generated `Tools/product_check.py`.
   - DoD: выполнено; fresh/developed checks не требуют `scripts/*`, а fresh repo нового образца получает ошибку при наличии `scripts/*`.
3. Синхронизировать документы-владельцы и `Tools/README.md`.
   - DoD: выполнено; новый каркас описан через `Tools/*`, а `Product_Service_Update_Route.md` сохраняет миграцию старых продуктов с наследием `scripts/*`.
4. Выполнить обязательные проверки и временный bootstrap.
   - DoD: выполнено; проверки зафиксированы в `QL-000100`.
5. Закрыть плановый и журнальный контур.
   - DoD: выполнено; `ROAD-000039`, `BACK-000104`, `PLAN-000093`, `CHG-000105` и `QL-000100` согласованы.

## Риски
- Старые уже созданные продукты могут сохранять совместимые shell-оболочки; их нельзя удалять без product-side миграции.
- Fresh check должен отличать новый каркас от старого продукта и не требовать возврата `scripts/*`.

## Артефакты
- `Tools/bp_bootstrap.py`
- `Tools/bp_lint.py`
- `Docs/Technical/Product_Bootstrap_Contract.md`
- `Docs/Technical/Product_Bootstrap_Domain_Matrix.md`
- `Docs/Technical/Product_Service_Update_Route.md`
- `Docs/Technical/Product_Bootstrap_Validation.md`
- `Tools/README.md`
- `Plans/*`
- `Logs/*`

## DoD
Новый продуктовый каркас создаётся без `scripts/*`, служебные команды нового продукта идут через `Tools/*`, проверки подтверждают fresh/auto/developed контуры, а маршрут старых продуктов сохраняет миграцию наследия `scripts/*`.
