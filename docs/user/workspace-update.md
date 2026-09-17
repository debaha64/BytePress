# Workspace Update

Workspace Update обновляет Harness в существующей рабочей среде. Продукт, идентичность проекта, история и выбранный режим источника истины сохраняются. Project Start предназначен для создания отдельного Workspace.

## Подготовить обновление

- Узнайте текущий `harness_version` в корневом Project Profile и версию новой поставки в `VERSION`.
- Подготовьте проверяемый снимок существующего Workspace.
- Укажите исполнителю, какой Workspace обновить, какую поставку использовать и какие частные изменения нужно сохранить.

Исполнитель запускается из новой проверенной distribution. Старый Workspace должен быть остановлен на non-executing checkpoint без active WPLAN; подготовительный research WPLAN под старым checker не открывается. Владелец отдельно разрешает exact backup/digest, новую distribution и полный список изменений после анализа различий. Исполнитель сопоставляет новую поставку с рабочей средой, обновляет только разрешённые поверхности и проверяет сохранность продукта и истории. Нормативная процедура принадлежит [change-management](../../sops/change-management.md#workspace-update).

## Ожидаемый результат

После проверок Workspace работает с обновлённым Harness; `harness_version` отражает успешно применённую версию. Принадлежащий продукту `VERSION`, продуктовая приёмка и разрешение выпуска имеют отдельные основания.

При отказе обновление не считается завершённым: сохраняются сведения о промежуточном состоянии и прежняя версия Harness; восстановление требует точного плана по подготовленному снимку. Изменения конкретного перехода описаны в [0.5.1 → 0.5.2](migration-0.5.1-to-0.5.2.md).

## 0.5.2 → 0.5.3 Workspace Update

Patch исправляет первый research, его authority и archive bootstrap, создаваемый SYSTEM registry и команды проверки Harness. Применяется [внешняя граница Update](../../sops/change-management.md#внешняя-граница-workspace-update); для точного обновления существующего Workspace, включая TAS, нужны следующие различия:

1. Сохранить снимок, Product root, WROAD/WBACK/WPLAN, историю, research и private overlay; начальный `harness_version` оставить `0.5.2`. Для существующего Profile повторная смена владельца конфигурации не требуется.
2. Создать отдельный reference Workspace из distribution `0.5.3`. По actual diff двух fresh deployments задать disposition для каждого changed path; COPY list недостаточен. По fixed copied manifest перенести изменённые checker/tests, phase-gates, SOP interview/project-management/research/change-management, active WPLAN и SYSTEM forms, этот guide. Private варианты объединить по смыслу, совпадающие copied files — по точным bytes/modes. Generated docs/technical/project-start.md получает GENERATED_MERGE; generated navigation также проверяется отдельно. Source-only new_project.py обновляется в distribution, в downstream его не переносить.
3. В существующий SYSTEM семантически добавить реестр из generated reference SYSTEM, подставив реальный Slug. Единственный marker `registry:protected-surfaces` и таблица `Path | Protection` остаются в SYSTEM; существующие более строгие защиты сохраняются. Product root защищён до implementation gate. Не заменять SYSTEM, AGENTS, README или planning/history целиком reference-файлами.
4. Не создавать archive layer ради первого research. Если имеется преждевременный один archives/README.md, считать его отдельным явно учтённым остатком при exact update disposition; не удалять historical archive/payload автоматически.
5. Выполнить copied bytes/modes read-back, checker, применимые tests и preservation checks при версии `0.5.2`. Bootstrap проверить на отдельной копии: первый research имеет `AUTHORITY_REF: none`, без implementation OD, с непустой рабочей границей и защищённым Product. Старый implementation OD не используется как обход ошибки.
6. Только после успешного read-back обновить текстовую проекцию версии SYSTEM, если она имеется, и последним переключить `harness_version` через canonical Profile serializer на `0.5.3`; повторить проверки. При отказе оставить прежнюю версию и промежуточные свидетельства.

Код и данные TAS для этой проверки не требуются: нейтральная fixture воспроизводит Product/history/WROAD preservation и bootstrap. Обновление конкретного Workspace выполняется только по отдельной exact authorization внешней операции. Для новой разработки TAS 0.0.2 выбирайте [New Product](first-start.md), используя старый TAS 0.0.1 как внешний reference corpus. Successful Update заканчивается append-only evidence в обновлённом Workspace; первая дальнейшая задача открывает обычный WPLAN. В обычной поставке deployed cleaner отсутствует; локальный private cleaner сохраняет собственный contract. Команды [change-management](../../sops/change-management.md) не требуют source-only tools.
