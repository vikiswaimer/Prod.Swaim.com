# PostHog — Tool Map (веб, без Cursor MCP)

## Статус
- [x] Проект в PostHog создан, Project API key найден (`phc_...`)
- [x] Ключ лежит только в `map/.env.local` (не в git)
- [x] Регион: **EU** → `https://eu.i.posthog.com`
- [ ] События с map доходят (Live events в веб PostHog)

> Если ключ светился в чате — в PostHog **ротируйте** Project API key и обновите `.env.local`.


## Куда класть ключ
1. Скопируйте `map/.env.local.example` → `map/.env.local`
2. Вставьте `POSTHOG_KEY=phc_...`
3. Укажите `POSTHOG_HOST` под ваш регион

## События v0
| Event | Когда |
|-------|--------|
| `map_viewed` | открыли map |
| `node_clicked` | клик по инструменту |
| `edge_clicked` | клик по связке |
| `paid_cta_clicked` | CTA на платный плейбук |

Проверка: PostHog → **Activity** / Live events после открытия map.

## Cursor MCP
Пока не используем (ошибка в Desktop). Аналитику смотрите в **веб PostHog**.
