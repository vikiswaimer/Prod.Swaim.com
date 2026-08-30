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
Открыть http://localhost:5173 · free map: `/free-map.html` · плейбук: `/playbook.html`

## Секреты
`config.local.js` / `.env.local` — не в git. PostHog EU.

## Публичный URL (цикл 2 / SWA-36)
Варианты: Cloudflare Pages / GitHub Pages на папку `map/` / любой static host.  
Landing: `landing/` (A/B/C + схемы) — UX-ветка; production default сейчас A на корне Pages.  
После деплоя — URL в комментарий SWA-35 и сюда.
