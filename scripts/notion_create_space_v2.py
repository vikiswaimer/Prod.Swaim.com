#!/usr/bin/env python3
"""Создать в конце корня SBS страницу «Пространство v2» + 6 групп.

  python3 scripts/notion_create_space_v2.py --dry-run
  python3 scripts/notion_create_space_v2.py --apply

Не трогает существующие модули v1 — только добавляет контейнер в конец.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import notion_client as nc  # noqa: E402

ROOT_DEFAULT = "dcf207ca-d379-82b8-9fa8-013434ecd77f"
REPORT_PATH = Path("docs/reports/notion-space-v2-page-map.json")
PARENT_TITLE = "Пространство v2 (черновик)"


def rt(text: str, **ann) -> list[dict]:
    return nc.rich(text, **ann)


def blocks_intro() -> list[dict]:
    return [
        nc.callout(
            "Отдельный каркас для фаундеров / PM / предпринимателей. "
            "Не заменяет модули v1 — лежит в конце, чтобы тестировать проще.",
            emoji="🧪",
        ),
        nc.heading(2, "Зачем"),
        nc.bulleted("Мало поверхностей — больше ясности"),
        nc.bulleted("Один маршрут дня: Сейчас → Продукт → Клиенты → Рост → Деньги → База"),
        nc.bulleted("Статусы везде одинаковые: сейчас / потом / стоп"),
        nc.heading(2, "Как пользоваться (2 минуты)"),
        nc.numbered("Откройте «Сейчас» — это домашняя страница"),
        nc.numbered("Держите 1–3 цели на неделю, не больше"),
        nc.numbered("Остальное заполняйте по мере боли, не «на будущее»"),
        nc.divider(),
        nc.heading(2, "Группы"),
        nc.paragraph("Ниже — шесть страниц. Начните с «Сейчас»."),
    ]


def blocks_now() -> list[dict]:
    return [
        nc.callout(
            "Домашняя страница. Открыли → за 30 секунд поняли состояние.",
            emoji="🏠",
        ),
        nc.heading(2, "Фокус недели"),
        nc.paragraph("Максимум 1–3 цели. Если больше — это уже не фокус."),
        nc.to_do("Цель 1: …"),
        nc.to_do("Цель 2: …"),
        nc.to_do("Цель 3 (опционально): …"),
        nc.quote("Вопрос-проверка: если успею только одно — что это?"),
        nc.heading(2, "Сегодня"),
        nc.paragraph("3–5 задач, которые двигают фокус недели."),
        nc.to_do("…"),
        nc.to_do("…"),
        nc.to_do("…"),
        nc.heading(2, "Сигналы"),
        nc.paragraph("Что горит или выглядит странно (баги, жалобы, касса, лиды)."),
        nc.bulleted("🔴 … — что сделаю: …"),
        nc.bulleted("🟡 … — что сделаю: …"),
        nc.heading(2, "Решения недели"),
        nc.bulleted("Дата — решение — почему так"),
    ]


def blocks_product() -> list[dict]:
    return [
        nc.callout("Что строим и зачем — без дорожной карты на год.", emoji="🎯"),
        nc.heading(2, "Для кого"),
        nc.bulleted("Кто клиент: …"),
        nc.bulleted("Какая боль / работа: …"),
        nc.bulleted("Чем пользуются сейчас вместо нас: …"),
        nc.bulleted("Почему могут выбрать нас: …"),
        nc.heading(2, "Гипотезы"),
        nc.paragraph("Только то, что проверяем сейчас (не каталог идей)."),
        nc.bulleted("Гипотеза → как проверим → сигнал успеха → статус"),
        nc.heading(2, "Бэклог"),
        nc.bulleted("Идея → зачем клиенту → сейчас / потом / стоп"),
        nc.quote("В «сейчас» одновременно мало пунктов. Остальное — потом или стоп."),
        nc.heading(2, "Релизы"),
        nc.bulleted("Дата — что вышло — чему научились — что дальше"),
    ]


def blocks_customers() -> list[dict]:
    return [
        nc.callout("CRM-лайт: статусы и смысл разговоров, не Salesforce.", emoji="👥"),
        nc.heading(2, "Воронка"),
        nc.bulleted("Имя — статус (лид / разговор / оффер / оплата / пауза) — следующий шаг"),
        nc.heading(2, "Разговоры"),
        nc.paragraph("Факты и поведение важнее комплиментов."),
        nc.bulleted("С кем / контекст"),
        nc.bulleted("Что пробовали раньше"),
        nc.bulleted("Что болит и сколько стоит проблема"),
        nc.bulleted("Что сделают дальше (их слова)"),
        nc.bulleted("Мой вывод: сигнал / шум / нужно ещё проверить"),
        nc.heading(2, "Обратная связь"),
        nc.bulleted("Дата — источник — цитата/запрос — что меняем (или ничего пока)"),
    ]


def blocks_growth() -> list[dict]:
    return [
        nc.callout(
            "Рост = эксперименты с результатом, не контент-план ради галочки.",
            emoji="📣",
        ),
        nc.heading(2, "Каналы"),
        nc.bulleted("Канал — зачем пробуем — пробуем / работает / стоп — вывод"),
        nc.heading(2, "Касания"),
        nc.bulleted("Касание — канал — черновик / отправлено / разобрать"),
        nc.heading(2, "Эксперименты"),
        nc.bulleted("Гипотеза — действие — срок — результат — усилить / повторить / стоп"),
    ]


def blocks_money() -> list[dict]:
    return [
        nc.callout("Три понятные цифры важнее тридцати отчётов.", emoji="💰"),
        nc.heading(2, "Снимок месяца"),
        nc.bulleted("Пришло: …"),
        nc.bulleted("Ушло: …"),
        nc.bulleted("Остаток / runway: …"),
        nc.paragraph("Короткий вывод недели: …"),
        nc.heading(2, "Цены и офферы"),
        nc.bulleted("Оффер — для кого — цена — что входит — продаём / тест / стоп"),
        nc.heading(2, "Риски"),
        nc.bulleted("Риск — насколько близко — что сделаю"),
    ]


def blocks_base() -> list[dict]:
    return [
        nc.callout(
            "Память пространства. Растёт медленно. Сюда не сваливаем всё подряд.",
            emoji="🧠",
        ),
        nc.heading(2, "Как работаем"),
        nc.bulleted("Понедельник: обзор «Сейчас» + фокус недели"),
        nc.bulleted("Середина недели: сигналы и воронка"),
        nc.bulleted("Конец недели: решения + чему научились"),
        nc.bulleted("Релиз: короткий вывод в Продукт → Релизы"),
        nc.heading(2, "Шаблоны"),
        nc.numbered("Оффер — кто / боль / обещание / цена / что входит"),
        nc.numbered("Интервью — см. Разговоры в Клиентах"),
        nc.numbered("Касание — одна мысль, один CTA, один канал"),
        nc.numbered("Чек-лист запуска — что должно работать до показа людям"),
        nc.heading(2, "Решения «как у нас принято»"),
        nc.bulleted("Как выбираем работу: фокус недели > срочные мелочи"),
        nc.bulleted("Когда стопаем идею: нет сигнала от людей / нет связи с фокусом"),
        nc.bulleted(
            "Что считаем релизом: люди получают ценность (лучше — платят)"
        ),
    ]


GROUPS = [
    ("Сейчас", "🏠", blocks_now),
    ("Продукт", "🎯", blocks_product),
    ("Клиенты", "👥", blocks_customers),
    ("Рост", "📣", blocks_growth),
    ("Деньги", "💰", blocks_money),
    ("База", "🧠", blocks_base),
]


def find_existing(token: str, parent_id: str, title: str) -> str | None:
    for b in nc.get_block_children(token, parent_id):
        if b.get("type") == "child_page" and (b.get("child_page") or {}).get("title") == title:
            return b["id"]
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=ROOT_DEFAULT)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not args.apply and not args.dry_run:
        args.dry_run = True

    token = nc.get_token()
    root = args.root

    plan = {
        "root_page_id": root,
        "parent_title": PARENT_TITLE,
        "groups": [{"title": t, "emoji": e} for t, e, _ in GROUPS],
    }
    print(json.dumps(plan, ensure_ascii=False, indent=2))

    if args.dry_run and not args.apply:
        print("\nDry-run only. Передайте --apply для создания в Notion.")
        return 0

    # Маркер секции в конце корня (текст), затем контейнер-страница
    existing = find_existing(token, root, PARENT_TITLE)
    if existing:
        print(f"Уже есть «{PARENT_TITLE}»: {existing}")
        print("Повторно не создаём. Удалите страницу вручную, если нужен чистый прогон.")
        return 1

    nc.append_children(
        token,
        root,
        [
            nc.divider(),
            nc.heading(2, "Пространство v2 (черновик)"),
            nc.paragraph(
                "Новый каркас для теста: Сейчас · Продукт · Клиенты · Рост · Деньги · База. "
                "Не заменяет модули выше — лежит отдельно."
            ),
        ],
    )

    parent = nc.create_page(
        token,
        parent_page_id=root,
        title=PARENT_TITLE,
        icon_emoji="🧪",
        children=blocks_intro(),
    )
    parent_id = parent["id"]
    print(f"Parent: {PARENT_TITLE} → {parent_id}")
    print(f"URL: {nc.notion_page_url(parent_id)}")

    pages: dict[str, str] = {PARENT_TITLE: parent_id}
    for title, emoji, builder in GROUPS:
        page = nc.create_page(
            token,
            parent_page_id=parent_id,
            title=title,
            icon_emoji=emoji,
            children=builder(),
        )
        pages[title] = page["id"]
        print(f"  + {emoji} {title} → {page['id']}")

    report = {
        "issue": 28,
        "root_page_id": root,
        "parent_title": PARENT_TITLE,
        "parent_page_id": parent_id,
        "parent_url": nc.notion_page_url(parent_id),
        "pages": pages,
        "git_path": "content/small-business-space-ru/Пространство-v2/",
    }
    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"\nSaved {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
