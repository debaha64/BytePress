# PLAN-000053 — Define verification tooling boundary

ID: PLAN-000053
Название: Зафиксировать tooling boundary verification-контура
Статус: Завершено
Связи: BACK-000065
Источник: Следующий узкий pass этапа `ROAD-000011`
Дата_создания: 2026-04-07
Дата_изменения: 2026-04-07
Основание: `Verification.md` и `Verification_Levels.md` уже описывают contract map и уровни verification-контура, но tooling boundary пока не вынесен отдельно. Нужен узкий pass, который пересоберёт `Tools/README.md` и зафиксирует роли `bp_lint`, будущего `bp_check` и будущего `bp_verify` без реализации нового toolchain.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000065
Связанные_ADR:
- отсутствуют

## Шаги
1. Синхронизировать planning-contour под новый verification pass.
   - Описание: Оставить `ROAD-000011` активным, создать одну реальную backlog-задачу и один новый current `Plan`, а предыдущий завершённый `Plan` вывести в archive.
   - DoD: `ROAD-000011`, `BACK-000065` и `PLAN-000053` согласованы как текущий stage/task/pass.
2. Провести audit verification tooling perimeter.
   - Описание: Проверить `Verification.md`, `Verification_Levels.md`, `Platform_Contracts.md`, `Tools/README.md` и `bp_lint.py` только на реальные противоречия между structural tooling, future verification tooling и procedural verification.
   - DoD: зафиксировано, какие роли должны быть описаны в tooling boundary, а какие остаются в `Docs/Technical/*` и `Pipeline/*`.
3. Пересобрать `Tools/README.md` как tooling boundary document.
   - Описание: Явно описать роль `bp_lint`, target role будущего `bp_check`, target role будущего `bp_verify`, классы checks и границы между `Tools/*` и technical contracts.
   - DoD: читателю ясно, что именно относится к structural tooling, verification tooling и procedural verification, без смешения ownership.
4. Подтвердить минимальный contract impact.
   - Описание: Проверить, нужны ли точечные updates в `Verification.md`, `Verification_Levels.md`, `Platform_Contracts.md` или `bp_lint.py`.
   - DoD: меняются только реально противоречащие линии; новые tools не реализуются.
5. Закрыть pass governance-сверкой.
   - Описание: Перевести backlog-задачу и `Plan` в финальные статусы только после согласования индекса backlog, `ROAD-000011`, текущего `Plan` и self-check.
   - DoD: `BACK-000065`, индекс backlog, `ROAD-000011`, `PLAN-000053` и self-check полностью согласованы.

## Ограничения
- без реализации `bp_check / bp_verify`;
- без рефакторинга всего `Tools/*`;
- без открытия `ROAD-000012`;
- без широкого переписывания `Docs/Technical/*`.

## Риски
- если tooling boundary останется неявным, future implementation снова смешает structural lint, contract checks и procedural verification;
- если target roles `bp_check / bp_verify` будут описаны как implementation, pass откроет преждевременный redesign toolchain;
- если расширить `bp_lint.py` без доказанной необходимости, boundary-pass превратится в изменение behavior вместо contract clarification.

## Артефакты
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/PLAN-000053-define-verification-tooling-boundary.md`
- `Plans/Archive/Plans/PLAN-000052-define-verification-levels.md`
- `Tools/README.md`
- `Docs/Technical/Verification.md`
- `Docs/Technical/Verification_Levels.md`
- `Docs/Technical/Platform_Contracts.md`
- `Tools/bp_lint.py`

## DoD
- `ROAD-000011` остаётся в `В_работе`.
- создана одна узкая задача этого pass.
- создан один current `Plan`.
- `Tools/README.md` фиксирует tooling boundary verification-контура.
- `python3 Tools/bp_lint.py --repo .` проходит.

## Результат
- `Tools/README.md` пересобран как boundary-document tooling verification contour с явным разделением ролей `bp_lint`, будущего `bp_check`, будущего `bp_verify` и procedural verification.
- `Docs/Technical/Verification_Levels.md` минимально синхронизирован ссылкой на tooling boundary.
- `Docs/Technical/Verification.md`, `Docs/Technical/Platform_Contracts.md`, `Tools/bp_lint.py` не менялись, потому что audit не подтвердил реального противоречия или contract impact.
- `bp_lint contract unaffected`
