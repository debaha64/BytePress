# Задачи пользователя

- **[Project Start — New Product](first-start.md)** — новый Workspace и пустой Product root.
- **[Project Start — Existing Product](existing-product.md)** — новый Workspace и точная копия реального Product root.
- [После Project Start](after-project-start.md) — перейти к первой задаче.
- [Режим источника истины](source-of-truth-mode.md) — понять файловый и Git-контуры.
- **[Workspace Update](workspace-update.md)** — существующий управляемый Workspace; обновляется Harness, сохраняются Product, состояние проекта и история.
- [Переход 0.5.1 → 0.5.2](migration-0.5.1-to-0.5.2.md) — узнать изменения конкретных версий.
- [Подготовка GitHub](github-repository-preparation.md) — подготовить внешний контур.

## Как выбрать

`Existing Product` — каталог самого продукта, который нужно физически перенести. Старый Workspace snapshot, research, logs, отчёты/чаты, `.txt`, `.md`, `.pdf`, `.zip` или `.tar.gz` не становятся Existing Product только из-за формата или возраста. Если это справочные материалы для новой разработки, выбирайте **Project Start — New Product** и передайте их как внешние input/reference materials первого research. Harness не импортирует их автоматически и не переносит старый Harness/history в новый Product root. Если обновляете уже управляемую среду с сохранением её работы, выбирайте Workspace Update.

## Обратная связь

[Как сообщить о своём опыте](feedback.md).
