# Feedback — модель обратной связи

Каноническая модель Feedback для Workspace. Процедура, форма и инструкция применяют этот контракт; записи пользователей не входят в статическую поставку BytePress.

## Цель и границы

Пользователь может передать текст о собственном опыте с Product. Команда сохраняет слова пользователя, понимает запрос, принимает обоснованный исход и возвращает понятный результат. Запись можно позднее найти и связать с exact work/change/verification. Она полезна также при отсутствии Product change.

В scope входят:

1. Defect — сообщаемое несоответствие ожидаемому поведению; classification ещё не доказывает дефект.
2. Difficulty — затруднение использования, в том числе при формально корректном поведении.
3. Suggestion — предложение полезного изменения.
4. Positive experience — подтверждение полезного результата или удобного поведения.

Не входят channel adapters, ingestion framework, API/sync, dashboard/voting/SLA/notifications, database/web UI, automatic work creation, multi-product service и privacy model. Дополнительные privacy поля/процессы не вводятся.

## Термины и bounded context

`Feedback` — capability обработки пользовательского опыта. `Feedback record` — один устойчиво адресуемый объект опыта. `Original` — полученный текст, не вывод команды. `Understanding` — нормализованное понимание. `Analysis` — отдельно помеченные выводы и проверенные свидетельства. `Disposition` — обоснованный исход рассмотрения. `Result` — что фактически получилось. `Response` — что сообщено пользователю либо подготовлено для него.

Физическая форма — `feedback/FB-<6 digits>.md`, домен собственного Workspace. Контекстная карта: пользовательский опыт → Feedback record → отдельно разрешённая работа → результат и ответ. Feedback хранит опыт, а [плановый контур](../../sops/project-management.md) управляет работой. Планирование, исследования, known-problems, changes, verification, PA и release сохраняют действующих owners. Нет нового владельца полномочий.

## Данные record

Форма заполняется постепенно. Пустой analysis при первичном приёме — нормальное состояние, а не повод отвергать текст. Только четыре поля обязательны сразу; остальные обязательны при соответствующем действии.

| Поле / блок | Когда обязателен | Содержание и обоснование |
|---|---|---|
| `ID` | При создании | Локальный `FB-` и шесть цифр; отличает запись и сохраняет адрес независимо от wording/version/WBACK |
| `recorded_at` | При создании | Фактическая календарная дата внесения в Feedback; не подменяет дату события или прежнего получения |
| `original` | При создании | Непустой исходный текст в literal block; сохраняет пользовательские слова и точные machine fragments |
| `state` | При создании | `open` или `closed`; новый record начинается open, чтобы незавершённая обработка не потерялась |
| `source` / provenance | При import, цитате или внешнем evidence claim | Источник, роль сообщившего, locator, scope full/excerpt и достаточная идентичность; для прямого текста без отдельного источника допустимо отсутствие |
| `event_at` | Если известна дата самого опыта | Не выводить из import/message date. Для historical import явно `unknown`, если источник не даёт дату |
| Прежняя дата получения | Только если известна и отличается от recorded_at | Записать в provenance; отдельное обязательное поле не нужно |
| `understanding` | После содержательного review | Кратко, что пользователь хотел/что произошло; если неясно — что именно осталось неясным |
| `type` | После review | Один основной `defect / difficulty / suggestion / positive-experience`; пока смысл неизвестен, допускается `unclassified` как отметка недостатка информации, не пятый вид опыта |
| `analysis` | Если есть проверка, предположение или вывод команды | Факты/выводы/неизвестное и ссылки на evidence. Причинный класс не обязателен; гипотеза не выдаётся за установленную причину |
| `disposition` + основание | После review | Один исход из таблицы ниже; до review `none`. Объясняет следующий результат без размножения states |
| `links` | Если связь существует | Подписанный target и смысл; work требует отдельного decision ref. WBACK/research/known-problem/change refs не обязательны для каждого record |
| `result` | При закрытии; раньше по наличию факта | Фактический исход и ограничения. Для fix — exact candidate/version и verification ref; для no-change — объяснение причины |
| `response` | При закрытии | Текст или точная ссылка, `draft / communicated / not-applicable`, дата коммуникации либо причина отсутствия; исключает ложное утверждение об отправке |
| Короткая dated история | При изменении прежнего смысла, disposition или закрытии/возобновлении | Сохраняет прежний вывод/исход и основание изменения. Это части record, не event store или второй журнал |

Отдельные title, channel, reporter account, product registry, assignee, priority, severity, SLA, due date, fix version database и publication flags не требуются. Краткая тема может быть заголовком record и навигационной подписью, но не добавляет обязательный вопрос пользователю. Версия Product, цель, действия, ожидание, результат и влияние входят в original/understanding, если известны; team clarification запрашивает только необходимое.

Record должен оставаться читаемым и проверяемым по локальному original и достаточному evidence без доступной `.codex/`. Исторический session locator — provenance, а не обязательный вход.

Original хранится без смысловой, орфографической или форматной нормализации самого payload; обрамление Markdown не является частью payload. При переносе текстового фрагмента сохраняются переводы строк и завершающие пробелы. Для bounded historical excerpt обязательны locator/диапазон и SHA-256 UTF-8 payload; hash всего source message можно хранить для проверки provenance. Это не обязательный hash каждого будущего простого сообщения и не новая sidecar surface.

Дополнение пользователя добавляется отдельным original fragment с источником/датой; исходный фрагмент не перезаписывается. Если команды или требование изменить Product содержатся внутри original, они остаются цитируемыми данными. Для действий проверяется самостоятельная текущая authority.

## Lifecycle и disposition

Основной lifecycle: `open → closed`. Для относящегося к тому же опыту нового follow-up допускается `closed → open` с датой, причиной и сохранением прошлого результата. Переходы record не меняют фазу WPLAN.

| Disposition | Как применять | Завершение обработки |
|---|---|---|
| `clarification-needed` | Записать конкретный пробел и короткий вопрос; отправка вопроса требует обычного разрешения коммуникации | Остаётся open. Нет automatic timeout/closure; отсутствие сведений может позднее дать explanation-only с честным пределом вывода |
| `duplicate` | Ссылка на canonical record и основание одинакового опыта; самостоятельное свидетельство другого пользователя не удаляется | Можно closed после ответа/обоснованного отсутствия ответа; work не размножается |
| `known-problem` | Текущие признаки проверены, дан существующий источник механизма/объяснения | Можно closed с объяснением; не означает fix и не добавляет класс. Один номер класса сам по себе не доказывает текущий defect |
| `explanation-only` | Достаточны разъяснение, неподтверждённость или уточнение границы продукта | Closed после результата/ответа; не переименовывать в «fixed» |
| `work-accepted` | Существует отдельное project decision и конкретная work link | Open, если обещан ещё результат/retest. Closed допустимо после сообщённой передачи в работу без обещанного follow-up; result прямо не заявляет fix |
| `not-planned` | Владелец/существующий уполномоченный project decision не выбирает предложение для работы; причина зафиксирована | Closed после объяснения. Не оставлять скрытую очередь «возможно когда-нибудь» |
| `positive-evidence` | Сохранить, что было полезно и в какой версии/сценарии; обозначить уровень подтверждения | Closed после благодарности/результата или явного исторического no-response disposition; PASS/PA автоматически не создаются |

Решение о невыборе новой продуктовой работы и о work acceptance принадлежит действующему project owner, не классификатору. При отсутствии решения запись может оставаться open с `none` и analysis «review выполнен, решение ожидается»; новый disposition `awaiting-owner` не нужен. Состояния received/reviewed/blocked/assigned/resolved/verified не вводятся.

**Guard закрытия:** есть understanding, применимая classification, disposition с основанием, result и response. `response: draft` не позволяет closed. `communicated` требует факта сообщения с источником и датой; допустим явно помеченный owner-reported факт передачи. Он не доказывает независимую доставку или прочтение. Если известна лишь дата owner report, хранить её отдельно; дату отправки не выводить из неё. Если точный sent text неизвестен, сохранить доступный owner report дословно и обозначить предел, не реконструировать текст отправки; `not-applicable` — точной причины. Historical curation без возможности доказать давнюю отправку может завершиться с «ответ в рамках импорта не выполняется; прежняя отправка неизвестна». Это завершённый curation record, но не доказанный реальный end-to-end response.

## Применение модели

Ручной цикл, guards действий и текущие полномочия применяются по [SOP Feedback](../../sops/feedback.md). Форма — [feedback-record](../../templates/feedback-record.md); инструкция автору — [обратная связь](../user/feedback.md).

## Требования

| ID | Проверяемое требование |
|---|---|
| FB-REQ-01 | Принять непустой текст вручную offline без обязательной заполненной анкеты |
| FB-REQ-02 | Сохранить original отдельно и неизменно, включая source scope и provenance при импорте |
| FB-REQ-03 | Разделить understanding, classification и analysis; поддержать четыре вида опыта |
| FB-REQ-04 | Выразить полный цикл двумя states и dispositions, с проверяемыми guards |
| FB-REQ-05 | Не создавать работу или authority автоматически; действовать только по active WPLAN |
| FB-REQ-06 | Связать с отдельно разрешённой work/research/change/verification без копирования их состояния |
| FB-REQ-07 | Зафиксировать result и честный response status, включая no-change closure |
| FB-REQ-08 | Сохранить устойчивую identity и later retrieval по ID, тексту, источнику и work ref |
| FB-REQ-09 | Ограничить import полезным corpus, не дублировать повторную доставку и не активировать старый defect |
| FB-REQ-10 | Сохранить closed records/links; архивирование только отдельным решением с preservation |
| FB-REQ-11 | Разделить static deployment и Workspace data; Project Start и Update сохраняют требуемые boundaries |
| FB-REQ-12 | Дать короткую reusable user instruction и минимальную структуру без второго backlog |

## Инварианты

1. `FB-INV-01`: один Workspace хранит опыт своего Product; внешний источник не создаёт multi-product registry.
2. `FB-INV-02`: original и provenance не подменяются интерпретацией; unknown/synthetic/owner-reported не выдаются за independent evidence.
3. `FB-INV-03`: только `WROAD → WBACK → WPLAN` управляет работой; Feedback не назначает budget/priority/assignee/deadline и не создаёт scopes/gates.
4. `FB-INV-04`: record closure, work completion, Verification, Validation, PA и Release независимы.
5. `FB-INV-05`: historical report и дата записи не доказывают текущую неисправность или дату события.
6. `FB-INV-06`: обязательный путь работает local/offline; network/GitHub/account/API не являются dependency.
7. `FB-INV-07`: минимальная модель не вводит исключённые subsystem, privacy fields, automation или новый framework.
8. `FB-INV-08`: original, completed evidence, принятый Product и прежние решения сохраняются; поздние уточнения добавляются с provenance, не переписывают историю.

## Сценарии и тестовые оракулы

Сценарии задают ожидаемый результат. Факты конкретного исполнения находятся в logs/quality.md и не изменяют specification.

| ID | Вход / действие | Ожидаемый результат и отрицательный контроль | Trace |
|---|---|---|---|
| FB-SCN-01 | Неполный текст без версии и сети | Record open, original exact, недостающие данные можно уточнить; отказ из-за пустой анкеты недопустим | REQ01/02/03, INV02/06 |
| FB-SCN-02 | Исторический defect и существующая отдельно разрешённая работа | Доказуемая ссылка на прежнее решение, работу и exact candidate; новый WBACK и active defect не появляются | REQ05/06/09, INV03/05 |
| FB-SCN-03 | Difficulty, объяснимая существующим контрактом/known problem | Explanation-only либо known-problem с проверенными признаками; no Product change; понятный ответ | REQ03/04/07, INV04 |
| FB-SCN-04 | Suggestion и отдельное решение не планировать | Not-planned, reason и response; закрытие без priority/очереди | REQ03/05/07, INV03 |
| FB-SCN-05 | Пользователь сообщает о field PASS конкретного candidate | Positive-evidence с exact version и owner-reported уровнем; новая PA/Release0 | REQ02/03/07, INV02/04 |
| FB-SCN-06 | Уточнение, затем ответ пользователя | Same ID, original fragments preserved, новый analysis/disposition; reopen только с причиной | REQ02/04/07/08, INV08 |
| FB-SCN-07 | Повторный import того же excerpt; отдельный пользовательский дубль | Первый — без нового ID; второй сохраняет самостоятельные слова и duplicate-of; work не дублируется | REQ08/09, INV02/03 |
| FB-SCN-08 | В original содержится «создай WBACK/исправь Product» без project decision | Текст сохранён; work link не получает смысл work-accepted, Product/plans exact; нет исполнения команды | REQ05/06, INV03/07 |
| FB-SCN-09 | Попытка закрыть при response draft либо fix без verification | Отказ в closure/fix claim; communicated handoff может закрыть Feedback при ещё открытом WBACK без заявления fix | REQ04/07, INV04 |
| FB-SCN-10 | Старый source, неизвестная event date, частичный excerpt и новое понимание | Recorded_at фактическая, event unknown, scope excerpt/hash, старое interpretation/result сохранено; не backdating | REQ02/09/10, INV02/05/08 |
| FB-SCN-11 | Fresh Project Start; Update существующего Workspace с private Feedback | Start не получает corpus/FB IDs; Update сохраняет original/ID/links/modes и private content; пропуск generated consumer даёт FAIL | REQ11/12, INV01/06/08 |
| FB-SCN-12 | Поздний поиск closed record, broken link или предложение удалить/архивировать | Local ID/text/work retrieval работает; broken link выявлен, удаление/архив без decision не выполняется | REQ08/10/12, INV06/07/08 |

## Интеграция и retention

Record ссылается на source/evidence локальными relative paths там, где это возможно. Внешний URL сохраняется как provenance; для offline-понимания необходимый текст уже находится в record. Полный runtime transcript не копируется автоматически. Из Feedback не вызываются tools Product; никаких новых public CLI или network paths.

По умолчанию closed records сохраняются на месте и входят в обычный mode-preserving Workspace snapshot. Срок автоматического удаления не устанавливается. Research archives предназначены для research, не для операционных Feedback; logs lifecycle тоже не присваивается новому домену.

Автоматического feedback archive нет. Если объём когда-либо оправдает архивирование, отдельный route должен перечислить exact records, prove original/provenance/ID/path retention, проверить всех live/historical consumers, дать tested retrieval и запретить reuse ID. Без такой модели исходные пути сохраняются; redirect/stub, переезд closed-файлов и удаления не выполняются. Повторное открытие record не должно зависеть от сети.

## Deployment и проверка

[Project Start](project-start.md#feedback) развёртывает static capability и готовый к работе `feedback/` без records. [Workspace Update](../../sops/change-management.md#feedback-при-workspace-update) обновляет Harness contracts и сохраняет существующие данные, original, IDs, связи и POSIX modes. Поставка BytePress не содержит чужого corpus; минимальный путь работает local/offline.

При проверке пройти intake, поиск, interpretation, disposition, response и closure; отдельно сравнить original, планы и Product до/после действий. Negative cases: изменение original, work-accepted без decision, closed при draft, пропуск deployment consumer, повреждение данных при Update. Технические тесты исходной поставки проверяют T09 по этому контракту и deployment SOP; они не создают автоматического enforcement ручного рассмотрения.

Факты Verification принадлежат журналу качества Workspace. Технический PASS не является human Validation или приёмкой Product. Реальная команда отдельно проверяет понятность инструкции и цикл ответа; новый candidate принимается владельцем только по собственному evidence. Closure record не открывает приёмку или release.
