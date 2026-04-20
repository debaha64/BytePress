# PLAN-000071 — Enforce first product-pass gating

ID: PLAN-000071
Название: Enforce first product-pass gating
Статус: Завершено
Связи: BACK-000083
Источник: Corrective pass after repeated `Minesweeper` field-test defects
Дата_создания: 2026-04-20
Дата_изменения: 2026-04-20
Основание: Повторный полевой тест generated product repo подтвердил оставшиеся first-pass defects: агент мог самозаполнять discovery interview, начинать write-pass без ответов пользователя, писать напрямую в `develop`, а bootstrap-created initial planning contour всё ещё подталкивал к раннему implementation вместо discovery-only старта.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000083
Связанные_ADR:
- отсутствуют

## Шаги
1. Синхронизировать planning-layer и зафиксировать corrective stage/pass.
   - DoD: для pass использованы `ROAD-000019`, `BACK-000083` и `PLAN-000071`, а stage закрывается в одном archive-consistent contour без residual active backlog.
2. Зафиксировать hard-gates первого product-start pass в contracts, discovery-layer и generated product `AGENTS.md`.
   - DoD: startup-handshake остаётся обязательным и наблюдаемым; self-answering discovery interview запрещён; до ответов пользователя write-изменения в product truth, planning, logs и code запрещены; direct writes в `main` / `develop` запрещены.
3. Перестроить initial planning contour generated product repo и синхронизировать bootstrap/lint.
   - DoD: bootstrap-created `ROAD-000001`, `BACK-000001` и `PLAN-000001` описывают discovery-only / write-later route, а `bp_lint.py` валидирует новый gating contract как в core repo, так и в generated product repo.
4. Подтвердить контур реальным smoke bootstrap.
   - DoD: `python3 Tools/bp_bootstrap.py --name Minesweeper --product-code MS --brand-profile Speculorg --target /tmp/bytepress-first-pass-gating-Fd6CMn/repo` и `python3 Tools/bp_lint.py --repo /tmp/bytepress-first-pass-gating-Fd6CMn/repo` проходят, а generated repo содержит новый gated startup contour без раннего implementation push.

## Ограничения
- не расширять release contour;
- не открывать новый широкий домен beyond bootstrap/discovery/planning/lint sync;
- не подменять hard-gates мягкими рекомендациями;
- не смешивать corrective pass с предметной разработкой `Minesweeper`.

## Артефакты
- `AGENTS.md`
- `Docs/Discovery/*`
- `Docs/Technical/Product_Bootstrap_Contract.md`
- `Docs/Technical/Product_Bootstrap_Validation.md`
- `Docs/Technical/Artifact_Lifecycle.md`
- `Templates/Interview.md`
- `Skills/Interview.md`
- `Tools/bp_bootstrap.py`
- `Tools/bp_lint.py`
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/Archive/Backlog/ROAD-000019.md`
- `Plans/Archive/PLAN-000071-enforce-first-product-pass-gating.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`

## DoD
- первый запуск нового продукта стал discovery-only по канону;
- self-answering interview явно запрещён;
- до ответов пользователя writes явно запрещены;
- writes в `main` / `develop` явно запрещены;
- startup-handshake остался обязательным;
- bootstrap initial planning contour перестроен правильно;
- lint валидирует новый product-start gating contour;
- smoke bootstrap проходит;
- no residual contradiction между contracts, bootstrap, generated repo и lint.

## Результат
- `ROAD-000019` / `BACK-000083` / `PLAN-000071` закрыты в одном corrective pass без открытия нового release contour.
- `AGENTS.md`, active discovery docs, bootstrap/validation contracts, `Templates/Interview.md`, `Skills/Interview.md`, `Tools/bp_bootstrap.py` и `Tools/bp_lint.py` синхронизированы вокруг hard-gating первого product-start pass.
- Generated product repo теперь materialize явный startup-handshake, discovery-only interview route, запрет self-answering, запрет write-изменений до ответов пользователя и запрет direct writes в `main` / `develop`.
- Initial `ROAD/BACK/PLAN` generated product repo больше не подталкивают к немедленному implementation-pass и вместо этого ведут к отдельному первому write-pass после подтверждённого discovery.
- Реальный bootstrap smoke в `/tmp/bytepress-first-pass-gating-Fd6CMn/repo` и `python3 Tools/bp_lint.py --repo /tmp/bytepress-first-pass-gating-Fd6CMn/repo` подтвердили отсутствие residual contradiction в corrective scope.
