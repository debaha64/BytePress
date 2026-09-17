# Управление изменениями

Целевой артефакт: связанные системные и продуктовые артефакты.
Шаблоны: `templates/change-record.md`, `templates/quality-record.md`.
Способ записи: проверка связей, правка и дозапись.

## Назначение

Процедура предотвращает рассинхронизацию между терминами, SOP, шаблонами, инструментами, фазой, SoT и пользовательскими документами.

## Когда применять

Применять в `system-editing`, открытом владельцем, а также при изменении:

1. термина или SOP;
2. шаблона или инструмента;
3. фазы, точки контроля или SoT;
4. README или пользовательской документации.

## Карта связей

- термин -> глоссарий, `SYSTEM.md`, `AGENTS.md`, связанные SOP и шаблоны, `logs/terminology.md`;
- SOP -> `SYSTEM.md`, `AGENTS.md`, связанные SOP, шаблоны и инструменты, `logs/changes.md`;
- шаблон -> `SYSTEM.md`, `templates/README.md`, применяющая SOP, журналы;
- инструмент -> `tools/README.md`, `SYSTEM.md`, `tests/README.md`, прямой тест инструмента и внешний Workspace `logs/quality.md`;
- фаза или точка контроля -> `docs/technical/sdlc.md`, `sops/sdlc.md`, `sops/project-management.md`, `roles/README.md`, `templates/workspace-plan-active.md` и связанные тесты;
- Project Profile и состав проекта -> `docs/architecture/project-profile.md`, `docs/architecture/domain-model.md`, `tools/project_profile.py`, `tests/test_project_profile.py`;
- роль -> `roles/README.md`, `templates/role.md`, прямые ссылки и проверка обязательных файлов;
- навык -> `skills/README.md`, `AGENTS.md`, `SYSTEM.md` и граница необязательной клиентской проекции;
- SoT -> `sops/sot.md`, `check_workspace.py`, глоссарий, `SYSTEM.md`, активный WPLAN и решения владельца;
- README -> `templates/product-readme.md`, `docs/user/`, идентичность продукта и текущая фаза;
- граница документов и SOP -> README соответствующих слоёв, связанная SOP, `logs/changes.md`, `logs/quality.md`.

## Процедура

1. Подтвердить активный WPLAN и разрешённые поверхности.
2. Определить затронутые связи по карте.
3. Изменить только ставшие ложными или неполными артефакты.
4. Если меняется шаблон, проверить `templates/README.md` и применяющую SOP.
5. Если меняются документы, обновить объяснения и пользовательские шаги; внутренние полномочия и порядок работы агента сохранять у SOP.
6. Если меняется инструмент, обновить `tools/README.md`, `SYSTEM.md` и относящиеся к нему проверки.
7. Если меняется граница роли или навыка, проверить канонический каталог, шаблон при наличии, прямых потребителей и отсутствие второй канонической проекции.
8. Если меняется SoT, подтвердить три изолированных обработчика: отсутствие Git-вызовов в `sot_files`; корень, ветвь, чистое дерево и отсутствие удалённого репозитория в `sot_git`; локальную идентичность, `origin`, отслеживаемую ветвь, `origin/HEAD`, допустимое расхождение и отсутствие сетевых вызовов в `sot_github`.
9. Записать факт в `logs/changes.md`, проверки — в `logs/quality.md`, изменившийся риск — в `logs/risks.md`.

## Проверки

```bash
python3 -B -c 'from pathlib import Path; paths = (Path("tools/check_workspace.py"), Path("tools/check_product.py"), Path("tools/project_profile.py")); [compile(path.read_text(encoding="utf-8"), str(path), "exec") for path in paths]'
python3 -B tools/check_workspace.py --workspace <deployed-workspace>
python3 -B tools/check_product.py --workspace <deployed-workspace>
```

Команды выше выполняются из корня deployed Workspace. `tools/new_project.py` и source-only `tools/bp_clean.py` принадлежат исходной distribution и проверяются Product tests; downstream Workspace их не требует. Project Start не поставляет cleaner; если existing Workspace сохраняет private `tools/bp_workspace_clean.py`, его используют только по локальному cleanup contract.

При изменении Harness, инструментов или тестов добавляется полный применимый регрессионный набор Product Unit. Project Start дополнительно проверяется `tests/test_new_project.py` и настоящими временными E2E для нового и существующего продукта с манифестами источника до и после. Для затронутого продуктового кода добавляются его тесты и проверка запуска; обычная несвязанная правка не требует безусловного полного набора.

## Запреты

1. Не менять связный артефакт без проверки его связей.
2. Не переписывать исторические журналы ради косметической синхронизации.
3. Не выводить продуктовую приёмку, выпуск, тег или GitHub-действия из технического PASS.
4. Не предлагать `system-editing` из `product-work`: при дефекте Harness вывести `HARNESS_BLOCKER: <краткое описание>` и остановиться.

До изменений определить владельцев смысла и потребителей и замкнуть точные `CREATE/UPDATE/PRESERVE/REMOVE` через Impact Scan. После основных действий выполнить Bugfixes и Consistency Closure; PASS требует по `0` устаревших ссылок, пропущенных потребителей, конкурирующих владельцев смысла и неизвестных потребителей.

Полная исходная база фиксируется до первого изменения. В точных разделах WPLAN каждая `CREATE` имеет `file|directory:mode`, каждая `UPDATE` — непустое подмножество `content,mode,type`, каждая `REMOVE` — исходный тип, а `PRESERVE` задаёт неизменяемый путь или дерево. После изменений проверяющий инструмент сопоставляет объявления с фактическими созданием, обновлением и удалением и требует `0` изменений защищённых поверхностей; он не выполняет исправлений.

Вызывающая сторона получает воспроизводимую исходную базу до изменений; проверяющий инструмент не пишет в Workspace:

```bash
python3 -B tools/check_workspace.py --workspace <path> --print-baseline-manifest > <external-complete-baseline.tsv>
```

Полученный stdout имеет точный заголовок `manifest<TAB>1<TAB>complete<TAB>.` и отсортированные строки `type<TAB>mode<TAB>sha256-or--<TAB>relative-path`; этот файл затем передаётся через `--baseline-manifest`. Полнота относится ко всей постоянной области проверки: служебные каталоги `.git/.agents/.codex`, `temp/` и канонические удаляемые остатки исключаются одинаково при выводе исходной базы и вычислении фактических изменений.

## Workspace Update

Workspace Update применяет новую поставку Harness к существующему Workspace. Идентичность проекта, фиксированный корень продукта, WROAD/WBACK/WPLAN, история, исследования, частные изменения и выбранный SoT сохраняются. Project Start создаёт новый Workspace и не используется для обновления. Обновление не является выпуском или Product Acceptance; отдельный инструмент или платформа миграции не нужны.

1. Подтвердить точные границы владельца, прежнюю поставку и развёрнутую версию, идентичность проекта, SoT и следующую точку контроля. Не выводить SoT из физического `.git`. Неясные полномочия, ссылка или специальный узел, несовместимая архитектура или необходимость изменения зависимых проектов требуют STOP.
2. Проверить точную резервную копию или снимок и контрольную сумму, безопасный единственный корень, пути, типы, содержимое и POSIX-режимы. Зафиксировать полный манифест постоянной области, манифесты продукта, частных материалов и истории, префиксы журналов и отдельно исключённые служебные проекции.
3. Только во внешнем временном родительском каталоге создать через Project Start эталонный Workspace из новой поставки. Нейтральные продукт и WROAD служат образцом структуры и не получают полномочий существующего проекта.
4. Сопоставить фиксированный перечень копируемой поставки, создаваемые контракты и частные изменения. Задать точные `CREATE/UPDATE/PRESERVE/REMOVE`. Копируемые поверхности без частных изменений получают точные байты и режимы поставки; создаваемые и частные документы объединяются по смыслу. История и продукт никогда не заменяются эталонным содержимым.
5. При разработке/квалификации контракта Update получить содержательный RED для применимых изменений конфигурации, версии, сохранности, отказов, контрольного чтения и трёх режимов SoT. Deployment использует квалифицированный контракт и не открывает research под старым Harness. Тесты возможности миграции принадлежат тестам продукта; проверки частного обновления собственного Workspace — корневым тестам.
6. При переносе прежней конфигурации остановить обычное исполнение. Удалить старое машинное поле, затем создать канонический `<Slug>.profile` через размещённый рядом `project_profile.serialize_project_profile(profile_name, document)` с прежним развёрнутым `harness_version`. Краткий промежуток без владельца конфигурации явно фиксируется; два машинных источника одновременно не допускаются. Не создавать проекцию или режим совместимости.
7. Обновить только объявленные контракты, инструменты и тесты Harness и прямых потребителей поставки. После обновления всех действующих импортов и команд удалить переходный проверяющий инструмент; обёртку или псевдоним не оставлять. Отдельный частный инструмент ограниченной очистки сохраняет свою ответственность.
8. Проверить обновлённые копируемые байты и режимы, профиль, Slug, корень продукта, настроенный SoT, маршрут, ссылки, защищённые и частные манифесты, префиксы дозаписи, служебные изменения, происхождение и остатки при прежнем `harness_version`. Структурный PASS сам по себе не доказывает обновление: обязательно контрольное чтение фактического развёртывания и результата по каждому пути.
9. Для `sot_files` вызовы Git, запись Git и сеть равны `0`; разрешённый служебный `.git` сохранён и исключён из снимка. Для `sot_git` сохранить ветвь, локальную историю и отсутствие удалённого подключения; выполнить только разрешённую локальную фиксацию обновления. Для `sot_github` дополнительно сохранить отдельную идентичность репозитория, `origin`, отслеживаемую ветвь и ссылку на ветвь по умолчанию; обновление не создаёт полномочий на сеть или запись. Тесты используют только локальные заготовки без сети.
10. Только после успешного контрольного чтения сменить `harness_version` канонической сериализацией на версию применённой поставки. Принадлежащий продукту `VERSION` не меняется вследствие обновления. Зафиксировать наблюдаемые исходное состояние, результат контрольного чтения, переключение версии и итоговое состояние.
11. Повторить полную проверку из корня Workspace и продукта на внешней свежей копии, заготовки всех режимов SoT и свежий Project Start для нового и существующего продукта. Bugfixes и Consistency Closure проверяют всех прямых потребителей; технический PASS не закрывает точку решения владельца по миграции.
12. При отказе прекратить обычное исполнение, сохранить точные промежуточные свидетельства и прежнюю развёрнутую версию. До разрешённого владельцем восстановления не заявлять успешное обновление; восстанавливать по точной резервной копии и манифесту сохранности, без сброса или исправления истории и служебных проекций. После последнего разрешённого изменения создать обычный снимок по процедуре архивации, проверить свежую распаковку и больше не писать в Workspace. Удалить внешний эталон после проверки.

### Внешняя граница Workspace Update

`REQ-BP-UPDATE-001`: Workspace Update — ограниченная операция deployment Harness из новой проверенной distribution над замороженным существующим Workspace. Она не является обычной project work под старым Harness и не требует сначала открывать research/system-editing WPLAN в нём. Старый Workspace должен быть quiescent: active WPLAN count `0`, явно записанный non-executing checkpoint, нет concurrent writes. Если это не так — STOP; существующий active route не закрывается автоматически.

Полномочие операции — фактическое отдельное разрешение владельца на exact snapshot/digest, source distribution identity, target identity и полный update disposition. Это внешний deployment contract, аналогичный границе доверия Project Start; generic implementation OD старого Workspace не синтезируется. Исполнитель работает из новой distribution, сохраняет backup, авторизацию и промежуточные свидетельства вне target. Нового updater executable, режима CLI, сервиса или типа решения нет.

Перед mutation подтвердить старую structural проверку на quiescent Workspace, immutable source/target manifests и authority. Известный отказ старого checker на первом research фиксируется как field evidence; его PASS на таком research не является условием Update. Checker не отключается: после переноса новый checker проверяет обновлённый Harness при прежнем `harness_version`. Ordinary project work и Product mutation остаются под обычными WPLAN/phase/owner gates.

`REQ-BP-UPDATE-002`: сравнить actual trees двух fresh Project Start deployments из exact старой и новой distributions, включая типы, bytes и modes. Fixed COPY list не является полным transition manifest. Каждый изменившийся downstream path получает ровно один disposition: `COPY`, `GENERATED_MERGE`, `PRESERVE`, `REMOVE` или `NOT_APPLICABLE` с причиной. Неизвестный, пропущенный или повторный path — FAIL до mutation. Generated `docs/technical/project-start.md` обязательно получает `GENERATED_MERGE`; mandatory contract нельзя скрыть через PRESERVE/NOT_APPLICABLE. Generated project state/history reference не импортируются. Частный overlay требует явного merge и preservation criteria, а не безусловного COPY.

`REQ-BP-UPDATE-003`: Product, project identity, WROAD/WBACK/completed WPLAN, research/history, SoT и service projections сохраняются. Apply меняет только разрешённый Harness delta. Проверить exact disposition read-back, preservation, новый checker и first research на отдельной копии при старой версии. Затем обновить связанную текстовую проекцию версии и последним среди Harness изменений переключить `harness_version`. После successful final read-back append-only записать evidence операции в обновлённом Workspace; эта ограниченная фиксация является окончанием deployment, а не открытием project work без WPLAN. Дальнейшая работа открывает обычный WPLAN.

При failure не заявлять успешный Update: до cutover старая версия остаётся без изменений; если отказ обнаружен после cutover, восстановить прежний version claim и сохранить точное intermediate evidence вне target. Восстановление Harness выполняется только в заранее разрешённой recovery boundary по backup, без изменения Product/history. Не продолжать обычную работу в промежуточном состоянии. Product tests квалифицируют deployment на self-contained projection настоящего released baseline; changing VERSION текущих исходников не создаёт старую distribution.

## Documentation Impact

При любом изменении продукта исполнитель определяет влияние на документацию. Для S1/S2 активный WPLAN содержит ровно один раздел `Documentation Impact` с полями:

- `Disposition: affected` либо `Disposition: not affected`;
- `Owners: <точные относительные пути владельцев смысла через запятую>`;
- `Reason: <что затронуто либо почему влияния нет>`.

Исполнитель сопоставляет изменение с нуждой читателя: устойчивый смысл продукта, текущий контракт, пользовательский путь, техническая тема, SOP, форма, термин и создаваемый инструментом текст. Поле не заменяет точный манифест миграции; S0 не требует такого объёма свидетельств.

Последовательность: изменение → Documentation Impact → владельцы смысла → связанные документы, SOP, формы и терминология → объективные проверки → применимое чтение человеком → Consistency Closure. Обязательность формы определяет применяющая SOP; наличие шаблона не требует отдельного документа. Пользовательские шаги принадлежат `docs/user`; полномочия агента, точки контроля, STOP и восстановление — соответствующей SOP. [Проверки и критерии чтения](verify-work.md), [изменение терминов](terminology.md) и [русский стиль](../docs/technical/system-style.md) имеют отдельных владельцев.

MOVE/RENAME включает все действующие Markdown-потребители, в том числе ссылки из принятых свидетельств. В таких свидетельствах допустимо только явно разрешённое владельцем ограниченное обслуживание ссылок: перенос адреса 1→1 при неизменных тексте ссылки и окружении; перенос 1→N сохраняет исторический исходный путь некликабельным только по точному разрешению. Все вхождения перечисляются до изменения; обратное преобразование разрешённых участков должно восстановить исходные байты. Находки, решения и выводы не переписываются. Неоднозначность вне разрешения требует STOP. Заглушка совместимости ради истории не создаётся.

## Feedback при Workspace Update

`FB-REQ-11` / `FB-SCN-11`: [модель Feedback](../docs/technical/feedback.md) отделяет static contracts от Workspace data. До apply включить весь `feedback/` target в backup и preservation manifest: пути, типы, bytes, POSIX modes, original/provenance, IDs, связи, закрытые записи и частный индекс. Наличие записей не разрешает active WPLAN или обход quiescent gate.

1. Четыре static owners из [Project Start](../docs/technical/project-start.md#feedback) и изменённые copied consumers получают `COPY`, если private overlay отсутствует. Частные изменения требуют точного `GENERATED_MERGE` с критериями сохранения.
2. Generated README/AGENTS/SYSTEM, docs/user/README.md, docs/technical/README.md и docs/technical/project-start.md получают `GENERATED_MERGE`: обновить ссылки и contracts, сохранить private смысл. Не переносить начальные reference plans/logs или authority.
3. Существующий `feedback/` и всё его содержимое получают `PRESERVE`. Не регенерировать и не перезаписывать `feedback/README.md`, records или original; не менять IDs, modes или private navigation. Если каталог либо README отсутствует, создать только отсутствующий элемент из пустого reference, без records. В полном old/new deployment disposition это условный `GENERATED_MERGE` домена; точный target manifest отдельно фиксирует `CREATE` отсутствующего и `PRESERVE` существующего.
4. У каждого изменённого downstream path должен быть ровно один disposition с причиной; source-only tests/new_project.py не копируются в Workspace. Пропущенный обязательный consumer, replacement данных или неизвестный private overlay дают FAIL до mutation.
5. До version cutover подтвердить static/copied/generated read-back и сохранность всей Feedback data surface. При failure оставить прежнюю версию; исправление только в заранее разрешённой recovery boundary по exact backup. Совпадающий `harness_version` не доказывает тождество candidates: сравнить exact distribution manifest/digest и actual deployed delta. Повторная доставка/Update не импортирует и не дублирует Feedback records.

## Минимальная проверка новой capability

Для S1/S2 перед завершением дать короткое соответствие «пункт → existing owner/evidence → PASS/pending/not-applicable + причина», пропорционально фактическому изменению. Один accepted specification может покрыть несколько пунктов; отдельных документов или нового gate не требуется. Blocking pending criterion остаётся открытым. SDD/DDD, authority и V&V сохраняют действующих owners.

1. Пользователь и наблюдаемая польза.
2. Bounded context, responsibilities и semantic owners без конкурирующих норм.
3. Достаточные inputs и наблюдаемые outputs.
4. Lifecycle, states и guards конкретной capability.
5. Authority и запрещённые автоматические действия.
6. Данные, provenance и неизменяемые части.
7. REQ/INV/SCN и positive/negative/failure cases до реализации по [task-flow](../docs/technical/task-flow.md).
8. Deployment/Workspace Update: static/data separation, full copied/generated/private disposition и preservation по этой SOP.
9. Documentation Impact: owners, инструкция пользователю, SOP/template и все direct navigation/generated consumers.
10. Verification: наблюдаемые оракулы, exact evidence и предел технического PASS по [verify-work](verify-work.md).
11. Реальное применение: пользователь/сценарий, данные и результат; synthetic/self-review не заменяют field use или human Validation.
12. Критерии переноса в Product: что доказано pilot, что осталось проверить и какое отдельное owner authorization требуется по [PM](project-management.md).
