# PLAN-000037 — Migrate remaining governance ID layer

ID: PLAN-000037
Название: Закрыть remaining governance/supporting `ID` tail для `Profiles/*`
Статус: Завершено
Связи: BACK-000049
Источник: Narrow remaining governance/supporting migration pass inside `ROAD-000009`
Дата_создания: 2026-04-07
Дата_изменения: 2026-04-07
Основание: После предыдущего pass active governance/supporting layer уже синхронизирован для `Rules/*`, `Standards/*`, `Templates/*` и `Schemas/*`, но remaining diagnostics всё ещё оставляет не до конца разведённый contract для `Profiles/*` и support-files вокруг `Docs/Terms/*`: profiles требуют явной фиксации hybrid filename/path-contract, а `Docs/Terms/*` требуют разведения serial term-card files и singleton support-files без открытия новых доменных моделей. Нужен отдельный pass, который закроет именно этот remaining tail без redesign других доменов.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000049
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать scope remaining governance/supporting pass внутри `ROAD-000009`.
   - Описание: Добавить одну реальную backlog-задачу и один новый текущий `Plan` только для `Profiles/*` и доказанно remaining active domains.
   - DoD: `BACK-000049` и `PLAN-000037` описывают только закрытие remaining migration-tail без открытия других доменов.
2. Применить минимальную migration model к remaining domains.
   - Описание: Довести `Profiles/*` до фактически реализованного hybrid contract и затронуть другие active domains только если диагностика доказывает реальное рассогласование.
   - DoD: migrated files и path-contract больше не спорят с `Standards/Naming.md`.
3. Синхронизировать только реально затронутые ссылки и support contracts.
   - Описание: Обновить только те active docs и tools, где migration меняет path/reference ожидания или снимает контрактное противоречие.
   - DoD: active-layer не содержит broken ссылок и не держит двусмысленность между filename/path и внутренними `ID`.
4. Подтвердить границы tooling contract.
   - Описание: Оценить влияние на `bp_lint.py` и `bp_bootstrap.py` и менять их только при доказанной необходимости.
   - DoD: tooling синхронизирован только если remaining migration реально меняет обязательный contract.
5. Закрыть pass governance-сверкой.
   - Описание: Перевести backlog-задачу и `Plan` в финальные статусы только после согласования индекса, связей и локальных проверок.
   - DoD: `BACK-000049`, индекс backlog, `ROAD-000009`, текущий `Plan` и self-check полностью согласованы.

## Ограничения
- без migration `ID` для `Docs/Product/*`, `Docs/Discovery/*`, `Docs/Technical/*`, `Docs/User/*`, `Adapters/*`, `Memory/*`, `Pipeline/*`, `MCP/*` и других доменов вне доказанного remaining governance/supporting scope;
- без изменения active/archive layout для `Plans` и backlog archive-layer;
- без широкого переписывания `Docs/Technical/*`, `AGENTS.md` и `Docs/User/*`;
- без создания новой модели `ID` сверх уже утверждённой unified `ID scheme`.

## Риски
- если трактовать already-synced domains как remaining, pass превратится в лишний redesign;
- если не развести hybrid artifact files и singleton support-files внутри governance/supporting layer, naming-contract останется формально противоречивым;
- если затронуть bootstrap или lint без реальной необходимости, появится лишнее расхождение между implemented contract и scope этого pass.

## Артефакты
- `Plans/Backlog.md`
- `Plans/Roadmap.md`
- `Plans/Archive/Plans/PLAN-000037-migrate-remaining-governance-id-layer.md`
- `Profiles/*`
- `Docs/Terms/*`
- `Standards/Naming.md`
- `Tools/bp_lint.py`
- `Tools/bp_bootstrap.py`

## DoD
- создана одна узкая backlog-задача только для migration remaining active governance/supporting domains.
- создан новый текущий `Plan` только под этот pass.
- `Profiles/*` приведены к unified `ID scheme` в реально необходимом объёме.
- другие remaining domains затронуты только при доказанном рассогласовании.
- `python3 Tools/bp_lint.py --repo .` проходит.

## Результат
- `Profiles/*` доведены до implemented hybrid contract без migration semantic filenames: внутренние `PROF-*` сохранены, а ссылочные списки `Активные_*` и `Резервные_*` нормализованы на canonical `ID`.
- `Docs/Terms/*` не потребовал file migration: `TERM-*` уже соответствовали serial contract, а singleton support-files внутри домена явно разведены с term-card layer.
- `Roles/*` дополнительной migration не потребовал: domain уже соответствовал singleton contract и использовал canonical internal `ROLE-*`.
- `Tools/bp_lint.py` минимально синхронизирован с новым profile-reference contract; `bp_bootstrap.py` не затронут, потому что filename/path generation не менялся.

bp_lint contract affected
