# Notion sync — группа Активность (issue #22)

Дата: 2026-07-26  
Ветка: `cursor/activity-lean-analytics-6e5e`  
Workspace: **"Swaim" - GeoNotes app** · integration `CursorAgent`  
Скрипт: `scripts/notion_sync_activity.py`

## Записано `--apply`

| Страница | page_id | Что сделано |
|----------|---------|-------------|
| **Гипотезы** (бывш. Идеи) | `4cf207ca-d379-82eb-baff-81b0dc1af094` | Rename + гайд; child DB → «Гипотезы» + новые свойства |
| **Аналитика** (новая) | `3a9207ca-d379-8137-9fad-eb55f83a0943` | Создана в DB Активность + полный гайд метрик |
| Цели | `f18207ca-…7859f4` | Гайд outcomes |
| Задачи | `57f207ca-…ad0665` | Гайд WIP / Linear·GitHub |
| Рефлексия | `2e9207ca-…8af5af` | BML |
| Заметки | `b7b207ca-…68e84` | Опционально / депрекейт |
| Календарь | `6a2207ca-…53acd` | Таймбокс обучения |
| Старт / Развитие | треки | Ссылки на Гипотезы + Аналитика |

Описания строк в DB **Активность** обновлены.

### DB Гипотезы — новые свойства

`Формулировка`, `Как проверим`, `Статус` (select), `Сигнал успеха`, `Вывод`, `Next step`, `Ссылка` (+ старые Trust/Ease/Impact/Score).

## Ссылки для оценки

- Гипотезы: https://app.notion.com/p/4cf207cad37982ebbaff81b0dc1af094  
- Аналитика: https://app.notion.com/p/3a9207cad37981379fadeb55f83a0943  
- Корень SBS: https://app.notion.com/p/dcf207cad37982b89fa8013434ecd77f  

## Руками в UI (по желанию)

1. На хабах **таблица базы сейчас над гайдом** (API сохраняет child DB и дописывает текст снизу) — перетащите таблицу **под** гайд.
2. Views: «К проверке», «В работе», «Вывод» для Гипотез; WIP ≤ 3 для Задач.
3. Демо-строки в базах можно заменить RU-примерами из Git или удалить.
4. Порядок строк в DB Активность: Цели → Гипотезы → Задачи → Аналитика → Рефлексия → Календарь → Заметки.

## Повтор

```bash
python3 scripts/notion_smoke.py
python3 scripts/notion_sync_activity.py --dry-run
python3 scripts/notion_sync_activity.py --apply
```
