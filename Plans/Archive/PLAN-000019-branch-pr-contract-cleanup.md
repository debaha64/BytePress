# PLAN-000019 — Branch and PR contract cleanup

ID: PLAN-000019
Название: Завершить process-contract для task-branch, push, PR и gh fallback
Статус: Завершено
Связи: BACK-000027, CHG-000031, QL-000026
Источник: Process-cleanup pass после repo-wide audit активного слоя
Дата_создания: 2026-03-28
Дата_изменения: 2026-03-28
Основание: В активном слое BytePress уже закреплены отдельные части branch/PR workflow, но process-facing карты и platform contract ещё не описывают одним коротким и непротиворечивым порядком локальные коммиты, момент final push, создание PR, `gh` diagnostics и fallback без автоматической переавторизации.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000027
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать управляемый контур прохода.
   - Описание: Перевести `BACK-000027` в `В_работе`, уточнить его process-scope и создать отдельный plan-file.
   - DoD: `Plans/Backlog.md` и `Plans/BP-000019-branch-pr-contract-cleanup.md` отражают фактическую задачу без расширения области.
2. Синхронизировать process-contract.
   - Описание: Минимально обновить `AGENTS.md`, `Setup_Guide.md`, `Docs/Technical/Platform_Contracts.md` и `Plans/README.md` только там, где не хватает единого алгоритма `develop -> task branch -> local commits -> self-check -> final push -> PR`.
   - DoD: process-facing документы согласованно фиксируют `gh` diagnostics, fallback без автопереавторизации и правило не использовать `--dry-run`, если флаг не поддерживается.
3. Удалить остаточный process-noise.
   - Описание: Убрать оставшиеся ссылки `Plans/PLAN-*.md` из активных ролей и обновить только минимальный follow-up в `Skills/*` или `Plans/README.md`, если он нужен для устранения явной двусмысленности.
   - DoD: активный слой не содержит остаточных process-формулировок, которые противоречат текущему канону.
4. Закрыть plan/backlog и журналы.
   - Описание: Обновить `ChangeLog` и `QualityLog`, а `ADR` создавать только при появлении нового устойчивого архитектурного решения.
   - DoD: `python3 Tools/bp_lint.py --repo .` проходит, `BACK-000027` переведён в финальный статус по факту результата, а `bp_lint.py` меняется только при доказанном изменении обязательного contract.

## Риски
- попытка расширить проход до полного process-doc rewrite выведет задачу за пределы согласованного scope;
- необоснованное изменение `bp_lint.py` создаст лишний contract drift вместо фиксации факта, что обязательный contract не изменился;
- правки historical layer, release governance или несвязанных доменов смешают process-cleanup с большим audit-pass.

## Артефакты
- `Plans/Backlog.md`
- `Plans/BP-000019-branch-pr-contract-cleanup.md`
- `AGENTS.md`
- `Setup_Guide.md`
- `Docs/Technical/Platform_Contracts.md`
- `Plans/README.md`
- `Roles/Developer.md`
- `Roles/QA.md`
- `Roles/Release.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`

## DoD
- `BACK-000027` отражает актуальный process-scope.
- `AGENTS.md`, `Setup_Guide.md` и `Docs/Technical/Platform_Contracts.md` согласованы по task-branch, local commits, self-check, final push, PR и `gh` fallback.
- остаточные ссылки `Plans/PLAN-*.md` удалены из активного слоя там, где они ещё оставались.
- `Plans/README.md` не содержит устаревшей конкретики о текущем диапазоне plan-files.
- `bp_lint.py` меняется только если process-pass реально меняет обязательный contract; иначе фиксируется `bp_lint contract unaffected`.

## Фактический результат
- `AGENTS.md`, `Setup_Guide.md` и `Docs/Technical/Platform_Contracts.md` теперь согласованно фиксируют один процесс: `develop -> task branch -> серия локальных коммитов -> self-check после каждого коммита -> final push -> проверка существующего PR -> создание PR`.
- В process-contract добавлены правило не использовать `--dry-run`, если его не поддерживает текущий `gh`, и fallback без автоматической переавторизации при ошибке `gh`.
- `Plans/README.md` очищен от устаревшей привязки к конкретному диапазону `BP-000001 ... BP-000006`.
- В `Roles/Developer.md`, `Roles/QA.md` и `Roles/Release.md` удалены остаточные ссылки `Plans/PLAN-*.md`; follow-up в `Skills/*` не потребовался.
- `bp_lint.py` не менялся, потому что обязательные пути, шаблоны и домены в этом проходе не изменялись.
