# Notion API pilot — Git→Notion sync

Дата: 2026-07-20  
Ветка: `cursor/notion-reimport-zip-7856`  
Workspace: **"Swaim" - GeoNotes app** · integration `CursorAgent`

## Корень копии

- **Small Business Space v.1.0 [RU]**  
  `dcf207ca-d379-82b8-9fa8-013434ecd77f`

Карта страниц **только этой копии** (37 шт.): [`notion-sbs-page-map.json`](notion-sbs-page-map.json).

## Формат блоков

Снимок до sync: [`notion-instructions-block-format.json`](notion-instructions-block-format.json).

API не ставит file-icon на callout → emoji без крупных child-картинок иконок (иначе дубли).

## Записано `--apply`

| Страница | Примечание |
|----------|------------|
| Instructions | блок «Чем вдохновлено»; без крупных icon-картинок |
| Твой продукт | чистый шаблон |
| Старт своего бизнеса | без книжных отсылок; ссылки на страницы SBS |
| Развитие своего бизнеса | без книжных отсылок; ссылки на страницы SBS |

Внутренние ссылки = `text.link` → id **только** из page-map корня SBS.

Проверка: «Опишите свой продукт» → `https://www.notion.so/569207cad37982e08734816a22514351` (ваш «Твой продукт»).
