from __future__ import annotations


CHECK_LEVEL = "check"

STATUS_OK = "OK"
STATUS_FAIL = "FAIL"
STATUS_BLOCKED = "BLOCKED"

DEFAULT_FORMAT = "text"
OUTPUT_FORMATS = ("text", "json")

CHECK_ID_MARKDOWN_LINKS = "CHK_MD_LINKS"
CHECK_ID_JSON_SCHEMAS = "CHK_JSON_SCHEMAS"
CHECK_ID_TERM_CARDS = "CHK_TERM_CARDS"
CHECK_ID_TERM_STATUS = "CHK_TERM_STATUS"
CHECK_ID_TERM_CONFLICT_DECISION = "CHK_TERM_CONFLICT_DECISION"

TERM_REQUIRED_FIELDS = (
    "ID",
    "Термин",
    "Статус",
    "Область",
    "Роль",
    "Связи",
    "Источник",
    "Дата_создания",
    "Дата_изменения",
    "Решение_по_конфликту",
)

TERM_REQUIRED_SECTIONS = (
    "Определение",
    "Границы",
    "Ключевые_характеристики",
    "Недопустимые_синонимы",
    "Связанные_термины",
)

TERM_ALLOWED_STATUSES = {
    "Кандидат",
    "Принят",
    "Заменён",
    "Устарел",
    "Запрещён",
}

TERM_ALLOWED_CONFLICT_DECISIONS = {
    "Не_требуется",
    "Принять",
    "Заменить",
    "Запретить",
    "Оставить_кандидатом",
    "Существующий_термин_достаточен",
}

INDEX_SOURCES = (
    ("CHK_INDEX_ROADMAP", "Plans/Roadmap.md", "ROAD"),
    ("CHK_INDEX_BACKLOG", "Plans/Backlog.md", "ROAD|BACK"),
    ("CHK_INDEX_CHANGELOG", "Logs/ChangeLog.md", "CHG"),
    ("CHK_INDEX_QUALITYLOG", "Logs/QualityLog.md", "QL"),
    ("CHK_INDEX_BASE_TERMS", "Docs/Terms/Base_Terms.md", "TERM"),
)

EXTERNAL_SCHEMES = {"http", "https", "mailto", "tel", "app"}
