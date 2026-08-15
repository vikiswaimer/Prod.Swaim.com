# Контекст агента: логика продукта и бэклог

Дополняет корневой [`AGENTS.md`](../AGENTS.md). Обновляй этот файл, когда закрываешь крупный пакет Issues или меняется процесс.

## Методология

Канон для мышления и правок: [`docs/methodology.md`](methodology.md) — Inspired (Cagan), Lean Startup (Ries), Mom Test (Fitzpatrick), Sprint (Knapp), MVP как ценный рабочий срез (Olsen + владелец).

При правках разделов сверяйся с картой «методология → модули» в том файле.

## Позиционирование

Зафиксировано в [`docs/positioning.md`](positioning.md) и отражено в `00-index.md` + `Instructions` (**пакет A выполнен**, issue #1).

Кратко: готовые решения для цифровых продуктов; без сборки с нуля; работа без ИИ или в паре с ИИ. Notion — UI для людей; Git — рабочая копия.

Остаточные формулировки «малый бизнес / корзина / купоны» и демо-шум в глубинных страницах — пакет **J** (и точечно в E–I по мере правок).

## Модули (смысл)

| Модуль | Смысл |
|--------|--------|
| Instructions | Как пользоваться шаблоном, типы страниц |
| Быстрый старт | Два трека-чеклиста со ссылками в модули |
| Бизнес | Foundation: продукт, клиенты, оффер, конкуренты, стратегия маркетинга, must-have шаги |
| Брэнд | Позиционирование + style guide |
| Активность | Ежедневная операционка: задачи, заметки, идеи, календарь, рефлексия, цели |
| Маркетинг | Операционные планировщики (соцсети, кампании, статьи, email, лид-магниты) |
| Финансы | Доходы/расходы/отчёт/инвойсы/оценка |
| Библиотека знаний | Советы, определения, каталог инструментов (очень много md) |
| Other | Дополнительно: мини-гайды + базы (отзывы, интервью, email, текстовые заготовки, ссылки, цифровая безопасность) — #17 ✅ |

Ключевые входы:

- [`content/small-business-space-ru/00-index.md`](../content/small-business-space-ru/00-index.md)
- [`content/small-business-space-ru/INDEX.md`](../content/small-business-space-ru/INDEX.md)
- Треки: `Быстрый старт/Старт своего бизнеса--66c3ee00.md`, `.../Развитие своего бизнеса--d23a7834.md`

## Бэклог контента

**Paperclip / Product Lead (2026-08-15):** sync — [`docs/reports/paperclip-team-sync.md`](reports/paperclip-team-sync.md); W1 brief — [`docs/reports/w1-mom-test-brief.md`](reports/w1-mom-test-brief.md); **SWA-9** decision — [`docs/reports/swa9-next-after-risk-map.md`](reports/swa9-next-after-risk-map.md); **SWA-10** review — [`docs/reports/swa10-productivity-review-swa9.md`](reports/swa10-productivity-review-swa9.md) (**ACCEPT**); risk-map — [`docs/risk-map-hypotheses.md`](risk-map-hypotheses.md). **WIP=1:** только W1 Mom Test.


**Актуальный процесс (issue #20):** новый чат = **одна группа** (блоки внутри) + **диалог**.  
[`roadmap-v2.md`](roadmap-v2.md) — **карта идей / архив**, не очередь «делай E→J».

Сделано: A–D ✅; **Other** ✅ (#17). Следующую группу выбирает владелец в новом чате.

### Foundation A–D ✅ (закрыть #8, #10 если ещё open)

| Пакет | Issue | Отчёт |
|-------|-------|--------|
| A позиционирование + «Твой продукт» | #1 | `docs/reports/pack-a.md` |
| B треки Старт / Развитие | #2 | `docs/reports/pack-b.md` |
| C язык / глоссарий / маркетинг | #3 | `docs/reports/pack-c.md` |
| D доверие + Instructions без GitHub | #8 | `docs/reports/pack-d.md` |
| Цифровая безопасность | #10 | `docs/reports/digital-security.md` |

### Группы / темы (подсказки, не очередь)

Опциональные черновики: [`docs/issue-drafts/`](issue-drafts/README.md). Не создавать issues «пачками» из этого списка.

| Группа / тема | Заметка | Школы |
|---------------|---------|--------|
| **Other** | ✅ мини-гайды + Интервью (#17) — эталон процесса | Cagan + сигнал |
| **Клиенты** | Портрет + **истории аудитории** (поведение/сигнал); Отзывы/Интервью уже есть | Mom Test + Ries (архетип как история) |
| **Активность** | Идеи / задачи / цели / рефлексия | Ries + Cagan |
| **Продукт / оффер / must-have** | Тонкий задел в A | Olsen + Cagan |
| **Календарь / кампании** | Learning launches | Knapp + Ries |
| **Брэнд / конкуренты** | Outcomes и альтернативы | Cagan |
| **Входы / INDEX / демо** | Можно точечно внутри чата группы | доверие |

### Инфра (не контент)

- #6 Notion MCP / `NOTION_TOKEN` — ✅; перенос по мере групповых чатов.
- #4 ZIP Git→Notion — won't do (см. `notion-reimport.md`).

## Правила правок контента

1. **Один чат = одна группа + один issue** (по умолчанию). Scope согласовать диалогом; не смешивать группы и не исполнять roadmap как скрипт.
2. Тон по умолчанию после пакета C: вежливое **«вы»**, язык **RU** (EN только как осознанный термин).
3. Плейсхолдеры ответов: короткий пример в отдельном файле `examples/`, не в основном шаблоне.
4. При переименовании файлов/папок — обновить `00-index.md`, `INDEX.md` и входящие markdown-ссылки; прогнать проверку «битых» ссылок.
5. CSV = схема/данные баз; менять осмысленно и описывать перенос в Notion (свойства, формулы, views).
6. Не удалять массово «Библиотека знаний» без отдельного issue — там сотни файлов.
7. Любая правка смысла продукта сверяется с [`methodology.md`](methodology.md) (Mom Test, гипотезы, MVP как ценный срез и т.д.).

## Процесс с владельцем

- Владелец в новом чате называет **группу** (или блок). Агент уточняет гипотезы и критерии в диалоге, затем правит.
- Один issue на чат (создаёт/привязывает под группу). Отдельные issues из одного чата — только по явной просьбе.
- Агент правит Git; по договорённости — `main` или ветка `cursor/<name>-ffef` + PR (**один** draft PR на чат/issue).
- В конце: список файлов + что перенести в Notion (или что уже записано через Integration/MCP).
- Посадочная страница и маркетинг-стратегия — **другие** чаты/issues.
- Подключение к Notion: [`notion-integration.md`](notion-integration.md). Без токена/MCP агент в Notion не пишет.

## История setup (чтобы не повторять)

1. Репозиторий был пустым (README).
2. Экспорт Notion `Markdown & CSV` → `import/SwaimProdFromNotion.zip` (внутри ещё один zip Part-1).
3. Распаковка с укорочением путей → `content/small-business-space-ru/` (548 файлов).
4. Починены битые ссылки; добавлены `00-index.md`, `INDEX.md`.
5. Пакеты A→C через Issues; D — в бэклоге.
6. Обратный импорт ZIP Git→Notion — **эксперимент отклонён** (лимит 5 MB, разметка/картинки). Актуальный путь: [`notion-integration.md`](notion-integration.md) (Notion MCP и/или `NOTION_TOKEN`).

## Полезные команды проверки ссылок

```bash
python3 - <<'PY'
import re, urllib.parse
from pathlib import Path
root = Path('content/small-business-space-ru')
link_re = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
ok=bad=0
for md in root.rglob('*.md'):
    for m in link_re.finditer(md.read_text(encoding='utf-8')):
        href=m.group(2)
        if href.startswith('http') or href.startswith('data:'):
            continue
        target = md.parent / urllib.parse.unquote(href.split('#')[0])
        ok += target.exists(); bad += not target.exists()
        if not target.exists():
            print('BAD', md, href)
print('ok', ok, 'bad', bad)
PY
```
