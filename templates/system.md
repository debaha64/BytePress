# SYSTEM.md

Применение: [sops/system-editing.md](../sops/system-editing.md).

## Домены

{{Точные пути и их назначение.}}

## Инварианты

{{ID, правило и канонический владелец смысла.}}

## Полномочия и защищённые поверхности

{{Границы ролей и ссылки на процедурных владельцев.}}

## Машинные проекции

{{Только проекции принятых контрактов с прямыми потребителями.}}

## Реестр защищённых поверхностей

Форма материализуется в SYSTEM создаваемого Workspace; `<Slug>` заменяется Slug из Project Profile. Единственный canonical owner реестра — полученный SYSTEM.md. `pre-implementation` запрещает изменения Product до завершённого implementation gate; `exact-wplan` требует точного исключения активного WPLAN. Machine contract: одна таблица `Path | Protection`, уникальные bounded paths и указанные ниже обязательные строки. Дополнительные защищённые пути сохраняют одну из этих политик.

registry:protected-surfaces

| Path | Protection |
|---|---|
| `<Slug>/**` | `pre-implementation` |
| `AGENTS.md` | `exact-wplan` |
| `SYSTEM.md` | `exact-wplan` |
| `sops/**` | `exact-wplan` |
| `roles/**` | `exact-wplan` |
| `skills/**` | `exact-wplan` |
| `templates/**` | `exact-wplan` |
| `tools/**` | `exact-wplan` |
