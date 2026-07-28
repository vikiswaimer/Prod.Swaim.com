#!/usr/bin/env python3
"""Синхронизация группы Бизнес в живую копию SBS (issue #24).

  python3 scripts/notion_sync_business.py --dry-run
  python3 scripts/notion_sync_business.py --apply
  python3 scripts/notion_sync_business.py --apply --only hubs
  python3 scripts/notion_sync_business.py --apply --only dbs
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import notion_client as nc  # noqa: E402
import notion_sync_pilot as pilot  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content/small-business-space-ru"
PAGE_MAP = ROOT / "docs/reports/notion-sbs-page-map.json"

BUSINESS_SECTION_DB = "279207ca-d379-82b8-be8e-8177d914578b"

HUBS = {
    "Твой продукт": {
        "page_id": "569207ca-d379-82e0-8734-816a22514351",
        "md": CONTENT / "Бизнес/Твой продукт--5ac1cda1.md",
        "description": "Ценность, гипотеза, минимальный полезный срез, риск",
        "keep_db": False,
        "db_id": None,
    },
    "Клиенты": {
        "page_id": "3f3207ca-d379-8390-9851-01d7d8b26890",
        "md": CONTENT / "Бизнес/Клиенты--ee4c1042.md",
        "description": "Сегмент через поведение, боль, workaround, сигнал",
        "keep_db": True,
        "db_id": "0f7207ca-d379-833e-a441-01dd3aabf724",
        "db_title": "Портрет сегмента",
    },
    "Продукты/Услуги": {
        "page_id": "f6f207ca-d379-829d-9967-81d11cfb9822",
        "md": CONTENT / "Бизнес/Продукты Услуги--4bbcfa4e.md",
        "description": "Оффер: для кого, scope, цена, статус проверки",
        "keep_db": True,
        "db_id": "35b207ca-d379-822c-9332-016f730f13da",
        "db_title": "Продукты и услуги",
    },
    "Конкуренты": {
        "page_id": "35b207ca-d379-835c-9758-016bbc0fa248",
        "md": CONTENT / "Бизнес/Конкуренты--b7cd0ad7.md",
        "description": "Прямые / косвенные / status quo через outcomes",
        "keep_db": True,
        "db_id": "fc7207ca-d379-8327-b109-0109471562d9",
        "db_title": "Конкуренты и альтернативы",
    },
    "Маркетинг": {
        "page_id": "669207ca-d379-8215-8aa4-0126aeb2a2c2",
        "md": CONTENT / "Бизнес/Маркетинг--62b1f924.md",
        "description": "Стратегия: 1–2 канала и действие (не операционка)",
        "keep_db": True,
        "db_id": "1e1207ca-d379-82cd-8df3-81ab9c043d6f",
        "db_title": "Каналы маркетинга",
    },
    "Необходимые шаги": {
        "page_id": "9db207ca-d379-83be-a6ca-01a1943ec547",
        "md": CONTENT / "Бизнес/Необходимые шаги--34c60f4e.md",
        "description": "Must-have до ценного среза / nice / не сейчас",
        "keep_db": True,
        "db_id": "792207ca-d379-83bd-9d3a-012d7aba7b8b",
        "db_title": "Шаги к срезу",
    },
}

TRACK_START = {
    "page_id": "9b0207ca-d379-8305-9d71-013fc7eb2fd7",
    "md": CONTENT / "Быстрый старт/Старт своего бизнеса--66c3ee00.md",
}

# Demo / template page ids inside DBs
DEMO_PAGES = {
    "sasha": "33c207ca-d379-83c1-aed7-01b332523ff8",
    "notion": "ee7207ca-d379-8362-a1b6-0164309e4f03",
    "miro": "b19207ca-d379-8289-b079-81d909ffb457",
}


def log(msg: str) -> None:
    print(msg, flush=True)


def tables_to_bullets(md: str) -> str:
    """Notion API: markdown tables → readable bullet blocks."""
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if (
            "|" in line
            and i + 1 < len(lines)
            and re.match(r"^\s*\|?\s*[-:| ]+\|[-:| ]+$", lines[i + 1])
        ):
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            while i < len(lines) and "|" in lines[i] and not lines[i].strip().startswith("#"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if len(cells) == len(header):
                    parts = [f"**{h}:** {c}" for h, c in zip(header, cells) if c and c != "—"]
                    if parts:
                        out.append("- " + " · ".join(parts))
                i += 1
            out.append("")
            continue
        out.append(line)
        i += 1
    return "\n".join(out)


def prepare_md(md: str) -> str:
    md = re.sub(r"^#\s+[^\n]+\n+", "", md, count=1)
    # CSV / examples links → plain or drop
    md = re.sub(r"\[([^\]]+)\]\(([^)]+\.csv)\)", r"\1 (таблица на этой странице)", md)
    md = re.sub(r"\[([^\]]+)\]\(([^)]*examples/[^)]+)\)", r"\1", md)
    md = re.sub(r"\[[^\]]*\]\([^)]+\.csv\)\s*\n?", "", md)
    # relative md links to child records — keep label only if not in page map
    md = tables_to_bullets(md)
    md = re.sub(r"</?b>", "", md, flags=re.I)
    md = re.sub(r"</?strong>", "", md, flags=re.I)
    return md.strip() + "\n"


def clear_keep_db(token: str, page_id: str) -> tuple[int, int]:
    kids = nc.get_block_children(token, page_id)
    kept = deleted = 0
    for b in kids:
        if b.get("type") == "child_database":
            kept += 1
            continue
        nc.delete_block(token, b["id"])
        deleted += 1
        time.sleep(0.3)
    return deleted, kept


def set_section_description(token: str, page_id: str, description: str) -> None:
    nc._request(
        "PATCH",
        f"/pages/{page_id}",
        token,
        body={
            "properties": {
                "Описание": {
                    "rich_text": [
                        {"type": "text", "text": {"content": description[:2000]}}
                    ]
                }
            }
        },
    )
    time.sleep(0.3)


def rename_database(token: str, db_id: str, title: str) -> None:
    nc._request(
        "PATCH",
        f"/databases/{db_id}",
        token,
        body={"title": [{"type": "text", "text": {"content": title}}]},
    )
    time.sleep(0.35)


def ensure_props(token: str, db_id: str, props: dict) -> None:
    """Add missing properties (skip existing names)."""
    db = nc._request("GET", f"/databases/{db_id}", token)
    existing = set((db.get("properties") or {}).keys())
    to_add = {k: v for k, v in props.items() if k not in existing}
    if not to_add:
        log(f"  props ok ({len(existing)} existing)")
        return
    nc._request(
        "PATCH",
        f"/databases/{db_id}",
        token,
        body={"properties": to_add},
    )
    log(f"  added props: {', '.join(to_add)}")
    time.sleep(0.4)


def rich_prop(text: str) -> dict:
    return {"rich_text": [{"type": "text", "text": {"content": text[:2000]}}]}


def select_prop(name: str) -> dict:
    return {"select": {"name": name}}


def write_page_body(
    token: str,
    *,
    page_id: str,
    md_path: Path,
    pages: dict[str, str],
    keep_db: bool,
    apply: bool,
    note_before_db: str | None = None,
) -> int:
    md = prepare_md(md_path.read_text(encoding="utf-8"))
    if keep_db and note_before_db:
        # Put a short note; DB stays on page (order: we clear non-db, append guide;
        # Notion may leave DB at top — OK with callout tip)
        md = note_before_db + "\n\n" + md
    blocks = pilot.md_to_blocks(
        md,
        assets_dir=None,
        token=token if apply else None,
        upload=False,
        pages=pages,
        nest_aside_images=False,
    )
    log(f"  blocks={len(blocks)}")
    for line in nc.summarize_blocks(blocks)[:12]:
        log(f"    {line}")
    if len(blocks) > 12:
        log(f"    ... +{len(blocks) - 12}")
    if not apply:
        log("  DRY-RUN")
        return len(blocks)
    if keep_db:
        d, k = clear_keep_db(token, page_id)
        log(f"  cleared {d}, kept db={k}")
    else:
        n = nc.clear_page_blocks(token, page_id)
        log(f"  cleared all {n}")
    nc.append_children(token, page_id, blocks)
    page = nc.get_page(token, page_id)
    log(f"  OK → {page.get('url')}")
    return len(blocks)


def sync_hubs(token: str, pages: dict[str, str], apply: bool) -> None:
    for title, cfg in HUBS.items():
        log(f"\n## Hub: {title}")
        note = None
        if cfg["keep_db"]:
            note = (
                "> Рабочая таблица раздела — на этой странице "
                "(при необходимости перетащите под гайд)."
            )
        write_page_body(
            token,
            page_id=cfg["page_id"],
            md_path=cfg["md"],
            pages=pages,
            keep_db=cfg["keep_db"],
            apply=apply,
            note_before_db=note,
        )
        if apply:
            set_section_description(token, cfg["page_id"], cfg["description"])
            log(f"  section Описание updated")


def sync_track_start(token: str, pages: dict[str, str], apply: bool) -> None:
    log("\n## Track: Старт своего бизнеса")
    write_page_body(
        token,
        page_id=TRACK_START["page_id"],
        md_path=TRACK_START["md"],
        pages=pages,
        keep_db=False,
        apply=apply,
    )


def sync_db_schemas(token: str, apply: bool) -> None:
    log("\n## DB schemas")
    if not apply:
        log("DRY-RUN: would add props + rename DBs")
        return

    # Portrait
    pid = HUBS["Клиенты"]["db_id"]
    rename_database(token, pid, HUBS["Клиенты"]["db_title"])
    ensure_props(
        token,
        pid,
        {
            "Контекст": {"rich_text": {}},
            "Боль": {"rich_text": {}},
            "Workaround": {"rich_text": {}},
            "Что пробовали": {"rich_text": {}},
            "Обязательства": {"rich_text": {}},
            "Доказательства": {
                "select": {
                    "options": [
                        {"name": "гипотеза", "color": "yellow"},
                        {"name": "частично", "color": "orange"},
                        {"name": "подтверждено", "color": "green"},
                    ]
                }
            },
        },
    )

    # Offer
    oid = HUBS["Продукты/Услуги"]["db_id"]
    rename_database(token, oid, HUBS["Продукты/Услуги"]["db_title"])
    ensure_props(
        token,
        oid,
        {
            "Сегмент": {"rich_text": {}},
            "Проблема / исход": {"rich_text": {}},
            "Входит": {"rich_text": {}},
            "Не входит": {"rich_text": {}},
            "Доказательства": {"rich_text": {}},
            "Статус проверки": {
                "select": {
                    "options": [
                        {"name": "гипотеза", "color": "yellow"},
                        {"name": "пробуют", "color": "blue"},
                        {"name": "платят", "color": "green"},
                        {"name": "пауза", "color": "gray"},
                        {"name": "архив", "color": "default"},
                    ]
                }
            },
        },
    )

    # Competitors
    cid = HUBS["Конкуренты"]["db_id"]
    rename_database(token, cid, HUBS["Конкуренты"]["db_title"])
    ensure_props(
        token,
        cid,
        {
            "Тип": {
                "select": {
                    "options": [
                        {"name": "прямая", "color": "red"},
                        {"name": "косвенная", "color": "orange"},
                        {"name": "status quo", "color": "gray"},
                    ]
                }
            },
            "Outcome": {"rich_text": {}},
            "Уже платят": {"rich_text": {}},
            "Почему переключатся": {"rich_text": {}},
            "Где мы проигрываем": {"rich_text": {}},
            "Сильные": {"rich_text": {}},
            "Слабые": {"rich_text": {}},
        },
    )

    # Must-have items
    iid = HUBS["Необходимые шаги"]["db_id"]
    rename_database(token, iid, HUBS["Необходимые шаги"]["db_title"])
    ensure_props(
        token,
        iid,
        {
            "Категория": {
                "select": {
                    "options": [
                        {"name": "До ценного среза", "color": "green"},
                        {"name": "Nice-to-have", "color": "yellow"},
                        {"name": "Не сейчас", "color": "gray"},
                    ]
                }
            },
            "Риск": {"rich_text": {}},
            "Статус": {
                "select": {
                    "options": [
                        {"name": "todo", "color": "blue"},
                        {"name": "doing", "color": "orange"},
                        {"name": "done", "color": "green"},
                        {"name": "later", "color": "gray"},
                    ]
                }
            },
        },
    )

    mid = HUBS["Маркетинг"]["db_id"]
    rename_database(token, mid, HUBS["Маркетинг"]["db_title"])


def replace_page_from_md(
    token: str, page_id: str, md_path: Path, pages: dict[str, str], apply: bool
) -> None:
    md = prepare_md(md_path.read_text(encoding="utf-8"))
    blocks = pilot.md_to_blocks(
        md,
        assets_dir=None,
        token=token if apply else None,
        upload=False,
        pages=pages,
        nest_aside_images=False,
    )
    log(f"  demo {md_path.name}: blocks={len(blocks)}")
    if not apply:
        return
    n = nc.clear_page_blocks(token, page_id)
    log(f"  cleared {n}")
    nc.append_children(token, page_id, blocks)


def sync_demo_rows(token: str, pages: dict[str, str], apply: bool) -> None:
    log("\n## Demo rows")
    # Sasha
    replace_page_from_md(
        token,
        DEMO_PAGES["sasha"],
        CONTENT / "Бизнес/Клиенты/Протрет пользователя/Саша--64d63e56.md",
        pages,
        apply,
    )
    if apply:
        nc._request(
            "PATCH",
            f"/pages/{DEMO_PAGES['sasha']}",
            token,
            body={
                "properties": {
                    "Name": {
                        "title": [
                            {
                                "type": "text",
                                "text": {"content": "Саша (демо)"},
                            }
                        ]
                    },
                    "Контекст": rich_prop(
                        "Основатель цифрового продукта на старте / соло"
                    ),
                    "Боль": rich_prop(
                        "Недели на сбор структуры вместо разговора с клиентами"
                    ),
                    "Workaround": rich_prop("Самосбор баз + советы из Twitter/чатов"),
                    "Что пробовали": rich_prop(
                        "Пустые шаблоны и чужие OS — бросала через 1–2 недели"
                    ),
                    "Обязательства": rich_prop(
                        "Пока гипотеза — проверить разговорами"
                    ),
                    "Доказательства": select_prop("гипотеза"),
                    "Occupation": rich_prop("Владелец цифрового продукта"),
                }
            },
        )
        time.sleep(0.35)

    # Competitors Notion / Miro
    replace_page_from_md(
        token,
        DEMO_PAGES["notion"],
        CONTENT / "Бизнес/Конкуренты/Конкуренты/Notion--839a51d3.md",
        pages,
        apply,
    )
    replace_page_from_md(
        token,
        DEMO_PAGES["miro"],
        CONTENT / "Бизнес/Конкуренты/Конкуренты/Miro--f09d4efc.md",
        pages,
        apply,
    )
    if apply:
        for pid, tip, outcome, pay, switch, lose, strong, weak in [
            (
                DEMO_PAGES["notion"],
                "косвенная",
                "Гибкое пространство — сам собираешь",
                "Время на настройку + часто подписка",
                "Если нужен готовый foundation быстрее самосбора",
                "Гибкость и экосистема",
                "Универсальность, привычка рынка",
                "Пустой canvas съедает недели",
            ),
            (
                DEMO_PAGES["miro"],
                "косвенная",
                "Визуальная фасилитация и карты",
                "Подписка + время на доски",
                "Редко прямой конкурент OS",
                "Сила в воркшопах",
                "Коллаборация в реальном времени",
                "Не заменяет оффер и foundation",
            ),
        ]:
            nc._request(
                "PATCH",
                f"/pages/{pid}",
                token,
                body={
                    "properties": {
                        "Тип": select_prop(tip),
                        "Outcome": rich_prop(outcome),
                        "Уже платят": rich_prop(pay),
                        "Почему переключатся": rich_prop(switch),
                        "Где мы проигрываем": rich_prop(lose),
                        "Сильные": rich_prop(strong),
                        "Слабые": rich_prop(weak),
                    }
                },
            )
            time.sleep(0.3)

        # Status quo row
        nc._request(
            "POST",
            "/pages",
            token,
            body={
                "parent": {"database_id": HUBS["Конкуренты"]["db_id"]},
                "properties": {
                    "Name": {
                        "title": [
                            {
                                "type": "text",
                                "text": {"content": "Status quo: Excel + чаты"},
                            }
                        ]
                    },
                    "Тип": select_prop("status quo"),
                    "Outcome": rich_prop("«И так работает» без нового инструмента"),
                    "Уже платят": rich_prop("Время на хаос и потерянный контекст"),
                    "Почему переключатся": rich_prop(
                        "При боли запуска / найма / повторных ошибок"
                    ),
                    "Где мы проигрываем": rich_prop(
                        "Привычка и нулевая цена входа"
                    ),
                    "Сильные": rich_prop("Знакомо всем"),
                    "Слабые": rich_prop(
                        "Нет единого среза ценности; сложно масштабировать обучение"
                    ),
                },
            },
        )
        log("  + Status quo row")
        time.sleep(0.35)

    # Mark product rows as archive in Status
    if apply:
        q = nc._request(
            "POST",
            f"/databases/{HUBS['Продукты/Услуги']['db_id']}/query",
            token,
            body={"page_size": 20},
        )
        for r in q.get("results") or []:
            name = ""
            for pn, pv in (r.get("properties") or {}).items():
                if pv.get("type") == "title":
                    name = "".join(
                        x.get("plain_text", "") for x in pv.get("title") or []
                    )
            nc._request(
                "PATCH",
                f"/pages/{r['id']}",
                token,
                body={
                    "properties": {
                        "Статус проверки": select_prop("архив"),
                        "Доказательства": rich_prop(
                            "Историческая строка автора — см. examples; замените своим оффером"
                        ),
                    }
                },
            )
            # Clear body lightly
            kids = nc.get_block_children(token, r["id"])
            for b in kids:
                nc.delete_block(token, b["id"])
                time.sleep(0.25)
            nc.append_children(
                token,
                r["id"],
                [
                    nc.callout(
                        "Архив экспорта / старая позиция. Не используйте как оффер. "
                        "Создайте новую строку по структуре: сегмент, проблема/исход, "
                        "входит/не входит, цена, статус проверки.",
                        "📦",
                    )
                ],
            )
            log(f"  archive product {name!r}")
            time.sleep(0.3)

        # Update Items categories for known rows
        items_q = nc._request(
            "POST",
            f"/databases/{HUBS['Необходимые шаги']['db_id']}/query",
            token,
            body={"page_size": 20},
        )
        cat_map = {
            "Логотип": ("Nice-to-have", "—", "later"),
            "Дизайн баннеров для социальных сетей": ("Не сейчас", "—", "later"),
            "Планировщик контента": ("Не сейчас", "—", "later"),
            "Дизайн Веб-сайта": ("Nice-to-have", "—", "later"),
            "Веб-сайт": ("Nice-to-have", "viable если канал", "later"),
            "Хостинг": ("До ценного среза", "feasible / usable", "todo"),
            "Тексты сайтов": ("До ценного среза", "valuable", "todo"),
            "Программное обеспечение для разработки": (
                "До ценного среза",
                "feasible",
                "todo",
            ),
        }
        for r in items_q.get("results") or []:
            name = ""
            for pn, pv in (r.get("properties") or {}).items():
                if pv.get("type") == "title":
                    name = "".join(
                        x.get("plain_text", "") for x in pv.get("title") or []
                    )
            if name not in cat_map:
                continue
            cat, risk, st = cat_map[name]
            nc._request(
                "PATCH",
                f"/pages/{r['id']}",
                token,
                body={
                    "properties": {
                        "Категория": select_prop(cat),
                        "Риск": rich_prop(risk),
                        "Статус": select_prop(st),
                        "Comment": rich_prop(
                            "Категория относительно полезного среза — см. гайд страницы"
                        ),
                    }
                },
            )
            log(f"  item {name!r} → {cat}")
            time.sleep(0.3)

        # Add core must-have rows if missing
        existing_names = set()
        for r in items_q.get("results") or []:
            for pn, pv in (r.get("properties") or {}).items():
                if pv.get("type") == "title":
                    existing_names.add(
                        "".join(x.get("plain_text", "") for x in pv.get("title") or [])
                    )
        for name, cat, risk, comment in [
            (
                "Способ отдать полезный срез клиенту",
                "До ценного среза",
                "valuable / usable",
                "Прототип или узкий пакет, которым уже можно пользоваться",
            ),
            (
                "Способ принять оплату или обязательство",
                "До ценного среза",
                "viable",
                "Счёт / форма / договор",
            ),
            (
                "Канал до первых людей сегмента",
                "До ценного среза",
                "viable",
                "1 канал из стратегии маркетинга",
            ),
            (
                "Сбор сигнала после использования",
                "До ценного среза",
                "valuable",
                "Отзыв / короткий разговор",
            ),
        ]:
            if name in existing_names:
                continue
            nc._request(
                "POST",
                "/pages",
                token,
                body={
                    "parent": {
                        "database_id": HUBS["Необходимые шаги"]["db_id"]
                    },
                    "properties": {
                        "Name": {
                            "title": [
                                {"type": "text", "text": {"content": name}}
                            ]
                        },
                        "Категория": select_prop(cat),
                        "Риск": rich_prop(risk),
                        "Comment": rich_prop(comment),
                        "Статус": select_prop("todo"),
                        "Cost": {"number": 0},
                    },
                },
            )
            log(f"  + item {name!r}")
            time.sleep(0.35)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", default=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument(
        "--only",
        choices=["hubs", "dbs", "demos", "track", "all"],
        default="all",
    )
    args = ap.parse_args()
    apply = bool(args.apply)
    if apply:
        args.dry_run = False

    token = nc.get_token()
    data = json.loads(PAGE_MAP.read_text(encoding="utf-8"))
    pages = dict(data.get("pages") or {})
    log(f"page map: {len(pages)} pages · apply={apply} · only={args.only}")

    only = args.only
    if only in ("hubs", "all"):
        sync_hubs(token, pages, apply)
    if only in ("track", "all"):
        sync_track_start(token, pages, apply)
    if only in ("dbs", "all"):
        sync_db_schemas(token, apply)
    if only in ("demos", "all"):
        # schemas first if demos need new props
        if only == "demos" and apply:
            sync_db_schemas(token, apply)
        sync_demo_rows(token, pages, apply)

    log("\nDone.")
    if not apply:
        log("Это dry-run. Запустите с --apply для записи в Notion.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
