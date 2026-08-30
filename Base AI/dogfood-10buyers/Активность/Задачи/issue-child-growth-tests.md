# Child — GrowthMarketer: UTM + 3 теста (+ бэклог→100)

## Статус бэклога
Список **~100** под нишу `solo-digital-services` уже в `Маркетинг/100-тестов-бэклог.md`.  
В срезе цикла 2: держать **ровно 3** в `running`; новые не добавлять, пока не появится `learned`.

## Гипотеза (viable)
Верим, что **соло-специалисты в digital, которые уже сами собирают стек**, чаще откроют map,
если оффер обещает **рабочие связки под нишу**, а не очередной список сервисов.

## Дешёвый эксперимент
Три органических размещения с одним и тем же оффером и разным `utm_content`:

| Тест | Канал | `utm_content` | Статус |
|------|-------|---------------|--------|
| 14 | Telegram no-code / solo-business чат | `tg_nocode_value` | `running` |
| 29 | LinkedIn пост про связку Notion ↔ Telegram | `li_notion_tg` | `running` |
| 34 | SEO-заметка «стек фрилансера-маркетолога» | `seo_freelancer_stack` | `running` |

## Метрика
Главная метрика цикла: **`map_viewed` по `utm_content`**.  
`paid_cta_clicked` — квалифицирующий сигнал спроса, но не главная метрика этого heartbeat.

## Что изменено в артефактах
1. `toolmap/landing/` — copy переписан под покупателя: кто и что меняется.
2. `toolmap/landing/index.html` — default route ведёт на landing A.
3. `toolmap/` — UTM сохраняются через landing → map → playbook, чтобы PO видел сигнал по тесту.
4. `Маркетинг/100-тестов-бэклог.md` — ровно 3 теста переведены в `running`.

## Проверка
- Browser test: `tg_nocode_value`, `li_notion_tg`, `seo_freelancer_stack` прошли путь `landing A → map → playbook`.
- Во всех 3 сценариях сохранились `utm_campaign=toolmap_solo_ds` и соответствующий `utm_content`.
- PostHog SDK грузится, но backend requests для анонимного трафика не уходят.

## CRITICAL
Реальный PostHog backend-signal для публичного anonymous traffic **заблокирован внешней настройкой проекта**:
- remote config PostHog возвращает `defaultIdentifiedOnly: true`;
- из-за этого `landing_viewed`, `map_viewed` и `paid_cta_clicked` не отправляются на backend для анонимного пользователя;
- локальный код уже усилен (`person_profiles: "always"` + `bootstrap.defaultIdentifiedOnly = false`), но blocker остаётся вне репозитория.

**Owner unblock:** PO / PostHog admin.  
**Action unblock:** выключить режим identified-only в настройках проекта PostHog и повторить 3 UTM-теста после обновления remote config.

## Одна сильная идея
Если первые `map_viewed` придут, следующий тест делать не про “tool map вообще”, а про **одну конкретную связку с прошлым поведением**:
`Notion ↔ Telegram для соло digital-услуг` как более узкое обещание, чем общий каталог стека.

## Done
Готово, когда 3 теста в `running`, оффер на лендинге говорит с нишей напрямую, `map_viewed` не теряет UTM и PostHog принимает anonymous events.

## Помощь
Live publish и реальные размещения — только через board / PO. Не выдумывать внешний запуск.
