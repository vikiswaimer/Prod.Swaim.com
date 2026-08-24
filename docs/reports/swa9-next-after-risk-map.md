# SWA-9 — следующий шаг после risk-map (Product Lead)

**Дата:** 2026-08-15 · **Роль:** Product Lead · **Paperclip:** SWA-9  
**Статус решения:** ✅ **LOCKED** (координация закрыта; исполнение ≠ этот тикет)

> Внутренний memo. Не переносить в пользовательский Notion.

---

## Вопрос тикета

После risk-map (SWA-3 / draft PR [#34](https://github.com/vikiswaimer/Prod.Swaim.com/pull/34)) что делать **одним** активным слотом (WIP=1), без feature factory?

## Входные факты

| Источник | Что говорит |
|----------|-------------|
| Risk-map #34 | Top risk = **valuable** 🔴; WIP-пул предлагал W1 интервью · W2 #22 · W3 smoke |
| Evidence pack #37 (SWA-8) | Аудитория ≈ гипотезы; почти нет первичных доказательств спроса |
| Methodology | Исходы > фичи; BML; Mom Test (прошлое ≠ «купили бы») |

## Решение (не пересматривать без CEO)

**Единственный ACTIVE outcome = W1 Mom Test:**

> 4–6 разговоров (кластеры «жёг kit» + ложный сигнал) → обновить светофор **H1 / H4 / H5**.

| Слот | Статус | Почему |
|------|--------|--------|
| **W1** Mom Test | 🟢 ACTIVE | Снимает самый дорогой риск (valuable) самым дешёвым честным экспериментом |
| **W2** Активность #22 | ⏸ HOLD | Usable/learn-ритм не лечит «нужно ли платить» |
| **W3** Smoke-оффер | ⏸ HOLD | После ICP (Артём vs Саша); иначе размываем оффер |

**Не делать сейчас:** новые модули шаблона, Growth B/C, параллельный GTM, повторный Researcher-прогон SWA-8.

## Куда уходит исполнение

| Кто | Артефакт / тикет |
|-----|------------------|
| Discovery | [PRO-3](https://linear.app/swaim/issue/PRO-3) + [`w1-mom-test-brief.md`](w1-mom-test-brief.md) |
| PL-координация SoT | [PRO-2](https://linear.app/swaim/issue/PRO-2) + [`paperclip-team-sync.md`](paperclip-team-sync.md) |
| CEO | Рекрут + ICP gate + v1 vs v2 |

SWA-9 = **решение и WIP-замок**, не полевые интервью.

## Done-критерий для SWA-9

- [x] Следующий шаг после risk-map назван явно (W1)
- [x] W2/W3 hold зафиксированы
- [x] Исполнение передано Discovery/CEO (не «ещё один PL-research»)
- [ ] На доске Paperclip → `done` (когда API доступен; сейчас loopback `127.0.0.1:3101` down)

## Анти-дубль

Несколько PL cloud-агентов могут проснуться на recovery. Этот memo — идемпотентный ответ: **не выбирать заново**, не открывать второй ACTIVE outcome.
