# Tools

`Tools/` содержит детерминированные инструменты `BytePress`.

## Назначение tooling-layer
`Tools/*` materialize только machine-executable operations поверх уже утверждённых contracts.

Этот слой нужен для ответа на вопросы:
- какие checks уже реально автоматизированы;
- какие future commands допустимы как target tooling horizon;
- где заканчивается tooling и начинается verification/validation contract;
- какие части verification и validation остаются procedural и не переходят в scripts.

## Базовые принципы
- инструмент выполняет воспроизводимую операцию;
- инструмент не подменяет роль и не хранит системное знание;
- инструмент работает с файлами и contracts `BytePress`;
- инструмент не требует конкретной модели;
- инструмент может использоваться как внутри самой системы, так и при инициализации продукта;
- tooling следует documents, а не определяет contract в одиночку.

## Tooling boundary verification и validation contour
`Tools/*` не владеет ни verification-layer, ни validation-layer целиком.

Граница проходит так:
- `Docs/Technical/Verification.md` владеет общей contract map verification-layer;
- `Docs/Technical/Verification_Levels.md` владеет уровнями verification и target split future automation;
- `Docs/Technical/Validation.md` владеет общей contract map validation-layer;
- `Docs/Technical/Validation_Levels.md` и `Docs/Technical/Validation_Evidence.md` владеют уровнями validation, evidence sufficiency и outcome interpretation basis;
- `Pipeline/*` владеет gates и phase approval;
- `Tools/*` владеет только implementation automatic checks, evidence/materialization support и bounded automation scaffolds.

Tooling-layer не должен:
- определять phase approval;
- закрывать pass сам по себе;
- подменять procedural verification;
- подменять procedural validation;
- интерпретировать validation result как final human verdict;
- подменять `Docs/Technical/*` как source of truth для verification и validation contracts.

## Роль `bp_lint.py`
### Текущая роль
`bp_lint.py` является текущим structural check инструмента `BytePress`.

Он отвечает за:
- проверку структурной полноты репозитория `BytePress`;
- проверку минимального bootstrap-contract product repo;
- deterministic pass/fail outcome для structural readiness;
- machine-executable input в verification contour, который validation потом может использовать как часть evidence basis, но не как готовый validation verdict.

### Не роль
`bp_lint.py` не должен:
- становиться общим движком всего verification contour;
- становиться движком validation contour;
- подменять semantic contract audit;
- интерпретировать procedural verification;
- интерпретировать procedural validation;
- принимать gate decision;
- закрывать `Backlog`, `Plan` или `Roadmap`.

### Класс checks
`bp_lint.py` относится к structural checks и к machine-executable readiness layer.

## Target role будущего `bp_check`
`bp_check` пока не реализован и в этом pass не вводится.

Его target role:
- собрать automatic checks verification-контура в один repo-native entrypoint;
- включать structural checks уровня `bp_lint` и другие deterministic contract checks, когда они будут явно описаны и введены;
- давать machine-readable overall result для automatic verification;
- поставлять upstream automatic basis, который validation contour может читать, но не заменять validation interpretation.

`bp_check` должен покрывать:
- structural checks;
- deterministic contract checks;
- automated evidence collection для automatic verification.

`bp_check` не должен:
- подменять procedural review;
- подменять procedural validation;
- автоматически принимать решение о pass closure;
- принимать process gate decision;
- скрывать, какие части verification и validation остались manual.

## Target role будущего `bp_verify`
`bp_verify` пока не реализован и в этом pass не вводится.

Его target role:
- собирать automatic evidence из `bp_check` и related deterministic checks;
- оформлять verification package для procedural verification;
- помогать verification contour и validation contour через handoff package без подмены человеческой интерпретации.

`bp_verify` должен покрывать:
- orchestration automatic evidence;
- scaffold для procedural verification checklist;
- handoff package для pass-close contour и, при необходимости, gate readiness input;
- linkage между automatic verification outputs и тем validation basis, который человек или агент потом интерпретирует процедурно.

`bp_verify` не должен:
- становиться заменой `Verification.md` или `Verification_Levels.md`;
- становиться заменой `Validation.md`, `Validation_Levels.md` или `Validation_Evidence.md`;
- превращаться в gate approval engine;
- автоматически закрывать pass;
- подменять review wording и semantic audit.

## Что может относиться к future validation tooling
Future validation tooling допустим только как support-layer вокруг уже утверждённого validation contract.

Сюда может относиться:
- сбор и упаковка validation basis из уже существующих evidence artifacts;
- checklist scaffold для validation levels без автоматического verdict;
- linkage reports между verification evidence, planning-state и validation scope;
- detection missing evidence или missing linkage для validation handoff;
- materialization summary templates для local pass-close или optional gate handoff.

Это не implementation backlog и не active tool perimeter. Любой такой tooling требует отдельного future pass и не вводится здесь.

## Что не должно автоматизироваться в validation
- интерпретация contract outcome, если она требует инженерного суждения;
- признание evidence package sufficient для local closure claim без procedural owner;
- перевод `Backlog`, `Plan` или `Roadmap` в финальные статусы;
- phase approval и любые gate decisions;
- переинтерпретация contradictions и quality wording, требующая смыслового review.

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

### Validation tooling support
Что это:
- bounded automation, которая помогает собрать validation basis, но не выносит validation verdict сама.

Где живёт:
- как future tooling target рядом с `bp_verify` или отдельным validation-support tool, если такой contract когда-нибудь будет явно введён.

Что сюда может входить:
- linkage validation inputs к текущему scope;
- summary missing evidence;
- packaging validation evidence bundle;
- scaffold для handoff note.

Что сюда не входит:
- outcome interpretation;
- closure approval;
- gate approval.

### Procedural validation
Что это:
- подтверждение или неподтверждение outcome относительно contract на основе evidence package и active artifacts.

Где живёт:
- в validation contour и governance practice, а не в `Tools/*`.

Что сюда входит:
- interpretation classes `validated`, `not_validated`, `validation_blocked`;
- решение, достаточен ли basis для local closure claim;
- явное различение validation result и gate decision.

## Граница между tooling support и human/procedural validation
Граница проходит так:
- tooling может собрать, связать и показать evidence bundle;
- tooling может подсветить missing inputs или missing linkage;
- tooling не должен сам утверждать validation result;
- human/agent pass owner остаётся owner procedural validation и его wording.

Следствие:
- даже полный future validation support package не равен `validated`;
- отсутствие tooling не запрещает procedural validation, если basis собран вручную и отражён в active artifacts.

## Граница между validation result и gate decision
Validation result и gate decision не совпадают даже при полном evidence package.

Validation result:
- подтверждает или не подтверждает outcome относительно contract;
- принадлежит validation contour;
- может стать input в gate contour.

Gate decision:
- разрешает или не разрешает phase transition;
- принадлежит `Pipeline/*` и process owner;
- не автоматизируется этим tooling boundary.

## Что не должно смешиваться
- `bp_lint` не должен называться полным verification engine;
- `bp_lint` не должен называться validation engine;
- future `bp_check` не должен включать process gate approval;
- future `bp_verify` не должен маскироваться под purely automatic check;
- future validation tooling не должно маскироваться под verdict engine;
- procedural verification не должно скрываться под shell command;
- procedural validation не должно скрываться под shell command;
- validation result не должен называться gate approval;
- documents не должны повторять implementation code, а tooling не должен становиться owner verification/validation contract.

## Текущий набор инструментов
### Обязательные repo-native tools
- `bp_lint.py` — текущий structural check `BytePress` и product bootstrap contract.
- `bp_bootstrap.py` — materialization first-usable replicated product repo по contract `BytePress`.
- `bp_integration_smoke.py` — deterministic integration smoke route для generated product repo без реальных внешних подключений.
- `bp_normalize_terms.py` — нормализация карточек терминов и пересборка индекса `Base_Terms.md`.

### Future tooling horizon
- `bp_check` — допустим как future automatic verification entrypoint.
- `bp_verify` — допустим как future verification-orchestration entrypoint.
- validation-support tooling — допустим только как future support-layer для packaging/linkage/scaffold validation basis.

Оба future commands:
- не реализуются этим pass;
- не считаются частью active tool perimeter до отдельного tooling pass;
- не должны проектироваться здесь как implementation spec.

Future validation-support tooling:
- не реализуется этим pass;
- не считается частью active tool perimeter до отдельного tooling pass;
- не должен описываться здесь как verdict engine или gate engine.

## Актуальный bootstrap contract
- `bp_bootstrap.py` требует `--name`, `--product-code`, `--brand-profile`, `--target`;
- `--product-code` обязателен, содержит 2-3 символа верхнего регистра и не генерируется автоматически;
- `--brand-profile` обязателен и валидируется по существующим brand profiles в `BytePress`;
- bootstrap создаёт `README.md`, `AGENTS.md`, `Setup_Guide.md` и обязательный `Docs/User/*` contour replicated repo;
- bootstrap создаёт канонический минимальный продуктовый слой `Docs/Product/README.md`, `Docs/Product/JTBD.md`, `Docs/Product/PRD.md`, `Docs/Product/Delivery.md`;
- bootstrap создаёт `Docs/Terms/README.md` и `Docs/Terms/Base_Terms.md` со стартовым пакетом терминов вместо полного term-layer `BytePress`;
- bootstrap создаёт `Profiles/Product.md`, adapter policy/registry и initial plan file `Plans/<PRODUCT_CODE>-000001-product-initialization.md`;
- bootstrap создаёт `scripts/integration-smoke.sh` как отдельный controlled handoff route к integration smoke tooling `BytePress`;
- bootstrap materialize initial `Roadmap`, `Backlog` и `Plan` продукта в состоянии `В_работе`;
- `bp_lint.py` требует `Templates/Delivery.md` в `BytePress` и проверяет наличие полного минимального `Docs/Product/*` набора в product repo;
- `bp_lint.py` проверяет наличие `AGENTS.md`, короткого стартового отчёта с приветствием, обязательного `Docs/User/*`, starter terms в `Docs/Terms/Base_Terms.md`, adapter policy/registry, `scripts/integration-smoke.sh`, `.gitignore` c `.codex/`, смысловых классов интервью и first-usable replicated planning contour;
- `bp_lint.py` требует `Docs/Discovery/README.md`, `Docs/Discovery/Interview.md` и `Templates/Interview.md` в `BytePress`;
- `bp_integration_smoke.py` проверяет, что generated product repo использует только local integration handoff и не materialize `MCP/*` или реальные внешние подключения;
- bootstrap использует 6-значные ID и текущую дату выполнения, без жёстко прошитых дат;
- из brand profile наследуются только `Брендовый_профиль` и `Язык_взаимодействия`.

## Отношение к соседним контурам
### К `Docs/Technical/*`
`Docs/Technical/*` владеет contracts verification-system и validation-system. `Tools/*` materialize только automatic part этих contracts и допустимый support-layer вокруг evidence/materialization.

### К `Verification.md`
`Verification.md` объясняет, как verification contour устроен в целом. `Tools/README.md` объясняет, какую часть этого contour реально занимает tooling.

### К `Verification_Levels.md`
`Verification_Levels.md` задаёт уровни и target split automation. `Tools/README.md` фиксирует, какие future roles у tooling возможны внутри этого split.

### К `Validation.md`
`Validation.md` объясняет, как validation contour интерпретирует outcome и evidence. `Tools/README.md` фиксирует только ту automation support boundary, которая может помочь validation без подмены verdict owner.

### К `Validation_Levels.md` и `Validation_Evidence.md`
Эти documents задают уровни validation, evidence sufficiency и outcome basis. `Tools/README.md` фиксирует, что tooling может только поддерживать сбор, linkage и packaging этого basis.

### К `Pipeline/*`
`Pipeline/*` остаётся owner gates. `Tools/*` может дать evidence input, но не владеет phase approval.

## Граница документа
`Tools/README.md` не является:
- implementation spec будущих `bp_check` / `bp_verify`;
- verification contract map;
- gate policy;
- procedural verification manual.

Он остаётся boundary-document tooling verification и validation contour, а также общего tool perimeter `BytePress`.

## Связи
- `ADR-000007`
- `ADR-000009`
- `CHG-000007`
- `CHG-000009`
