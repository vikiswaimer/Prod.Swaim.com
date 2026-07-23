#!/usr/bin/env python3
"""Залить страницу «Ссылки» в Notion из Git (сохранить child DB Links).

  python3 scripts/notion_sync_links.py --dry-run
  python3 scripts/notion_sync_links.py --apply
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
PAGE_ID = "6d6207ca-d379-8343-a366-015a6f57b209"
MD_PATH = ROOT / "content/small-business-space-ru/Other/Ссылки--82a24257.md"
PAGE_MAP = ROOT / "docs/reports/notion-sbs-page-map.json"


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


def prepare_md(md: str) -> str:
    md = tables_to_bullets(md)
    md = re.sub(
        r"Таблица:\s*\[[^\]]*\]\([^)]+\.csv\)\s*",
        "Таблица **Links** — база на этой странице ниже.\n\n",
        md,
    )
    md = re.sub(r"- \[([^\]]+)\]\(Ссылки/Links/[^)]+\)", r"- \1", md)
    md = re.sub(r"- \[([^\]]+)\]\([^)]*Links/[^)]+\)", r"- \1", md)
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", default=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    if args.apply:
        args.dry_run = False

    token = nc.get_token()
    pages = pilot.load_page_map(PAGE_MAP)
    md = prepare_md(MD_PATH.read_text(encoding="utf-8"))
    blocks = pilot.md_to_blocks(
        md,
        assets_dir=None,
        token=None,
        upload=False,
        pages=pages,
    )
    print(f"page map: {len(pages)} pages")
    print(f"blocks prepared: {len(blocks)}")
    for line in nc.summarize_blocks(blocks)[:50]:
        print(line)
    if len(blocks) > 50:
        print(f"... +{len(blocks) - 50}")

    linked = 0
    for b in blocks:
        t = b.get("type")
        for r in (b.get(t) or {}).get("rich_text") or []:
            if (r.get("text") or {}).get("link"):
                linked += 1
                print(
                    "SBS link:",
                    (r.get("text") or {}).get("content"),
                    "->",
                    (r.get("text") or {}).get("link"),
                )
    print(f"inline SBS links: {linked}")

    if args.dry_run:
        print("DRY-RUN: ничего не записано. Добавьте --apply.")
        return 0

    page = nc.get_page(token, PAGE_ID)
    print(f"updating {nc.page_title(page)!r}")
    print(page.get("url"))
    n, db_id = clear_non_db(token, PAGE_ID)
    print(f"cleared {n} text blocks; kept DB={db_id}")
    append_at_start_ordered(token, PAGE_ID, blocks)
    print(f"inserted {len(blocks)} blocks at start (DB stays below)")

    kids = nc.get_block_children(token, PAGE_ID)
    types = [b.get("type") for b in kids]
    print(f"children now: {len(kids)}; first={types[:3]}; has_db={'child_database' in types}")
    print(page.get("url"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
