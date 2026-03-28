# Setup_Guide

## Базовая среда
Основная среда разработки для BytePress — Linux.
На Windows используется WSL2.

Минимальные требования:
- Linux или WSL2
- Python 3.11+
- Git
- Node.js 20+
- pre-commit
- Codex CLI

Windows-native установка Codex не используется.

## Рабочий каталог
Все проекты должны находиться в домашнем каталоге пользователя.

Рекомендуемая структура:

```text
~/code
```

Пример:

```text
/home/<user>/code
    BytePress
```

Репозиторий BytePress должен находиться по пути:

```text
~/code/BytePress
```

Работа из каталогов вида `/mnt/c/Users/...` не рекомендуется.

## Установка зависимостей
### Python
Проверить версию:

```bash
python3 --version
```

Требуется `Python 3.11+`.

### Node.js
Рекомендуется установка через `nvm`:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash
source ~/.bashrc
nvm install 22
nvm use 22
```

### Codex CLI
Установить глобально:

```bash
npm install -g @openai/codex
```

Проверить установку:

```bash
codex --version
```

### pre-commit
Установить:

```bash
pip install pre-commit
```

Активировать hooks в репозитории:

```bash
pre-commit install
```

## Установка BytePress
Клонировать репозиторий:

```bash
git clone <repo-url> ~/code/BytePress
```

Перейти в каталог проекта:

```bash
cd ~/code/BytePress
```

## Локальный профиль Codex
При необходимости задать проект-локальный профиль:

```bash
export CODEX_HOME="$PWD/.codex"
```

## GitHub CLI и PR-контур
Для Auto-PR требуется минимально настроенный GitHub CLI:

```bash
gh auth login
gh auth status
```

На стороне GitHub для репозитория BytePress должны быть включены:
- automatic deletion of head branches после merge;
- защита `develop` и `main` в режиме PR-only.

Рабочий порядок для task-ветки:
1. перейти на `develop`, выполнить `git fetch --prune origin` и `git pull --ff-only origin develop`;
2. создать `task branch` в формате `<type>/<NNNNNN>-<slug>`;
3. сделать серию локальных коммитов в этой ветке;
4. выполнять локальный self-check после каждого коммита;
5. делать `final push` только после завершения задачи;
6. перед созданием PR проверить, нет ли уже открытого PR для head-ветки;
7. если `gh pr create --help` не содержит `--dry-run`, не использовать этот флаг;
8. если `gh` не сработал, не переавторизовывать CLI автоматически, а вывести готовую команду `gh pr create`;
9. после merge считать head-ветку закрытой и не использовать повторно.

## Проверка среды
Запустить базовую проверку структуры:

```bash
python3 Tools/bp_lint.py --repo .
```

Если ошибок нет, базовая среда считается корректной.

## Release branch workflow
Создать release-ветку только от `develop`:

```bash
git checkout develop
git fetch --prune origin
git pull --ff-only origin develop
git checkout -b release/000019-0.1.0-rc2
git push -u origin release/000019-0.1.0-rc2
```

Открыть PR из `release/*` только в `main`:

```bash
gh pr create --base main --head release/000019-0.1.0-rc2
```

После merge удалить release-ветку:

```bash
git branch -d release/000019-0.1.0-rc2
git push origin --delete release/000019-0.1.0-rc2
```
