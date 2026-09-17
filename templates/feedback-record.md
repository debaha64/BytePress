# FB-<6 digits> — <краткая тема, если известна>

ID: FB-<6 digits>
recorded_at: <фактическая YYYY-MM-DD>
state: open

## Original

````text
<непустой исходный payload без нормализации>
````

<!-- На intake обязательны только ID, recorded_at, original и state. Следующие блоки заполняются при соответствующем действии; отсутствие analysis/версии не блокирует intake. Условия и допустимые значения принадлежат ../docs/technical/feedback.md. -->

## Provenance

<При import/excerpt: source role, local locator, scope и SHA-256 UTF-8 payload; source message date отдельно от event_at, unknown если неизвестна. Достаточный текст хранится локально; внешний locator не является зависимостью. Follow-up добавляется отдельным immutable original fragment с собственной provenance.>

## Понимание

understanding: <смысл опыта или точный пробел>
type: unclassified

## Анализ

<Проверенные факты; выводы; неизвестное; evidence links. Original здесь не заменяется.>

## Исход рассмотрения

disposition: none
reason: <основание после review>

## Связи

<Подписанные work/decision/research/known-problem/change/verification/duplicate-of/related ссылки только при наличии. Work требует отдельного decision ref; priority/assignee/due/queue не вводятся.>

## Результат

result: <факт и ограничения; для fix exact candidate/verification; для no-change причина>

## Ответ

response: draft
<Текст/точная ссылка; для communicated дата и источник факта, для not-applicable точная причина. Owner report отделён от независимого receipt. Draft не закрывает record.>

## История

<Дата — действие, прежний смысл/исход и причина изменения/закрытия/reopen.>

[Модель](../docs/technical/feedback.md) · [SOP](../sops/feedback.md).
