# Настройка среды

## Назначение
Этот документ описывает пользовательскую подготовку локальной среды для работы с `BytePress`.

Он не является владельцем рабочего процесса, release-маршрута или PR-процедуры. Эти договоры живут в `../../Pipeline/Workflows.md`, `../../Rules/Git.md` и `../Technical/Verification.md`.

## Базовая среда
Основная среда разработки для BytePress — Linux. На Windows используется WSL2.

Минимальные требования:
- Linux или WSL2;
- Python 3.11+;
- Git;
- Node.js 20+;
- `pre-commit`;
- Codex CLI;
- GitHub CLI, если пользователь будет создавать PR из локального контура.

Установка Codex напрямую в Windows не используется.

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

### GitHub CLI
Проверить авторизацию, если локальный проход должен создавать PR:

```bash
gh auth status
```

Если авторизации нет, выполнить:

```bash
gh auth login
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

## Проверка среды
Запустить базовую проверку структуры:

```bash
python3 Tools/bp_lint.py --repo .
```

Если ошибок нет, пользовательская среда достаточно подготовлена для чтения документов и запуска обычного локального прохода.

## Куда идти дальше
- первый маршрут: [First_Start.md](First_Start.md);
- режим работы: [Operating_Mode.md](Operating_Mode.md);
- агентный вход: [../../AGENTS.md](../../AGENTS.md);
- рабочие процедуры: [../../Pipeline/Workflows.md](../../Pipeline/Workflows.md);
- правила Git и PR: [../../Rules/Git.md](../../Rules/Git.md);
- проверочный контур: [../Technical/Verification.md](../Technical/Verification.md).
