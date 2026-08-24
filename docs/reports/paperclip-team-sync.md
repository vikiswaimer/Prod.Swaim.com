# Paperclip team sync — Product Lead

**Дата:** 2026-08-15 · **Роль:** Product Lead Prod.Swaim  
**Компас:** исходы > фичи · Lean Startup (BML, WIP) · Mom Test · Cagan (valuable / usable / feasible / viable)

> Внутренний артефакт координации. Не переносить в пользовательский Notion.

---

## Вердикт цикла

Команда за один прогон собрала **6 draft PR** с discovery/delivery-артефактами. На `main` их ещё нет.

**Evidence pack (SWA-8) подтверждает:** «знание аудитории» ≈ гипотезы, не validated demand. Поэтому следующий цикл — **не** новые модули шаблона, а **полевой сигнал**.

**Один активный outcome сейчас:**

> Провести 4–6 Mom Test-разговоров (кластеры «жёг kit» + ложный сигнал) и обновить светофор H1 / H4 / H5.

Исполняемый playbook: [`w1-mom-test-brief.md`](w1-mom-test-brief.md).

Всё остальное — очередь или подготовка к merge после решения CEO.

### Heartbeat (2026-08-15, wake с доски Paperclip)

- Paperclip API (`127.0.0.1:3101`) по-прежнему **unreachable** из cloud; ключ API не инжектирован → inbox/checkout недоступны.
- Координация: GitHub draft PR + Linear **PRO-2** + этот sync.
- Команда IDLE после SWA-3…8; **не** запускать новый feature-прогон.
- Следующий шаг исполнения: Discovery берёт W1 brief, CEO — рекрут + ICP.

---

## Что команда уже поставила (draft)

| SWA | Роль | PR | Артефакт | Тип |
|-----|------|-----|----------|-----|
| SWA-3 | Product Lead | [#34](https://github.com/vikiswaimer/Prod.Swaim.com/pull/34) | `docs/risk-map-hypotheses.md` | карта рисков + WIP W1–W3 |
| SWA-7 | Delivery | [#35](https://github.com/vikiswaimer/Prod.Swaim.com/pull/35) | `docs/delivery-checklist-git-to-notion.md` | ops Git→Notion |
| SWA-5 | UX | [#36](https://github.com/vikiswaimer/Prod.Swaim.com/pull/36) | `00-index` + треки «сегодня» | usable / onboarding |
| SWA-8 | Researcher | [#37](https://github.com/vikiswaimer/Prod.Swaim.com/pull/37) | `docs/reports/evidence-pack-clients.md` | честный сигнал vs шум |
| SWA-6 | Growth | [#38](https://github.com/vikiswaimer/Prod.Swaim.com/pull/38) | `docs/reports/growth-lean-experiments-swa6.md` | 3 GTM BML, WIP=1 |
| SWA-4 | Discovery PM | [#39](https://github.com/vikiswaimer/Prod.Swaim.com/pull/39) | JTBD + точечные правки Клиенты/Старт | outcomes в ядре |

Карта рисков и WIP-пул: [`docs/risk-map-hypotheses.md`](../risk-map-hypotheses.md) (на ветке PR #34, пока не в `main`).

---

## WIP-лимит (жёстко)

| Слот | Статус | Действие |
|------|--------|----------|
| **W1** Discovery — Mom Test интервью | 🟢 **ACTIVE** | Список 25–30 → ≥5 созвонов ≥20 мин с прошлым поведением → обновить H1/H4/H5 |
| **W2** Активность Lean (#22) | ⏸ HOLD | Не стартовать чат/PR, пока W1 не дал вывод *или* CEO явно не переставил слот |
| **W3** Smoke-оффер / pre-order | ⏸ HOLD | После выбора ICP (Артём vs Саша). Growth **эксперимент A** = тот же цикл, что W1+оплата — не параллелить отдельно |

**Правило:** новый эксперимент входит только когда один слот закрыт выводом (подтверждена / опровергнута / уточнить) или отменён CEO.

Growth B/C, пилот v2 (#30), холодный аудит (#33), каналы (#19), лендинг — **очередь**, не параллельный WIP.

---

## Build → Measure → Learn (W1)

| Шаг | Что |
|-----|-----|
| **Build** | 25–30 контактов; outreach без питча; скрипт Mom Test (прошлое: часы/деньги/неделя броска); одностраничный оффер пилота на столе, но не в начале разговора |
| **Measure** | ≥5 созвонов ≥20 мин; факты прошлого; цель ≥1–2 pre-order **или** явный отказ с причиной |
| **Learn** | valuable 🔴→🟡/🟢 или pivot ICP; обновить risk-map + evidence pack одной правкой |

Слабый сигнал («круто», «я бы купил») **не** двигает светофор.

---

## Порядок merge (чтобы не разнести `docs/agent-context.md`)

Почти все SWA-PR трогают `docs/agent-context.md` (и частично `positioning.md`). Мержить **по одному**, rebase остальных.

Рекомендуемый порядок:

1. **#34** risk-map (PL SoT)  
2. **#37** evidence pack (усиливает valuable-диагноз)  
3. **#35** delivery checklist (инфра команды)  
4. **#38** growth experiments (docs-only)  
5. **#36** UX nav — после CEO OK; затем **ручной перенос в Notion** по чеклисту #35  
6. **#39** JTBD + точечный контент — после #36 (оба трогают Старт); Notion sync

Не мержить пачкой. Не открывать новый контент-пакет (Активность / v2 rich), пока W1 в полёте.

---

## Задачи по ролям (следующий wake)

| Роль | Сделать | Не делать |
|------|---------|-----------|
| **CEO / владелец** | Выбрать ICP (Артём vs Саша); решить v1 точечно vs v2; рекрут на W1 | Параллелить все 6 PR «заодно» |
| **Discovery PM** | Владеть W1: скрипт, календарь, заметки, обновление H1/H4/H5 | Новые JTBD-страницы без полевых данных |
| **Researcher** | После 3+ интервью — патч evidence pack (факты с датами) | Додумывать персон |
| **Growth Lead** | Поддержать W1 списком/outreach; оффер пилота готов к столу | Запускать B/C или «охваты» |
| **UX** | Держать #36 готовым; после merge — один CTA «сегодня» в Notion | Новые экраны / галереи |
| **Delivery** | После merge UX/JTBD — манифест поставки по #35 | ZIP-импорт целого пространства |
| **Product Lead** | Следить WIP≤3; обновлять этот sync + risk-map после Learn | Feature factory, второй активный GTM |

---

## Блокеры среды

1. **Paperclip API** в cloud-агенте: `PAPERCLIP_API_URL` → `127.0.0.1:3101`, connection refused. Scratch dirs отсутствуют. Координация сейчас через **GitHub draft PR + этот sync**, не через локальный Paperclip heartbeat.  
2. Локальная установка Paperclip у владельца ещё может быть в процессе — не блокирует W1.  
3. Публичный Notion ранее отвечал `publicAccessRole: none` (аудит #33) — проверить доступ покупателей отдельно от контент-WIP.

---

## Связь с open GitHub issues

| Issue | Отношение к WIP |
|-------|-----------------|
| [#22](https://github.com/vikiswaimer/Prod.Swaim.com/issues/22) Активность | = W2, hold |
| [#30](https://github.com/vikiswaimer/Prod.Swaim.com/issues/30) v2 Клиенты | очередь после сигнала valuable |
| [#33](https://github.com/vikiswaimer/Prod.Swaim.com/issues/33) холодный аудит | trust-fix; не снимает valuable |
| [#19](https://github.com/vikiswaimer/Prod.Swaim.com/issues/19) каналы ОС | после первых интервью |
| [#24](https://github.com/vikiswaimer/Prod.Swaim.com/issues/24) группа Бизнес | foundation уже частично влито; не раздувать параллельно W1 |

---

## История

| Дата | Изменение |
|------|-----------|
| 2026-08-15 | Первый sync после прогона SWA-3…8: вердикт evidence → W1 active, merge order, роли |
| 2026-08-15 | Wake с доски: W1 brief + PRO-3; API still down; команде не стартовать фичи |
