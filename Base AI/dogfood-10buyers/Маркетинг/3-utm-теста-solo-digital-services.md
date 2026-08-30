# 3 UTM-теста — solo-digital-services

Для соло-специалистов и микро-фаундеров в digital Tool Map сокращает перебор сервисов и показывает рабочую связку под задачу.

## Одна growth-гипотеза

Верим, что люди из ниши `solo-digital-services` уже ищут не "ещё один список инструментов", а короткий способ собрать рабочий стек под услуги и инфопродукт; если дать value-first пост с 1 конкретной связкой и ссылкой на live map, то увидим первые `map_viewed` по UTM.

## Один дешёвый эксперимент

Не строим GTM-машину. Запускаем один срез: **3 value-first размещения** с одной и той же логикой оффера.

- Не продаём "весь каталог".
- Не обещаем неготовую оплату.
- Ведём весь трафик на live map: `https://vikiswaimer.github.io/Prod.Swaim.com/`

## Одна метрика

**Главная метрика:** `map_viewed` с разрезом по `utm_content`.

`paid_cta_clicked` смотрим как диагностический сигнал глубины интереса, но не как главную метрику этого запуска.

## 3 теста

| ID | Канал | utm_content | Live URL | Value-first срез поста | Статус |
|---|---|---|---|---|---|
| 14 | Telegram: no-code / solo-business чат | `tg_nocode_value` | `https://vikiswaimer.github.io/Prod.Swaim.com/?utm_source=telegram&utm_medium=community&utm_campaign=toolmap_solo_ds&utm_content=tg_nocode_value` | "Если вы собираете стек под соло-услуги, начните не с топ-50 сервисов, а с 1 карты связок: Notion → Telegram → Tilda → оплата. Собрала live map, где видно, что с чем стыкуется и что можно не брать на старте." | `running` |
| 29 | LinkedIn: 1 пост про связку Notion ↔ Telegram | `li_notion_tg` | `https://vikiswaimer.github.io/Prod.Swaim.com/?utm_source=linkedin&utm_medium=organic_social&utm_campaign=toolmap_solo_ds&utm_content=li_notion_tg` | "For solo digital services, the real problem is not tool discovery but tool fit. I mapped one practical stack — Notion, Telegram, Tilda, payments — so you can see the flow before buying another tool." | `running` |
| 34 | SEO/заметка: "стек фрилансера маркетолога" | `seo_freelancer_stack` | `https://vikiswaimer.github.io/Prod.Swaim.com/?utm_source=seo&utm_medium=organic_article&utm_campaign=toolmap_solo_ds&utm_content=seo_freelancer_stack` | "Стек фрилансера-маркетолога полезнее начинать не со списков, а со связки задач: где у вас контент, заявки, оплата и созвоны. В карте видно, как собрать базовый маршрут без лишних подписок." | `running` |

## Keep / kill сигнал для PO

- **Keep / iterate:** один из `utm_content` даёт первые осмысленные `map_viewed` и хотя бы единичный переход к `paid_cta_clicked`.
- **Kill / pause:** тест не приводит к `map_viewed`, либо просмотры есть, но value-first сообщение не дотягивает до CTA и требует другой формулировки боли.

## Что менять следующим, если сигнал слабый

1. Не менять сразу нишу.
2. Сначала переписать первый абзац под более конкретную боль:
   - "не понимаю, чем связать заявки, оплату и контент";
   - "не хочу платить за 5 сервисов до первой выручки";
   - "нужен не каталог, а рабочий маршрут".
3. Только потом менять канал.
