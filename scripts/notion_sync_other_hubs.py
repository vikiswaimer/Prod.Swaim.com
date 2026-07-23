#!/usr/bin/env python3
"""Залить хабы Other (кроме Ссылки и Цифровая безопасность) в Notion.

Сохраняет child DB на страницах. Демо-записи обновляет под Git.

  python3 scripts/notion_sync_other_hubs.py --dry-run
  python3 scripts/notion_sync_other_hubs.py --apply
  python3 scripts/notion_sync_other_hubs.py --apply --only reviews
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import notion_client as nc  # noqa: E402
import notion_sync_pilot as pilot  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PAGE_MAP = ROOT / "docs/reports/notion-sbs-page-map.json"
CONTENT = ROOT / "content/small-business-space-ru"

# Не трогаем: Ссылки, Цифровая безопасность
TARGETS = {
    "reviews": {
        "page_id": "7bd207ca-d379-82fa-b774-0114a42b71ee",
        "md": CONTENT / "Other/Отзывы--593380ce.md",
        "title": None,  # оставить «Отзывы»
        "demo": {
            "page_id": "2ec207ca-d379-82f5-9a9b-817c0369cd1d",
            "md": CONTENT / "Other/Отзывы/Feedback/Alice--62984f63.md",
            "title": "Alice (демо)",
        },
    },
    "email": {
        "page_id": "c7a207ca-d379-829d-a21c-013c14eaf38a",
        "md": CONTENT / "Other/Email шаблоны--facf40e0.md",
        "title": None,
        "demo": {
            "page_id": "e2c207ca-d379-8306-9e55-01a0f70eb1e3",
            "md": CONTENT
            / "Other/Email шаблоны/Email Snippets/Thank you for your purchase--13e50e84.md",
            "title": "Спасибо за покупку (демо)",
        },
    },
    "snippets": {
        "page_id": "b35207ca-d379-82d7-be8f-817d028d0ef9",
        "md": CONTENT / "Other/Text Snippets--1dbd68f8.md",
        "title": "Текстовые заготовки",
        "demo": {
            "page_id": "c11207ca-d379-8316-8992-01823941e76a",
            "md": CONTENT
            / "Other/Text Snippets/Snippets/Thanks for reaching out--a336704c.md",
            "title": "Спасибо, что написали (демо)",
        },
    },
}


def tables_to_bullets(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if "|" in line and i + 1 < len(lines) and re.match(
            r"^\s*\|?\s*[-:| ]+\s*\|?\s*$", lines[i + 1]
        ):
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                cols = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                while len(cols) < len(header):
                    cols.append("")
                if len(header) >= 2:
                    left = re.sub(r"\*+", "", cols[0]).strip()
                    right = re.sub(r"\*+", "", cols[1]).strip()
                    out.append(f"- **{left}** — {right}" if left else f"- {right}")
                else:
                    out.append("- " + " · ".join(c for c in cols if c))
                i += 1
            continue
        out.append(line)
        i += 1
    return "\n".join(out)


def prepare_hub_md(md: str) -> str:
    md = tables_to_bullets(md)
    # CSV → указание на DB на странице
    md = re.sub(
        r"Таблица(?: записей)?:\s*\[[^\]]*\]\([^)]+\.csv\)\s*",
        "База записей — блок таблицы на этой странице (ниже).\n\n",
        md,
    )
    md = re.sub(
        r"Таблица:\s*\[[^\]]*\]\([^)]+\.csv\)\s*",
        "База записей — блок таблицы на этой странице (ниже).\n\n",
        md,
    )
    # локальные демо-файлы → plain text (страницы DB обновим отдельно)
    md = re.sub(r"- \[([^\]]+)\]\([^)]+/(?:Feedback|Email Snippets|Snippets)/[^)]+\)", r"- \1", md)
    md = re.sub(r"\[[^\]]*\]\([^)]+\.svg\)", "", md)
    # убрать битые img aside paths already handled by pilot
    return md


def clear_non_db(token: str, page_id: str) -> tuple[int, str | None]:
    kids = nc.get_block_children(token, page_id)
    db_id = None
    n = 0
    for b in kids:
        if b.get("type") == "child_database":
            db_id = b["id"]
            continue
        if b.get("type") == "child_page":
            continue
        nc.delete_block(token, b["id"])
        n += 1
        time.sleep(0.35)
    return n, db_id


def append_at_start_ordered(token: str, page_id: str, children: list[dict]) -> None:
    if len(children) <= 100:
        nc._request(
            "PATCH",
            f"/blocks/{page_id}/children",
            token,
            body={"children": children, "position": {"type": "start"}},
        )
        return
    chunks = [children[i : i + 100] for i in range(0, len(children), 100)]
    for chunk in reversed(chunks):
        nc._request(
            "PATCH",
            f"/blocks/{page_id}/children",
            token,
            body={"children": chunk, "position": {"type": "start"}},
        )
        time.sleep(0.35)


def set_page_title(token: str, page_id: str, title: str) -> None:
    page = nc.get_page(token, page_id)
    props = page.get("properties") or {}
    title_prop = None
    for name, prop in props.items():
        if prop.get("type") == "title":
            title_prop = name
            break
    if not title_prop:
        print(f"WARN no title prop on {page_id}", file=sys.stderr)
        return
    nc._request(
        "PATCH",
        f"/pages/{page_id}",
        token,
        body={
            "properties": {
                title_prop: {
                    "title": [{"type": "text", "text": {"content": title}}]
                }
            }
        },
    )


def replace_page_body(token: str, page_id: str, blocks: list[dict]) -> int:
    """Полная замена блоков страницы записи (без child DB обычно)."""
    n = nc.clear_page_blocks(token, page_id)
    nc.append_children(token, page_id, blocks)
    return n


def build_blocks(md: str, pages: dict[str, str]) -> list[dict]:
    return pilot.md_to_blocks(
        md,
        assets_dir=None,
        token=None,
        upload=False,
        pages=pages,
    )


def sync_one(
    token: str,
    pages: dict[str, str],
    key: str,
    cfg: dict,
    *,
    apply: bool,
) -> None:
    page_id = cfg["page_id"]
    md = prepare_hub_md(cfg["md"].read_text(encoding="utf-8"))
    blocks = build_blocks(md, pages)
    page = nc.get_page(token, page_id)
    print(f"\n## {key}: {nc.page_title(page)!r} ({page_id})")
    print(page.get("url"))
    print(f"hub blocks: {len(blocks)}")
    for line in nc.summarize_blocks(blocks)[:25]:
        print(" ", line)
    if len(blocks) > 25:
        print(f"  ... +{len(blocks) - 25}")

    demo = cfg.get("demo")
    demo_blocks: list[dict] = []
    if demo:
        dmd = prepare_hub_md(demo["md"].read_text(encoding="utf-8"))
        demo_blocks = build_blocks(dmd, pages)
        print(f"demo blocks: {len(demo_blocks)} → {demo['title']}")

    if not apply:
        print("DRY-RUN")
        return

    n, db_id = clear_non_db(token, page_id)
    print(f"cleared {n} text blocks; kept DB={db_id}")
    append_at_start_ordered(token, page_id, blocks)
    print(f"inserted {len(blocks)} at start")

    if cfg.get("title"):
        set_page_title(token, page_id, cfg["title"])
        print(f"page title → {cfg['title']}")

    if demo and demo_blocks:
        cleared = replace_page_body(token, demo["page_id"], demo_blocks)
        set_page_title(token, demo["page_id"], demo["title"])
        print(f"demo updated (cleared {cleared}): {demo['title']}")

    kids = nc.get_block_children(token, page_id)
    types = [b.get("type") for b in kids]
    print(
        f"verify children={len(kids)} first={types[:2]} "
        f"has_db={'child_database' in types} last={types[-1:]}"
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", default=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument(
        "--only",
        choices=["all", *TARGETS.keys()],
        default="all",
    )
    args = ap.parse_args()
    if args.apply:
        args.dry_run = False

    token = nc.get_token()
    pages = pilot.load_page_map(PAGE_MAP)
    print(f"page map: {len(pages)} pages; apply={args.apply}")

    keys = list(TARGETS) if args.only == "all" else [args.only]
    for key in keys:
        sync_one(token, pages, key, TARGETS[key], apply=args.apply)

    if args.dry_run:
        print("\nDRY-RUN OK. Добавьте --apply для записи.")
    else:
        print("\nDONE. Ссылки и Цифровая безопасность не изменялись.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
