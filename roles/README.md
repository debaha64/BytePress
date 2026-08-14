# Роли Product Unit

`roles/` хранит контракты основных ролей канонических фаз SDLC: ответственность, полномочия, запреты, границу владельца, ожидаемый результат и передачу.

Граница слоя:

1. Одна каноническая фаза имеет ровно одну самостоятельную основную роль.
2. Один исполнитель может последовательно принимать несколько ролей; сущности ролей разных фаз не объединяются.
3. Контракт роли ссылается на процедуры, но не владеет SOP, PLAN или SYSTEM-инвариантами и не расширяет их разрешения.
4. Канонический полный SDLC находится в [docs/technical/sdlc.md](../docs/technical/sdlc.md), процедуры — в [sops/](../sops/README.md).

## Соответствие фаз и ролей

1. `01 Замысел` — [Concept Developer](01-concept-developer.md).
2. `02 Обсуждение` — [Discussion Facilitator](02-discussion-facilitator.md).
3. `03 Интервью` — [Interviewer](03-interviewer.md).
4. `04 Исследование` — [Researcher](04-researcher.md).
5. `05 Требования` — [Requirements Engineer](05-requirements-engineer.md).
6. `06 Основание` — [Systems Analyst](06-systems-analyst.md).
7. `07 Архитектура` — [Architect](07-architect.md).
8. `08 Проектирование` — [System Designer](08-system-designer.md).
9. `09 Планирование` — [Planner](09-planner.md).
10. `10 Утверждение` — [Decision Coordinator](10-decision-coordinator.md).
11. `11 Реализация` — [Developer](11-developer.md).
12. `12 Проверка` — [Verification Engineer](12-verification-engineer.md).
13. `13 Обзор владельцем` — [Review Coordinator](13-review-coordinator.md).
14. `14 Продуктовая приёмка` — [Product Acceptance Coordinator](14-product-acceptance-coordinator.md).
15. `15 Готовность к выпуску` — [Release Readiness Reviewer](15-release-readiness-reviewer.md).
16. `16 Выпуск` — [Release Engineer](16-release-engineer.md).
17. `17 Передача` — [Transition Coordinator](17-transition-coordinator.md).
18. `18 Эксплуатация` — [Operator](18-operator.md).
19. `19 Сопровождение` — [Maintenance Engineer](19-maintenance-engineer.md).
20. `20 Ретроспектива` — [Retrospective Facilitator](20-retrospective-facilitator.md).
21. `21 Вывод из эксплуатации` — [Decommissioning Engineer](21-decommissioning-engineer.md), terminal state: `retired`.
