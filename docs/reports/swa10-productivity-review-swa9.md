# SWA-10 — Review productivity for SWA-9

**Дата:** 2026-08-15 · **Роль:** Product Lead · **Paperclip:** SWA-10  
**Объект:** Paperclip **SWA-9** («следующий шаг после risk-map, только Product Lead»)  
**Компас:** исходы > фичи · Ries (движение ≠ прогресс) · WIP=1

> Внутренний review. Не переносить в пользовательский Notion.  
> Не путать с Linear SWA-9 (PRD Swaim Browser) — другой продукт.

---

## Вердикт

| Поле | Значение |
|------|----------|
| **Outcome SWA-9** | **ACCEPT** — координационное решение принято и зафиксировано |
| **Продуктивность смысла** | Высокая: после risk-map сжали WIP ≤3 → **WIP=1 = W1 Mom Test** |
| **Продуктивность процесса** | Низкая: параллельные heartbeats → 3 одинаковых draft PR |
| **Retry SWA-9** | **Нет** |
| **Новый PL-документ / feature-wake** | **Нет** |
| **Следующий шаг команды** | Discovery **PRO-3** + CEO-рекрут (поле), не ещё один sync |

---

## Что проверяли

1. Был ли у SWA-9 ясный assignment recovery goal?
2. Появился ли проверяемый deliverable (не «агент поработал»)?
3. Совпадает ли решение с методологией (valuable-first, Mom Test, WIP)?
4. Не открыли ли параллельный feature-прогон?
5. Что делать с дублями артефактов?

---

## Evidence

| Критерий | Факт |
|----------|------|
| Goal SWA-9 | Assignment recovery: next step после risk-map / SWA-3, только PL |
| Decision | ACTIVE = W1 Mom Test → H1/H4/H5; W2 (#22) / W3 smoke = HOLD |
| Memo | [`swa9-next-after-risk-map.md`](swa9-next-after-risk-map.md) |
| Risk-map §8 | WIP-пул схлопнут до 1 в [`risk-map-hypotheses.md`](../risk-map-hypotheses.md) |
| Исполнение вне тикета | Linear [PRO-2](https://linear.app/swaim/issue/PRO-2) / [PRO-3](https://linear.app/swaim/issue/PRO-3) + [`w1-mom-test-brief.md`](w1-mom-test-brief.md) |
| Не делали | правки Notion-шаблона, лендинг, повторный Researcher, merge пачкой |

Почему решение верное: evidence pack (SWA-8 / PR #37) уже сказал, что архетипы ≠ validated demand. Самый дорогой риск — **valuable**, не usable-модули.

---

## Thrashing (процесс, не смысл)

Параллельные Paperclip PL heartbeats на один assignment:

| PR | Ветка | Заметка |
|----|-------|---------|
| [#42](https://github.com/vikiswaimer/Prod.Swaim.com/pull/42) | `cursor/pl-swa9-wip-lock-db02` | тот же LOCK |
| [#43](https://github.com/vikiswaimer/Prod.Swaim.com/pull/43) | `cursor/swa9-wip1-after-riskmap-4393` | тот же LOCK, другой filename memo |
| [#44](https://github.com/vikiswaimer/Prod.Swaim.com/pull/44) | `cursor/pl-swa9-wip1-after-riskmap-2647` | тот же LOCK **+** risk-map в tip |

Решение в трёх PR **идентично**. Шум — дубли веток/комментов в Linear, не смена курса.

**Канон для merge:** **#44** (самый полный tip: sync + SWA-9 memo + risk-map §8).  
**Закрыть как duplicate:** #42, #43 (и более ранние PL sync #40/#41 после rebase/merge #44).

Не открывать четвёртый «ещё один SWA-9».

---

## Root cause stranded board

1. `PAPERCLIP_API_URL` → `127.0.0.1:3101` из cloud = connection refused.  
2. Нет инжектированного `PAPERCLIP_API_KEY` / reachable base URL.  
3. Heartbeats не сериализованы → storm параллельных PL-runs.

Координация до bridge: GitHub draft PR + Linear PRO-2 + этот sync. На доске Paperclip SWA-9 / SWA-10 → `done` вручную, когда API жив.

---

## Действия после review (чеклист)

- [x] Вердикт ACCEPT записан (этот файл)
- [ ] CEO/владелец: merge **#44** (или rebase #44 на main), close #42/#43 as duplicate
- [ ] Paperclip: SWA-9 → `done`, SWA-10 → `done` (вручную при живом bridge)
- [ ] Discovery: только PRO-3 / полевой brief — без новых JTBD-страниц
- [ ] Не спавнить новые PL cloud-agents под тот же heartbeat
- [ ] Env: ключ + reachable Paperclip API (запрошено в cloud setup actions)

---

## Когда снова нужен Product Lead

После ≥3–5 карточек Mom Test-сигнала: pivot/persevere ICP, открытие W2/W3, патч risk-map. Не раньше и не параллельным feature-wake.

---

## История

| Дата | Изменение |
|------|-----------|
| 2026-08-15 | SWA-10: ACCEPT SWA-9; канон merge #44; дубли #42/#43; WIP остаётся W1 |
