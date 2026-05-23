# PLAN-000081 — Синхронизация терминов и проверок нового product skeleton

ID: PLAN-000081
Название: Синхронизация терминов и проверок нового product skeleton
Статус: Завершено
Связи: ROAD-000028, BACK-000093, CHG-000093, QL-000088
Источник: Запрос владельца от 2026-04-28
Дата_создания: 2026-04-28
Дата_изменения: 2026-04-28
Основание: После `PLAN-000080` часть терминов, интервью и generated artifacts ещё ссылалась на старый product skeleton с `Runtime/*`, `Profiles/Product.md` и `Adapters/*`.
Связанные_требования:
- AGENTS.md
Связанные_backlog:
- BACK-000093
Связанные_ADR:
- ADR-000022
Артефакты:
- Docs/Terms/TERM-000019-repository-scaffold.md
- Docs/Terms/TERM-000018-product-profile.md
- Docs/Discovery/Interview.md
- Docs/Technical/Product_Bootstrap_Contract.md
- Docs/Technical/Product_Bootstrap_Domain_Matrix.md
- Docs/Technical/Product_Bootstrap_Validation.md
- Tools/bp_bootstrap.py
- Tools/bp_lint.py
- Plans/Roadmap.md
- Plans/Backlog.md
- Plans/Archive/Backlog/ROAD-000028.md
- Logs/ChangeLog.md
- Logs/QualityLog.md
Риски:
- Уже созданные продукты со старым `Profiles/Product.md` и `Adapters/*` требуют отдельного migration/update route.
- Product passport в `Docs/Product/Product_Passport.md` фиксирует только skeleton metadata и не должен стать governance domain.
DoD:
- Термин `Каркас репозитория` описывает новый product skeleton.
- Термин `Профиль продукта` не требует `Profiles/Product.md` и фиксирует паспорт в `Docs/Product/Product_Passport.md`.
- Active interview синхронизирован с новой моделью.
- Forbidden product domains дают нормальную ошибку lint.
- Generated `Templates/*` имеют уникальные IDs.
- Проверки из запроса пройдены.

## Шаги
1. Синхронизировать термины и interview
   - Описание: убрать старые ссылки на `Runtime/*`, `Profiles/Product.md`, `Adapters/*` как части product skeleton.
   - DoD: активные owner-documents описывают новый skeleton.
2. Исправить tools
   - Описание: исправить product lint forbidden-domain path и generated template IDs.
   - DoD: negative forbidden-domain check падает нормальной ошибкой, не traceback.
3. Синхронизировать contracts и logs
   - Описание: обновить bootstrap docs, planning и factual logs.
   - DoD: `ROAD/BACK/PLAN/CHG/QL` согласованы.
4. Проверить временный продукт
   - Описание: bootstrap, fresh/auto, negative forbidden-domain, developed и local tools checks.
   - DoD: все проверки из запроса пройдены.

## Результат
Новая модель product skeleton согласована в терминах, interview, bootstrap artifacts и lint checks без переноса `Skills/*`, без удаления legacy domains и без изменения `Minesweeper`.
