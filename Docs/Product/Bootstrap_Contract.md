# Bootstrap_Contract

## Назначение
Этот документ фиксирует, какой минимальный продуктовый каркас обязан уметь материализовать `bp_bootstrap.py` в `BytePress v1`.

## CLI contract
Обязательные параметры:
- `--name`
- `--product-code`
- `--brand-profile`
- `--target`

Правила:
- `--product-code` обязателен, содержит 2-3 символа верхнего регистра и не генерируется автоматически;
- без `--product-code` bootstrap не запускается;
- `--brand-profile` обязателен и должен указывать на существующий `brand profile` в репозитории `BytePress`;
- при отсутствии указанного brand profile bootstrap завершается понятной ошибкой.

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
- `Profiles/Product.md`
- `Runtime/*`
- `Plans/README.md`, `Plans/Roadmap.md`, `Plans/Backlog.md`, initial plan file `Plans/<PRODUCT_CODE>-000001-product-initialization.md`
- `Logs/README.md`, `ChangeLog.md`, `ADRlog.md`, `QualityLog.md`, `ReleaseLog.md`, `SupportLog.md`
- `Adapters/README.md` и базовые каталоги адаптеров
- `scripts/` с управляемыми точками входа проекта

## Инварианты
- продукт создаётся как отдельный репозиторий;
- продукт не содержит копию системных доменов `BytePress`, не относящихся к продукту;
- продукт не зависит на выполнение от исходного репозитория `BytePress`;
- продукт получает только минимальный пригодный каркас и может далее развиваться отдельно;
- bootstrap использует 6-значные ID: `ROAD-000001`, `BACK-000001`, `PLAN-000001`, `PROF-000001` и аналогичные;
- bootstrap использует текущую дату выполнения, а не жёстко зашитые даты;
- из brand profile наследуются только `Брендовый_профиль` и `Язык_взаимодействия`.

## Связи
- `ADR-0009`
- `BACK-000016`
- `CHG-0009`
