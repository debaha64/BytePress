# PLAN-000040 — Clarify technical contract map

ID: PLAN-000040
Название: Уточнить карту системных контрактов technical-layer
Статус: Завершено
Связи: BACK-000052
Источник: Следующий узкий pass этапа `ROAD-000010`
Дата_создания: 2026-04-07
Дата_изменения: 2026-04-07
Основание: После boundary-pass `ROAD-000010` границы и минимальное ядро `Docs/Technical/*` уже зафиксированы, но active layer всё ещё не разводит поимённо обязательные и вспомогательные technical-documents, а пересечение между `Docs/Technical/Pipeline.md` и `Pipeline/*` остаётся недостаточно явным. Нужен отдельный узкий pass, который оформит именно contract map technical-layer без широкого переписывания technical-documents.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000052
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать текущий contract-map pass внутри `ROAD-000010`.
   - Описание: Добавить одну реальную backlog-задачу и один новый текущий `Plan` только для уточнения contract map technical-layer.
   - DoD: `ROAD-000010`, `BACK-000052` и `PLAN-000040` согласованы как текущий stage/task/pass.
2. Провести audit technical-layer и process-layer.
   - Описание: Проверить `Docs/Technical/*` и `Pipeline/*` на required/supporting composition и на remaining смысловые пересечения.
   - DoD: подтверждены required core, supporting layer и места допустимого пересечения между доменами.
3. Зафиксировать contract map без redesign.
   - Описание: Обновить главный entrypoint technical-layer и только минимально необходимые прямые references.
   - DoD: для каждого current technical-document понятны его роль, обязательность и граница относительно `Pipeline/*`.
4. Подтвердить tooling contract.
   - Описание: Проверить, нужен ли update `bp_lint.py`.
   - DoD: tooling меняется только если contract-map реально меняет обязательный check.
5. Закрыть pass governance-сверкой.
   - Описание: Перевести backlog-задачу и `Plan` в финальные статусы только после согласования индекса backlog, `ROAD-000010`, текущего `Plan` и self-check.
   - DoD: `BACK-000052`, индекс backlog, `ROAD-000010`, `PLAN-000040` и self-check полностью согласованы.

## Ограничения
- без широкого рефакторинга `Docs/Technical/*`;
- без массового переписывания существующих technical-documents;
- без создания нового домена или нового technical-document без доказанной необходимости;
- без открытия `ROAD-000011`.

## Риски
- если required core и supporting layer не развести явно, следующий pass будет заново спорить о составе technical-layer;
- если начать переписывать `Docs/Technical/Pipeline.md` как новый process canon, pass потеряет узкий scope и дублирует `Pipeline/*`;
- если менять standards или lint без фактической необходимости, contract-map pass расползётся за пределы задачи.

## Артефакты
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/Archive/Plans/PLAN-000040-clarify-technical-contract-map.md`
- `Docs/Technical/README.md`
- `Docs/Technical/Pipeline.md`
- `Pipeline/README.md`
- `Pipeline/Artifacts.md`
- `Tools/bp_lint.py`

## DoD
- создана одна узкая backlog-задача только для карты системных контрактов technical-layer.
- создан новый текущий `Plan` только под этот pass.
- `Docs/Technical/README.md` фиксирует required ядро и карту документов technical-layer.
- разведение `Docs/Technical/*` и `Pipeline/*` описано ясно и без новой двусмысленности.
- `python3 Tools/bp_lint.py --repo .` проходит.

## Результат
- `Docs/Technical/README.md` теперь явно делит current technical-documents на required core и supporting layer и фиксирует роль каждого документа в слое.
- `Docs/Technical/Pipeline.md` возвращён к supporting technical view: из active layer убран дублирующий process-canon, а приоритет `Pipeline/*` как process-domain закреплён явно.
- дополнительные изменения в `Standards/*`, `Plans/README.md` и `bp_lint.py` не потребовались: audit не подтвердил реального contract contradiction за пределами entrypoint technical-layer и его supporting pipeline view.
- `bp_lint contract unaffected`
