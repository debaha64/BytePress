# Жизненный цикл артефактов

Product Unit хранит планы, журналы, документы, SOP, шаблоны, инструменты и при необходимости кодовые слои.

## Правила

1. Управляющий контур находится в `plans/` и `logs/`.
2. Исторические completed PLAN другого проекта не переносятся.
3. Exact disposable set состоит из каталогов `__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, суффиксов `.pyc`, `.pyo`, `.tmp`, `.temp`, `.orig` и точного glob `*:Zone.Identifier`.
4. Generic `*.Identifier` не является disposable pattern и сохраняется как обычный durable path.
5. `.agents/` и `.codex/` являются opt-in local-service paths. В `.codex/` raw logs и clean logs с действующей runtime-ссылкой являются durable evidence и сохраняются при cleanup.
6. Выпуск, tag, архив выпуска и архив исследования относятся к отдельным решениям владельца.

Процедуры описаны в [../../sops/sot.md](../../sops/sot.md), [../../sops/project-management.md](../../sops/project-management.md) и [../../sops/clean-exit.md](../../sops/clean-exit.md).
