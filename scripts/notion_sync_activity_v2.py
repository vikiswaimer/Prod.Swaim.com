#!/usr/bin/env python3
"""Сжать Активность в Notion до 4 поверхностей (issue #22, итерация).

Ядро: Цели · Гипотезы · Аналитика · Обзор недели
Архив страниц: Задачи, Заметки, Календарь
Рефлексия → переименовать в Обзор недели
Убрать вложенные child_database с Целей и Обзора (полный clear).
На Гипотезах: оставить одну child DB, заменить гайд.

  python3 scripts/notion_sync_activity_v2.py --dry-run
  python3 scripts/notion_sync_activity_v2.py --apply
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
PAGE_MAP_PATH = ROOT / "docs/reports/notion-sbs-page-map.json"

ACTIVITY_DB = "a2a207ca-d379-8344-9a0b-0152fb52fcc0"

CORE = {
    "Цели": (
        "f18207ca-d379-822c-beaa-8167847859f4",
        CONTENT / "Активность/Цели--864823f3.md",
        "Куда идём: 1–3 исхода, baseline → target",
        False,  # keep_db
    ),
    "Гипотезы": (
        "4cf207ca-d379-82eb-baff-81b0dc1af094",
        CONTENT / "Активность/Идеи--8e1bd74e.md",
        "Что проверяем: формула, статус, вывод; исполнение в Linear/GitHub",
        True,
    ),
    "Аналитика": (
        "3a9207ca-d379-8137-9fad-eb55f83a0943",
        CONTENT / "Активность/Аналитика--a1f4c901.md",
        "Measure: метрики и инструменты простым языком",
        False,
    ),
    # Рефлексия page id → becomes Обзор недели
    "Обзор недели": (
        "2e9207ca-d379-83ba-8a69-01b6628af5af",
        CONTENT / "Активность/Обзор недели--c0a1e501.md",
        "Learn-ритуал раз в неделю: Build → Measure → Learn",
        False,
    ),
}

ARCHIVE = {
    "Задачи": "57f207ca-d379-83e1-b273-011148ad0665",
    "Заметки": "b7b207ca-d379-829b-b10b-815737f68e84",
    "Календарь": "6a2207ca-d379-8237-918b-81f8fdd53acd",
}

TRACKS = {
    "Старт своего бизнеса": (
        "9b0207ca-d379-8305-9d71-013fc7eb2fd7",
        CONTENT / "Быстрый старт/Старт своего бизнеса--66c3ee00.md",
    ),
    "Развитие своего бизнеса": (
        "329207ca-d379-837b-9966-81eee8afa61d",
        CONTENT / "Быстрый старт/Развитие своего бизнеса--d23a7834.md",
    ),
}


def log(msg: str) -> None:
    print(msg, flush=True)


def prepare_md(md: str) -> str:
    md = re.sub(r"^#\s+[^\n]+\n+", "", md, count=1)
    md = re.sub(r"\n\[[^\]]+\]\([^)]+\.csv\)\s*$", "\n", md)
    md = re.sub(r"</?b>", "", md, flags=re.I)
    md = re.sub(r"</?strong>", "", md, flags=re.I)
    return md.strip() + "\n"


def set_props(token: str, page_id: str, title: str, description: str) -> None:
    nc._request(
        "PATCH",
        f"/pages/{page_id}",
        token,
        body={
            "properties": {
                "Name": {
                    "title": [{"type": "text", "text": {"content": title[:2000]}}]
                },
                "Description": {
                    "rich_text": [
                        {"type": "text", "text": {"content": description[:2000]}}
                    ]
                },
            }
        },
    )
    time.sleep(0.3)


def archive_page(token: str, page_id: str) -> None:
    nc._request("PATCH", f"/pages/{page_id}", token, body={"archived": True})
    time.sleep(0.35)


def clear_all(token: str, page_id: str) -> int:
    """Удалить все блоки, включая child_database."""
    kids = nc.get_block_children(token, page_id)
    for b in kids:
        nc.delete_block(token, b["id"])
        time.sleep(0.3)
    return len(kids)


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


def write_page(
    token: str,
    *,
    page_id: str,
    title: str,
    md_path: Path,
    pages: dict[str, str],
    keep_db: bool,
    apply: bool,
    description: str | None = None,
    set_activity_props: bool = True,
) -> None:
    md = prepare_md(md_path.read_text(encoding="utf-8"))
    if keep_db:
        md = (
            "> Рабочая таблица гипотез — на этой странице "
            "(перетащите под гайд при необходимости).\n\n"
            + md
        )
    blocks = pilot.md_to_blocks(
        md,
        assets_dir=None,
        token=token if apply else None,
        upload=False,
        pages=pages,
        nest_aside_images=False,
    )
    log(f"\n## {title} ({page_id}) keep_db={keep_db} blocks={len(blocks)}")
    for line in nc.summarize_blocks(blocks)[:10]:
        log(f"  {line}")
    if not apply:
        log("DRY-RUN")
        return
    if set_activity_props and description is not None:
        set_props(token, page_id, title, description)
    if keep_db:
        d, k = clear_keep_db(token, page_id)
        log(f"cleared {d}, kept db={k}")
    else:
        n = clear_all(token, page_id)
        log(f"cleared all {n} (incl. nested DBs)")
    nc.append_children(token, page_id, blocks)
    page = nc.get_page(token, page_id)
    log(f"OK → {page.get('url')}")


def update_page_map() -> None:
    data = json.loads(PAGE_MAP_PATH.read_text(encoding="utf-8"))
    pages = data.setdefault("pages", {})
    pages["Гипотезы"] = CORE["Гипотезы"][0]
    pages["Аналитика"] = CORE["Аналитика"][0]
    pages["Цели"] = CORE["Цели"][0]
    pages["Обзор недели"] = CORE["Обзор недели"][0]
    # reflection key → обзор
    pages.pop("Рефлексия", None)
    data["count"] = len(pages)
    PAGE_MAP_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    log(f"page map updated")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", default=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    apply = bool(args.apply)

    token = nc.get_token()
    pages = pilot.load_page_map(PAGE_MAP_PATH)
    pages["Гипотезы"] = CORE["Гипотезы"][0]
    pages["Обзор недели"] = CORE["Обзор недели"][0]
    pages["Аналитика"] = CORE["Аналитика"][0]
    pages["Цели"] = CORE["Цели"][0]
    pilot.TITLE_ALIASES["гипотезы"] = "Гипотезы"
    pilot.TITLE_ALIASES["обзор недели"] = "Обзор недели"
    pilot.TITLE_ALIASES["рефлексия"] = "Обзор недели"

    log(f"mode={'APPLY' if apply else 'DRY-RUN'}")

    # 1) archive noise
    for name, pid in ARCHIVE.items():
        log(f"\n## Archive {name} ({pid})")
        if apply:
            # short stub then archive — stub optional; archive hides from DB
            archive_page(token, pid)
            log("archived")
        else:
            log("DRY-RUN archive")

    # 2) core pages
    for title, (pid, md_path, desc, keep_db) in CORE.items():
        write_page(
            token,
            page_id=pid,
            title=title,
            description=desc,
            md_path=md_path,
            pages=pages,
            keep_db=keep_db,
            apply=apply,
            set_activity_props=True,
        )

    # 3) tracks (обычные страницы — без props DB Активность)
    for name, (pid, md_path) in TRACKS.items():
        write_page(
            token,
            page_id=pid,
            title=name,
            md_path=md_path,
            pages=pages,
            keep_db=False,
            apply=apply,
            set_activity_props=False,
        )

    if apply:
        update_page_map()

    log("\nDone.")
    if not apply:
        log("Для записи: python3 scripts/notion_sync_activity_v2.py --apply")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
