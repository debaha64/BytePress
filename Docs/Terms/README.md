# Terms

## Назначение
Слой `Terms/` хранит базовую терминологию BytePress и правила её изменения.

## Состав
- `Base_Terms.md` — индекс базового словаря.
- `Term_Change_Policy.md` — порядок ввода, конфликта, замены и запрета терминов.
- `TERM-*.md` — отдельные карточки терминов.

## Целевой контракт
`Docs/Terms/` является серийным доменом.

Целевой контракт для term-files:
- filename: `Docs/Terms/TERM-<NNNNNN>-<slug>.md`
- внутренний ID: `TERM-<NNNNNN>`
- `slug`: `kebab-case`

Новые term-артефакты должны создаваться только по этому контракту.

Поддерживающие singleton files внутри `Docs/Terms/` не считаются term-card entities:
- `Docs/Terms/README.md` — navigator и карта домена;
- `Docs/Terms/Base_Terms.md` — индекс словаря;
- `Docs/Terms/Term_Change_Policy.md` — policy-файл терминологических изменений.

## Текущий слой
Актуальные term-card files уже приведены к контракту `Docs/Terms/TERM-<NNNNNN>-<slug>.md` и используют 6-значный внутренний `TERM ID`.

## Правило
Определение термина хранится только в карточке термина. Индекс и другие документы ссылаются на термин по ID.
