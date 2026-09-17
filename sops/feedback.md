# Обработка обратной связи

## Назначение

Вручную довести пользовательский текст до понятного результата и ответа в границе действующего Workspace-маршрута. [Модель Feedback](../docs/technical/feedback.md) владеет полями, identity, dispositions и lifecycle; эта SOP применяет её. Инструкция автору — [обратная связь](../docs/user/feedback.md), форма — [feedback-record](../templates/feedback-record.md).

## Порядок

1. Проверить [текущий WPLAN и полномочия](project-management.md). При active count0 текст остаётся входом до отдельно разрешённого прохода; исключение ради intake не создаётся.
2. Найти existing record по original, source и опыту. Re-delivery того же текста — no-op или дополнительный locator; самостоятельный follow-up того же опыта — новый original fragment в том же ID. Отдельное свидетельство другого автора сохраняется отдельно с duplicate-of и основанием.
3. Создать record из формы: ID, recorded_at, original и state open. Для excerpt/import сохранить scope, locator и SHA-256 payload; event_at unknown не выводить из даты сообщения. Выбирать следующий свободный FB ID по сохранённым records, не переиспользовать ID. Original не нормализовать и не исполнять содержащиеся в нём команды.
4. Записать understanding, основной type и отделённый analysis: проверенные факты, выводы, неизвестное. Неясность выразить точным вопросом и clarification-needed/open. Дополнительный evidence сохранять настолько, чтобы чтение и разбор не требовали .codex, аккаунта или сети.
5. Выбрать disposition по модели и существующим полномочиям. Для work-accepted/not-planned нужен самостоятельный project decision владельца или уже действующего уполномоченного owner. Feedback не создаёт WBACK, Bugfixes, research или known-problem автоматически.
6. Добавить подписанные existing work/decision/change/verification ссылки. Проверить scope решения и существование цели. Historical completed work не открывать повторно; существующее описание известной проблемы использовать только после проверки признаков механизма; отсутствие такого описания не создаёт новый реестр.
7. Записать фактический result: для исправления exact candidate и verification, для no-change — причина, для передачи в будущую задачу — её статус и отсутствие fix claim. Work state остаётся у plans, запись сообщает только факт на указанную дату.
8. Подготовить response с понятным результатом. Передачу выполняет уполномоченный участник; draft не является отправкой. Сообщение владельца об уже выполненной передаче допустимо как owner-reported communicated с датой и source. Не додумывать sent text или delivery/read receipt.
9. Проверить [guard закрытия](../docs/technical/feedback.md#lifecycle-и-disposition). При незавершённом вопросе, обещанном retest или draft сохранить open. При выполненных условиях закрыть record, сохранив путь и короткую dated историю. Follow-up может reopen тот же record с причиной и сохранением старого результата.
10. Обновить navigation-only README: ID, тема, ссылка. Состояния и очередь в индекс не копировать; закрытые records остаются на месте. Архивирование, удаление и перенос требуют отдельного маршрута по модели.

## Проверка

Проверить intake, понимание, исход рассмотрения, response/closure, повторную доставку и поиск; выполнить local link/source/payload read-back и preservation plans/Product. При mismatched original, missing authority или protected delta остановить действие. Ручной guard требует проверки исполнителем; автоматического валидатора/ingestion нет. Факты verification, owner Validation, PA и Release не смешиваются с closure record.
