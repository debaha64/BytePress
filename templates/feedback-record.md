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

<!-- Дальнейшие understanding/type/analysis/disposition/result/response/history добавляются только при соответствующем действии по модели, без пустых обязательных блоков. Узкая регистрация использует точную форму из task-intake, источник и прямой запрос в записи. -->

[Модель](../docs/technical/feedback.md) · [SOP](../sops/feedback.md).
