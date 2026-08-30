# Child — GrowthMarketer: UTM + 3 теста (+ бэклог→100)

## Статус бэклога
Список **~100** под нишу `solo-digital-services` уже в `Маркетинг/100-тестов-бэклог.md`.  
В срезе цикла 2: запустить **ровно 3** (см. таблицу внизу файла бэклога) после публичного URL.

## Гипотеза (viable)
Бесплатные value-first размещения с UTM дадут первые `map_viewed`; каналы отделим в PostHog по `utm_content`.

## Срез
1. URL map есть: `https://vikiswaimer.github.io/Prod.Swaim.com/`
2. UTM: `utm_campaign=toolmap_solo_ds` + `utm_content` на каждый тест.
3. Запустить **ровно 3** value-first теста.
4. Лог в dogfood: `Маркетинг/3-utm-теста-solo-digital-services.md`

## Done
3 теста `running` или `learned`. Не покупать рекламу. Live publish только value-first.

## Помощь
Не выдумывать трафик и не тащить новые каналы сверх 3 WIP.
