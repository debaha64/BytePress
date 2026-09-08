# Первый Workspace

Создадим рабочую среду для нового продукта `Notes`. В результате появится `WS_Notes` с пустым каталогом продукта и готовыми средствами управления работой.

## Подготовить

Нужны Python `3.12+`, распакованный BytePress и существующий каталог `~/code`. Каталог `~/code/WS_Notes` должен отсутствовать. Выполняйте команды из каталога распакованного BytePress. Имя `Notes` можно заменить своим: латинская буква в начале, далее буквы, цифры, `_` или `-`.

## Посмотреть будущий результат

```bash
python3 -B tools/new_project.py preview --source-distribution . --destination-parent ~/code --slug Notes --display-name "Личные заметки" --wroad "Создать инструмент для личных заметок" --product new
```

Проверьте путь `WS_Notes` и цель проекта в результате `preview`. Эта команда ничего не создаёт. Сохраните показанный `preview_sha256`: он связывает ваше разрешение с просмотренным составом изменений.

## Создать Workspace

Вставьте полученную контрольную сумму вместо `PREVIEW_SHA256`:

```bash
python3 -B tools/new_project.py apply --source-distribution . --destination-parent ~/code --slug Notes --display-name "Личные заметки" --wroad "Создать инструмент для личных заметок" --product new --authorization-sha256 PREVIEW_SHA256
```

Ожидаемый результат — успешное создание `~/code/WS_Notes`, файла `Notes.profile` и пустого `Notes/`. Проверить среду можно так:

```bash
cd ~/code/WS_Notes
python3 -B tools/check_workspace.py --workspace .
python3 -B tools/check_product.py --workspace .
```

Обе проверки должны завершиться PASS. Теперь откройте [что делать после Project Start](after-project-start.md).

Если контрольная сумма больше не совпадает, повторите `preview` и проверьте изменившиеся входы. При `RECOVERY_REQUIRED` сохраните сообщение и обратитесь к [контракту восстановления](../technical/project-start.md#восстановление); произвольное удаление оставшихся файлов не является восстановлением. Для уже существующего продукта есть [отдельная инструкция](existing-product.md).
