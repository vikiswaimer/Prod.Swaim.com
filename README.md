# Prod.Swaim.com

Цифровой продукт / шаблон для управления и развития цифровых продуктов и малого бизнеса.

**Для нового чата с агентом:** сначала [`AGENTS.md`](AGENTS.md) и [`docs/agent-context.md`](docs/agent-context.md).

## Содержимое

| Путь | Назначение |
|------|------------|
| [`AGENTS.md`](AGENTS.md) | Инструкция для Cursor/Cloud Agent (читать в новом чате) |
| [`docs/agent-context.md`](docs/agent-context.md) | Бэклог логики, пакеты A–D, правила правок |
| [`docs/positioning.md`](docs/positioning.md) | Позиционирование продукта (пакет A) |
| [`docs/methodology.md`](docs/methodology.md) | Методология: Cagan / Ries / Mom Test / Sprint / MVP |
| [`docs/glossary.md`](docs/glossary.md) | Глоссарий терминов (пакет C) |
| [`docs/reports/`](docs/reports/) | Отчёты по пакетам изменений |
| [`content/small-business-space-ru/`](content/small-business-space-ru/) | Рабочая копия **Small Business Space v.1.0 [RU]** (markdown + csv). Старт: [`00-index.md`](content/small-business-space-ru/00-index.md), оглавление: [`INDEX.md`](content/small-business-space-ru/INDEX.md). |
| [`docs/structure.md`](docs/structure.md) | Карта модулей |
| [`import/SwaimProdFromNotion.zip`](import/SwaimProdFromNotion.zip) | Исходный экспорт Notion |
| [`import/ProdSwaim-Notion-import.zip`](import/ProdSwaim-Notion-import.zip) | Обратный пакет Git→Notion (md+csv+картинки) |
| [`import/ProdSwaim-Notion-import-mini-Instructions.zip`](import/ProdSwaim-Notion-import-mini-Instructions.zip) | Мини-проба импорта (Instructions + картинки) |
| [`docs/notion-reimport.md`](docs/notion-reimport.md) | Как импортировать обратно в Notion |
| [`scripts/pack-notion-import.py`](scripts/pack-notion-import.py) | Сборка ZIP для импорта |

Публичный Notion: https://swaim.notion.site/Small-Business-Space-v-1-0-RU-22a207cad37981ddbd72d4d9f0ed54c3

## Рабочий процесс

1. Существенные изменения — через **GitHub Issues**.
2. Правки — в markdown/csv в `content/`, через PR (или напрямую в `main` по договорённости).
3. Синхронизация обратно в Notion — ZIP-импорт по [`docs/notion-reimport.md`](docs/notion-reimport.md) (сначала мини-проба); Integration — позже отдельным issue.
4. Лендинг и маркетинг-стратегия — отдельные чаты/issues.

## Obsidian

`Open folder as vault` → выберите каталог `content/` (или `content/small-business-space-ru/`).
