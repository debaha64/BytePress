# Нативная Windows через настольное приложение

Минимальный сценарий: Windows 10 x64, нативный Python 3.14, PowerShell 5.1, NTFS и `tar` из Windows (bsdtar). WSL и отдельный пользовательский запуск Codex CLI не нужны. Это предварительно подготовленный путь; успешное выполнение на конкретной машине подтверждает её агент отдельным отчётом.

Откройте в настольном приложении каталог распакованной проверенной поставки BytePress. Выберите нативную Windows для агента; оболочка встроенного терминала настраивается отдельно. Попросите агента выполнить `Get-Location`, `python -X utf8 -B -c "import sys; print(sys.platform, sys.version)"` и `tar --version` именно в выбранном проекте. Наличие `windows.sandbox=elevated` описывает изолированную среду, но не подтверждает исполнение этих команд.

Git нужен отдельным функциям приложения, например панели просмотра изменений; GitHub CLI — функциям GitHub. Команды BytePress в `sot_files` их не вызывают. Подтверждение команд агента проверяется отдельно от доступности панели изменений. См. [Windows app](https://learn.chatgpt.com/docs/windows/windows-app) и [Windows sandbox](https://learn.chatgpt.com/docs/windows/windows-sandbox), сверено 25.10.2026. Windows 10 у OpenAI поддерживается по принципу best effort (без полной гарантии поддержки): возможность работы проверяется на целевой машине.

## Создать Workspace

В PowerShell используйте Python с явным UTF-8; редакторские файлы сохраняйте как UTF-8 без BOM. Перенаправление `>` PowerShell 5.1 не используйте для машинного UTF-8: оно может записать UTF-16. Исходники и профиль читаются инструментами явно как UTF-8.

```powershell
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
$OutputEncoding = [Console]::OutputEncoding
$env:PYTHONIOENCODING = 'utf-8'
$StartArgs = @('--source-distribution', '.', '--destination-parent', 'C:\BytePressLab', '--slug', 'Notes', '--display-name', 'Личные заметки', '--wroad', 'Подготовить инструмент заметок', '--product', 'new')
New-Item -ItemType Directory -Path 'C:\BytePressLab' -ErrorAction Stop
$Preview = python -X utf8 -B tools/new_project.py preview @StartArgs | ConvertFrom-Json
if ($LASTEXITCODE -ne 0) { throw 'preview failed' }
$Preview.human_readable
python -X utf8 -B tools/new_project.py apply @StartArgs --authorization-sha256 $Preview.preview_sha256
if ($LASTEXITCODE -ne 0) { throw 'apply failed' }
```

Прочитайте просмотренный состав перед apply. Каталог `WS_Notes` должен отсутствовать; занятый путь даёт отказ. Для реального существующего продукта используйте [Existing Product](existing-product.md), заменив `python3` на `python -X utf8`; Workspace Update для уже управляемой среды выполняется по [отдельной процедуре](workspace-update.md).

## Одна задача и проверки

Откройте `C:\BytePressLab\WS_Notes` отдельным проектом приложения. Попросите агента прочитать карту и фактических владельцев состояния. Передайте одну ограниченную задачу, например: «Исследуй требования к локальным заметкам; сохрани результат исследования по действующей процедуре, без реализации продукта». Дальше применяется [после Project Start](after-project-start.md); Start сам WBACK/WPLAN не создаёт.

```powershell
python -X utf8 -B tools/check_workspace.py --workspace .
python -X utf8 -B tools/check_product.py --workspace .
```

Ожидаются два PASS. Если нужен исходный TSV для `actual-delta`, сохраните stdout через Python `subprocess.run(..., stdout=поток_открытый_wb, check=True)` либо через `[IO.File]::WriteAllText` с `UTF8Encoding($false)`. Проверяйте результат задачи и реальную дельту по [verify-work](../../sops/verify-work.md). Права и восстановление при прерывании имеют [нативную семантику](../technical/project-start.md#нативная-файловая-семантика).

## Снимок и проба восстановления

После всех записей и проверок остановите записи в Workspace. Откройте [общую процедуру полного снимка](../../sops/release-management.md#полный-снимок-и-восстановление): она явно выбирает USTAR UTF-8, проверяет физические заголовки, полный состав и свежее восстановление. Свойства и границы сохранности принадлежат [artifact-lifecycle](../technical/artifact-lifecycle.md#обычный-снимок); имя — SOP SemVer, момент передачи — clean-exit. WSL и GNU tar не нужны: используется существующий нативный Windows tar (bsdtar) и Python standard library.

Сохраните единственный Python-блок общей процедуры как snapshot.py вне Workspace. Не меняйте его для Windows. Укажите три абсолютных пути: существующий Workspace, новый архив вне него и отсутствующий каталог пробы восстановления. Если Python и tar уже доступны, установка не требуется.

```powershell
python -X utf8 -B C:\BytePressLab\snapshot.py C:\BytePressLab\WS_Notes C:\BytePressSnapshots\Notes-backup.tar.gz C:\BytePressRestore\probe1
if ($LASTEXITCODE -ne 0) { throw 'Снимок или восстановление не прошли проверку' }
```

Для имён заголовков и извлечения общий пример передаёт bsdtar явный --options hdrcharset=UTF-8. После извлечения он восстанавливает read-only файлов по заголовкам USTAR: сам bsdtar на проверенной Windows этот признак не восстанавливает. ACL, ADS, владелец и xattrs не объявляются сохранёнными. Неподдерживаемые ссылки/reparse points и жёсткие ссылки Windows вызывают явный отказ с путём; объект не пропускается. Не принимайте rc0 и наличие файла за полноту.

После отказа сохраняйте исходный Workspace и сообщение; непроверенный результат не считается снимком. После PASS исходный Workspace не изменяется. Нативный автоматический запуск не подтверждает запуск агента в настольном приложении или продуктовую приёмку.
