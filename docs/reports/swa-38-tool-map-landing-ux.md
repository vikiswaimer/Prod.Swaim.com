# SWA-38 — Tool Map landing: UX-ревью + 3 визуальных направления

**Дата:** 2026-08-25 · **Роль:** UX Designer  
**Parent:** SWA-35 · **Портрет:** фаундеры / предприниматели · **Продукт:** Tool Map (не Prod.Swaim kit)  
**Статус:** lean-прототип v1 · **Live copy:** только с board

---

## Вопрос прототипа (один)

> За **≤2 секунды** фаундер понимает: **что получит бесплатно** (карта инструментов под нишу), **какой следующий шаг**, и **чем платный playbook отличается от free map**?

Опора: Knapp (timebox, checkable artifact) · Mom Test (не «красиво», а «открыли бы карту?») · Olsen (free map = уже полезный срез; playbook = платящий outcome).

**Не проверяем в v1:** полный каталог инструментов, pricing page, SEO-лонгриды, бренд Prod.Swaim.

---

## UX summary

| Критерий | A Map First | B Problem First | C Portfolio |
|----------|-------------|-----------------|-------------|
| Иерархия за 2 с | ✅ продукт = hero | ⚠️ сначала боль, карта ниже fold | ✅ «выбери нишу» |
| Ясность Free vs Paid | ⚠️ playbook — ghost CTA | ✅ compare-блок | ✅ tiers под CTA |
| Один primary CTA | ✅ «Открыть карту» | ✅ «Получить карту бесплатно» | ✅ после выбора ниши |
| Mom Test copy | нейтрально | ✅ про прошлое («уже платите») | нейтрально |
| Риск dark pattern | низкий | низкий | низкий |
| Масштаб портфеля ниш | ❌ одна ниша в hero | ❌ один пример | ✅ grid ниш |
| Handoff Engineer | средний | простой | сложнее (state) |

**Рекомендация для публичного URL:** **Variant C (Portfolio)** — с доработками из B.

**Почему не A:** карта в hero сильна для return-visit, но cold traffic не знает нишу; «SaaS-ниша» захардкожена — ломает портфель.

**Почему не B alone:** лучший Mom Test copy и Free/Paid compare, но нет механики портфеля ниш (scope SWA-35).

**Почему C + элементы B:** первый клик = ниша (portfolio), compare Free/Paid переносим под fold; визуал C (indigo, card grid) — нейтральный, не конфликтует с Prod.Swaim kit.

---

## Ревью вариантов

### A — Map First (`variant-a-map-first.html`)

**Сильное:** продукт виден сразу; dark UI = «инструмент для работы»; badge Free на H1.

**Слабое:**
- Hero привязан к одной нише (SaaS) — cold visitor другой ниши отваливается.
- «Playbook →» в nav без контекста — неясно, платно ли.
- Ghost CTA «Как устроен playbook» конкурирует с primary.

**Empty/error (slice):** если карта не загрузилась — нет fallback; добавить одну строку «карта временно недоступна → PDF-пример».

### B — Problem First (`variant-b-problem-first.html`)

**Сильное:** Mom Test формулировка («уже платите за 12 инструментов»); compare Free/Paid — лучший на slice; editorial tone доверяет фаундеру.

**Слабое:**
- Карта ниже fold на mobile — 2-секундный тест проваливается без скролла.
- Один пример (SaaS seed) — не portfolio.
- Serif + warm accent — узнаваемый, но отдельный бренд; не reuse Prod.Swaim style guide (OK по scope).

**Empty/error:** «Посмотреть пример» без выбранной ниши — нужен default или modal.

### C — Portfolio (`variant-c-portfolio.html`)

**Сильное:** IA портфеля ниш = core SWA-35; selection state + dynamic CTA; tiers Free/Paid без давления.

**Слабое:**
- Без выбора ниши CTA disabled — на first paint «B2B SaaS» preselected (OK для dogfood, уточнить в A/B).
- «Предложить нишу» — хороший Mom Test hook, но без формы = dead end.
- Нет preview карты — user commits before seeing product.

**Empty/error:** disabled card «Предложить нишу» — нужен microcopy «расскажите нишу → мы приоритизируем».

---

## Схема 1: Free map → Paid playbook

```text
┌──────────────┐     email opt-in      ┌─────────────────┐
│ Landing (C)  │ ────────────────────► │ Free Tool Map   │
│ Pick niche   │     (optional v1)     │ PDF + web view  │
└──────────────┘                       └────────┬────────┘
                                                │
                     usage signal: export,       │ gap found
                     return 2×/week,            │ «как внедрять?»
                     share link                 ▼
                                       ┌─────────────────┐
                                       │ Paid Playbook   │
                                       │ sequence +      │
                                       │ criteria +      │
                                       │ templates       │
                                       └─────────────────┘
```

**Правила UX (anti dark pattern):**
- Free map **полный** для ниши — не «10 из 24, остальное за paywall».
- Playbook upsell только после **конкретного триггера**: пробел на карте, экспорт, или явный «Playbook» CTA (не popup на входе).
- Цена playbook — на отдельном экране после intent, не на landing hero.

---

## Схема 2: Портфель ниш

```text
                    ┌─────────────────────────────────────┐
                    │         toolmap.example/            │
                    │  [B2B SaaS] [Creator] [D2C] [Agency]│
                    └───────────┬─────────────────────────┘
                                │
          ┌─────────────────────┼─────────────────────┐
          ▼                     ▼                     ▼
   /map/b2b-saas         /map/creator           /map/d2c
   (free, canonical)     (free)                 (free)
          │                     │                     │
          └─────────────────────┴─────────────────────┘
                                │
                    shared: playbook upsell component
                    per-niche: playbook/b2b-saas (paid)
```

**IA правило:** landing = router; каждая ниша = **canonical URL** для SEO и share. Landing не дублирует карту — редирект или deep link.

**WIP portfolio (dogfood):** 3–4 ниши max в v1; «Предложить нишу» = Mom Test intake, не promise instant map.

---

## Рекомендация: публичный URL

**Вести в prod:** **Variant C** как `/` (portfolio router).

**3 правки max (до FoundingEngineer):**

1. **Перенести compare Free/Paid из B** — блок под niche-grid, до CTA: две колонки «Free · Карта» / «Paid · Playbook» (copy из variant-b).
2. **Preview-on-select** — при выборе ниши показывать мини-превью 3–4 узлов карты (snippet из A) справа от grid на desktop / под grid на mobile. Отвечает на «что получу» до клика.
3. **Primary CTA copy:** «Открыть карту [Niche]» → Mom Test: «Посмотреть карту — бесплатно» (убирает страх paywall на первом касании).

**Не в v1:** регистрация, pricing table, A/B infra, больше 4 ниш.

---

## AC (проверяемые)

- [ ] **AC1:** На landing ровно **один** primary CTA; secondary — text/ghost, не конкурирует визуально.
- [ ] **AC2:** 5-секундный тест (1 фаундер, cold): называет «карту инструментов» + «бесплатно» + «можно выбрать нишу» — ≥4/5 без подсказок.
- [ ] **AC3:** Free vs Paid различим **без скролла** на 1440×900 (compare-блок или tiers).
- [ ] **AC4:** Каждая ниша в grid ведёт на **отдельный URL** `/map/{slug}` — не modal-only.
- [ ] **AC5:** Нет упоминаний Prod.Swaim kit, GitHub, internal docs в пользовательском copy.
- [ ] **AC6:** Empty: ниша «скоро» — одна строка + «Предложить нишу»; error: карта недоступна — PDF fallback link.

---

## Как узнаем, что срез сработал

| Метод | Порог | Когда |
|-------|-------|-------|
| 5-секундный тест | ≥4/5: free map + niche | после impl FoundingEngineer |
| Mom Test | «Искали бы такую карту до покупки следующего SaaS?» — прошлое | W1 dogfood, 3 фаундера |
| Click signal | ≥40% landing → open map (niche selected) | PostHog, 2 недели |
| Fail pivot | «Не понял, за что платить playbook» >2/5 → усилить compare из B | stop / iterate |

---

## Handoff

### → FoundingEngineer

**Scope v1:**
- Implement **Variant C** as `/` + `/map/{slug}` routes.
- Merge compare block from B (static HTML component).
- Preview snippet on niche select (reuse A map-grid partial).
- Screenshot rendered UI in PR — **без скрина → возврат UX**.

**Pattern names:** `NicheCard` · `NicheGrid` · `TierCompare` · `MapPreview` · `PrimaryCTA`

**Files:**
- [`docs/base-ai/dogfood-10buyers/map/landing/variant-c-portfolio.html`](../base-ai/dogfood-10buyers/map/landing/variant-c-portfolio.html) — base layout
- [`variant-b-problem-first.html`](../base-ai/dogfood-10buyers/map/landing/variant-b-problem-first.html) — compare section source
- [`variant-a-map-first.html`](../base-ai/dogfood-10buyers/map/landing/variant-a-map-first.html) — map preview source

### → GrowthMarketer

- Hero H1 C: «Выберите свою нишу — получите карту стека» — проверить Mom Test альтернативы:
  - «Стек инструментов для [ниша] — на одной карте»
  - «Перестаньте платить за инструменты, которые не стыкуются»
- CTA: «Посмотреть карту — бесплатно»
- Playbook upsell copy (post-map): не на landing — отдельный brief.

---

## Остаточный риск

| Риск | Митигация |
|------|-----------|
| C без preview = низкая конверсия в open map | Правка #2 preview-on-select |
| Портфель раздувается >4 ниш | WIP cap; «Предложить нишу» = intake, не обещание |
| Playbook perceived as upsell scam | Free map полный; compare explicit; no timer/popup |
| Prod.Swaim brand bleed | Отдельный Tool Map visual; не reuse kit colors/copy |
| Файлы не были в cloud до этого run | Прототипы созданы UX в `docs/base-ai/…`; sync с local Base AI vault — board |

---

## Артефакты

| Артефакт | Путь |
|----------|------|
| Index landing | [`docs/base-ai/dogfood-10buyers/map/landing/README.md`](../base-ai/dogfood-10buyers/map/landing/README.md) |
| Variant A | [`variant-a-map-first.html`](../base-ai/dogfood-10buyers/map/landing/variant-a-map-first.html) |
| Variant B | [`variant-b-problem-first.html`](../base-ai/dogfood-10buyers/map/landing/variant-b-problem-first.html) |
| Variant C ★ | [`variant-c-portfolio.html`](../base-ai/dogfood-10buyers/map/landing/variant-c-portfolio.html) |
| UX report (этот файл) | [`docs/reports/swa-38-tool-map-landing-ux.md`](swa-38-tool-map-landing-ux.md) |

---

## Комментарий для SWA-35 (copy-paste)

**Выбранный вариант:** **C (Portfolio)** + compare из B + map preview из A.

**Файлы:**
- `docs/base-ai/dogfood-10buyers/map/landing/variant-c-portfolio.html`
- `docs/reports/swa-38-tool-map-landing-ux.md`

**3 правки до impl:** compare Free/Paid · preview-on-select · CTA «Посмотреть карту — бесплатно».

**Live copy:** ждём board.

---

## История

| Дата | Изменение |
|------|-----------|
| 2026-08-25 | SWA-38 v1: 3 HTML-прототипа + UX-ревью + рекомендация C |
