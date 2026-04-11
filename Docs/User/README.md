# User

## Назначение
`Docs/User/*` — канонический human-facing layer `BytePress`.

Этот слой отвечает на вопросы:
- как человеку входить в `BytePress` как в рабочую систему;
- в каком operating mode человек взаимодействует с агентом и репозиторием;
- какой первый маршрут старта нужен перед началом работы;
- какие базовые сценарии использования системы уже считаются нормальным путём.

## Канонический состав
- `README.md` — entrypoint user-layer и карта маршрутов.
- `Operating_Mode.md` — human operating mode: роль человека, отношение к агенту и общий режим работы с системой.
- `First_Start.md` — первый маршрут входа в `BytePress` после клонирования или получения репозитория.
- `Usage_Scenarios.md` — базовые сценарии использования `BytePress` как системы.

## Что входит в user-layer
- human-facing объяснение режима работы;
- маршрут к setup, planning, checks и operating artifacts;
- короткие сценарии использования системы без раскрытия внутреннего техслоя;
- guidance, какой owner-document читать следующим шагом.

## Что не входит в user-layer
- `Docs/User/*` не подменяет `AGENTS.md` как operating canon агента;
- `Docs/User/*` не дублирует `Setup_Guide.md` как пошаговый setup/install guide;
- `Docs/User/*` не подменяет `Docs/Technical/*` как источник технических контрактов;
- `Docs/User/*` не хранит planning-state вместо `Plans/*`;
- `Docs/User/*` не превращается в широкий product manual или в полный onboarding-course.

## Первый маршрут входа
1. Прочитать `README.md`, чтобы понять назначение системы и доменную карту.
2. Прочитать `Operating_Mode.md`, чтобы понять human operating mode и отношение человека к агенту.
3. Прочитать `First_Start.md`, чтобы выбрать первый шаг входа и не перепутать user-layer с setup-layer.
4. Перейти в owner-documents: `Setup_Guide.md`, `Plans/*`, `Tools/*`, `AGENTS.md`, `Docs/Technical/*` по реальной задаче.

## Базовые user-documents
- human operating mode раскрыт в `Operating_Mode.md`;
- порядок первого старта раскрыт в `First_Start.md`;
- базовые сценарии использования раскрыты в `Usage_Scenarios.md`.

## Связи
- карта для человека: `../../README.md`
- operating canon агента: `../../AGENTS.md`
- установка и среда: `../../Setup_Guide.md`
- техническая модель и системные контракты: `../Technical/README.md`
- продуктовая рамка: `../Product/README.md`
- planning-contour: `../../Plans/README.md`
- инструменты и checks: `../../Tools/README.md`
