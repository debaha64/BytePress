# Logs

`Logs/` хранит журналы фактов.

## Состав
- `ChangeLog.md` — значимые изменения.
- `ADRlog.md` — архитектурные и продуктовые решения.
- `QualityLog.md` — проверки и результаты контроля.
- `ReleaseLog.md` — выпуски и передачи.
- `SupportLog.md` — факты сопровождения.

## Contract
- log-files в `Logs/` остаются singleton-артефактами с semantic filenames;
- serial `ID` получают внутренние записи журналов там, где журнал ведёт serial fact registry;
- ссылка на конкретную запись идёт по её внутреннему `ID`, а path к singleton log-file добавляется только для навигации.
