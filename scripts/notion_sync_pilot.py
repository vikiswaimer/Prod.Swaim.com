#!/usr/bin/env python3
"""Пилот: обновить одну страницу Notion из markdown (callout + внутренние ссылки SBS).

Ссылки резолвятся **только** по карте страниц вашей копии Small Business Space
(`docs/reports/notion-sbs-page-map.json`), не по всему workspace.

  python3 scripts/notion_sync_pilot.py --page-id <id> --md ... --dry-run
  python3 scripts/notion_sync_pilot.py --page-id <id> --md ... --apply
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
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
HASH_SUFFIX_RE = re.compile(r"--[0-9a-fA-F]{6,12}$")

# Indication icons: API can't set file-icon on callout; nesting them = huge duplicates.
ASIDE_ICON_FILES = {
    "paper.png",
    "thunder.png",
    "folder.png",
    "archive.png",
}

# Git filename / link-text aliases → title in SBS page map
TITLE_ALIASES = {
    "продукты услуги": "Продукты/Услуги",
    "оффер / продукты": "Продукты/Услуги",
    "руководство по стилю": "Style Guide",
    "style guide": "Style Guide",
    "финансовый отчёт": "Финансовый отчет",
    "финансовый отчет": "Финансовый отчет",
    "счета": "Счет-фактуры",
    "счет-фактуры": "Счет-фактуры",
    "ссылки": "Ссылки ",
    "развитию": "Развитие своего бизнеса",
    "развитие": "Развитие своего бизнеса",
    "соцсети": "Планировщик Социальных Медиа",
    "статьи": "Планировщик статей",
    "рассылки": "Планировщик Рассылок",
    "список email": "Список Email-ов",
    "список email-ов": "Список Email-ов",
    "шаблоны email": "Email шаблоны",
    "текстовые заготовки": "Text Snippets",
    "text snippets": "Text Snippets",
    "стратегия маркетинга": "Маркетинг",
}

DEFAULT_PAGE_MAP = Path("docs/reports/notion-sbs-page-map.json")


def load_page_map(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    pages = dict(data.get("pages") or {})
    # normalized lookup helpers
    return pages


def build_title_index(pages: dict[str, str]) -> dict[str, str]:
    """lower(title.strip()) -> canonical title in map."""
    idx: dict[str, str] = {}
    for title in pages:
        idx[title.strip().lower()] = title
        idx[title.lower()] = title
    for alias, canon in TITLE_ALIASES.items():
        if canon in pages:
            idx[alias] = canon
        # also if canon with trailing space
        spaced = canon if canon in pages else f"{canon} "
        if spaced in pages:
            idx[alias] = spaced
    return idx


def stem_from_href(href: str) -> str:
    path = urllib.parse.unquote(href.split("#")[0].strip())
    name = Path(path).name
    if name.lower().endswith(".md"):
        name = name[:-3]
    name = HASH_SUFFIX_RE.sub("", name)
    return name.replace("_", " ").strip()


def resolve_page_id(
    href: str,
    label: str,
    pages: dict[str, str],
    title_index: dict[str, str],
) -> str | None:
    """Only resolves to pages inside the provided SBS map."""
    if href.startswith(("http://", "https://", "mailto:")):
        return None
    # git-only docs / examples — не линкуем в Notion
    low = href.lower()
    if "docs/" in low or "examples/" in low or low.endswith("methodology.md"):
        return None

    candidates = [stem_from_href(href), label.strip()]
    for raw in candidates:
        if not raw:
            continue
        key = raw.strip().lower()
        # direct
        if raw in pages:
            return pages[raw]
        if key in title_index:
            return pages[title_index[key]]
        # try without trailing punctuation
        key2 = key.rstrip(".,;:")
        if key2 in title_index:
            return pages[title_index[key2]]
    return None


def plain_no_md(text: str) -> str:
    text = text.replace("**", "")
    text = text.replace("__", "")
    # italic markers only when wrapping a run
    text = re.sub(r"(?<!\w)_([^_]+)_(?!\w)", r"\1", text)
    text = text.replace("`", "")
    return text


def md_inline_to_rich(
    text: str,
    pages: dict[str, str],
    title_index: dict[str, str],
    *,
    italic: bool = False,
) -> list[dict]:
    """Parse markdown links → Notion text+link to SBS pages only."""
    parts: list[dict] = []
    pos = 0
    for m in LINK_RE.finditer(text):
        if m.start() > pos:
            chunk = plain_no_md(text[pos : m.start()])
            if chunk:
                parts.extend(nc.rich(chunk, italic=italic))
        label = plain_no_md(m.group(1))
        href = m.group(2).strip()
        page_id = resolve_page_id(href, m.group(1), pages, title_index)
        if page_id:
            # custom label + link into *this* product copy
            parts.extend(nc.rich(label or "page", italic=italic, link=nc.notion_page_url(page_id)))
        else:
            parts.extend(nc.rich(label, italic=italic))
        pos = m.end()
    if pos < len(text):
        chunk = plain_no_md(text[pos:])
        if chunk:
            parts.extend(nc.rich(chunk, italic=italic))
    return parts


def parse_aside(inner: str) -> tuple[list[str], str, str]:
    imgs: list[str] = []
    for m in IMG_HTML_RE.finditer(inner):
        imgs.append(m.group(1).strip())
    inner = IMG_HTML_RE.sub("", inner)
    for m in MD_IMG_RE.finditer(inner):
        imgs.append(m.group(2).strip())
    inner = MD_IMG_RE.sub("", inner)
    text = re.sub(r"(?im)^\s*[-*]\s*Пример:?\s*$", "", inner)
    text = re.sub(r"\s+", " ", text).strip()
    text = LINK_RE.sub(r"\1", text)
    text = plain_no_md(text)
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
    pages: dict[str, str],
    nest_aside_images: bool = False,
) -> list[dict]:
    title_index = build_title_index(pages)

    lines = md.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    text = "\n".join(lines).strip() + "\n"

    blocks: list[dict] = []
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
        name = Path(src).name
        if name.lower() in ASIDE_ICON_FILES:
            return None
        path = assets_dir / name
        if not path.exists():
            path = assets_dir / src
        if not path.exists():
            print(f"WARN missing asset {src}", file=sys.stderr)
            return None
        if upload and token:
            uid = nc.upload_local_file(token, path)
            return nc.image_file_upload(uid)
        return nc.callout(f"[image: {path.name}]", "🖼️")

    def rt(s: str, *, italic: bool = False) -> list[dict]:
        return md_inline_to_rich(s, pages, title_index, italic=italic)

    buf_para: list[str] = []

    def flush_para() -> None:
        nonlocal buf_para
        if not buf_para:
            return
        rich_text = rt(" ".join(buf_para))
        if rich_text:
            blocks.append(nc.paragraph_rt(rich_text))
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
            if nest_aside_images:
                for img in imgs:
                    ib = resolve_image(img)
                    if ib:
                        children.append(ib)
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
            blocks.append(nc.heading_rt(len(m_h.group(1)), rt(m_h.group(2))))
            continue

        m_q = QUOTE_RE.match(line)
        if m_q:
            flush_para()
            blocks.append(nc.quote_rt(rt(m_q.group(1))))
            continue

        if line.strip() == "---":
            flush_para()
            blocks.append(nc.divider())
            continue

        m_todo = TODO_RE.match(line)
        if m_todo:
            flush_para()
            checked = m_todo.group(1).lower() == "x"
            blocks.append(nc.to_do_rt(rt(m_todo.group(2)), checked=checked))
            continue

        m_b = BULLET_RE.match(line)
        if m_b:
            flush_para()
            orig = m_b.group(1)
            italic = orig.strip().startswith("_")
            blocks.append(nc.bulleted_rt(rt(orig, italic=italic)))
            continue

        m_n = NUM_RE.match(line)
        if m_n:
            flush_para()
            orig = m_n.group(2)
            italic = orig.strip().startswith("_")
            blocks.append(nc.numbered_rt(rt(orig, italic=italic)))
            continue

        buf_para.append(line)

    flush_para()
    return blocks


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--page-id", required=True)
    ap.add_argument("--md", type=Path, required=True)
    ap.add_argument("--assets-dir", type=Path, default=None)
    ap.add_argument(
        "--page-map",
        type=Path,
        default=DEFAULT_PAGE_MAP,
        help="JSON карта страниц только вашей копии SBS",
    )
    ap.add_argument(
        "--nest-aside-images",
        action="store_true",
        help="Вкладывать картинки из aside (по умолчанию нет — иконки дублировались крупно)",
    )
    ap.add_argument("--dry-run", action="store_true", default=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    if args.apply:
        args.dry_run = False

    token = nc.get_token()
    pages = load_page_map(args.page_map)
    print(f"page map: {args.page_map} ({len(pages)} pages, root-scoped)")

    md = args.md.read_text(encoding="utf-8")
    # Пакет D: не тащить в Notion ссылки на docs/Git/examples
    md = re.sub(
        r"Подробнее: \[позиционирование\]\([^)]+\)[^\n]*\n?",
        "",
        md,
    )
    md = re.sub(
        r"\[примером заполнения\]\([^)]+\)",
        "примером заполнения",
        md,
    )
    md = re.sub(r"\[пример\]\([^)]+\)", "примером", md)
    md = re.sub(
        r"Канон для агента: `docs/methodology\.md` в Git\.",
        "",
        md,
    )

    common = dict(
        assets_dir=args.assets_dir,
        token=token,
        pages=pages,
        nest_aside_images=args.nest_aside_images,
    )

    if args.dry_run:
        blocks = md_to_blocks(md, upload=False, **common)
        print(f"blocks prepared: {len(blocks)}")
        for line in nc.summarize_blocks(blocks)[:55]:
            print(line)
        if len(blocks) > 55:
            print(f"... +{len(blocks)-55} more")
        # show how many rich links resolved
        linked = 0
        for b in blocks:
            t = b.get("type")
            rts = (b.get(t) or {}).get("rich_text") or []
            for r in rts:
                if (r.get("text") or {}).get("link"):
                    linked += 1
        print(f"inline links to SBS pages: {linked}")
        print("DRY-RUN: ничего не записано. Добавьте --apply для записи.")
        return 0

    page = nc.get_page(token, args.page_id)
    print(f"updating {nc.page_title(page)!r} {page.get('url')}")
    blocks = md_to_blocks(md, upload=True, **common)
    print(f"blocks prepared: {len(blocks)}")
    for line in nc.summarize_blocks(blocks)[:55]:
        print(line)
    n = nc.clear_page_blocks(token, args.page_id)
    print(f"cleared {n} old blocks")
    nc.append_children(token, args.page_id, blocks)
    print(f"appended {len(blocks)} blocks OK")
    print(page.get("url"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
