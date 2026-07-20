#!/usr/bin/env python3
"""Инспекция доступных страниц Notion + снимок блоков (формат копии продукта).

Примеры:
  python3 scripts/notion_inspect.py
  python3 scripts/notion_inspect.py --query "Small Business"
  python3 scripts/notion_inspect.py --page-id <id> --dump /tmp/page-blocks.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# allow `python3 scripts/notion_inspect.py`
sys.path.insert(0, str(Path(__file__).resolve().parent))
import notion_client as nc  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", default="Small Business", help="Поиск страниц")
    ap.add_argument("--page-id", default="", help="Снимок конкретной страницы")
    ap.add_argument("--dump", type=Path, help="Куда сохранить JSON блоков")
    ap.add_argument("--depth-children", action="store_true", help="Тянуть детей callout/toggle")
    args = ap.parse_args()

    token = nc.get_token()

    if args.page_id:
        page = nc.get_page(token, args.page_id)
        print(f"PAGE {args.page_id}")
        print(f"  title={nc.page_title(page)!r}")
        print(f"  url={page.get('url')}")
        blocks = nc.get_block_children(token, args.page_id)
        if args.depth_children:
            enriched = []
            for b in blocks:
                item = dict(b)
                if b.get("has_children"):
                    item["_children"] = nc.get_block_children(token, b["id"])
                enriched.append(item)
            blocks = enriched
        # merge fetched _children into payload.children for summarize
        for b in blocks:
            kids = b.pop("_children", None)
            if kids is not None:
                t = b.get("type")
                if t and isinstance(b.get(t), dict):
                    b[t] = dict(b[t])
                    b[t]["children"] = kids
        for line in nc.summarize_blocks(blocks):
            print(line)
        if args.dump:
            args.dump.write_text(json.dumps(blocks, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"wrote {args.dump}")
        return 0

    print(f"Search query={args.query!r}")
    pages = nc.search(token, args.query, filter_type="page")
    if not pages:
        pages = nc.search(token, args.query)
    print(f"found {len(pages)}")
    for p in pages:
        if p.get("object") != "page":
            continue
        pid = p["id"]
        title = nc.page_title(p) or "(no title)"
        print(f"- {title}\n    id={pid}\n    url={p.get('url')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
