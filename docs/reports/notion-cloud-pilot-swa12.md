# Notion Cloud pilot — SWA-12

Дата: 2026-08-19  
Run: Cloud Agent (FoundingEngineer)  
Integration: `CursorAgent` · workspace **"Swaim" - GeoNotes app**

## Env (Cloud secrets)

| Secret | Назначение |
|--------|------------|
| `NOTION_TOKEN` | Internal Integration Secret (`ntn_…`), Runtime Secret |
| `NOTION_ROOT_PAGE_ID` | опционально: `dcf207ca-d379-82b8-9fa8-013434ecd77f` (корень SBS) |

Подключение integration к страницам — см. `docs/notion-integration.md`.

## Проверки

```bash
python3 scripts/notion_smoke.py
# OK /users/me (bot CursorAgent); с NOTION_ROOT_PAGE_ID — OK /pages/…

python3 scripts/notion_sync_pilot.py \
  --page-id a9f207ca-d379-831a-9185-0192f489348b \
  --md content/small-business-space-ru/Other/Цифровая\ безопасность--ab1df728.md \
  --apply

python3 scripts/notion_inspect.py --page-id a9f207ca-d379-831a-9185-0192f489348b --depth-children
```

## Результат `--apply`

| Модуль | page_id | Git source |
|--------|---------|------------|
| Цифровая Безопасность | `a9f207ca-d379-831a-9185-0192f489348b` | `Other/Цифровая безопасность--ab1df728.md` |

- 58 блоков записано (callout, to_do, headings, lists)
- Read-back: заголовок «Практический мини-чеклист» и quote про секреты на месте
- URL: https://app.notion.com/p/a9f207cad379831a91850192f489348b

## Сигнал

Write-path Git→Notion работает в Cloud без ручного copy-paste для одного модуля.

## Следующий срез

- Добавить `NOTION_ROOT_PAGE_ID` в Cloud secrets (если ещё нет)
- Следующий модуль по issue/группе — через `notion_sync_pilot.py` + page-map
