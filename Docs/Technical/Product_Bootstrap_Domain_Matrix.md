# Product Bootstrap Domain Matrix

## Назначение
`Docs/Technical/Product_Bootstrap_Domain_Matrix.md` фиксирует каноническую классификацию всех top-level доменов `BytePress` для product bootstrap.

Этот document отвечает на вопросы:
- какие top-level домены materialize по умолчанию в generated product repo;
- какие домены не materialize в bootstrap default и могут появиться только отдельным product-pass;
- какие домены остаются только в самом `BytePress`;
- есть ли в текущем каноне optional bootstrap profile.

## Категории матрицы
- `Default` — materialize текущим bootstrap contract как часть first-usable generated product repo.
- `Optional` — materialize только отдельным явно поддержанным bootstrap profile. В текущем каноне таких доменов нет.
- `Later product-pass` — не materialize bootstrap'ом; могут появиться в product repo только отдельным утверждённым product-pass.
- `BytePress-only` — не materialize в product repo текущим каноном и не считаются частью раннего product-side replication contour.

## Каркас репозитория по матрице
Термин `Каркас репозитория` в bootstrap scope означает именно bootstrap-default из этой матрицы:
- `README.md`
- `AGENTS.md`
- `Setup_Guide.md`
- `.gitignore`
- `scripts/*`

и default-домены:
- `Docs/*` только в минимальном startup subset;
- `Plans/*`;
- `Logs/*`;
- `Runtime/*`;
- `Profiles/Product.md`;
- `Adapters/*`.

Это не полная копия доменной структуры `BytePress`, а только обязательный bootstrap outcome раннего product-start.

## Каноническая матрица
| Top-level domain `BytePress` | Канон | Product-side materialization | Причина |
| --- | --- | --- | --- |
| `Docs/` | `Default` | materialize только минимальный startup subset: `Docs/Discovery/*`, `Docs/User/*`, `Docs/Product/*`, ограниченный `Docs/Technical/*`, `Docs/Terms/Base_Terms.md` и `Docs/Terms/README.md` | generated repo должен иметь current-truth route, human entry, product placeholders, минимальный technical contour и стартовый пакет терминов, но не полную копию knowledge-layer `BytePress` |
| `Plans/` | `Default` | materialize initial roadmap/backlog/current plan продукта | ранний product-start gate обязан иметь repo-native planning owner |
| `Logs/` | `Default` | materialize singleton fact logs продукта | pass-close contour не должен зависеть только от памяти или runtime |
| `Runtime/` | `Default` | materialize temporary execution carrier продукта | нужен controlled runtime-local contour и cleanup route, но не новый source-of-truth |
| `Profiles/` | `Default` | materialize только `Profiles/Product.md` | product repo должен иметь собственный product profile, а brand profiles остаются в `BytePress` |
| `Adapters/` | `Default` | materialize minimal adapter policy/registry contour продукта | product repo получает controlled execution contour без переноса `MCP/*` |
| `Pipeline/` | `Later product-pass` | не materialize bootstrap'ом | раннему product-start gate достаточно `Plans/*`; repo-native process-canon требует отдельного product decision |
| `Rules/` | `Later product-pass` | не materialize bootstrap'ом | отдельный product rule-layer допустим только после явного решения, а не как неявная копия `BytePress` |
| `Standards/` | `Later product-pass` | не materialize bootstrap'ом | product-side normative layer вводится только отдельным governance pass |
| `Schemas/` | `Later product-pass` | не materialize bootstrap'ом | ранний product-start не требует repo-native schema layer |
| `Templates/` | `Later product-pass` | не materialize bootstrap'ом | product-side template layer нужен только после отдельного решения о serial/hybrid artifacts продукта |
| `Roles/` | `Later product-pass` | не materialize bootstrap'ом | раннему старту достаточно agent/user entry, без local role catalog |
| `Skills/` | `Later product-pass` | не materialize bootstrap'ом | product-side procedural library не должна materialize по умолчанию |
| `Tools/` | `BytePress-only` | не materialize в product repo; generated repo использует только `scripts/*` и `BYTEPRESS_ROOT` handoff | canonical tool ownership остаётся в `BytePress`, чтобы bootstrap/lint/smoke не расходились между двумя copies |
| `Memory/` | `BytePress-only` | не materialize | future memory contour не нужен раннему product-start и не должен создавать ложное впечатление active storage layer |
| `MCP/` | `BytePress-only` | не materialize | connector policy и registry остаются в `BytePress`; generated repo получает только controlled handoff через `scripts/*` |

## Optional bootstrap profile
Текущий канон не вводит ни одного `Optional` top-level domain.

Это означает:
- current `bp_bootstrap.py` не materialize отдельный optional profile;
- если product repo когда-либо потребуется optional governance pack, такой профиль должен быть принят отдельным pass и синхронизирован между contracts, bootstrap и lint;
- отсутствие current optional profile является осознанным ограничением, а не пропуском.

## Early product-start gate и матрица
Default matrix materialize только тот subset, который нужен для controlled first product-start pass.

Это не даёт права считать generated repo готовым к предметной реализации сразу после bootstrap:
- bootstrap-created `Docs/Discovery/Interview.md` стартует в состоянии `Статус_текущей_истины: Не_подтверждена`;
- пока пользователь не дал явные ответы и current truth не подтверждена, агент остаётся в discovery-only contour;
- до подтверждения current truth допускаются только `Docs/Discovery/*`, `Plans/*`, `Logs/*` и reset/cleanup route failed product-start;
- наличие bootstrap-created `Docs/Product/*`, `Docs/Technical/*`, `Runtime/*` и `scripts/*` не считается разрешением на их предметное изменение в первом pass.

## Failed product-start reset route
Канонический reset/cleanup route после failed product-start:
1. запустить `scripts/reset-product-start.sh` в generated repo, чтобы убрать runtime-local smoke artifact и получить явный drift report;
2. если drift ограничен `Docs/Discovery/*`, `Plans/*` и `Logs/*`, решить отдельно, какие текущие current-truth/planning/log edits сохранить;
3. если появились tracked changes вне раннего discovery-only contour, canonical cleanup route — отбросить damaged repo и materialize fresh target новым bootstrap run, а не чинить out-of-gate drift вручную как новый baseline.

## Граница документа
`Product_Bootstrap_Domain_Matrix.md`:
- не подменяет `Product_Bootstrap_Contract.md` как owner bootstrap obligations;
- не подменяет `Product_Bootstrap_Validation.md` как owner acceptance criteria;
- не подменяет `Artifact_Lifecycle.md` как owner sync-loop и lifecycle policy;
- фиксирует только top-level replication canon и ранний bootstrap perimeter.
