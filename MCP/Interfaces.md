# Interfaces

## Controlled interfaces `BytePress` к MCP

`MCP/*` не является source-of-truth layer и не materialize vendor runtime. Этот домен фиксирует только controlled connector handoff boundary текущего `BytePress`.

### Реестр подключения
Хранит идентификатор, назначение, область доступа, статус и профиль, который допускает подключение.

### Политика доступа
Определяет, кто и в каком режиме может использовать подключение.

### Контур исполнения
Связывает подключение с профилями, ролями, навыками и инструментами без подмены системной логики.

### Граница относительно `Adapters/*`
- `Adapters/*` определяет исполнительный и модельный contour;
- `MCP/*` определяет connector classes, access envelope и допустимые integration handoff points;
- адаптер не становится owner'ом connector registry, а `MCP/*` не становится owner'ом execution mode.

### Граница относительно generated product repo
- generated product repo не получает `MCP/*` в bootstrap-baseline;
- product repo получает только local scripts route, который может вызвать repo-native tool `BytePress`;
- product repo не открывает connector runtime напрямую и не хранит secrets.

### Граница относительно `scripts/*` и `Tools/*`
- `scripts/integration-smoke.sh` в generated product repo является только local entrypoint;
- repo-native tool `BytePress` читает `MCP/*`, `Adapters/*` и product contour как contracts;
- tool возвращает deterministic smoke result и не делает network calls.

## Статус `0.2.0`
Реальные внешние интерфейсы не реализованы. Документ фиксирует только текущую controlled handoff model и границу будущих расширений.
