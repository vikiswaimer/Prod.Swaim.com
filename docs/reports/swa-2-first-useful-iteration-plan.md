# SWA-2 — план первой полезной итерации

**Issue:** Paperclip SWA-2 · **Роль:** Product Lead · **Дата:** 2026-08-16  
**Ревизия:** v1.1 (retry после failed disposition)  
**Статус:** план в Git готов · формальный Paperclip `request_confirmation` — **blocked** (нет API)  
**Опора:** [`methodology.md`](../methodology.md) · risk-map SWA-3 (PR #34) · evidence pack SWA-8 (PR #37) · WIP-lock SWA-9 (PR #42 / #43) · sync (PR #40)

> Внутренний план координации. **Не** копировать в пользовательский Notion целиком. Лендинг / маркетинг-стратегию Prod.Swaim не трогаем.

---

## Вердикт в одном абзаце

Первая полезная итерация — **не** новый модуль шаблона, а **полевой цикл Mom Test**: снять главный риск **valuable** дешёвым честным экспериментом. Foundation A–D + Other + группа Бизнес уже дают usable срез; evidence pack показывает, что «знание аудитории» ≈ гипотезы без первичных обязательств. Поэтому WIP=1 = W1 интервью; контент-пакеты и GTM — HOLD. Команда целиком не будится.

---

## 1. Один outcome цикла

> Провести **≥5 разговоров ≥20 мин** с людьми из кластера «уже жгли kit / оболочку» (+ при возможности 1–2 «ложный сигнал»), зафиксировать прошлое поведение (часы, деньги, неделя броска, workaround) и обновить светофор **H4 / H1 / H5**.

**Считается успехом итерации (любой из):**

- ≥1–2 **pre-order / предоплата / intro** с причиной, **или**
- ≥3 карточки с суммой + неделей броска + workaround (даже без оплаты), **или**
- явный **отказ с причиной** (тоже Learn) → решение pivot / persevere / уточнить ICP.

**Не outcome:** «круто», лайки, новые страницы шаблона, параллельный старт Активности / v2 rich / лендинга.

Playbook исполнения: [`w1-mom-test-brief.md`](w1-mom-test-brief.md) (draft PR [#40](https://github.com/vikiswaimer/Prod.Swaim.com/pull/40), [#42](https://github.com/vikiswaimer/Prod.Swaim.com/pull/42)).

---

## 2. Три гипотезы (проверяем в этом цикле)

Формат: *верим, что [клиент] имеет [проблему]; если [решение], то [сигнал]*.

| ID | Гипотеза | Кластер | Как поймём |
|----|----------|---------|------------|
| **H4** | Узкий RU digital-product kit без retail-шума → **покупка + возврат на 2-й месяц** у тех, кто уже платил/жёг время на чужие оболочки | Артём · Юля · Катя | Суммы/недели прошлого; pre-order или отказ с причиной на наш пилот |
| **H1** | Готовый RU-маршрут «клиент → продукт → оффер» + пример → за первую неделю **заполнены ≥2 раздела** и есть **2-я сессия** | Саша (если есть часы на самосбор) | Наблюдение онбординга после разговора; не «обещал заполнить» |
| **H5** | Светофор сильный/слабый сигнал + вопросы про прошлое → **отсечение шума** до большой поставки | Марина (+ антипример Игорь) | Доля 🔴-карточек в отчёте; после «круто» — что сделали за 7 дней |

Источник реестра: risk-map (PR [#34](https://github.com/vikiswaimer/Prod.Swaim.com/pull/34)). Анти-ICP: интерес без обязательств (Игорь) — **не** звать в ядро выборки.

---

## 3. Какой один issue взять первым

| Приоритет | Issue | Owner | Зачем |
|-----------|-------|-------|-------|
| **1 · ACTIVE** | **Discovery: W1 Mom Test** — Linear [PRO-3](https://linear.app/swaim/issue/PRO-3/discovery-ispolnit-w1-mom-test-brief) (уже In Progress) · parent [PRO-2](https://linear.app/swaim/issue/PRO-2) | Discovery PM + CEO (рекрут) | Единственный слот WIP=1; снимает valuable |
| HOLD | GH [#22](https://github.com/vikiswaimer/Prod.Swaim.com/issues/22) Активность / Lean | Content | W2 — после вывода W1 |
| HOLD | Smoke-оффер / pre-order как отдельный Growth-прогон | Growth | W3 — после ICP (Артём vs Саша) |
| OUT | Лендинг / маркетинг-стратегия Prod.Swaim | — | Отдельный чат; не этот цикл |

**Правило команды:** не будить CTO / UX / Growth / Researcher параллельно. После accept plan — **один** wake: Discovery (CEO помогает с рекрутом). Остальные IDLE, пока W1 не дал вывод.

Координационный SoT: Linear [PRO-2](https://linear.app/swaim/issue/PRO-2) + [`paperclip-team-sync.md`](paperclip-team-sync.md) (draft PR #40 / #42).

---

## 4. Почему не «ещё Клиенты в Git»

Черновик v0 этого тикета предлагал снова править хаб **Клиенты**. Это отклоняем как ACTIVE:

| Кандидат | Решение |
|----------|---------|
| Контент Клиенты / pack E | ⏸ Контент-каркас уже есть (Бизнес #26, истории #32, Other #17). Без полевых данных — feature factory |
| Активность #22 | ⏸ Usable/learn не лечит «платят ли» |
| Пилот v2 #30 | ⏸ После сигнала, что v1/kit вообще нужен |
| Лендинг | ❌ Вне scope |

MVP Olsen здесь = **уже полезный срез обучения с рынком** (интервью + решение по ICP), а не «сломанный черновик» новых страниц.

---

## 5. Build → Measure → Learn (кратко)

| Шаг | Действие |
|-----|----------|
| **Build** | Список 25–30 контактов; outreach без питча; скрипт про прошлое; оффер пилота на столе *после* фактов |
| **Measure** | ≥25 исходящих · ≥8 ответов с фактами · ≥5 созвонов · цель ≥1–2 обязательства или отказы с причиной |
| **Learn** | Патч светофора H4/H1/H5 + строка в evidence pack; pivot / persevere / уточнить ICP **до** W2/W3 |

---

## 6. Done для SWA-2 (этот тикет)

- [x] 1 outcome назван
- [x] 3 гипотезы названы (H4, H1, H5)
- [x] Один первый issue назван (Discovery W1 / PRO-3); команда не разбужена пачкой
- [x] План зафиксирован в Git (`docs/reports/swa-2-first-useful-iteration-plan.md`) + draft PR
- [ ] Plan записан в Paperclip document + `request_confirmation` (**блокер: API**)
- [ ] Board accepted → SWA-2 → `done`; исполнение остаётся у Discovery (PRO-3), не новый PL-research

**Interim review path (пока нет Paperclip API):** CEO / board читает этот файл в draft PR и отвечает комментарием на Linear [PRO-2](https://linear.app/swaim/issue/PRO-2) («accept W1 plan» / правки). После появления API — повторить через `request_confirmation`.

---

## 7. Перенести в Notion вручную

**Ничего из этого плана в пользовательский шаблон не переносить.**

После полевых разговоров (уже не SWA-2):

1. При необходимости — 1–2 коротких примера сигнала в `examples/` (не в основной хаб).
2. Если менялись свойства DB Интервью/Отзывы — свойства + views «Сильный сигнал».
3. Не тащить в Notion ссылки на GitHub / Linear / этот `docs/reports/*`.

---

## 8. Disposition (runtime)

| Что | Статус |
|-----|--------|
| Содержательный deliverable SWA-2 (outcome + 3 гипотезы + 1 ACTIVE issue) | ✅ готов в Git |
| Paperclip control plane из Cursor Cloud | ❌ loopback `PAPERCLIP_API_URL` → connection refused; `https://paperclip.inc/api` → 401 без ключа |
| Запрошено в Cloud env | `PAPERCLIP_API_KEY` (required) · `PAPERCLIP_API_BASE_URL` (optional) |

**Disposition этого heartbeat:** `blocked`

**Unblock owner:** Board / Paperclip ops + владелец Cloud Agent environment.  
**Action:** инжект `PAPERCLIP_API_KEY` (+ опционально `PAPERCLIP_API_BASE_URL=https://paperclip.inc`) или рабочий bridge → re-wake Product Lead → PUT plan document → `request_confirmation` (idempotencyKey `confirmation:{SWA-2}:plan:{revision}`) → status `in_review` → после accept → `done`.

Не оставлять `in_progress` без live path: live path = появление API / ключа, не «ещё один research-раунд».
