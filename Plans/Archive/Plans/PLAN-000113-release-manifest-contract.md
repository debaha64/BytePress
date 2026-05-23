# PLAN-000113 — Manifest-договор release archive

ID: PLAN-000113
Название: Manifest-договор release archive
Статус: Завершено
Связи: ROAD-000047, BACK-000125, CHG-000125, QL-000120
Источник: Запрос владельца от 2026-05-24
Дата_создания: 2026-05-24
Дата_изменения: 2026-05-24
Основание: Владелец запросил закрепить manifest-договор release archive и zip-пакета без создания zip-архивов и без manifest конкретных релизов.
Связанные_требования:
- Определить состав release manifest.
- Определить связь manifest с logs, tag, commit, `ROAD/BACK/PLAN` и проверками.
- Определить условия, при которых допустим zip-пакет.
- Не создавать zip-архивы.
- Не создавать release manifest для конкретных версий.
- Подготовить следующий проход для manifest релизов `0.1.0`, `0.2.0`, `0.3.0`.
- Не удалять и не архивировать `Logs`, `Rules`, `Pipeline`, `Docs`, `Templates`, `Schemas`, `Tools`.
- Не менять product bootstrap.
- Не начинать `ROAD-000048`.
- Не расширять `bp_check.py` и `bp_lint.py` без необходимости.
Связанные_backlog:
- BACK-000125
Связанные_ADR:
- ADR-000028 не создан
Артефакты:
- `Plans/Archive/Releases/README.md`
- `Plans/Archive/Releases/MANIFEST_TEMPLATE.md`
- `Plans/README.md`
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/Archive/Backlog/ROAD-000047.md`
- `Docs/Technical/Verification.md`
- `Docs/Technical/Artifact_Lifecycle.md`
- `Pipeline/Workflows.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`
Риски:
- Исторические release facts для `0.1.0`, `0.2.0`, `0.3.0` уже есть в `Logs/ReleaseLog.md`, но manifest конкретных выпусков создаётся отдельным следующим проходом, чтобы не смешивать договор и заполнение архива.
Определение_готовности:
- Release manifest описан как проверяемый мост, который не заменяет `ReleaseLog`, `ChangeLog`, `QualityLog` и tag.
- Состав manifest включает версию, tag, release commit, release PR, post-release sync PR, `ROAD/BACK/PLAN`, `CHG/QL/RL`, выполненные проверки, непроверенные зоны, состав release package и решение по zip.
- Zip допустим только как проверяемый исторический пакет, не является текущим источником истины, имеет manifest и проверку состава.
- Крупные бинарные архивы не допускается добавлять в репозиторий без отдельного решения владельца.
- Следующий проход для manifest релизов `0.1.0`, `0.2.0`, `0.3.0` подготовлен без создания этих manifest.
- `ROAD-000047`, `BACK-000125` и `PLAN-000113` согласованы.
- Выполнены `git diff --check`, `python3 Tools/bp_lint.py --repo .`, `python3 Tools/bp_check.py --repo .` и `python3 Tools/bp_check.py --repo . --format json`.

## Шаги
1. Открыть плановый контур.
   - Описание: Завести `BACK-000125` и текущий `PLAN-000113` внутри активного `ROAD-000047`.
   - Определение_готовности: `Plans/Roadmap.md`, `Plans/Backlog.md` и `PLAN-000113` согласованы.
2. Закрепить manifest-договор.
   - Описание: Уточнить `Plans/Archive/Releases/README.md` и при необходимости добавить шаблон manifest.
   - Определение_готовности: Manifest связывает release facts, planning facts, checks, package composition и zip decision без подмены журналов и tag.
3. Синхронизировать lifecycle, verification и workflow.
   - Описание: Обновить только те owner-documents, где manifest/zip меняет проверочный, lifecycle или process contract.
   - Определение_готовности: `Docs/Technical/Verification.md`, `Docs/Technical/Artifact_Lifecycle.md` и `Pipeline/Workflows.md` не спорят с release archive.
4. Закрыть проход.
   - Описание: Добавить `CHG-000125` и `QL-000120`, выполнить проверки и архивировать `PLAN-000113`.
   - Определение_готовности: Журналы содержат факты, проверки пройдены, `BACK-000125` и `PLAN-000113` завершены, `ROAD-000047` остаётся `В_работе` до следующего manifest-заполнения.

## Итог
`BACK-000125` и `PLAN-000113` завершены. Release manifest закреплён как проверяемый мост между release package, `Logs/ReleaseLog.md`, `Logs/ChangeLog.md`, `Logs/QualityLog.md`, tag, release commit, release PR, post-release sync PR, `ROAD/BACK/PLAN`, проверками, непроверенными зонами и решением по zip. Добавлен `Plans/Archive/Releases/MANIFEST_TEMPLATE.md`.

Zip-файлы не создавались. Manifest конкретных версий не создавались. Zip допустим только как проверяемый исторический package с manifest и проверкой состава; крупный бинарный zip не добавляется в репозиторий без отдельного решения владельца. Следующий проход внутри `ROAD-000047` должен создать manifest для `0.1.0`, `0.2.0` и `0.3.0` по закреплённому договору. `ROAD-000048` не начат. `ADR-000028` не создан, потому что новое архитектурное решение не принималось.
