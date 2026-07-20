# Подключение агента к Notion (вместо ZIP-импорта)

ZIP Markdown/CSV **не подходит** как основной способ вернуть проработанный контент в Notion:
- ломается/теряется разметка (callouts, asides, views, формулы);
- картинки переносятся ненадёжно;
- лимит импорта ~5 MB (наш полный пакет больше).

Нужен путь, где агент **правит существующие страницы** в живом Notion, а не создаёт кривой клон.

---

## Два рабочих способа

| Способ | Где работает | Картинки | Кому подходит |
|--------|--------------|----------|---------------|
| **A. Notion MCP (OAuth)** | Cursor Desktop / локальный чат | Пока **нет** в MCP (roadmap Notion); картинки — отдельно через API | Быстрые правки текста на месте |
| **B. Internal Integration + `NOTION_TOKEN`** | Cloud Agent и скрипты в репо | Да, через [File Upload API](https://developers.notion.com/guides/data-apis/working-with-files-and-media) | Автономные прогоны, точечный sync Git→Notion |

**Рекомендация для Prod.Swaim:** включить **оба**. MCP — для живой правки в Desktop; токен — для Cloud Agent и загрузки картинок.

ZIP-пакеты в `import/ProdSwaim-Notion-import*.zip` оставляем только как архив эксперимента (см. [`notion-reimport.md`](notion-reimport.md)).

---

## Способ A — Notion MCP в Cursor Desktop

Официально: https://developers.notion.com/guides/mcp/get-started-with-mcp

1. Cursor → **Settings → MCP → Add new global MCP server** (или проектный `.cursor/mcp.json` в репо).
2. Конфиг:

```json
{
  "mcpServers": {
    "notion": {
      "url": "https://mcp.notion.com/mcp"
    }
  }
}
```

3. Сохранить, перезапустить Cursor при необходимости.
4. При первом вызове Notion-инструмента пройти **OAuth** и выдать доступ workspace.
5. В чате: «обнови страницу Instructions в Notion по файлу `content/.../Instructions/_index.md`».

Ограничения MCP (на сейчас):
- нужны права вашего Notion-аккаунта на эти страницы;
- **загрузка файлов/картинок через MCP пока не поддерживается** — для иконок/скринов используйте способ B или ручную вставку;
- OAuth неудобен для headless Cloud Agent без человека в сессии.

В репозитории лежит шаблон: [`.cursor/mcp.json`](../.cursor/mcp.json).

---

## Способ B — Internal Integration (для Cloud Agent)

### Что сделать владельцу (один раз)

1. Открыть https://www.notion.so/my-integrations → **New integration**.
2. Имя, например: `Prod.Swaim Cloud Agent`.
3. Capabilities: **Read content**, **Update content**, **Insert content** (+ комментарии по желанию).
4. Скопировать **Internal Integration Secret** (`ntn_…` или `secret_…`).
5. На **корневой** странице шаблона (и на нужных дочерних, если access не наследуется):
   - `⋯` → **Connections** / **Add connections** → выбрать эту integration.
6. Положить секрет туда, где его видит **Cloud Agent** (не в Git и не в чат):

   1. Откройте https://cursor.com/dashboard/cloud-agents  
   2. Вкладка / секция **Secrets**  
   3. **Add Secret** (лучше scope **Personal**, если Environment не подхватывается):
      - Name: `NOTION_TOKEN`  
      - Value: Internal Integration Secret из Notion (`ntn_…`)  
      - Type: **Runtime Secret** (чтобы токен не светился в логах)  
   4. Опционально второй секрет: `NOTION_ROOT_PAGE_ID` = id корневой страницы шаблона (32 символа из URL страницы Notion).  
   5. **Сохраните** и **запустите новый** Cloud Agent чат/run — уже открытый агент старые секреты часто не видит.

   Альтернатива без Cloud secrets: править Notion из **Cursor Desktop** через MCP OAuth (способ A выше) — токен Integration тогда не нужен.

**Не коммитьте токен в Git и не присылайте его в чат.**

### Что сможет агент после этого

- читать и искать страницы, к которым дан доступ;
- заменять/дописывать блоки на страницах (тексты пакетов A–C и дальше);
- загружать локальные картинки из `content/**` через File Upload API и вставлять `image` blocks;
- **не** восстановит магически все board/gallery views и сложные формулы одним кликом — их по-прежнему донастраивают в UI при необходимости.

### Smoke-проверка

Когда `NOTION_TOKEN` уже в окружении:

```bash
python3 scripts/notion_smoke.py
```

Скрипт дергает `GET /v1/users/me` и (если задан) читает корневую страницу. Без токена — понятная ошибка с чеклистом.

---

## Практичный процесс правок (после подключения)

1. Правки смысла по-прежнему в Git (`content/**`) + Issue.
2. Перенос в Notion — **точечно по страницам** (не «весь космос заново»):
   - Instructions
   - Твой продукт
   - треки Быстрый старт
   - и т.д. по чеклисту из отчётов пакетов
3. Картинки: если на странице уже стоят нужные ассеты — текст можно менять без перезаливки; новые/битые — через File Upload API (способ B).
4. В конце ответа агента: список изменённых Notion page id + что ещё руками в views/формулах.

---

## Что выбрать прямо сейчас

| Ваша цель | Действие |
|-----------|----------|
| «Хочу в Desktop-чате сказать: поправь Notion» | Способ A (MCP + OAuth) |
| «Хочу, чтобы Cloud Agent сам дописывал страницы и картинки» | Способ B (`NOTION_TOKEN` в secrets + share страниц) |
| «Вернуть всё пространство одним ZIP» | Не используем |

После того как токен или MCP появятся в окружении — напишите в чат: можно начать с одной страницы (например Instructions или «Твой продукт») как пилота.
