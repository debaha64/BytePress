# Tools

`Tools/` содержит детерминированные инструменты `BytePress`.

## Назначение tooling-layer
`Tools/*` materialize только machine-executable operations поверх уже утверждённых contracts.

Этот слой нужен для ответа на вопросы:
- какие checks уже реально автоматизированы;
- какие future commands допустимы как target tooling horizon;
- где заканчивается tooling и начинается verification contract;
- какие части verification остаются procedural и не переходят в scripts.

## Базовые принципы
- инструмент выполняет воспроизводимую операцию;
- инструмент не подменяет роль и не хранит системное знание;
- инструмент работает с файлами и contracts `BytePress`;
- инструмент не требует конкретной модели;
- инструмент может использоваться как внутри самой системы, так и при инициализации продукта;
- tooling следует documents, а не определяет contract в одиночку.

## Tooling boundary verification-контура
`Tools/*` не владеет verification-layer целиком.

Граница проходит так:
- `Docs/Technical/Verification.md` владеет общей contract map verification-layer;
- `Docs/Technical/Verification_Levels.md` владеет уровнями verification и target split future automation;
- `Pipeline/*` владеет gates и phase approval;
- `Tools/*` владеет только implementation automatic checks и materializers.

Tooling-layer не должен:
- определять phase approval;
- закрывать pass сам по себе;
- подменять procedural verification;
- подменять `Docs/Technical/*` как source of truth для verification contracts.

## Роль `bp_lint.py`
### Текущая роль
`bp_lint.py` является текущим structural check инструмента `BytePress`.

Он отвечает за:
- проверку структурной полноты репозитория `BytePress`;
- проверку минимального bootstrap-contract product repo;
- deterministic pass/fail outcome для structural readiness.

### Не роль
`bp_lint.py` не должен:
- становиться общим движком всего verification contour;
- подменять semantic contract audit;
- интерпретировать procedural verification;
- принимать gate decision;
- закрывать `Backlog`, `Plan` или `Roadmap`.

### Класс checks
`bp_lint.py` относится к structural checks и к machine-executable readiness layer.

## Target role будущего `bp_check`
`bp_check` пока не реализован и в этом pass не вводится.

Его target role:
- собрать automatic checks verification-контура в один repo-native entrypoint;
- включать structural checks уровня `bp_lint` и другие deterministic contract checks, когда они будут явно описаны и введены;
- давать machine-readable overall result для automatic verification.

`bp_check` должен покрывать:
- structural checks;
- deterministic contract checks;
- automated evidence collection для automatic verification.

`bp_check` не должен:
- подменять procedural review;
- автоматически принимать решение о pass closure;
- принимать process gate decision;
- скрывать, какие части verification остались manual.

## Target role будущего `bp_verify`
`bp_verify` пока не реализован и в этом pass не вводится.

Его target role:
- собирать automatic evidence из `bp_check` и related deterministic checks;
- оформлять verification package для procedural verification;
- помогать верифицировать pass-close contour без подмены человеческой интерпретации.

`bp_verify` должен покрывать:
- orchestration automatic evidence;
- scaffold для procedural verification checklist;
- handoff package для pass-close contour и, при необходимости, gate readiness input.

`bp_verify` не должен:
- становиться заменой `Verification.md` или `Verification_Levels.md`;
- превращаться в gate approval engine;
- автоматически закрывать pass;
- подменять review wording и semantic audit.

## Классы checks и их место
### Structural checks
Что это:
- machine-executable checks на structural readiness и базовую целостность репозитория.

Где живут:
- в `Tools/*`, сейчас прежде всего в `bp_lint.py`.

Что сюда входит:
- `git diff --check` как shell-level structural signal;
- `python3 Tools/bp_lint.py --repo .`.

### Contract / verification checks
Что это:
- automatic deterministic checks, которые подтверждают отдельные contracts verification-layer.

Где живут:
- как future tooling target внутри `bp_check`, если contract явно введён;
- contract meaning живёт в `Docs/Technical/*`, не в code.

Что сюда не входит:
- manual interpretation;
- gate approval;
- pure semantic review текста.

### Procedural verification
Что это:
- проверки, которые требуют инженерного суждения, governance interpretation и pass-level review.

Где живёт:
- в verification contour и governance practice, а не в `Tools/*`.

Что сюда входит:
- governance-сверка backlog/roadmap/plan;
- semantic audit противоречий в active layer;
- решение о достаточности evidence для pass-close contour.

## Что не должно смешиваться
- `bp_lint` не должен называться полным verification engine;
- future `bp_check` не должен включать process gate approval;
- future `bp_verify` не должен маскироваться под purely automatic check;
- procedural verification не должно скрываться под shell command;
- documents не должны повторять implementation code, а tooling не должен становиться owner verification contract.

## Текущий набор инструментов
### Обязательные repo-native tools
- `bp_lint.py` — текущий structural check `BytePress` и product bootstrap contract.
- `bp_bootstrap.py` — materialization минимального product skeleton по contract `BytePress`.
- `bp_normalize_terms.py` — нормализация карточек терминов и пересборка индекса `Base_Terms.md`.

### Future tooling horizon
- `bp_check` — допустим как future automatic verification entrypoint.
- `bp_verify` — допустим как future verification-orchestration entrypoint.

Оба future commands:
- не реализуются этим pass;
- не считаются частью active tool perimeter до отдельного tooling pass;
- не должны проектироваться здесь как implementation spec.

## Актуальный bootstrap contract
- `bp_bootstrap.py` требует `--name`, `--product-code`, `--brand-profile`, `--target`;
- `--product-code` обязателен, содержит 2-3 символа верхнего регистра и не генерируется автоматически;
- `--brand-profile` обязателен и валидируется по существующим brand profiles в `BytePress`;
- bootstrap создаёт канонический минимальный продуктовый слой `Docs/Product/README.md`, `Docs/Product/JTBD.md`, `Docs/Product/PRD.md`, `Docs/Product/Delivery.md`;
- bootstrap создаёт `Profiles/Product.md` и initial plan file `Plans/<PRODUCT_CODE>-000001-product-initialization.md`;
- `bp_lint.py` требует `Templates/Delivery.md` в `BytePress` и проверяет наличие полного минимального `Docs/Product/*` набора в product repo;
- `bp_lint.py` требует `Docs/Discovery/README.md`, `Docs/Discovery/Interview.md` и `Templates/Interview.md` в `BytePress`;
- bootstrap использует 6-значные ID и текущую дату выполнения, без жёстко прошитых дат;
- из brand profile наследуются только `Брендовый_профиль` и `Язык_взаимодействия`.

## Отношение к соседним контурам
### К `Docs/Technical/*`
`Docs/Technical/*` владеет contracts verification-system. `Tools/*` materialize только automatic part этих contracts.

### К `Verification.md`
`Verification.md` объясняет, как verification contour устроен в целом. `Tools/README.md` объясняет, какую часть этого contour реально занимает tooling.

### К `Verification_Levels.md`
`Verification_Levels.md` задаёт уровни и target split automation. `Tools/README.md` фиксирует, какие future roles у tooling возможны внутри этого split.

### К `Pipeline/*`
`Pipeline/*` остаётся owner gates. `Tools/*` может дать evidence input, но не владеет phase approval.

## Граница документа
`Tools/README.md` не является:
- implementation spec будущих `bp_check` / `bp_verify`;
- verification contract map;
- gate policy;
- procedural verification manual.

Он остаётся boundary-document tooling verification-контура и общего tool perimeter `BytePress`.

## Связи
- `ADR-000007`
- `ADR-000009`
- `CHG-000007`
- `CHG-000009`
