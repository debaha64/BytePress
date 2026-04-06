# Naming

## Версии
Версии оформляются в формате `MAJOR.MINOR.PATCH`.

Текущая baseline-version `BytePress`: `0.1.0`.

Активные документы используют semver, а не метки вида `vN`, когда речь идёт о текущем operational contract системы.

Semver применяется к текущему operational contract `BytePress`, а не к rewrite истории журналов.

## ID сущностей
Числовая часть ID содержит 6 знаков.

Типовой префикс сущности сохраняется:
- `PLAN-000001`
- `BACK-000001`
- `ADR-000001`
- `CHG-000001`
- `PROF-000001`

Целевая `ID scheme` описывает не только формат самого `ID`, но и то, где он обязан находиться:
- только во внутреннем содержимом артефакта;
- только в filename не используется;
- одновременно во внутреннем содержимом и в filename для serial domains.

## Имена файлов и путей
Имена файлов и путей строятся по семантике домена и не дублируют родительский контекст без необходимости.

`slug` оформляется в `kebab-case`.

Имя файла не должно дублировать родительский каталог.

## Классы артефактов по модели идентификации
Домены делятся на три класса:
- `serial domains` — каждый артефакт имеет serial `ID` и обязан нести его одновременно во внутреннем содержимом и в filename;
- `hybrid domains` — filename остаётся семантическим, но внутренний `ID` обязателен;
- `singleton domains` — filename остаётся семантическим и serial `ID` в filename не требуется; внутренний `ID` задаётся только там, где это требует контракт конкретного singleton-артефакта.

### Serial domains
Для serial domains serial `ID` обязателен и в filename, и внутри содержимого артефакта.

Целевой filename-contract для serial domains:

`<DOMAIN>/<PREFIX>-<NNNNNN>-<slug>.md`

Где:
- `PREFIX` совпадает с типовым префиксом сущности;
- `NNNNNN` — 6-значная числовая часть `ID`;
- `slug` оформляется в `kebab-case`.

Целевые serial domains в текущем репозитории:
- `Plans/`: активный текущий `Plan` хранится как `Plans/PLAN-<NNNNNN>-<slug>.md`, завершённые `Plan` хранятся как `Plans/Archive/PLAN-<NNNNNN>-<slug>.md`
- `Docs/Terms/`: `Docs/Terms/TERM-<NNNNNN>-<slug>.md`

Для serial domains:
- внутренний `ID` обязан совпадать с `ID`, выраженным в filename;
- прямые ссылки между документами по смыслу идут через внутренний `ID`;
- filename/path добавляется тогда, когда нужно открыть конкретный файл или когда ссылка используется как файловая навигация.

### Hybrid domains
Для hybrid domains serial `ID` в filename не нужен; filename остаётся семантическим, но внутренний `ID` обязателен.

Целевые hybrid domains:
- `Profiles/`
- `Schemas/`
- `Templates/`

Для hybrid domains:
- filename выражает семантическую роль артефакта;
- внутренний `ID` остаётся каноническим идентификатором для ссылок и зависимостей;
- ссылка по одному внутреннему `ID` обычно достаточна, а filename/path добавляется только для навигации или когда semantic filename важен сам по себе.

### Singleton domains
Singleton domains не используют serial `ID` в filename и не масштабируются как serial-реестр файлов.

Целевые singleton domains:
- `Rules/`
- `Standards/`
- `Roles/`
- `Skills/`
- `Adapters/`
- `Memory/`
- `MCP/`
- singleton-документы верхнего уровня, такие как `Plans/Roadmap.md`, `Plans/Backlog.md`, `Logs/ADRlog.md`, `Logs/ChangeLog.md`, `Logs/QualityLog.md`

Для singleton domains:
- semantic filename является каноническим способом локализации файла;
- внутренний `ID` используется там, где singleton-артефакт является нормируемой сущностью;
- serial `ID` в filename не требуется и не вводится по умолчанию.

Исторический backlog прошлых этапов использует stage-keyed archive path contract:
- `Plans/Archive/Backlog/ROAD-<NNNNNN>.md`

Этот archive contract не делает `Backlog` serial domain: активный backlog остаётся singleton-файлом `Plans/Backlog.md`, а archive files служат stage-scoped historical records.

## Правила ссылок и упоминания ID
- Внутренний `ID` является канонической ссылкой на сущность в текстах, связях и зависимостях.
- Для serial domains ссылка по `ID` является основной; filename/path добавляется только когда нужна файловая навигация или указание конкретного serial-файла.
- Для hybrid domains каноническая смысловая ссылка идёт по внутреннему `ID`, а semantic filename может использоваться как вспомогательный путь к файлу.
- Для singleton domains ссылка на semantic path допустима как навигационная; если у singleton-артефакта есть внутренний `ID`, в контрактных связях предпочтителен именно он.
- Внутренние ссылки не должны подменять `ID` свободным текстом там, где у сущности уже есть канонический `ID`.

## Целевая схема и transitional state
Целевая схема:
- новые serial-артефакты создаются только по serial filename-contract;
- новые hybrid-артефакты создаются только с semantic filename и обязательным внутренним `ID`;
- singleton domains сохраняют semantic filenames и не переводятся на serial filename без отдельного решения.

Transitional legacy-state:
- transitional state не меняет целевую схему и не разрешает создавать новые legacy-артефакты там, где уже определён target contract.

## Политика фазной миграции
Migration `ID scheme` в `BytePress` выполняется полностью, но доменно и фазами.

Принципы:
- новые артефакты создаются только по целевому контракту своего класса;
- legacy-слой мигрируется отдельными управляемыми pass, а не одним массовым rewrite;
- migration policy не означает немедленную физическую перестройку всего historical слоя;
- прямые зависимости домена нормализуются вместе с целевой фазой migration, а не заранее по всему репозиторию.

Целевой порядок будущей migration по доменам:
1. `planning contour`: завершено для plan-files, archive layout и backlog history-layer; active `Backlog.md` и `Plans/Archive/Backlog/ROAD-<NNNNNN>.md` уже приведены к целевому contract.
2. `logs`: serial и внутренние `ID` журнальных сущностей и прямые ссылки на них.
3. `rules / standards / templates / schemas`: выравнивание внутренних `ID`, semantic filenames и ссылочного слоя.
4. остальные домены: `Profiles/` и прочие hybrid/singleton domains, которые ещё требуют синхронизации под общую схему.

Домены, уже приведённые к целевой схеме, не открываются повторно без отдельного pass на доказанное рассогласование.

## Рабочие ветки
Формат рабочей ветки: `<type>/<NNNNNN>-<slug>`.

Допустимые `type`:
- `feat`
- `fix`
- `chore`
- `docs`
- `refactor`
- `release`
- `hotfix`
