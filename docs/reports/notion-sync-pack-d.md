# Notion sync — пакет D (issue #8)

Дата: 2026-07-20  
Ветка: `cursor/notion-sync-pack-d-dd6b`  
Workspace: **"Swaim" - GeoNotes app** · integration `CursorAgent`  
Корень: `dcf207ca-d379-82b8-9fa8-013434ecd77f`  
Скрипт: `scripts/notion_sync_pack_d.py`

## Записано `--apply`

| Страница | page_id | Что сделано |
|----------|---------|-------------|
| Instructions | `e45207ca-d379-83cb-af54-01ada6afeab0` | Блок «Работа с ИИ»; налоги/Untitled в indications; без Git/docs-ссылок |
| Развитие своего бизнеса | `329207ca-d379-837b-9966-81eee8afa61d` | Примечание: пароли не ядро, внешний менеджер |
| Пароли | `a9f207ca-d379-831a-9185-0192f489348b` | Новый текст; title «Пароли (не ядро шаблона)»; пустая Password manager (без демо-секрета Behance) |
| Финансовый отчет | `1a2207ca-d379-8379-b2c9-010d04bba86a` | Intro про параметр ставки; БД пересоздана |
| Оценка | (DB `7d8207ca-…`) | Демо-строка «2022 May» архивирована |
| Задачи | (DB `331207ca-…`) | Пустой Untitled → «Пример задачи (удалите или замените)» + пояснение |
| INV-0001 | (в DB Счет-фактуры) | Title «INV-0001 (пример)» + callout про демо / свою ставку Tax |

## Финансовый отчёт — новая child DB

- **id:** `3a3207ca-d379-81d9-a7b3-e250f7328fda` (старая `18c207ca-…` снята с страницы вместе с «Taxes (30%)» и демо «2022 May»)
- Свойства: `Date`, `Income`, `Expenses`, `✏️ Tax rate %` (number), `✏️ Taxes` (number), `⛔️ Profit`, `⛔️ Profit %`
- Smoke: Income 1000 / Expenses 200 / Taxes 100 → Profit 700, Profit % 0.7

## Пароли — новая child DB

- **id:** `3a3207ca-d379-81c7-b6ad-dde481d961cb` — пустая (`Account`, `Email/Username`, `Website`, `Password`)

## Руками в UI (по желанию)

- Views/галереи у пересозданных БД — если нужны кастомные виды, настроить в Notion.
- В инвойсе старый layout (колонки) сохранён; callout с пометкой «пример» добавлен в конец страницы записи.
- Массовые Untitled-картинки в Библиотеке знаний — вне скоупа пакета D.

## Повтор

```bash
python3 scripts/notion_smoke.py
python3 scripts/notion_sync_pack_d.py --dry-run
python3 scripts/notion_sync_pack_d.py --apply
# точечно:
python3 scripts/notion_sync_pack_d.py --apply --only finance
```
