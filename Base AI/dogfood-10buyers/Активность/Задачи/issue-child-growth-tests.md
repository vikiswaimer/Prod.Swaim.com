# Child — GrowthMarketer: UTM + 3 теста (+ бэклог→100)

## Статус бэклога
Список **~100** под нишу `solo-digital-services` уже в `Маркетинг/100-тестов-бэклог.md`.  
В этом срезе держим **ровно 3** теста и один общий критерий решения.

## Гипотеза (viable)
Верим, что **соло-специалисты digital-услуг**, которые уже собирают стек вручную, теряют время на списках сервисов без порядка внедрения.  
Если дать им **бесплатную карту ниши + платный плейбук за $60**, то хотя бы один из трёх честных value-first тестов даст **`paid_cta_clicked`** из кампании `toolmap_solo_ds`.

## Один эксперимент и одна метрика
- **Эксперимент:** три дешёвых value-first размещения с разным углом входа, но с одним оффером.
- **Главная метрика:** `paid_cta_clicked` по `utm_campaign=toolmap_solo_ds` с разбивкой по `utm_content`.
- `map_viewed` используем как диагностический сигнал дистрибуции, но не как критерий keep.

## 3 теста в этом цикле

| # | Канал / тест | `utm_content` | Угол сообщения | Статус |
|---|---|---|---|---|
| 14 | Telegram no-code / solo-business чат | `tg_nocode_value` | «Вот карта связок для соло-услуг: меньше сравнений, быстрее собрать рабочий стек» | ready |
| 29 | LinkedIn пост про связку | `li_notion_tg` | «Notion + Telegram — не два инструмента, а один рабочий поток» | ready |
| 41 | Dogfood-кейс «как собрал стек за вечер» | `dogfood_stack_evening` | «Не топ-50 SaaS, а конкретная связка под один сценарий» | ready |

## Срез
1. UTM: `utm_campaign=toolmap_solo_ds`.
2. Один оффер на всех каналах: free map → paid playbook `$60`.
3. После первых кликов смотрим не на комплименты, а на `paid_cta_clicked`.
4. Если есть `map_viewed`, но нет `paid_cta_clicked`, меняем copy/offer раньше, чем добавляем новые каналы.

## Лог для PO: keep / iterate / kill

| `utm_content` | `map_viewed` | `paid_cta_clicked` | Решение | Что узнали |
|---|---:|---:|---|---|
| `tg_nocode_value` | 0 | 0 | pending | Ждём запуска board/PO |
| `li_notion_tg` | 0 | 0 | pending | Ждём запуска board/PO |
| `dogfood_stack_evening` | 0 | 0 | pending | Ждём запуска board/PO |

## Done
Готово к запуску: 3 теста, один оффер, одна главная метрика, лог keep/iterate/kill.  
Live publish и перевод статусов в `running` / `learned` — только с ок board/PO.

## Помощь
Нет board/PO ok на live publish — не помечать тесты как `running`, не выдумывать трафик.
