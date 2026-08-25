# Tool Map v0

## Портрет
Фаундеры и предприниматели (стабильный каркас).

## Ниши
Данные: `niches.js`. Статусы: backlog → testing → keep | paused | killed.  
Активная сейчас: `solo-digital-services` (testing).  
Добавить нишу = новый объект в `items` + nodes/edges; убрать = `killed` / снять `activeSlug`.

## Локально
```bash
npx --yes serve -p 5173
```
Открыть http://localhost:5173 · плейбук: `/playbook.html`

## Секреты
`config.local.js` / `.env.local` — не в git. PostHog EU.

## Публичный URL (цикл 2)
**Хостинг:** GitHub Pages · папка `toolmap/` · workflow `.github/workflows/toolmap-pages.yml`  
**URL:** https://vikiswaimer.github.io/Prod.Swaim.com/ (после merge + Pages → Source = GitHub Actions)  
**Секреты repo:** `TOOLMAP_POSTHOG_KEY`, `TOOLMAP_POSTHOG_HOST`  
**Landing:** default **A (Cartograph)** — `landing/a-cartograph.html` (override в SWA-35)  
**Домен:** swaimapp.com CNAME — позже (`Base AI/dogfood-10buyers/Маркетинг/Хостинг-домен.md`)
