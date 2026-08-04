# Отчёт: Пространство v2 (черновик) → Notion

**Issue:** [#28](https://github.com/vikiswaimer/Prod.Swaim.com/issues/28)  
**Дата:** 2026-07-30  
**Ветка:** `cursor/space-v2-skeleton-ffef`

## Что сделано

1. Собран markdown-каркас в Git: `content/small-business-space-ru/Пространство-v2/`
2. В Notion (копия SBS) в **конце корня** создана страница-контейнер и 6 групп
3. Существующие модули v1 **не менялись**

## Notion

| Страница | URL |
|----------|-----|
| Пространство v2 (черновик) | https://www.notion.so/3ad207cad379814dad44efb58e917b17 |
| Сейчас | https://www.notion.so/3ad207cad37981c7aad2c73685c6872c |
| Продукт | https://www.notion.so/3ad207cad37981ac9446d398f264d6c5 |
| Клиенты | https://www.notion.so/3ad207cad37981fd83fdf99e684ceab0 |
| Рост | https://www.notion.so/3ad207cad379813d8fd1c3868e4e0991 |
| Деньги | https://www.notion.so/3ad207cad379817096a2ebb32e03d191 |
| База | https://www.notion.so/3ad207cad37981a4b88edcea003e4d33 |

Карта id: [`notion-space-v2-page-map.json`](notion-space-v2-page-map.json)

Корень SBS: `dcf207ca-d379-82b8-9fa8-013434ecd77f`

## Git

- `content/small-business-space-ru/Пространство-v2/00-index.md` + 6 групп
- `scripts/notion_create_space_v2.py` — идемпотентный create (не дублирует, если контейнер уже есть)
- `scripts/notion_client.py` — добавлен `create_page`

## Вне скоупа (осознанно)

- Замена/миграция модулей v1
- Полноценные Notion DB / board / формулы
- Права на закрытие probe-issue #27 (нужно вручную)
