# MCP

`MCP/` хранит канонический contour подключений и политики интеграции `BytePress`.

## Назначение
- зафиксировать, зачем системе нужен слой подключений;
- развести файловый источник истины и внешние инструменты;
- подготовить реестр допустимых подключений и границы их использования.

## Статус `0.2.0`
В `0.2.0` домен активен как controlled connector contour: он задаёт policy, interfaces и registry допустимых connector classes, но по-прежнему не открывает реальные внешние подключения.

## Участие в lifecycle
`MCP/` участвует только когда pass затрагивает integration contour, connector policy или controlled handoff через `Tools/*` и generated product repo. В обычном task-pass домен не становится активным источником данных и не подменяет файловую модель репозитория.

## Границы
- `MCP/` не является источником истины;
- `MCP/` не подменяет файловый репозиторий, `Adapters/` и knowledge-domains.
- `MCP/` не materialize runtime connectors сам по себе и не переносится bootstrap'ом внутрь generated product repo.

## Состав домена
- `Policy.md` — общая политика подключений;
- `Interfaces.md` — controlled connector handoff model;
- `Registry.md` — реестр кандидатов и статусов подключения.
