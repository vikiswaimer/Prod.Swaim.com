# SWA-9 — следующий шаг после risk-map (Product Lead)

**Дата:** 2026-08-15 · **Роль:** только Product Lead · **Paperclip:** SWA-9  
**Входы:** risk-map ([PR #34](https://github.com/vikiswaimer/Prod.Swaim.com/pull/34)) · evidence pack ([PR #37](https://github.com/vikiswaimer/Prod.Swaim.com/pull/37))  
**Компас:** исходы > фичи · Ries WIP=1 · Mom Test · Cagan valuable-first

> Внутренний decision log. Не переносить в пользовательский Notion.

---

## Решение (закрывает SWA-9)

После карты рисков **не** открываем второй контент-пакет и **не** держим три активных слота.

| Было в risk-map (SWA-3) | Стало (SWA-9) |
|-------------------------|---------------|
| WIP-пул ≤3: W1 + W2 + W3 «активны» | **WIP=1:** только **W1** Mom Test |
| Следующий шаг размыт между интервью / Активность / smoke | Следующий шаг = **полевые разговоры** → обновить H1/H4/H5 |
| Feature-агенты могут стартовать «по списку» | Feature / W2 / W3 / Growth B–C — **hold** |

**Активный outcome:**

> ≥5 Mom Test-созвонов (кластер «жёг kit» + по необходимости ложный сигнал) → Learn по valuable → патч светофора.

Исполнение: [`w1-mom-test-brief.md`](w1-mom-test-brief.md) · Linear [PRO-2](https://linear.app/swaim/issue/PRO-2) / [PRO-3](https://linear.app/swaim/issue/PRO-3).

---

## Почему так (1 абзац)

Evidence pack честно сказал: архетипы ≠ validated demand. Самый дорогой риск сейчас — **valuable** (H4/H1/H5), не usable-модули и не GTM-охват. Параллелить Активность (#22) или smoke-оффер до выбора ICP и полевого сигнала = движение без обучения.

---

## Что Product Lead сделал в этом тикете

1. Зафиксировал **WIP=1** в [`docs/risk-map-hypotheses.md`](../risk-map-hypotheses.md) (§8).
2. Подтвердил playbook W1 и дочернюю Discovery-задачу (PRO-3) — без нового Researcher/feature-прогона.
3. Обновил team sync: SWA-9 = decision done; исполнение у Discovery + CEO-рекрут.

**Не делали:** правки шаблона Notion, лендинг, merge всех draft PR пачкой, повторный research.

---

## Критерий done для SWA-9 (координация)

- [x] Явный next step после risk-map записан
- [x] WIP схлопнут до 1 активного слота
- [x] Команда знает, кто исполняет (Discovery) и что на hold
- [x] Paperclip SWA-9 → координационно закрыт (см. SWA-10 review); на доске `done` вручную, пока API down

---

## Когда снова нужен Product Lead

После ≥3–5 карточек сигнала: pivot/persevere ICP, открытие W3 или W2, обновление sync — **не** раньше и не параллельным feature-wake.

---

## История

| Дата | Изменение |
|------|-----------|
| 2026-08-15 | Decision log SWA-9: WIP=1 → W1 после risk-map |
