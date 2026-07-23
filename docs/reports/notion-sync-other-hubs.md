# Notion sync — Other hubs (без Ссылки / Цифровая безопасность)

Дата: 2026-07-23  
Ветка: `cursor/other-mini-guides-7cdb`  
Скрипт: `scripts/notion_sync_other_hubs.py`  
Workspace: **"Swaim" - GeoNotes app** · integration `CursorAgent`

## Не трогали

- **Ссылки** `6d6207ca-…` — уже залита ранее
- **Цифровая безопасность** `a9f207ca-…` — эталон, без изменений

## Записано `--apply`

| Страница | page_id | DB сохранена | Демо |
|----------|---------|--------------|------|
| Отзывы | `7bd207ca-d379-82fa-b774-0114a42b71ee` | Feedback | Alice → «Alice (демо)» |
| Email шаблоны | `c7a207ca-d379-829d-a21c-013c14eaf38a` | Email Snippets | → «Спасибо за покупку (демо)» |
| Текстовые заготовки (было Text Snippets) | `b35207ca-d379-82d7-be8f-817d028d0ef9` | Snippets | → «Спасибо, что написали (демо)» |

URL:
- https://app.notion.com/p/7bd207cad37982fab7740114a42b71ee
- https://app.notion.com/p/Email-c7a207cad379829da21c013c14eaf38a
- https://app.notion.com/p/Text-Snippets-b35207cad37982d7be8f817d028d0ef9

Текст хабов вставлен **выше** child DB (`position: start`).

## Повтор

```bash
python3 scripts/notion_smoke.py
python3 scripts/notion_sync_other_hubs.py --dry-run
python3 scripts/notion_sync_other_hubs.py --apply
# точечно:
python3 scripts/notion_sync_other_hubs.py --apply --only reviews
python3 scripts/notion_sync_other_hubs.py --apply --only email
python3 scripts/notion_sync_other_hubs.py --apply --only snippets
```

## Руками в UI (по желанию)

- ~~Descriptions в родительской таблице Other~~ — обновлены через API 2026-07-23 (вкл. исправление «Управление паролями» → принципы безопасности; тела страниц Ссылки/Безопасность не переписывались).
- Переименовать DB `Feedback` / `Email Snippets` / `Snippets` / `Links` на RU — по желанию.
- Views/иконки — по вкусу.
