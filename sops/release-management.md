# Управление выпуском и свидетельствами

Формы имён поставки, ветки, окончательного тега и выпуска BytePress задаёт [SOP версий](semver.md#имена-снимков-и-поставок), где B — числовая база. Эта процедура владеет выпускными полномочиями и проверкой точного содержимого; версии пользовательских продуктов определяются их собственным договором.

## Назначение

Выполнить предварительную проверку выпуска без записи и независимое контрольное чтение в точном маршруте, разрешённом владельцем. Нормативное поведение, матрица способов переноса и границы фактов принадлежат [спецификации свидетельств](../docs/technical/release-evidence.md). Контракт фаз и решений остаётся у [phase-gates](../docs/technical/phase-gates.md).

## Проверка конкретного PR перед слиянием

1. Получить новое наблюдение репозитория, наборов правил, настроек и прав. Скрытые поля сверить с новым наблюдением владельца или администратора через веб-интерфейс, привязанным к текущей точке контроля.
2. Выбрать один существующий PR и передать `contract.pr_numbers=[N]`; прочитать наблюдаемые идентичность, состояние и автора. Пустой выбор означает только `potential-route-only` и `NOT_YET_OBSERVED` для конкретной точки контроля.
3. Связать точные репозиторий, ссылку и SHA исходной ветви с зафиксированным кандидатом и рабочим маршрутом, а целевой ветви — с текущей ожидаемой базой. Проверить, что PR открыт, не является черновиком и ещё не слит.
4. Получить свежие рецензии выбранного PR постранично; проверить идентичность, состояние и `commit_id` каждой рецензии и повторно прочитать текущий коммит PR. Число утверждений считать по разным действительным утверждающим текущего коммита.
5. Отдельно доказать выполнение требования об утверждении последнего проверяемого изменения. `last_pusher` из контракта, автор коммита и REST `mergeable` не являются таким доказательством. Текущий инструмент сохраняет `OWNER_ACTION_REQUIRED`; независимое наблюдение владельца или администратора может завершить только сверку человеком с явными источником, датой, наблюдателем, PR, исходным коммитом, целевой ветвью и правилами. Автоматический PASS из него не выводится.
6. Доказать закрытие обсуждений, проверку назначенных рецензентов или CODEOWNERS и требования статуса. При отсутствии фактического состояния — `OWNER_ACTION_REQUIRED`. `mergeable=true` означает только отсутствие обнаруженного конфликта слияния.
7. После рассмотрения текущих машинных свидетельств и сверки человеком получить отдельное точное Release Authorization владельца для действия, PR, исходного и целевого коммитов, кандидата, способа слияния и участника.
8. Непосредственно перед записью повторить полное наблюдение и точное сравнение. Новое изменение или текущий коммит, смена утверждения, его отмена или требование правок, смена целевой ветви, правил рецензирования или прав делают затронутые свидетельства и разрешение недействительными. Обновить доказательства и пройти точку решения владельца заново.
9. После закрытия всех требований отдельный уполномоченный исполнитель выполняет только точно разрешённую запись. Операция `preflight` остаётся без записи и всегда выводит `write_authorized=false`.
10. Получить независимое контрольное чтение по следующему разделу. Сверить выбранный PR и фактический результат с [контрактом проверки PR](../docs/technical/release-evidence.md#конкретный-pr-и-наблюдаемые-рецензии).

Метаданные и рецензии читаются только для выбранного номера; общий список открытых PR содержит только номера. Подробный состав наблюдения и ограничение API находятся в [спецификации](../docs/technical/release-evidence.md#цепочка-участников-и-состав-наблюдения).

Права, настройки, наборы правил, аутентификация и правила разделения участников автоматически не меняются. Недоказанный шаг требует `STOP / OWNER_ACTION_REQUIRED`. Наблюдение прошлой точки контроля не переносится на будущую выпускную точку.

Прямой PR из исходной ветви в целевую допустим при `source_ref == working_ref != base_ref`. Условная ветвь `release/<B>` используется только по отдельному маршруту владельца; [условия ссылок](../docs/technical/release-evidence.md#цепочка-участников-и-состав-наблюдения) проверяются явно. Потенциальная выполнимость не выбирает маршрут и не создаёт ветвь.

## Независимое контрольное чтение

1. До записи зафиксировать каноническое наблюдение и точную разрешённую ожидаемую разницу: названные объекты, ссылки и SHA, участника, идентичность PR, тега, выпуска и файлов, способ слияния.
2. После записи независимо получить наблюдение через `readback --contract <gate.json> --before <preflight.json> --delta <delta.json>`. Ответ операции записи не использовать как доказательство фактического состояния.
3. Сопоставить весь наблюдаемый состав объектов, точные изменённые объекты и неизменённые настройки, правила и права. Неожиданная, частичная или не давшая результата запись даёт FAIL. Исчезновение из списка открытых PR допускается только для выбранного слитого PR; посторонние изменения дают FAIL.
4. Для обычного коммита слияния независимо наблюдать `merged_by`, итоговую целевую ссылку, `merge_commit_sha` и родителей `[pre-base, pre-head]`. Не заполнять новые факты из предположений предварительной проверки или ответа записи. Для `squash/rebase`, создателя ветви или тега и других ненаблюдаемых фактов получить отдельные независимые свидетельства события или аудита. Инструмент даёт `OWNER_ACTION_REQUIRED` и не выводит участника из автора коммита.
5. Сохранить неизвестное состояние правил даже при сравнении без изменений. `comparison_verdict=PASS` означает только равенство наблюдаемой поверхности и не доказывает отсутствие скрытых или кратковременных внешних изменений.
6. Не повторять запись, не исправлять состояние автоматически и не продолжать маршрут автоматически. Передать владельцу точное частичное состояние.

## Снимок и публичные файлы выпуска

Обычный снимок задачи создаётся только после постоянных изменений и последней записи в Workspace, без обычного сопроводительного файла `.sha256`. Контрольная сумма передаётся в отчёте владельцу. Упаковка и свежая распаковка выполняются по разделу [полного снимка](#полный-снимок-и-восстановление).

Кандидат на приёмку хранит точную идентичность и контрольную сумму в свидетельствах. Публичный файл выпуска требует равенства загруженных байтов, контрольной суммы и отдельного выпускного сопроводительного файла; затем проверяется внутренний формат архива. PA-*, Release Authorization, публикация и контрольное чтение остаются отдельными фактами.

Если отчёт приводит количество записей tar, он всегда раздельно указывает:

- `total tar entries` — все записи архива;
- `explicit root entry` — число явных записей корня, с его именем;
- `entries below root` — записи ниже корня, без самого корня.

При детализации отдельно указываются `files below root` и `directories below root`. Это правило описания существующего архива, без нового формата manifest или metadata schema.

## Свидетельства и исполнение

Машинный вывод запрашивается явно через `--format machine`; по умолчанию вывод владельцу краток. Инженерное представление содержит ссылки, правила, цепочку участников, препятствия и контрольную сумму. Источник и дата наблюдения человека сохраняются без снимков экрана, секретов, окружения или необработанных ответов API.

Инструмент запускается только явно; он не входит в исполнение универсальных проверок или Project Start. Свежий Workspace в `sot_files` не нуждается в Git/GitHub для PASS универсальных проверок. Формат и пределы свидетельств заданы в [спецификации](../docs/technical/release-evidence.md#свидетельства-и-границы-состояния).

## Входной Product Acceptance

Release Readiness потребляет существующий `PA-*` со значением accepted, в том числе из предыдущего WPLAN, по [границам Product Acceptance](../docs/technical/phase-gates.md#границы-product-acceptance). Новый WPLAN выпуска не требует повторной приёмки того же точного результата и не меняет происхождение PA.

До внешних записей выпускная процедура связывает точного кандидата из PA и квалификационных свидетельств с подготовленным артефактом и целевыми ссылками по [release-evidence](../docs/technical/release-evidence.md): проверяет идентичность кандидата и равенство свойств выбранного способа переноса. Несовпадение кандидата останавливает маршрут; PA прежнего результата не принимает изменённый Product. Это обязанность release-readiness, а не универсального инструмента Workspace. Release Authorization остаётся отдельным решением владельца.

Узкая регистрация по [task-intake](task-intake.md#узкая-регистрация) не является исполняемым проходом и не требует обычного снимка. Остальные правила снимков сохраняются.


## Полный снимок и восстановление

Полнота и сохранность принадлежат [artifact-lifecycle](../docs/technical/artifact-lifecycle.md#обычный-снимок), имя — [SemVer](semver.md#имена-снимков-и-поставок), момент передачи — [clean-exit](clean-exit.md#закрытие-маршрута-и-снимок). Выполните все записи и проверки до упаковки; остановите параллельные записи. Полный обход включает скрытые файлы и пустые каталоги, служебные данные и всё оставшееся temp; фильтров проверки изменений здесь нет.

Используйте существующие Python standard library и tar: POSIX tar с поддержкой --format ustar либо нативный Windows bsdtar. Формат всегда явно USTAR UTF-8, без PAX/GNU расширений. Заранее создайте один новый пустой внешний каталог операции и сохраните в нём следующий единственный исполняемый пример как snapshot.py. Запустите python3 -B /absolute/snapshot-operation/snapshot.py /absolute/WS_Example /absolute/backup.tar.gz /absolute/snapshot-operation; [Windows](../docs/user/windows.md#снимок-и-проба-восстановления) задаёт платформенный вызов того же примера. Все пути абсолютные. Workspace, итоговый архив и каталог операции не вложены друг в друга; родитель архива существует. В каталоге операции перед запуском только собственный snapshot.py: посторонний состав вызывает отказ без очистки. Имеющийся архив не заменяется. Восстановление и временный архив создаются только внутри операции.

На POSIX сохраняются поддерживаемые типы, байты, POSIX-права, целый mtime и связи hardlinks; symlink хранится ссылкой без обхода цели. На Windows сохраняются обычные файлы/каталоги, байты, целый mtime и read-only файлов; reparse points и hardlinks отклоняются, как в прежнем Windows-примере. ACL, ADS, xattrs и владение не заявляются сохранёнными. Непредставимость или невозможность полного резервирования означает отказ всего снимка с путём и причиной, а не сокращение состава. Для такого источника нужен подходящий способ полного резервирования по решению владельца; менять обещанную сохранность автоматически нельзя.

Пример предварительно проверяет представимость, независимо сопоставляет физический состав USTAR с исходником, распаковывает в свежую область штатным tar и сравнивает пути, типы, байты и сохраняемые свойства. rc0 отдельно не доказывает полноту. Исходник повторно проверяется по составу и признакам изменений. Только прошедший проверку архив получает итоговое имя; после PASS не записывайте ничего в Workspace. После PASS сценарий, временный архив и fresh restore удаляются вместе с собственным каталогом операции; рядом остаётся только итоговый архив. При FAIL новый итоговый архив не выдаётся либо удаляется, а один каталог операции сохраняет сценарий, проверяемый архив (возможен неполный), область restore и result.txt с точной причиной. Сообщите его абсолютный путь; чужие файлы рядом не трогайте. Сумма и состав передаются отчётом без записи обратно. Отказ предусловий занятого пути не даёт права удалить его или включить в свою диагностику.

<!-- full-snapshot-python -->
```python
import gzip
import hashlib
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile


def fail(path, reason):
    raise RuntimeError(f"{path}: {reason}")


def inventory(base):
    values, guards, hardlinks = {}, {}, {}
    def visit(path):
        info = path.lstat()
        relative = path.relative_to(base).as_posix()
        if any(ord(c) < 32 or c == "\\" or ord(c) == 127 for c in relative):
            fail(path, "неподдерживаемое имя")
        if getattr(info, 'st_file_attributes', 0) & 0x400:
            fail(path, "reparse point требует полного подходящего резервирования")
        mode = stat.S_IMODE(info.st_mode)
        if stat.S_ISLNK(info.st_mode):
            kind, content = 'symlink', os.readlink(path)
            if mode != 0o777 or any(ord(c) < 32 or c == "\\" for c in content):
                fail(path, "непредставимые свойства symlink")
        elif stat.S_ISDIR(info.st_mode):
            kind, content = 'directory', None
        elif stat.S_ISREG(info.st_mode):
            kind = 'file'
            with path.open('rb') as stream:
                content = hashlib.file_digest(stream, 'sha256').hexdigest()
            if os.name == 'nt' and info.st_nlink != 1:
                fail(path, "Windows hardlink требует полного подходящего резервирования")
            if info.st_nlink > 1:
                hardlinks.setdefault((info.st_dev, info.st_ino), []).append(relative)
        else:
            fail(path, "неподдерживаемый тип объекта USTAR")
        properties = (bool(mode & 0o222) if kind == 'file' else None) if os.name == 'nt' else mode
        values[relative] = (kind, content, properties, int(info.st_mtime))
        guards[relative] = (info.st_dev, info.st_ino, info.st_size, info.st_mode,
                            info.st_mtime_ns, info.st_ctime_ns, info.st_nlink)
        if kind == 'directory':
            for child in sorted(path.iterdir()):
                visit(child)
    visit(base)
    groups = sorted(sorted(group) for group in hardlinks.values() if len(group) > 1)
    return values, guards, groups


def compare(expected, observed, base, reason):
    for path in sorted(set(expected) | set(observed)):
        if expected.get(path) != observed.get(path):
            fail(base / path, reason)


def preflight(root, before):
    for relative, (kind, content, mode, mtime) in before[0].items():
        path = root / relative
        info = path.lstat()
        name = root.name if relative == '.' else root.name + '/' + relative
        header = tarfile.TarInfo(name + ('/' if kind == 'directory' else ''))
        header.type = {'file': tarfile.REGTYPE, 'directory': tarfile.DIRTYPE,
                       'symlink': tarfile.SYMTYPE}[kind]
        header.mode = stat.S_IMODE(info.st_mode)
        header.uid, header.gid, header.mtime = info.st_uid, info.st_gid, mtime
        header.size = info.st_size if kind == 'file' else 0
        if kind == 'symlink':
            header.linkname = content
        try:
            header.tobuf(format=tarfile.USTAR_FORMAT, encoding='utf-8', errors='strict')
        except (ValueError, UnicodeError) as exc:
            fail(path, 'непредставимо в USTAR: ' + str(exc))


def physical_headers(archive, root, expected):
    names, kinds = set(), {}
    with gzip.open(archive, 'rb') as stream:
        while True:
            block = stream.read(512)
            if block == bytes(512):
                if stream.read(512) != bytes(512):
                    fail(archive, 'неполный USTAR trailer')
                while tail := stream.read(1024 * 1024):
                    if any(tail):
                        fail(archive, 'данные после USTAR trailer')
                break
            if len(block) != 512 or block[257:265] != b'ustar\0' + b'00':
                fail(archive, 'ожидался физический USTAR без PAX/GNU')
            if sum(block[:148]) + 256 + sum(block[156:]) != int(block[148:156].strip(b'\0 ') or b'0', 8):
                fail(archive, 'неверная checksum USTAR')
            kind = block[156:157]
            if kind not in (b'0', b'\0', b'1', b'2', b'5'):
                fail(archive, 'расширение или тип вне USTAR: ' + repr(kind))
            name = block[:100].split(b'\0', 1)[0]
            prefix = block[345:500].split(b'\0', 1)[0]
            name = ((prefix + b'/' if prefix else b'') + name).decode('utf-8', 'strict').rstrip('/')
            parts = name.split('/')
            if parts[0] != root.name or any(p in ('', '.', '..') or '\\' in p for p in parts) or name in names:
                fail(name, 'небезопасный или повторный USTAR путь')
            for index in range(1, len(parts)):
                if kinds.get('/'.join(parts[:index])) != b'5':
                    fail(name, 'родитель не является ранее объявленным каталогом')
            size = int(block[124:136].strip(b'\0 ') or b'0', 8)
            if kind == b'1':
                target = block[157:257].split(b'\0', 1)[0].decode('utf-8', 'strict')
                if kinds.get(target) not in (b'0', b'\0'):
                    fail(name, 'небезопасная цель hardlink')
            if kind not in (b'0', b'\0') and size:
                fail(name, 'неверный размер специального USTAR объекта')
            names.add(name)
            kinds[name] = kind
            remaining = ((size + 511) // 512) * 512
            while remaining:
                data = stream.read(min(remaining, 1024 * 1024))
                if not data:
                    fail(name, 'обрезанное содержимое USTAR')
                remaining -= len(data)
    for name in sorted(expected ^ names):
        fail(name, 'состав USTAR отличается от полного источника')
    return len(names)


def remove_operation(work):
    def writable_retry(function, path, error):
        if not Path(path).is_symlink():
            os.chmod(path, 0o700)
        function(path)
    shutil.rmtree(work, onerror=writable_retry)


def snapshot(root, out, work):
    if not all(p.is_absolute() for p in (root, out, work)):
        fail(root, 'нужны абсолютные пути')
    if root.is_symlink() or not root.is_dir():
        fail(root, 'ожидался каталог Workspace')
    if work.is_symlink() or not work.is_dir():
        fail(work, 'нужен заранее назначенный каталог операции со snapshot.py')
    root, out, work = (p.resolve() for p in (root, out, work))
    if any(a == b or a in b.parents or b in a.parents for a, b in
           ((root, work), (root, out), (work, out))):
        fail(work, 'Workspace, архив и каталог операции должны быть независимы')
    script = work / 'snapshot.py'
    if set(work.iterdir()) != {script} or script.is_symlink() or not script.is_file():
        fail(work, 'посторонний состав; разрешён только собственный snapshot.py')
    if script.stat().st_nlink != 1 or Path(__file__).resolve() != script:
        fail(script, 'ожидался собственный сценарий этой операции')
    if out.exists() or out.is_symlink():
        fail(out, 'путь уже занят')
    if not out.parent.is_dir():
        fail(out.parent, 'каталог результата должен существовать')
    script_bytes = script.read_bytes()
    stage, restore = work / 'archive.tar.gz', work / 'restore'
    published = False
    output_identity = None
    try:
        stage.touch(exist_ok=False)
        restore.mkdir()
        before = inventory(root)
        preflight(root, before)
        charset = ['--options', 'hdrcharset=UTF-8'] if os.name == 'nt' else []
        with stage.open('wb') as stream:
            subprocess.run(['tar', '--format', 'ustar', *charset, '-czf', '-', '-C', str(root.parent), root.name], stdout=stream, check=True)
        compare(before[1], inventory(root)[1], root, 'источник изменился при упаковке')
        expected = {root.name if p == '.' else root.name + '/' + p for p in before[0]}
        count = physical_headers(stage, root, expected)
        digest = hashlib.sha256(stage.read_bytes()).hexdigest()
        subprocess.run(['tar', *charset, '-xzpf', str(stage), '-C', str(restore)], check=True)
        if os.name == 'nt':
            with tarfile.open(stage, encoding='utf-8', errors='strict') as archive:
                for member in archive:
                    if member.isfile():
                        os.chmod(restore / member.name, 0o666 if member.mode & 0o222 else 0o444)
        restored = inventory(restore / root.name)
        compare(before[0], restored[0], restore / root.name, 'восстановление отличается')
        if before[2] != restored[2]:
            fail(restore / root.name, 'связи hardlinks отличаются')
        compare(before[1], inventory(root)[1], root, 'источник изменился при проверке')
        if hashlib.sha256(stage.read_bytes()).hexdigest() != digest:
            fail(stage, 'архив изменился при проверке')
        with out.open('xb') as destination:
            output_info = os.fstat(destination.fileno())
            output_identity = (output_info.st_dev, output_info.st_ino)
            published = True
            with stage.open('rb') as source:
                shutil.copyfileobj(source, destination)
        compare(before[1], inventory(root)[1], root, 'источник изменился при передаче')
        if hashlib.sha256(out.read_bytes()).hexdigest() != digest:
            fail(out, 'итоговые байты отличаются')
        files = sum(row[0] == 'file' for row in before[0].values())
        directories = sum(row[0] == 'directory' for row in before[0].values())
        # Счётчик объектов получен из независимо проверенных физических заголовков.
        remove_operation(work)
        print('PASS', out, digest, 'USTAR/PAX0', 'objects', count,
              'files', files, 'directories', directories)
    except BaseException as error:
        # Предусловия не дают права удалять занятые чужие пути.
        work.mkdir(exist_ok=True)
        if not script.exists():
            script.write_bytes(script_bytes)
        if published:
            info = out.lstat()
            if (info.st_dev, info.st_ino) == output_identity and not out.is_symlink():
                if not stage.exists():
                    shutil.copyfile(out, stage)
                out.unlink()
            else:
                error = RuntimeError(str(error) + '; итоговый путь заменён извне, не удалён')
        stage.touch(exist_ok=True)
        restore.mkdir(exist_ok=True)
        message = f'FAIL: {error}\nДиагностика: {work}\nАрхив archive.tar.gz может быть неполным; это не итоговый снимок.\n'
        (work / 'result.txt').write_text(message, encoding='utf-8')
        raise RuntimeError(message) from error


if __name__ == '__main__':
    snapshot(*(Path(p) for p in sys.argv[1:]))
```
