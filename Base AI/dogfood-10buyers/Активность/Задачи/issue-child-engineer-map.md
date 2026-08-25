# Child — FoundingEngineer: map + PostHog

## Статус
**Готово локально** (2026-08-25): `Base AI/dogfood-10buyers/map/`

## Гипотеза (feasible)
Лёгкая публичная страница map одной ниши достаточна для кликов и событий аналитики.

## Срез
1. Артефакт: `map/index.html` + `app.js` + `styles.css` — 8 узлов, 8 рёбер, панель, CTA.
2. PostHog browser SDK (EU): `map_viewed`, `node_clicked`, `edge_clicked`, `paid_cta_clicked`.
3. Ключ в `config.local.js` / `.env.local` — **не** в git.
4. README: как открыть.

## Done
Страница открывается; без ключа — stub в console. Оплата плейбука — следующий цикл.

