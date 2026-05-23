# PLAN-000054 — Define verification evidence contract

ID: PLAN-000054
Название: Зафиксировать contract verification evidence
Статус: Завершено
Связи: BACK-000066
Источник: Следующий узкий pass этапа `ROAD-000011`
Дата_создания: 2026-04-08
Дата_изменения: 2026-04-08
Основание: Verification contracts уже выделены в `Verification.md`, `Verification_Levels.md` и tooling boundary, но evidence contract пока не зафиксирован как отдельный документ. Нужен узкий pass, который введёт `Docs/Technical/Verification_Evidence.md` и определит виды evidence, обязательность, storage и linkage к pass-close contour без реализации нового toolchain.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000066
Связанные_ADR:
- отсутствуют

## Шаги
1. Синхронизировать planning-contour под новый verification pass.
   - Описание: Оставить `ROAD-000011` активным, создать одну реальную backlog-задачу и один новый current `Plan`, а предыдущий завершённый `Plan` вывести в archive.
   - DoD: `ROAD-000011`, `BACK-000066` и `PLAN-000054` согласованы как текущий stage/task/pass.
2. Провести audit evidence perimeter.
   - Описание: Проверить `Verification.md`, `Verification_Levels.md`, `Artifact_Lifecycle.md`, `System_Invariants.md`, `Pipeline/Phase_Gates.md` и `Tools/README.md` только на реальные противоречия по evidence, storage и pass-close linkage.
   - DoD: зафиксировано, какие evidence requirements уже подразумеваются contracts и где нужен явный contract.
3. Ввести `Docs/Technical/Verification_Evidence.md`.
   - Описание: Создать singleton technical document на базе `Templates/Document.md` и описать evidence classes, mandatory/optional, storage и linkage к `Plan`, `Backlog`, `Roadmap` и `Logs/*`.
   - DoD: читателю ясно, что считается достаточным evidence, что является insufficient evidence и что не считается evidence.
4. Подтвердить минимальный contract impact.
   - Описание: Проверить, нужны ли точечные updates в `Verification.md`, `Verification_Levels.md`, `Artifact_Lifecycle.md`, `Pipeline/Phase_Gates.md`, `Tools/README.md` или `bp_lint.py`.
   - DoD: меняются только реально противоречащие линии; tooling не реализуется.
5. Закрыть pass governance-сверкой.
   - Описание: Перевести backlog-задачу и `Plan` в финальные статусы только после согласования индекса backlog, `ROAD-000011`, текущего `Plan` и self-check.
   - DoD: `BACK-000066`, индекс backlog, `ROAD-000011`, `PLAN-000054` и self-check полностью согласованы.

## Ограничения
- без реализации `bp_check / bp_verify`;
- без рефакторинга всего `Tools/*`;
- без открытия `ROAD-000012`;
- без широкого переписывания `Docs/Technical/*`.

## Риски
- если evidence contract останется неявным, future verification work снова смешает stdout, planning-sync и gate handoff;
- если evidence станет требовать хранения raw output в репозитории по умолчанию, это создаст шум и неустойчивую историю;
- если расширить `bp_lint.py` без доказанной необходимости, pass превратится в toolchain change вместо contract clarification.

## Артефакты
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/Archive/Plans/PLAN-000054-define-verification-evidence-contract.md`
- `Plans/Archive/Plans/PLAN-000053-define-verification-tooling-boundary.md`
- `Docs/Technical/Verification.md`
- `Docs/Technical/Verification_Levels.md`
- `Docs/Technical/Verification_Evidence.md`
- `Docs/Technical/Artifact_Lifecycle.md`
- `Docs/Technical/System_Invariants.md`
- `Pipeline/Phase_Gates.md`
- `Tools/README.md`

## DoD
- `ROAD-000011` остаётся в `В_работе`.
- создана одна узкая задача этого pass.
- создан один current `Plan`.
- `Verification_Evidence.md` фиксирует contract evidence.
- `python3 Tools/bp_lint.py --repo .` проходит.

## Результат
- `Docs/Technical/Verification_Evidence.md` создан как singleton contract verification evidence: evidence classes, обязательность, storage и linkage к pass-close contour.
- `Docs/Technical/Verification.md` и `Docs/Technical/Verification_Levels.md` минимально синхронизированы ссылками на evidence contract.
- `Artifact_Lifecycle.md`, `System_Invariants.md`, `Pipeline/Phase_Gates.md`, `Tools/README.md` и `bp_lint.py` не менялись, потому что audit не подтвердил реального противоречия или contract impact.
- `bp_lint contract unaffected`
