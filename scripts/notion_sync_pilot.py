#!/usr/bin/env python3
"""Пилот: обновить одну страницу Notion из markdown (формат callout + image).

Сначала смотрим живую копию (notion_inspect), затем:
  python3 scripts/notion_sync_pilot.py --page-id <id> --md content/.../Instructions/_index.md \\
      --assets-dir content/.../Instructions --dry-run
  python3 scripts/notion_sync_pilot.py --page-id <id> --md ... --assets-dir ... --apply
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import notion_client as nc  # noqa: E402

ASIDE_RE = re.compile(r"<aside>(.*?)</aside>", re.S | re.I)
IMG_HTML_RE = re.compile(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', re.I)
MD_IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^(#{1,3})\s+(.*)$")
TODO_RE = re.compile(r"^[-*]\s+\[([ xX])\]\s+(.*)$")
BULLET_RE = re.compile(r"^[-*]\s+(.*)$")
NUM_RE = re.compile(r"^(\d+)\.\s+(.*)$")
QUOTE_RE = re.compile(r"^>\s?(.*)$")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def strip_md_inline(text: str) -> str:
    text = LINK_RE.sub(r"\1", text)
    text = text.replace("**", "")
    text = text.replace("_", "")
    text = text.replace("`", "")
    return text.strip()


def parse_aside(inner: str) -> tuple[list[str], str, str]:
    """return (image_srcs, emoji_hint, text).

    Live Notion format (captured): Pages indications = callout + custom icon image;
    API cannot set file icons on callouts → emoji callout + image as *child*.
    Columns indications = emoji callout; example screenshots as children.
    """
    imgs: list[str] = []
    for m in IMG_HTML_RE.finditer(inner):
        imgs.append(m.group(1).strip())
    inner = IMG_HTML_RE.sub("", inner)
    for m in MD_IMG_RE.finditer(inner):
        imgs.append(m.group(2).strip())
    inner = MD_IMG_RE.sub("", inner)
    # drop leftover "Пример:" bullets noise → keep short callout text
    text = re.sub(r"(?im)^\s*[-*]\s*Пример:?\s*$", "", inner)
    text = re.sub(r"\s+", " ", text).strip()
    text = strip_md_inline(text)
    emoji = "📌"
    if "⛔" in text or "Not editable" in text:
        emoji = "⛔"
    elif "✏️" in text or "Editable" in text:
        emoji = "✏️"
    elif "Document" in text:
        emoji = "📄"
    elif "Activity" in text:
        emoji = "⚡"
    elif "Database" in text:
        emoji = "📁"
    elif "Archive" in text:
        emoji = "📦"
    return imgs, emoji, text


def md_to_blocks(
    md: str,
    *,
    assets_dir: Path | None,
    token: str | None,
    upload: bool,
) -> list[dict]:
    # drop leading H1 (page title already in Notion)
    lines = md.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    text = "\n".join(lines).strip() + "\n"

    blocks: list[dict] = []
    # extract asides first, replace with placeholders
    asides: list[tuple[list[str], str, str]] = []

    def aside_sub(m: re.Match[str]) -> str:
        asides.append(parse_aside(m.group(1)))
        return f"\n@@ASIDE_{len(asides)-1}@@\n"

    text = ASIDE_RE.sub(aside_sub, text)

    def resolve_image(src: str) -> dict | None:
        if src.startswith("http"):
            return nc.image_external(src)
        if not assets_dir:
            return None
        # strip folder prefix Instructions/
        name = Path(src).name
        path = assets_dir / name
        if not path.exists():
            path = assets_dir / src
        if not path.exists():
            print(f"WARN missing asset {src}", file=sys.stderr)
            return None
        if upload and token:
            uid = nc.upload_local_file(token, path)
            return nc.image_file_upload(uid)
        # dry-run placeholder as callout
        return nc.callout(f"[image: {path.name}]", "🖼️")

    buf_para: list[str] = []

    def flush_para() -> None:
        nonlocal buf_para
        if not buf_para:
            return
        para = strip_md_inline(" ".join(buf_para))
        if para:
            blocks.append(nc.paragraph(para))
        buf_para = []

    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip():
            flush_para()
            continue

        m_aside = re.match(r"@@ASIDE_(\d+)@@$", line.strip())
        if m_aside:
            flush_para()
            imgs, emoji, atext = asides[int(m_aside.group(1))]
            children: list[dict] = []
            for img in imgs:
                ib = resolve_image(img)
                if ib:
                    children.append(ib)
            # API: file icons on callouts unsupported → emoji + images as children
            if atext:
                blocks.append(nc.callout(atext, emoji, children=children or None))
            else:
                blocks.extend(children)
            continue

        m_img = MD_IMG_RE.fullmatch(line.strip())
        if m_img:
            flush_para()
            ib = resolve_image(m_img.group(2).strip())
            if ib:
                blocks.append(ib)
            continue

        m_h = HEADING_RE.match(line)
        if m_h:
            flush_para()
            blocks.append(nc.heading(len(m_h.group(1)), strip_md_inline(m_h.group(2))))
            continue

        m_q = QUOTE_RE.match(line)
        if m_q:
            flush_para()
            blocks.append(nc.quote(strip_md_inline(m_q.group(1))))
            continue

        if line.strip() == "---":
            flush_para()
            blocks.append(nc.divider())
            continue

        m_todo = TODO_RE.match(line)
        if m_todo:
            flush_para()
            checked = m_todo.group(1).lower() == "x"
            blocks.append(nc.to_do(strip_md_inline(m_todo.group(2)), checked=checked))
            continue

        m_b = BULLET_RE.match(line)
        if m_b:
            flush_para()
            orig = m_b.group(1)
            item = strip_md_inline(orig)
            italic = orig.strip().startswith("_")
            blocks.append(nc.bulleted(item, italic=italic))
            continue

        m_n = NUM_RE.match(line)
        if m_n:
            flush_para()
            orig = m_n.group(2)
            item = strip_md_inline(orig)
            italic = orig.strip().startswith("_")
            blocks.append(nc.numbered(item, italic=italic))
            continue

        buf_para.append(line)

    flush_para()
    return blocks


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--page-id", required=True)
    ap.add_argument("--md", type=Path, required=True)
    ap.add_argument("--assets-dir", type=Path, default=None)
    ap.add_argument("--dry-run", action="store_true", default=True)
    ap.add_argument("--apply", action="store_true", help="Реально очистить страницу и записать блоки")
    args = ap.parse_args()
    if args.apply:
        args.dry_run = False

    token = nc.get_token()
    md = args.md.read_text(encoding="utf-8")
    # skip git-only docs link noise for Notion
    md = re.sub(
        r"Подробнее: \[позиционирование\]\([^)]+\)[^\n]*\n?",
        "Подробнее о позиционировании — в Git-копии docs/positioning.md.\n",
        md,
    )
    md = re.sub(
        r"\[примером заполнения\]\([^)]+\)",
        "примером заполнения (в Git: examples/)",
        md,
    )
    md = re.sub(r"\[пример\]\([^)]+\)", "пример в Git: examples/", md)

    if args.dry_run:
        blocks = md_to_blocks(
            md,
            assets_dir=args.assets_dir,
            token=token,
            upload=False,
        )
        print(f"blocks prepared: {len(blocks)}")
        for line in nc.summarize_blocks(blocks)[:50]:
            print(line)
        if len(blocks) > 50:
            print(f"... +{len(blocks)-50} more")
        print("DRY-RUN: ничего не записано. Добавьте --apply для записи.")
        return 0

    page = nc.get_page(token, args.page_id)
    print(f"updating {nc.page_title(page)!r} {page.get('url')}")
    blocks = md_to_blocks(
        md,
        assets_dir=args.assets_dir,
        token=token,
        upload=True,
    )
    print(f"blocks prepared: {len(blocks)}")
    for line in nc.summarize_blocks(blocks)[:50]:
        print(line)
    if len(blocks) > 50:
        print(f"... +{len(blocks)-50} more")
    n = nc.clear_page_blocks(token, args.page_id)
    print(f"cleared {n} old blocks")
    nc.append_children(token, args.page_id, blocks)
    print(f"appended {len(blocks)} blocks OK")
    print(page.get("url"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
