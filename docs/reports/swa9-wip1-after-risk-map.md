# SWA-9 — WIP=1 после risk-map (решение Product Lead)

**Issue:** Paperclip SWA-9 · **Дата:** 2026-08-15  
**Роль:** Product Lead · **Статус:** ✅ решение принято — можно закрывать SWA-9 как `done`

> Внутренний артефакт. Не переносить в пользовательский Notion.

---

## Вопрос тикета

Risk-map (SWA-3 / [PR #34](https://github.com/vikiswaimer/Prod.Swaim.com/pull/34)) предложил пул **W1–W3**.  
SWA-9 требует от Product Lead **один** следующий шаг (WIP=1), не три параллельных трека.

---

## Решение (жёстко)

| | |
|--|--|
| **ACTIVE** | **W1** — 4–6 Mom Test-разговоров (кластеры «жёг kit» + ложный сигнал) → обновить светофор **H1 / H4 / H5** |
| **Риск** | **valuable** 🔴 (Cagan) — kit экономит время / меняет поведение у ICP? |
| **Гипотезы** | H4 (платят и остаются) · H1 (возврат после недели) · H5 (отсечение ложного сигнала) |
| **HOLD** | W2 Активность [#22](https://github.com/vikiswaimer/Prod.Swaim.com/issues/22) · W3 smoke-оффер / pre-order |
| **Почему не W2/W3** | Evidence pack (SWA-8 / [PR #37](https://github.com/vikiswaimer/Prod.Swaim.com/pull/37)): аудитория ≈ гипотезы, не validated demand. Delivery без сигнала = feature factory. Smoke без ICP = vanity |

**Исход цикла (не фичи):** полевые факты прошлого поведения + ≥1–2 обязательства (pre-order / intro) **или** отказы с причиной → Learn: persevere / pivot ICP / уточнить оффер.

---

## Почему именно это (Lean)

1. **Build–Measure–Learn:** самый дешёвый честный сигнал — разговор про прошлое, не новый модуль шаблона.  
2. **WIP=1 (Ries):** risk-map дал *кандидатов*; PL сжимает до одного ACTIVE, иначе обучение не сходится.  
3. **Mom Test:** «круто» / «я бы купил» не двигают светофор.  
4. **MVP (Olsen + владелец):** полезный платящий срез нельзя заявить без valuable-сигнала.

---

## Исполнение (не этот тикет)

| Артефакт | Где |
|----------|-----|
| Playbook W1 | [`w1-mom-test-brief.md`](w1-mom-test-brief.md) |
| Координация команды | [`paperclip-team-sync.md`](paperclip-team-sync.md) |
| Linear parent | [PRO-2](https://linear.app/swaim/issue/PRO-2) |
| Linear Discovery | [PRO-3](https://linear.app/swaim/issue/PRO-3) — Todo → In Progress при первом outreach |
| Risk-map SoT | draft [PR #34](https://github.com/vikiswaimer/Prod.Swaim.com/pull/34) |

**Владельцы исполнения:** Discovery PM (созвоны/карточки) + CEO (рекрут, ICP-гейт).  
**Product Lead:** WIP-страж; не открывать W2/W3 и feature-пакеты, пока W1 не дал вывод.

---

## Что команде *не* делать сейчас

- Новые модули / Активность #22 / Growth B–C / пилот v2 #30  
- Перезапуск Researcher на SWA-8 (evidence pack уже принят)  
- Параллельный merge всех SWA-PR «заодно» (порядок в sync)  
- Второй ACTIVE GTM рядом с W1

---

## CEO gates (не блокируют старт outreach)

1. ICP на GTM: Артём («сжёг kit») vs Саша («первая оболочка») — желательно до pre-order.  
2. v1 точечно vs ставка на v2 — до W3 / Q2.  
3. Рекрут: список 25–30 контактов для W1.

---

## Закрытие Paperclip SWA-9

| Поле | Значение |
|------|----------|
| Outcome | WIP=1 выбран: W1 Mom Test |
| Next | PRO-3 исполняет brief; PL idle по координации до Learn |
| Доска | при живом API → `done` (этот документ = proof) |
| Notion | не требуется |

---

## История

| Дата | Изменение |
|------|-----------|
| 2026-08-15 | SWA-9 continuation: формальное PL-решение WIP=1 после risk-map |
