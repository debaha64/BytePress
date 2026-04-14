# Pass Request

## Назначение
Этот документ объясняет, как человеку формулировать pass для агента внутри `BytePress`.

Он не дублирует operating loop агента из `../../AGENTS.md`; его задача — помочь человеку задать корректный scope через уже существующие repo contracts.

## На что должен опираться pass request
- на текущий stage/task/pass в `../../Plans/*`;
- на ограничения и quality contracts из `../../Rules/*` и `../../Standards/*`;
- на technical-owner documents из `../Technical/*`, если pass затрагивает system contract;
- на `../../Setup_Guide.md` и `../../Tools/README.md`, если pass зависит от среды или checks.

## Минимальная форма pass request
1. Назвать stage или указать, что нужен новый pass внутри текущего `ROAD-*`.
2. Сформулировать узкую цель pass.
3. Перечислить scope: какие owner-documents или домены затрагиваются.
4. Перечислить ограничения: что нельзя открывать, переписывать или активировать.
5. Указать self-check, governance-check и desired outcome, если они не противоречат repo contracts.

## Что стоит указывать явно
- branch name, если он уже определён;
- какой `ROAD-*` должен остаться активным или быть закрыт;
- нужно ли архивировать previous current `Plan` или stage backlog;
- какие direct-reference sync допустимы, если обнаружится реальное противоречие;
- если pass release- или journaling-related, какие factual log closures ожидаются и что уже подтверждено tag/history;
- какой итоговый report-format нужен человеку.

## Чего не нужно делать
- не переписывать весь operating loop агента вручную, если он уже задан в `../../AGENTS.md`;
- не описывать технические контракты вместо `../Technical/*`;
- не заменять `Plans/*` собственным списком статусов;
- не расширять scope pass расплывчатой формулировкой вроде "приведи всё в порядок".

## Куда идти дальше
- если нужно понять human operating mode: `Operating_Mode.md`;
- если нужен первый маршрут входа: `First_Start.md`;
- если нужен текущий planning-state: `../../Plans/README.md`;
- если нужен operating canon агента: `../../AGENTS.md`.
