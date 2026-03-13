# Bootstrap_Contract

## Назначение
Этот документ фиксирует, какой минимальный продуктовый каркас обязан уметь материализовать `bp_bootstrap.py` в `BytePress v1`.

## Минимальный состав продукта
- `README.md`
- `Setup_Guide.md`
- `Docs/User/README.md`
- `Docs/Product/README.md`
- `Docs/Technical/README.md`
- `Docs/Technical/Architecture.md`
- `Docs/Technical/Interfaces.md`
- `Docs/Technical/System_Invariants.md`
- `Docs/Terms/README.md`
- `Docs/Terms/Base_Terms.md`
- `Runtime/*`
- `Plans/README.md`, `Plans/Roadmap.md`, `Plans/Backlog.md`, минимум один `Plan`
- `Logs/README.md`, `ChangeLog.md`, `ADRlog.md`, `QualityLog.md`, `ReleaseLog.md`, `SupportLog.md`
- `Adapters/README.md` и базовые каталоги адаптеров
- `scripts/` с управляемыми точками входа проекта

## Инварианты
- продукт создаётся как отдельный репозиторий;
- продукт не содержит копию системных доменов `BytePress`, не относящихся к продукту;
- продукт не зависит на выполнение от исходного репозитория `BytePress`;
- продукт получает только минимальный пригодный каркас и может далее развиваться отдельно.

## Связи
- `ADR-0009`
- `BACK-0016`
- `CHG-0009`
