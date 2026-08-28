# Paperclip: продуктовая команда (найм)

**Дата:** 2026-08-16  
**Роль:** координация org, не полевой цикл W1  
**Опора:** Cagan (empowered product team, исходы > фичи) · Ries (WIP, BML) · Mom Test · Olsen (MVP = полезный срез)

> Внутренний артефакт. **Не** копировать в пользовательский Notion.

---

## Вердикт

В Paperclip уже есть **роли продуктовой команды**, но первый прогон разбудил их **всех сразу** — получилась feature factory: 6 draft PR за один heartbeat, потом шторм дублей Product Lead.

Нужно не «нанять C-suite» (CTO / CMO / CFO), а **одну команду вокруг бизнес-цели**, с жёстким лимитом гипотез в работе.

Живой POST в Paperclip из этого Cloud-рана **не выполнен**: нет `PAPERCLIP_API_KEY`. Канон найма — этот файл + [`docs/paperclip-hires.json`](../paperclip-hires.json). Скрипт: `python3 scripts/paperclip_hire_product_team.py`.

---

## 1. Кто уже есть (аудит)

Paperclip control plane из cloud недоступен (`127.0.0.1:3101` refuse; `https://paperclip.inc/api` → 401 без ключа). Состав восстановлен по Cursor Cloud-агентам `source: sdk` с именами `Paperclip *` и по draft PR SWA-3…8.

| Роль в Paperclip | Что уже сделала | PR | Статус для org |
|------------------|-----------------|----|----------------|
| **Product Lead** | Карта рисков, WIP-замок W1 | [#34](https://github.com/vikiswaimer/Prod.Swaim.com/pull/34), [#40](https://github.com/vikiswaimer/Prod.Swaim.com/pull/40), [#42](https://github.com/vikiswaimer/Prod.Swaim.com/pull/42)–[#46](https://github.com/vikiswaimer/Prod.Swaim.com/pull/46) | **оставить** · страж WIP |
| **Discovery PM** | JTBD / Клиенты | [#39](https://github.com/vikiswaimer/Prod.Swaim.com/pull/39) | **оставить** · единственный ACTIVE на W1 |
| **Researcher** | Evidence pack | [#37](https://github.com/vikiswaimer/Prod.Swaim.com/pull/37) | **слить в Discovery** · не держать отдельный backlog |
| **UX Designer** | Навигация «сегодня» | [#36](https://github.com/vikiswaimer/Prod.Swaim.com/pull/36) | **оставить** · heartbeat HOLD, пока W1 в поле |
| **Delivery Engineer** | Чеклист Git→Notion | [#35](https://github.com/vikiswaimer/Prod.Swaim.com/pull/35) | **оставить** · heartbeat HOLD |
| **Growth Lead** | 3 GTM-эксперимента, WIP=1 | [#38](https://github.com/vikiswaimer/Prod.Swaim.com/pull/38) | **оставить в команде** · не отдел маркетинга · HOLD до W3 |
| **CEO** | Board / владелец | — | **человек** (vikiswaimer). ИИ-CEO — только если нужен heartbeat-оркестратор; не плодить второй strategy-loop |

Параллельные recovery Product Lead (десятки IDLE cloud-агентов) — **не** новые сотрудники. Не будить пачкой.

**Не нанимать:** CTO, CMO, CFO, QA, DevOps, контент-райтер «под маркетинг». Это функциональные силосы из дефолтного org Paperclip, не команда Cagan.

---

## 2. Видение: одна product team, не отделы

Cagan: команда **находит** решения под outcome, а не исполняет бэклог фич. Discovery и delivery в **одной** команде. Growth — эксперименты той же команды, не свой канал «охватов».

```text
Board (человек)
└── CEO* (стратегия, ICP-гейт, бюджет, approve hire)
    └── Product team «Prod.Swaim» — один продукт, один WIP-борд
        ├── Product Lead (pm)     — outcomes, 4 риска, страж WIP
        ├── Discovery (pm)        — Mom Test, evidence; поглощает Researcher
        ├── UX Designer           — usable
        ├── Delivery Engineer     — feasible (Git + Notion)
        └── Growth Lead           — viable-эксперименты в том же WIP
```

\*ИИ-CEO опционален. Пока ключа нет — Board = человек, Product Lead координирует через Git/Linear.

Все тикеты и гипотезы ведут к **одной company goal**, не к локальным KPI роли.

---

## 3. Точные WIP-цифры (Lean Startup → этот продукт)

Ries в книге не ставит «магическую тройку»; ставит **лимит незавершённого**, чтобы ускорить поток обучения. Цифры ниже — **наша реализация** (шаблон + risk-map + замок Product Lead).

| Слой | Лимит | Где зафиксировано | Смысл |
|------|-------|-------------------|--------|
| **Гипотезы «в работе»** | **1–3** | ветка Активность #22 (`Гипотезы`: «В работе одновременно 1–3») | Канбан To learn / Doing / Learned |
| **Слоты экспериментов компании** | **≤ 3** (W1–W3) | risk-map §8 (PR #34) | Новый слот только после вывода |
| **Сейчас (замок valuable 🔴)** | **WIP = 1** | SWA-9 LOCKED · Linear [PRO-2](https://linear.app/swaim/issue/PRO-2) | Только W1 Mom Test |
| **Цели** | **1–3 активные** | Пространство v2 `Сейчас`; #22 `Цели` | Исход, не список фич |
| **Задачи (v1 на main)** | **~3 активных**, не 15 | `Активность/Задачи` | После #22 исполнение — Linear/GitHub |
| **GTM-эксперименты** | **1** из трёх | SWA-6 Growth | A/B/C не параллелить |
| **Heartbeat агента** | **1** concurrent run | Paperclip V1 | Не плодить второй wake той же роли |
| **Ставка обучения / неделя** | **1** | история «Дима» в customer-stories | 1 проверяемая ставка vs «10 надо бы» |

**Правило найма:** наличие роли в org chart ≠ право стартовать свой бэклог. Одновременно в статусе «в работе» не больше **трёх** гипотез; пока valuable не снят — **одна**.

Текущий ACTIVE: W1 → Linear [PRO-3](https://linear.app/swaim/issue/PRO-3). HOLD: W2 Активность #22, W3 smoke-оффер.

---

## 4. Company goal (зачем команда существует)

**Исход, не фича:** подтвердить или опровергнуть **valuable** узкого ICP (кластер «уже жгли kit») честным сигналом: pre-order / intro / отказ с причиной; обновить светофор H4 / H1 / H5.

Не цель: «закрыть 6 PR», «нанять 12 агентов», «сделать модуль Активность», охваты.

После Learn W1 — CEO выбирает ICP (Артём vs Саша) и можно открыть **один** следующий слот (W2 или W3), не оба.

---

## 5. Кого нанять / оставить / не будить

| Агент | Paperclip `role` | Reports to | Heartbeat сейчас | Зачем |
|-------|------------------|------------|------------------|--------|
| Product Lead | `pm` | CEO / Board | редкий (30–60 мин), только WIP-страж | Не пишет фичи параллельно Discovery |
| Discovery | `pm` | Product Lead | **ACTIVE** на W1 | Поле, карточки сигнала, патч H1/H4/H5 |
| UX Designer | `designer` | Product Lead | **paused** | Wake после merge UX-PR или сигнала usable |
| Delivery Engineer | `engineer` | Product Lead | **paused** | Wake на поставку Git→Notion после CEO-OK |
| Growth Lead | `general` | Product Lead | **paused** | Wake на W3 / эксперимент A — не B/C сразу |
| Researcher | — | — | **не нанимать отдельно** | После ≥3 карточек Discovery зовёт патч evidence; иначе дубль |

ИИ-CEO (`ceo`, `reportsTo: null`) — **только если** нужен org-root в Paperclip. Capabilities: ICP-гейты, approve hire, не feature-прогон.

Бюджет старта (рекомендация Paperclip $100–500/агент/мес): CEO $400, Product Lead $300, остальные $200. Компания: не раздувать, пока нет ключа и живого heartbeat.

---

## 6. Как нанять, когда появится API

1. В Cloud env: `PAPERCLIP_API_KEY` + опционально `PAPERCLIP_API_BASE_URL` (`https://paperclip.inc` или `http://127.0.0.1:3100`).
2. `python3 scripts/paperclip_hire_product_team.py` — идемпотентно: list agents → create missing → pause HOLD.
3. Company goal создать/привязать (см. JSON `companyGoal`).
4. **Не** `wakeup` всей команды. Wake: Discovery на PRO-3; Product Lead — только если слот WIP нарушен.
5. Hire Researcher / CTO / CMO — отклонять.

Payloads: [`docs/paperclip-hires.json`](../paperclip-hires.json).

---

## 7. Антипаттерны, которые уже случились

1. Разбудить Product Lead + Discovery + Researcher + UX + Delivery + Growth **в одном прогоне**.
2. Несколько recovery Product Lead → дубли PR #42/#43/#44.
3. Путать «агент существует» с «агент имеет свой ACTIVE outcome».
4. Дефолтный org Paperclip (CEO→CTO/CMO/CFO) вместо одной product team.

---

## 8. Перенос в Notion

**Ничего из этого файла в пользовательский шаблон не переносить.**

WIP-цифры для людей уже живут / поедут в Активность (#22): 1–3 гипотезы, 1–3 цели. Org агентов — внутренняя операционка.

---

## История

| Дата | Изменение |
|------|-----------|
| 2026-08-16 | Аудит существующих Paperclip-ролей + найм как Cagan-команда + точные WIP-лимиты |
