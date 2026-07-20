# ZIP-импорт Git→Notion (эксперимент, не рекомендуем)

**Статус:** проверено владельцем — **не подходит** как основной путь:
- картинки переносятся плохо;
- разметка Notion не сохраняется;
- лимит импорта ~5 MB (полный пакет больше).

Актуальный способ подключить агента к Notion: **[`notion-integration.md`](notion-integration.md)** (MCP и/или `NOTION_TOKEN`).

Ниже — что осталось в репо от эксперимента (можно игнорировать).

## Артефакты

| Файл | Назначение |
|------|------------|
| [`import/ProdSwaim-Notion-import-mini-Instructions.zip`](../import/ProdSwaim-Notion-import-mini-Instructions.zip) | Мини-проба Instructions |
| [`import/ProdSwaim-Notion-import.zip`](../import/ProdSwaim-Notion-import.zip) | Полный ZIP (>5 MB) |
| [`scripts/pack-notion-import.py`](../scripts/pack-notion-import.py) | Пересборка ZIP |

```bash
python3 scripts/pack-notion-import.py --also-mini --out-dir import
```
