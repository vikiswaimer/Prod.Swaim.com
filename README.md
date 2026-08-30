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

## Growth (SWA-37)
Посадочная: https://vikiswaimer.github.io/Prod.Swaim.com/  
SEO-заметка теста: `/notes/stek-freelancer.html` · campaign `toolmap_solo_ds`.

## Публичный URL (цикл 2 / SWA-36)
Варианты: Cloudflare Pages / GitHub Pages на папку `map/` / любой static host.  
Landing: `landing/` (A/B/C + схемы) — выбор UX **SWA-38**.  
После деплоя — URL в комментарий SWA-35 и сюда.
