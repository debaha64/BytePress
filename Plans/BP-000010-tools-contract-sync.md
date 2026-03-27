# PLAN-000010 — Tools contract sync

ID: PLAN-000010
Название: Синхронизировать инструментальный контур с naming/profile/language contracts
Статус: Завершено
Связи: BACK-000022, CHG-000019
Источник: Следующая фаза после sync-проходов по schemas, terms и profile contracts
Дата_создания: 2026-03-18
Дата_изменения: 2026-03-18
Основание: После фиксации naming, profile, language и term contracts нужно синхронизировать `bp_bootstrap.py`, `bp_lint.py` и product bootstrap docs без большого рефакторинга tools.
Связанные_требования:
- PROF-000001
- PLAN-000001
Связанные_backlog:
- BACK-000022
Связанные_ADR:
- ADR-000015
- ADR-000016

## Шаги
1. Синхронизировать CLI bootstrap contract.
   - DoD: `bp_bootstrap.py` требует `--name`, `--product-code`, `--brand-profile`, `--target`, а `--product-code` и `--brand-profile` валидируются по новому контракту.
2. Синхронизировать bootstrap output contract.
   - DoD: bootstrap создаёт `Profiles/Product.md`, initial plan file `Plans/<PRODUCT_CODE>-000001-product-initialization.md`, 6-значные ID и текущую дату выполнения.
3. Минимально обновить lint под product bootstrap output.
   - DoD: `bp_lint.py` понимает новый product plan filename pattern, `Profiles/Product.md` и базовый bootstrap output contract без архитектурного рефакторинга.
4. Синхронизировать product bootstrap docs и журналы.
   - DoD: `Tools/README.md`, `Docs/Technical/Product_Bootstrap_Contract.md`, `Docs/Technical/Product_Bootstrap_Validation.md`, `Profiles/README.md`, `Plans/Backlog.md`, `Logs/ChangeLog.md` и `Logs/QualityLog.md` отражают только факты этого прохода.

## Риски
- частичная синхронизация bootstrap и lint оставит расхождение между генерацией и проверкой продукта;
- автоматическая генерация `product-code` нарушит уже принятый naming contract;
- слишком глубокое наследование brand profile смешает brand и product profile модели раньше отдельного решения.

## Артефакты
- `Tools/README.md`
- `Tools/bp_bootstrap.py`
- `Tools/bp_lint.py`
- `Docs/Technical/Product_Bootstrap_Contract.md`
- `Docs/Technical/Product_Bootstrap_Validation.md`
- `Profiles/README.md`
- `Plans/Backlog.md`
- `Plans/BP-000010-tools-contract-sync.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`

## DoD
Инструментальный контур BytePress синхронизирован с naming/profile/language contracts: bootstrap и lint понимают новый product bootstrap contract, product bootstrap docs обновлены, а smoke-проверка проходит без выхода за scope текущего прохода.
