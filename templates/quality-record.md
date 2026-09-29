# Запись качества

Применение: [sops/record-quality.md](../sops/record-quality.md). Один самостоятельный факт проверки; результат WPLAN ссылается на него, не копирует содержимое.

```text
RECORD_ID: QUALITY-000001
WPLAN_ID: <WPLAN-ID>
VERDICT: <PASS | FAIL>
DATE: YYYY-MM-DD
SUMMARY: <проверенный результат и граница>
SOURCE_REF: <workspace-relative-path>#<anchor-or-lines>
```

- Ожидаемое поведение: <критерий>.
- Наблюдение и команды: <воспроизводимая проверка и её фактический результат>.
- Ограничения: <если есть>.

SOURCE_REF ведёт к сохранённым команде, наблюдению и результату по [контракту свидетельств](../docs/technical/artifact-lifecycle.md#источники-свидетельств). Для прежнего SDLC_TRANSITION добавляется применимый EVIDENCE_KIND. Класс/прослеживаемость, Validation, Product Acceptance, Release Authorization и GUI-свидетельство добавляются только при собственном применимом факте. Неприменимые status/ref и копии текущего WPLAN не требуются.
