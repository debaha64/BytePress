# Profiles

## Назначение
Профиль — верхняя единица организации и режима.

## Brand и product profiles
- `brand profile` хранится только в `BytePress` и выбирается через параметр bootstrap `--brand-profile`;
- `product profile` хранится только в product repo в файле `Profiles/Product.md`;
- bootstrap валидирует существование выбранного brand profile в `BytePress`, но не копирует его целиком в продукт.

## Минимальное наследование в product repo
Из brand profile в product repo наследуются только:
- `Брендовый_профиль`
- `Язык_взаимодействия`

## Product profile `v1`
`Profiles/Product.md` хранит минимально нужные поля:
- `ID`
- `Тип_профиля: product`
- `Название`
- `Код_продукта`
- `Брендовый_профиль`
- `Язык_взаимодействия`

## Чего product profile сейчас не наследует
- роли;
- правила;
- стандарты;
- навыки;
- адаптеры;
- историю и журналы.
