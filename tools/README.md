# Справочник команд Harness

Команды запускаются через `python3 -B`. `--help` показывает синтаксис; stdout содержит результат, диагностический stderr не является результатом проверки. Технический PASS не принимает продукт и не разрешает запись. Product-инструменты защищённого исходника проверяются только на свежей внешней копии по [verify-work](../sops/verify-work.md).

## Команды, модули и испытательные средства

| Имя | Назначение и область | Чтение/запись |
|---|---|---|
| `check_workspace.py` | Workspace, Profile, маршрут, ссылки, исходный и фактический состав | Только чтение; не исполняет Product |
| `check_product.py` | Состав Product из Profile; по явному запросу — объявленные проверки продукта | По умолчанию чтение; native-команда может писать в пределах разрешённого продукта |
| `new_project.py` | Создание нового Workspace из distribution; остаётся в distribution | `preview` читает; `apply` создаёт целевой Workspace через промежуточный каталог |
| `clean_product.py` | Временные остатки статической Product Unit BytePress; остаётся в distribution | По умолчанию чтение; `--apply` удаляет выбранные остатки |
| `release_preflight.py` | Отдельная проверка выпускных свидетельств и последующее контрольное чтение | Чтение локальных входов и, когда разрешено контрактом, сети; внешних записей нет |

`project_profile.py` — **библиотечный модуль**, не команда. Он владеет разбором schema v1, проверкой состава/версии и канонической сериализацией. Проверяющие инструменты и Project Start используют его; `check_profile.py` и копии parser отсутствуют. `tests/test_*.py` — определения испытаний, не пользовательские команды. Запускатель продуктовых прогонов и приватные навыки конкретного Workspace в Product не поставляются.

## check_workspace.py

Проверяет короткий `WORK_CONTRACT: v1` и совместимо читает прежний `SDLC_TRANSITION: v1`. Условия действий принадлежат [phase-gates](../docs/technical/phase-gates.md); роль или технический PASS не создают полномочий.

| Аргумент | Смысл и сочетания |
|---|---|
| `--workspace PATH` | Обязательный корень Workspace |
| `--format text\|json` | По умолчанию text; JSON пригоден для прямых потребителей, включая ошибки аргументов |
| `--print-baseline-manifest` | Только полный исходный TSV на stdout; несовместим с другими manifest, `--check-result`, регистрациями и JSON |
| `--baseline-manifest FILE` | Полный состав до записей; проверка фактической дельты по точным разрешениям WPLAN |
| `--preservation-manifest FILE` | Дополнительная независимая проверка сохранённых файлов/каталогов/префиксов; совместима с baseline |
| `--registration-input FILE` | Повторяемый вход проверки уже разрешённой регистрации; требует baseline |
| `--check-result` | Проверяет обязательный результат WPLAN отдельно от использования разрешений |

Baseline: заголовок `manifest<TAB>1<TAB>complete<TAB>.`, затем `type<TAB>mode<TAB>sha256-or--<TAB>relative-path`. Тип `f/d`, права восьмеричные. Preservation не имеет заголовка: те же четыре поля либо `prefix<TAB>число-байтов<TAB>sha256<TAB>relative-path`. Процедура — [change-management](../sops/change-management.md).

JSON: `schema: generic.workspace-check.v1`, `status`, `checks[]` с `id/status/value|message`, `errors[]`, `fail_count`, `warn_count`, `archive_state`, `preservation`. Проверка `actual-delta` содержит фактическую дельту, `primary_delta`, проверенные регистрации и `unused_permissions`. Неиспользованное разрешение не является ошибкой. Коды: `0` PASS, `1` проверка выявила нарушение, `2` некорректный вызов/нечитаемый вход. Статус ошибки вызова — `STOP`.

```bash
python3 -B tools/check_workspace.py --workspace /path/WS_Example --format json
python3 -B tools/check_workspace.py --workspace /path/WS_Example --print-baseline-manifest > /outside/before.tsv
python3 -B tools/check_workspace.py --workspace /path/WS_Example --baseline-manifest /outside/before.tsv --check-result
```

### registration-input

Это временный **вход проверки**, не команда записи и не источник полномочий. Разрешение принадлежит прямому запросу владельца и [task-intake](../sops/task-intake.md#узкая-регистрация). Checker читает уже записанный результат и вычитает только доказанную регистрацию из основной дельты. Без WPLAN оставшаяся дельта должна быть нулевой.

Пример структуры входа будущей задачи:

```json
{
  "kind": "backlog",
  "id": "WBACK-000123",
  "owner_request": "Прямой запрос владельца зарегистрировать будущую задачу",
  "source": "Сообщение владельца с датой и доступным локальным оригиналом",
  "wroad": "WROAD-000001",
  "result": "Ожидаемый результат будущей задачи",
  "expected_sha256": "<SHA-256 прежних байтов backlog>",
  "before_base64": "<base64 тех же прежних байтов>"
}
```

Перед разрешённой записью исполнитель читает реальные байты `plans/backlog.md` и сохраняет их во внешней временной области; `expected_sha256` и `before_base64` вычисляются из **одного** чтения, не восстанавливаются из памяти или текста отчёта. Файл регистрации затем проверяет точное прежнее содержимое и допустимый суффикс по task-intake. Для следующей регистрации берутся байты непосредственно перед ней. Исходная база основной работы остаётся прежней.

Для `kind: feedback` нужны `id: FB-NNNNNN`, `owner_request`, `source`, точный `original` и `recorded_at: YYYY-MM-DD`; `before_base64` не нужен, создаётся только новый record. Существующий текст Feedback не редактируется. Общий новый каталог `feedback/` проверяется один раз для последовательности.

```bash
python3 -B tools/check_workspace.py --workspace /path/WS_Example --baseline-manifest /outside/before.tsv --registration-input /outside/registration-1.json
python3 -B tools/check_workspace.py --workspace /path/WS_Example --baseline-manifest /outside/before.tsv --registration-input /outside/registration-1.json --registration-input /outside/registration-2.json --format json
```

Входы передаются в порядке записей одного последовательного исполнителя. Это не блокировка и не протокол нескольких писателей. Несвежие байты/revision, повтор ID, неверный ROAD, изменение старого текста/маршрута, типа/прав, подмена оригинала Feedback, перестановка зависимых регистраций или незаявленная основная дельта дают FAIL. При конкурентной записи остановиться и перечитать фактическое состояние; не затирать его сохранённой копией.

## check_product.py

Обязателен `--workspace PATH`; `--format text|json`. Без дополнительных флагов проверяет только состав. `--run-native-checks` разрешает выполнение объявленных Profile-команд и требует положительного целого `--timeout-seconds N`. `--native-check ID` выбирает одну объявленную проверку; без него выполняются все. `--native-check` и `--timeout-seconds` допустимы только с `--run-native-checks`.

Запуск — прямой массив argv без shell, с ограниченными cwd и executable, закрытым stdin, перехваченным выводом и временем ожидания. JSON: `schema: generic.product-check.v1`, `status`, `mode`, `composition`, `native_validation`, `native_execution`, `fail_count`, `warn_count`; при ошибке — `error`. Коды `0` PASS, `1` FAIL проверки/команды, `2` ошибка вызова/входа. Разные состав и выполнение не сливаются в одну неявную операцию.

```bash
python3 -B tools/check_product.py --workspace /path/WS_Example --format json
python3 -B tools/check_product.py --workspace /path/WS_Example --run-native-checks --native-check unit --timeout-seconds 60 --format json
```

## new_project.py

Операции `preview` и `apply` принимают одинаковые обязательные `--source-distribution`, `--destination-parent`, `--slug`, `--display-name`, `--wroad`, `--product new|existing`. Для existing обязателен `--existing-product`; для new он запрещён. Повторяемый `--exclude-vcs-path` задаёт точные обнаруженные VCS-пути существующего продукта. `apply` дополнительно требует `--authorization-sha256`, равный `preview_sha256` согласованного preview. Хэш связывает точные входы и действия; сам по себе не является решением владельца.

```bash
python3 -B /distribution/tools/new_project.py preview --source-distribution /distribution --destination-parent /work --slug Example --display-name 'Новый продукт' --wroad 'Создать продукт' --product new
python3 -B /distribution/tools/new_project.py apply --source-distribution /distribution --destination-parent /work --slug Example --display-name 'Новый продукт' --wroad 'Создать продукт' --product new --authorization-sha256 <preview_sha256>
```

Результат всегда JSON: preview содержит `operation`, `state: PREVIEW_READY`, `authorization_payload`, `preview_sha256`, `warnings`, `vcs_exclusions`, `human_readable`; apply — состояние материализации и привязку к тому же digest. Ошибки JSON с `state/error` идут в stderr. Коды: `0` успех; `2` INPUT_ERROR или ошибка синтаксиса argparse; `3` ABORTED до записи (вход/разрешение); `4` ABORTED при материализации; `5` RECOVERY_REQUIRED; `6` INTERNAL_ERROR. Для синтаксиса argparse stderr текстовый. Успешный повтор exact apply восстанавливается по существующему маркеру; чужое состояние не перезаписывается.

Полный договор, состав COPY/GENERATED и Product preservation: [Project Start](../docs/technical/project-start.md). Source-only cleaner и generator в новый Workspace не копируются.

## clean_product.py

`--repo PATH` задаёт корень статической Product Unit BytePress, по умолчанию `.`. `--apply` включает удаление. `--local-service` отдельно включает ограниченную очистку служебных `.agents/.codex`; долговечные raw-трассы и прикреплённые исторические журналы сохраняются. Обычный запуск служебные каталоги не очищает и трасс не требует. `--format text|json` выбирает представление; JSON содержит `schema: bytepress.product-clean.v1`, `status: DRY_RUN|APPLIED|STOP`, `paths`, `removed`, `retained` и при отказе `error`. Коды `0` успешный scan/apply, `1` STOP, `2` ошибка аргументов. `--repo` не является синонимом `--workspace`: это другой объект очистки.

```bash
python3 -B /copy/BytePress/tools/clean_product.py --repo /copy/BytePress --format json
python3 -B /copy/BytePress/tools/clean_product.py --repo /copy/BytePress --apply
```

Apply проверяет точный Product root и не следует по ссылкам. Допустимые остатки и их защита принадлежат [жизненному циклу артефактов](../docs/technical/artifact-lifecycle.md). Очистка не исправляет нарушения checker и не принимает результат.

## release_preflight.py

Операции `preflight` и `readback` требуют `--contract FILE`; обе принимают `--timeout N` (положительное конечное число секунд, default `30`) и `--format owner|engineering|machine` (default owner). `preflight` принимает необязательный `--human-policy FILE`. `readback` требует `--before FILE` и `--delta FILE`; контракт before должен совпасть с текущим.

```bash
python3 -B tools/release_preflight.py preflight --contract /outside/contract.json --format machine
python3 -B tools/release_preflight.py readback --contract /outside/contract.json --before /outside/before.json --delta /outside/delta.json --timeout 30 --format engineering
```

Machine — JSON с `verdict`, результатом проверок и происхождением наблюдений; ошибочный вход возвращает JSON `verdict: FAIL`, `external_writes: 0`, `error`. Точные входные схемы и достаточность свидетельств принадлежат [release-evidence](../docs/technical/release-evidence.md). Коды `0` PASS, `1` FAIL, `2` OWNER_ACTION_REQUIRED; синтаксическая ошибка также `2`, но с диагностикой stderr и без результата verdict. Текст ошибки не раскрывает аргументы с возможными credentials. `--timeout` ограничивает сетевое наблюдение, `--timeout-seconds` у Product checker — выполнение процесса; имена сохранены для действующих потребителей. Ни один результат не разрешает внешнюю запись.
