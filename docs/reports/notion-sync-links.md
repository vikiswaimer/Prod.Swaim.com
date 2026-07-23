# Notion sync — страница «Ссылки»

Дата: 2026-07-23  
Ветка: `cursor/other-mini-guides-7cdb`  
Скрипт: `scripts/notion_sync_links.py`  
Workspace: **"Swaim" - GeoNotes app** · integration `CursorAgent`

## Записано `--apply`

| Страница | page_id | Что сделано |
|----------|---------|-------------|
| Ссылки | `6d6207ca-d379-8343-a366-015a6f57b209` | Текст мини-гайда из Git; child DB **Links** сохранена; контент вставлен **выше** базы (`position: start`) |

URL: https://app.notion.com/p/6d6207cad3798343a366015a6f57b209

- Внутренняя ссылка на [Цифровая безопасность](https://www.notion.so/a9f207cad379831a91850192f489348b).
- Таблицы md → bullet-списки (API без md-tables в пилоте).
- CSV/локальные демо-пути в тексте убраны; демо-записи остаются в DB Links (4 шт.).

## Повтор

```bash
python3 scripts/notion_smoke.py
python3 scripts/notion_sync_links.py --dry-run
python3 scripts/notion_sync_links.py --apply
```

## Руками в UI (по желанию)

- Переименовать DB `Links` → «Ссылки», если хотите RU в UI.
- Description пункта в родительской таблице Other — подтянуть из Git CSV.
