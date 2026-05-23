# PLAN-000080 — Локальный Tools создаваемого продукта и переходный product lint

ID: PLAN-000080
Название: Локальный Tools создаваемого продукта и переходный product lint
Статус: Завершено
Связи: ROAD-000027, BACK-000092, CHG-000092, QL-000087
Источник: Запрос владельца от 2026-04-28
Дата_создания: 2026-04-28
Дата_изменения: 2026-04-28
Основание: После `ADR-000022` и `PLAN-000079` нужно начать инструментальную реализацию профильного самодостаточного product skeleton без удаления legacy domains `BytePress`.
Связанные_требования:
- AGENTS.md
Связанные_backlog:
- BACK-000092
Связанные_ADR:
- ADR-000022
Артефакты:
- Tools/bp_bootstrap.py
- Tools/bp_lint.py
- Tools/README.md
- Docs/Technical/Product_Bootstrap_Contract.md
- Docs/Technical/Product_Bootstrap_Validation.md
- Docs/Technical/Artifact_Lifecycle.md
- Docs/Technical/Verification_Evidence.md
- Docs/Technical/Validation_Evidence.md
- Docs/Technical/Domain_Model_Migration_Plan.md
- Docs/Technical/Product_Bootstrap_Domain_Matrix.md
- Plans/Roadmap.md
- Plans/Backlog.md
- Plans/Archive/Backlog/ROAD-000027.md
- Logs/ChangeLog.md
- Logs/QualityLog.md
Риски:
- Уже созданные продукты со старым skeleton требуют отдельного service update route.
- `bp_lint.py` теперь различает legacy `BytePress` layout и новый product layout; ошибки классификации repo могут ломать проверки.
- Generated `scripts/*` остаются только compatibility layer и не должны снова стать primary service layer.
DoD:
- `bp_bootstrap.py` materialize local product `Tools/*` как основной service layer.
- Новый product skeleton получает lightweight `Pipeline/*`, bounded `Templates/*` и `Schemas/*`.
- Новый product skeleton не получает `Adapters/*`, `Memory/*`, `MCP/*`, `Runtime/*`, `Roles/*`, `Skills/*`, `Standards/*`.
- `bp_lint.py` проверяет текущий `BytePress` и новый product skeleton.
- Выполнены repo/product checks, включая local product tools во временном продукте.

## Шаги
1. Обновить bootstrap materialization
   - Описание: заменить primary `scripts/*`/`BYTEPRESS_ROOT` route на local product `Tools/*` и добавить lightweight `Pipeline`, bounded `Templates`, bounded `Schemas`.
   - DoD: fresh generated product не содержит forbidden placeholder domains.
2. Обновить product lint
   - Описание: сохранить legacy BytePress checks и добавить product checks для нового skeleton.
   - DoD: `bp_lint.py --repo .` и product fresh/auto/developed checks проходят.
3. Синхронизировать contracts
   - Описание: обновить bootstrap contract, validation, lifecycle/evidence docs, migration plan, tools map, planning/log closure.
   - DoD: документы не утверждают старый primary `scripts/*` route как текущий target.
4. Проверить временный продукт
   - Описание: сгенерировать временный product repo, проверить fresh/auto/developed state и local product tools.
   - DoD: проверки из запроса пройдены.
5. Подготовить PR
   - Описание: commit, push и PR в `develop`.
   - DoD: branch pushed, PR открыт.

## Результат
Переходная инструментальная модель начата: новый product skeleton становится self-contained для базовых проверок через local `Tools/*`, а legacy domains `BytePress` остаются нетронутыми до следующих passes.
