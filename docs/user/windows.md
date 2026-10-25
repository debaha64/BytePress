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

После всех записей и проверок остановите записи в Workspace. Используйте существующий bsdtar; частный навык Workspace BytePress с GNU tar не является зависимостью этого сценария. Ниже ограниченный файловый резерв: весь состав обычных файлов и каталогов, включая скрытые, байты, mtime в целых секундах и read-only файлов. ACL, владелец, ADS, xattrs не сохраняются этим договором. Ссылки, точки повторной обработки (reparse points) и жёсткие ссылки требуют отдельного подходящего резервирования; пример отказывается их упаковывать. Полное имя выбирайте по договору своего проекта, существующий архив не заменяйте. На Windows кодировка имён заголовков явно задаётся как UTF-8 при упаковке и извлечении через `--options hdrcharset=UTF-8`; иначе bsdtar 3.5.2 может использовать текущую OEM-кодировку. Параметр описан в [libarchive 3.5.2](https://github.com/libarchive/libarchive/blob/v3.5.2/libarchive/archive_write_set_options.3). После извлечения Python восстанавливает read-only обычных файлов по режимам USTAR: bsdtar на проверенной Windows сам этот признак не восстановил. ACL этим не создаются. Проверка состава и восстановления обязательна; несовпадение вызывает отказ.

Укажите три абсолютных пути: существующий Workspace, новый архив вне него и отсутствующий каталог пробы восстановления. Выполните из терминала приложения следующий блок. Он проверяет восстановление до сообщения PASS; каталог пробы сохраняется для осмотра, исходный Workspace после снимка не изменяется.

```powershell
$Workspace = 'C:\BytePressLab\WS_Notes'
$Archive = 'C:\BytePressSnapshots\Notes-backup.tar.gz'
$Restore = 'C:\BytePressRestore\probe1'
@'
import hashlib, os, pathlib, stat, subprocess, sys, tarfile
root, out, restore = map(lambda x: pathlib.Path(x).absolute(), sys.argv[1:])
assert root.is_dir() and not out.exists() and not restore.exists()
assert root != out.parent and root not in out.parents and root not in restore.parents
out.parent.mkdir(parents=True, exist_ok=True)
def manifest(base):
    result = {}
    def walk(path):
        info = path.lstat()
        assert not getattr(info, 'st_file_attributes', 0) & 0x400, path
        assert not path.is_symlink(), path
        isdir = stat.S_ISDIR(info.st_mode)
        assert isdir or stat.S_ISREG(info.st_mode) and info.st_nlink == 1, path
        result[path.relative_to(base).as_posix()] = (
            'directory' if isdir else 'file', int(info.st_mtime),
            None if isdir else bool(info.st_mode & stat.S_IWRITE),
            None if isdir else hashlib.sha256(path.read_bytes()).hexdigest())
        if isdir:
            for child in sorted(path.iterdir()): walk(child)
    walk(base)
    return result
before = manifest(root)
charset = ['--options', 'hdrcharset=UTF-8'] if os.name == 'nt' else []
with out.open('xb') as stream:
    subprocess.run(['tar', '--format', 'ustar', *charset, '-czf', '-', '-C', str(root.parent), root.name], stdout=stream, check=True)
assert manifest(root) == before, 'source changed during packing'
with tarfile.open(out) as archive:
    members = archive.getmembers()
    names = [m.name.rstrip('/') for m in members]
    assert len(names) == len(set(names))
    expected = {root.name if p == '.' else root.name + '/' + p for p in before}
    assert set(names) == expected and all(m.isfile() or m.isdir() for m in members)
restore.mkdir(parents=True)
subprocess.run(['tar', *charset, '-xzf', str(out), '-C', str(restore)], check=True)
if os.name == 'nt':
    for member in members:
        if member.isfile():
            os.chmod(restore / member.name, 0o666 if member.mode & 0o222 else 0o444)
assert manifest(restore / root.name) == before, 'restoration differs'
assert manifest(root) == before, 'source changed during verification'
print('PASS', out.name, hashlib.sha256(out.read_bytes()).hexdigest(), 'objects', len(before))
'@ | python -X utf8 -B - $Workspace $Archive $Restore
if ($LASTEXITCODE -ne 0) { throw 'snapshot or restoration failed; keep evidence' }
```

После отказа не считайте архив проверенным. Сохраните сообщение и исходный Workspace; повтор выбирает новый путь после выяснения причины. Снимок и проверка восстановления не означают приёмку продукта.
