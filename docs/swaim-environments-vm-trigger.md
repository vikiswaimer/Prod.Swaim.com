# Swaim Environments + VM (триггер)

**Статус:** не активно. Открыть отдельный issue, когда дойдём до **сайта на VM**, **агента на сервере** (сбор данных, nginx, почта, деплой, логи).

## Суть (1 абзац)

**Environments** в Swaim/Paperclip = *где выполняется агент* (Local / SSH / Sandbox), не «где лежит сайт». Сайт на VM обычно деплоит **CI**; Environments нужны, если агент **сам заходит на VM** (деплой, конфиги, healthcheck, почта). Сейчас для правок `content/` в Git — **не включать**.

## Когда включать

- SSH environment на VM + override агента «деплой/инфра»
- Sandbox + custom image, если долгий setup toolchain на каждый run
- Цепочка: override агента → default instance → Local

## Включение

Settings → Instance settings → **Experimental** → **Enable Environments** → Environments → Add (SSH/Sandbox).

Дока: https://docs.paperclip.ing/experimental/environments.md

## Границы Prod.Swaim

Лендинг и маркетинг — **отдельный** контур/issue ([`AGENTS.md`](../AGENTS.md)). Шаблон Notion — этот репо.
