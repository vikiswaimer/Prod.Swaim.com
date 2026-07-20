# Notion API pilot — Git→Notion sync

Дата: 2026-07-20  
Ветка: `cursor/notion-reimport-zip-7856`  
Workspace: **"Swaim" - GeoNotes app** · integration `CursorAgent`

## Корень копии

- **Small Business Space v.1.0 [RU]**  
  `dcf207ca-d379-82b8-9fa8-013434ecd77f`  
  https://app.notion.com/p/Small-Business-Space-v-1-0-RU-dcf207cad37982b89fa8013434ecd77f

## Формат блоков (снят с live Instructions до sync)

Снимок: [`notion-instructions-block-format.json`](notion-instructions-block-format.json).

- Pages indications: callout с **file-icon** (paper/Thunder/Folder/archive)
- Columns indications: callout с emoji ⛔ / ✏️
- Картинок на верхнем уровне не было

**Ограничение API:** file-icon на callout через File Upload **нельзя** (`validation_error`).  
Рабочий обход: emoji-callout + image как **child** (проверено).

## Записано через `notion_sync_pilot.py --apply`

| Страница | page_id | Источник Git | Блоки |
|----------|---------|--------------|-------|
| Instructions | `e45207ca-d379-83cb-af54-01ada6afeab0` | `Instructions/_index.md` + 6 ассетов | 32 (6 callout с image children) |
| Твой продукт | `569207ca-d379-82e0-8734-816a22514351` | `Бизнес/Твой продукт--5ac1cda1.md` | 24 |
| Старт своего бизнеса | `9b0207ca-d379-8305-9d71-013fc7eb2fd7` | `Быстрый старт/Старт…--66c3ee00.md` | 41 |
| Развитие своего бизнеса | `329207ca-d379-837b-9966-81eee8afa61d` | `Быстрый старт/Развитие…--d23a7834.md` | 51 |

## Перенести / проверить в Notion UI

1. Открыть Instructions — тексты пакета A, callout + картинки внутри.
2. «Твой продукт» — чистый шаблон (не toggles; bullets + плейсхолдеры).
3. Треки Быстрый старт — тексты пакета B, чеклисты `to_do`.
4. Внутренние wiki-ссылки Notion на дочерние страницы из markdown **не** восстанавливались (в to_do остаётся текст ссылки).
5. File-icon на callout (как в оригинале) — вручную, если нужен пиксель-в-пиксель вид.

## Следующие страницы (по желанию)

По чеклистам pack A–C: позиционирование на корне, пример «Твой продукт», глоссарий / маркетинг-split — точечно тем же пилотом.
