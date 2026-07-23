# Title

```
Дополнительно: мини-гайды + Интервью + Notion sync
```

---

## Цель

Группа **Other / Дополнительно** — не склад сущностей, а мини-гайды (эталон — «Цифровая безопасность»): зачем блок, что даёт бизнесу, как вести, какими инструментами.

В этом чате: переписаны хабы, залиты в Notion, добавлен блок **Интервью** (правильный сбор обратной связи через разговоры — без упоминания книги в пользовательском тексте).

## Критерии готовности

- [x] Хабы: Отзывы, Email шаблоны, Текстовые заготовки, Ссылки — в духе Цифровой безопасности
- [x] Ссылки: честно про удобный захват (не «веди каталог в Notion»)
- [x] Notion: Ссылки, Отзывы, Email, Текстовые заготовки; тела Ссылки/Безопасность при дозаливе не ломались
- [x] Новый блок **Интервью** в Git + Notion (DB «Заметки интервью» + демо)
- [x] Навигация: `00-index`, `INDEX`, CSV Other, треки Старт/Развитие
- [x] PR: https://github.com/vikiswaimer/Prod.Swaim.com/pull/15

## Что сделано (файлы / Notion)

### Git
- `Other/Отзывы--*`, `Email шаблоны--*`, `Text Snippets--*` (UI: Текстовые заготовки), `Ссылки--*`
- `Other/Интервью--a07ead21.md` + база заметок + демо
- `00-index.md`, `INDEX.md`, треки, `docs/glossary.md`, отчёты в `docs/reports/`
- Скрипты: `scripts/notion_sync_links.py`, `scripts/notion_sync_other_hubs.py`

### Notion
| Страница | Статус |
|----------|--------|
| Цифровая безопасность | эталон, тело не трогали в конце |
| Ссылки | залита; Description в таблице Other обновлён |
| Отзывы | залита + связка с Интервью |
| Email шаблоны | залита |
| Текстовые заготовки | залита (rename с Text Snippets) |
| **Интервью** | создана: https://app.notion.com/p/3a6207cad37981b7ad46d088bde34822 |

### Методология
- Cagan (outcomes), Ries (delivery vs learning)
- Mom Test / интервью — в шаблоне **без** названия книги; внутренний отчёт: `docs/reports/other-interviews.md`

## Вне скоупа / рядом
- Пакеты E–J (roadmap v2) — отдельный план/черновики issues: `docs/roadmap-v2.md`, `docs/issue-drafts/`, PR #14
- Массовая библиотека знаний, лендинг

## Перенос в Notion (осталось по желанию)
- [ ] RU-имена child DB (`Feedback`, `Email Snippets`, `Snippets`, `Links`)
- [ ] Иконка страницы Интервью / views у «Заметки интервью»
- [ ] Треки Старт/Развитие в Notion (ссылки на Интервью) — если ещё не руками

## Ветка / PR
- Ветка: `cursor/other-mini-guides-7cdb`
- PR: https://github.com/vikiswaimer/Prod.Swaim.com/pull/15
- Отчёты: `docs/reports/other-mini-guides.md`, `notion-sync-links.md`, `notion-sync-other-hubs.md`, `other-interviews.md`
