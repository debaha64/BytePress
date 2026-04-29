# PLAN-000083 — Маршрут обновления already-created product repo на local tools baseline

ID: PLAN-000083
Название: Маршрут обновления already-created product repo на local tools baseline
Статус: Завершено
Связи: ROAD-000030, BACK-000095, CHG-000095, QL-000090
Источник: Запрос владельца от 2026-04-28
Дата_создания: 2026-04-28
Дата_изменения: 2026-04-30
Основание: После перехода нового product skeleton на local `Tools/*` уже созданные продукты со старым service layer требуют явного update route без повторного bootstrap.
Связанные_требования:
- AGENTS.md
Связанные_backlog:
- BACK-000095
Связанные_ADR:
- ADR-000022
Артефакты:
- Docs/Technical/Product_Service_Update_Route.md
- Docs/Technical/README.md
- Docs/Technical/Product_Bootstrap_Contract.md
- Docs/Technical/Product_Bootstrap_Validation.md
- Docs/Technical/Domain_Model_Migration_Plan.md
- Plans/Roadmap.md
- Plans/Backlog.md
- Plans/Archive/Backlog/ROAD-000030.md
- Logs/ChangeLog.md
- Logs/QualityLog.md
Риски:
- Реальный старый product repo может иметь предметное содержимое в legacy `Runtime/*`, `Adapters/*` или `Profiles/Product.md`; такой content нельзя удалять по generic route.
- Product-local tools могут расходиться между продуктами до появления profile versioning.
DoD:
- Route описывает add/replace/delete наборы.
- Route фиксирует protected artifacts.
- Route содержит migration smoke scenario для старого product repo.
- Bootstrap/validation contracts и migration plan синхронизированы.
- Repo и temporary product migration checks пройдены.

## Шаги
1. Описать service update route
   - Описание: добавить owner-document с add/replace/delete, protected artifacts и verification route.
   - DoD: already-created product repo обновляется как product-side pass, а не fresh bootstrap.
2. Синхронизировать technical contracts
   - Описание: добавить ссылку из technical map, bootstrap contract, validation contract и migration plan.
   - DoD: route не дублируется как hidden rule в нескольких documents.
3. Проверить миграционный сценарий
   - Описание: bootstrap temporary product, смоделировать старый service layer, применить update route и проверить developed product state.
   - DoD: local `Tools/product_check.py`, compatibility `scripts/dev-test.sh` и `bp_lint.py --mode auto` проходят.
4. Закрыть planning/log contour
   - Описание: оформить `ROAD/BACK/PLAN/CHG/QL` как один завершённый pass.
   - DoD: active backlog снова пуст, logs содержат factual closure.

## Результат
Маршрут обновления already-created product repo на local tools baseline зафиксирован без изменения `Minesweeper`, без удаления legacy domains `BytePress`, без переноса `Skills/*` и без удаления transition `scripts/*`.
