# Tools

`Tools/` содержит детерминированные инструменты `BytePress`.

## Принципы
- инструмент выполняет воспроизводимую операцию;
- инструмент не подменяет роль и не хранит системное знание;
- инструмент работает с файлами и контрактами `BytePress`;
- инструмент не требует конкретной модели;
- инструмент может использоваться как внутри самой системы, так и при инициализации продукта.

## Набор `0.1.0`
- `bp_lint.py` — проверка структуры `BytePress` и базового bootstrap-контракта продуктового репозитория;
- `bp_bootstrap.py` — генерация минимального продуктового каркаса по контракту `BytePress`;
- `bp_normalize_terms.py` — проверка карточек терминов и пересборка индекса `Base_Terms.md`.

## Актуальный bootstrap contract
- `bp_bootstrap.py` требует `--name`, `--product-code`, `--brand-profile`, `--target`;
- `--product-code` обязателен, содержит 2-3 символа верхнего регистра и не генерируется автоматически;
- `--brand-profile` обязателен и валидируется по существующим brand profiles в `BytePress`;
- bootstrap создаёт канонический минимальный продуктовый слой `Docs/Product/README.md`, `Docs/Product/JTBD.md`, `Docs/Product/PRD.md`, `Docs/Product/Delivery.md`;
- bootstrap создаёт `Profiles/Product.md` и initial plan file `Plans/<PRODUCT_CODE>-000001-product-initialization.md`;
- `bp_lint.py` требует `Templates/Delivery.md` в `BytePress` и проверяет наличие полного минимального `Docs/Product/*` набора в product repo;
- `bp_lint.py` требует `Docs/Discovery/README.md`, `Docs/Discovery/Interview.md` и `Templates/Interview.md` в `BytePress`;
- bootstrap использует 6-значные ID и текущую дату выполнения, без жёстко прошитых дат;
- из brand profile наследуются только `Брендовый_профиль` и `Язык_взаимодействия`.

## Связи
- `ADR-000007`
- `ADR-000009`
- `CHG-000007`
- `CHG-000009`
