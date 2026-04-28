# Rules

`Rules/` хранит обязательные проектно-специфичные ограничения `BytePress`.

## Назначение
- фиксировать запреты и обязательные условия;
- принимать обязательные нормы, перенесённые из legacy `Standards/*`;
- давать проверяемые границы для агента, человека и инструментов.

## Границы
Правило отвечает на вопрос «что обязательно или запрещено». Рекомендации, которые не являются обязательными условиями, не должны жить в `Rules/*`. Технический договор живёт в `Docs/Technical/*`, а факты выполнения — в `Logs/*`.

## Карта артефактов
- `Repository_As_Source_Of_Truth.md` — репозиторий как источник истины.
- `Domain_Boundaries_Are_Explicit.md` — явные границы доменов.
- `Rules_Are_Not_Standards.md` — разделение правил и стандартов.
- `Logs_Record_Facts_Only.md` — журналы фиксируют только факты.
- `Plans_Require_Approved_Backlog.md` — план должен иметь основание в реестре работ.
- `Runtime_Is_Temporary.md` — `Runtime/` остаётся временным.
- `No_Secrets_In_Git.md` — секреты не попадают в Git.
- `Terms_Governance.md` — ввод терминов проходит через словарь.
- `Contracts_Before_Mass_Content.md` — договоры раньше массового наполнения.
- `Approval_Strictness.md` — строгость утверждений и гейтов.
- `Premature_Domains_Are_Removed.md` — запрет placeholder domains без механизма, потребителя и проверки.

## Куда идти дальше
- migration plan сокращения стандартов: `../Docs/Technical/Domain_Model_Migration_Plan.md`;
- технические границы: `Docs/Technical/README.md`;
- проверка структуры: `Tools/README.md`.
