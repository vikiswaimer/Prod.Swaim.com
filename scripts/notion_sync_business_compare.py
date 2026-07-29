#!/usr/bin/env python3
"""Залить дубликаты группы Бизнес (Claude Opus / PR #26) рядом с первым прогоном.

Основные страницы (Grok / PR #25) НЕ перезаписываются.
Создаёт страницы в DB «Бизнес» с суффиксом «· Claude (сравнение)» + индекс.

  python3 scripts/notion_sync_business_compare.py --dry-run
  python3 scripts/notion_sync_business_compare.py --apply
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
# Источник markdown: либо worktree Claude-ветки, либо явный --content-root
DEFAULT_CONTENT = ROOT / "content/small-business-space-ru"
PAGE_MAP = ROOT / "docs/reports/notion-sbs-page-map.json"
BUSINESS_SECTION_DB = "279207ca-d379-82b8-be8e-8177d914578b"
ROOT_PAGE = "dcf207ca-d379-82b8-9fa8-013434ecd77f"

# Основные страницы первого прогона (не трогать)
ORIGINALS = {
    "Твой продукт": "569207ca-d379-82e0-8734-816a22514351",
    "Клиенты": "3f3207ca-d379-8390-9851-01d7d8b26890",
    "Продукты/Услуги": "f6f207ca-d379-829d-9967-81d11cfb9822",
    "Конкуренты": "35b207ca-d379-835c-9758-016bbc0fa248",
    "Маркетинг": "669207ca-d379-8215-8aa4-0126aeb2a2c2",
    "Необходимые шаги": "9db207ca-d379-83be-a6ca-01a1943ec547",
}

HUB_FILES = {
    "Твой продукт": "Бизнес/Твой продукт--5ac1cda1.md",
    "Клиенты": "Бизнес/Клиенты--ee4c1042.md",
    "Продукты/Услуги": "Бизнес/Продукты Услуги--4bbcfa4e.md",
    "Конкуренты": "Бизнес/Конкуренты--b7cd0ad7.md",
    "Маркетинг": "Бизнес/Маркетинг--62b1f924.md",
    "Необходимые шаги": "Бизнес/Необходимые шаги--34c60f4e.md",
}

SUFFIX = " · Claude (сравнение)"
INDEX_NAME = "Сравнение прогонов Бизнес"


def log(msg: str) -> None:
    print(msg, flush=True)


def tables_to_bullets(md: str) -> str:
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
                    parts = [
                        f"**{h}:** {c}" for h, c in zip(header, cells) if c and c != "—"
                    ]
                    if parts:
                        out.append("- " + " · ".join(parts))
                i += 1
            out.append("")
            continue
        out.append(line)
        i += 1
    return "\n".join(out)


def prepare_md(md: str, *, original_url: str | None = None) -> str:
    md = re.sub(r"^#\s+[^\n]+\n+", "", md, count=1)
    md = re.sub(r"\[([^\]]+)\]\(([^)]+\.csv)\)", r"\1 (таблица — на основной странице)", md)
    md = re.sub(r"\[([^\]]+)\]\(([^)]*examples/[^)]+)\)", r"\1", md)
    md = tables_to_bullets(md)
    banner = (
        "> **Дубликат для сравнения** (Claude Opus / PR #26). "
        "Основная страница первого прогона (Grok) не изменена. "
        "Рабочие таблицы смотрите на основной странице раздела.\n"
    )
    if original_url:
        banner += f"\n> Основная версия: {original_url}\n"
    return banner + "\n" + md.strip() + "\n"


def find_existing_by_title(token: str, title: str) -> str | None:
    q = nc._request(
        "POST",
        f"/databases/{BUSINESS_SECTION_DB}/query",
        token,
        body={
            "page_size": 50,
            "filter": {"property": "Name", "title": {"equals": title}},
        },
    )
    results = q.get("results") or []
    if results:
        return results[0]["id"]
    return None


def create_or_get_page(
    token: str,
    *,
    title: str,
    description: str,
    apply: bool,
) -> str | None:
    existing = find_existing_by_title(token, title)
    if existing:
        log(f"  reuse existing {title!r} → {existing}")
        if apply:
            nc._request(
                "PATCH",
                f"/pages/{existing}",
                token,
                body={
                    "properties": {
                        "Описание": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {"content": description[:2000]},
                                }
                            ]
                        },
                        "Готово": {"checkbox": False},
                    }
                },
            )
            time.sleep(0.3)
        return existing
    log(f"  create {title!r}")
    if not apply:
        return None
    page = nc._request(
        "POST",
        "/pages",
        token,
        body={
            "parent": {"database_id": BUSINESS_SECTION_DB},
            "properties": {
                "Name": {
                    "title": [{"type": "text", "text": {"content": title}}]
                },
                "Описание": {
                    "rich_text": [
                        {"type": "text", "text": {"content": description[:2000]}}
                    ]
                },
                "Готово": {"checkbox": False},
            },
        },
    )
    time.sleep(0.4)
    return page["id"]


def write_body(
    token: str,
    *,
    page_id: str,
    md: str,
    pages: dict[str, str],
    apply: bool,
) -> int:
    blocks = pilot.md_to_blocks(
        md,
        assets_dir=None,
        token=token if apply else None,
        upload=False,
        pages=pages,
        nest_aside_images=False,
    )
    log(f"    blocks={len(blocks)}")
    for line in nc.summarize_blocks(blocks)[:8]:
        log(f"      {line}")
    if not apply:
        return len(blocks)
    n = nc.clear_page_blocks(token, page_id)
    log(f"    cleared {n}")
    nc.append_children(token, page_id, blocks)
    page = nc.get_page(token, page_id)
    log(f"    OK → {page.get('url')}")
    return len(blocks)


def build_index_md(dup_urls: dict[str, str]) -> str:
    lines = [
        "Страницы-**дубликаты** варианта Claude Opus (PR #26) рядом с основным прогоном Grok (PR #25).",
        "",
        "Основные страницы **не перезаписывались**. Сравнивайте гайды и формулировки; рабочие базы данных — на основных страницах.",
        "",
        "## Основной прогон (Grok / уже в разделе)",
        "",
    ]
    for name, pid in ORIGINALS.items():
        lines.append(f"- [{name}]({nc.notion_page_url(pid)})")
    lines += ["", "## Дубликаты Claude (этот набор)", ""]
    for name, url in dup_urls.items():
        if name == INDEX_NAME:
            continue
        lines.append(f"- [{name}]({url})")
    lines += [
        "",
        "## На что смотреть при сравнении",
        "",
        "1. **Клиенты** — «пять вопросов о прошлом» и светофор сигнала vs портрет первого прогона.",
        "2. **Твой продукт / оффер** — маршрут раздела и формулировки MVP.",
        "3. **Конкуренты** — акцент на status quo.",
        "4. **Необходимые шаги** — связка «риск → шаг».",
        "",
        "После выбора линии дубликаты можно архивировать.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", default=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument(
        "--content-root",
        type=Path,
        default=DEFAULT_CONTENT,
        help="Корень small-business-space-ru с markdown Claude-ветки",
    )
    args = ap.parse_args()
    apply = bool(args.apply)
    content = args.content_root

    token = nc.get_token()
    pages = dict(json.loads(PAGE_MAP.read_text(encoding="utf-8")).get("pages") or {})
    log(f"content={content} apply={apply}")

    # Verify hub files exist
    for name, rel in HUB_FILES.items():
        path = content / rel
        if not path.exists():
            log(f"ERROR missing {path}")
            return 1

    created: dict[str, str] = {}
    urls: dict[str, str] = {}

    # Index page first
    log(f"\n## Index: {INDEX_NAME}")
    index_id = create_or_get_page(
        token,
        title=INDEX_NAME,
        description="Дубликаты Claude рядом с основным прогоном Grok — для сравнения",
        apply=apply,
    )
    if index_id:
        created[INDEX_NAME] = index_id

    for name, rel in HUB_FILES.items():
        title = f"{name}{SUFFIX}"
        log(f"\n## {title}")
        path = content / rel
        orig_id = ORIGINALS[name]
        orig_url = nc.notion_page_url(orig_id)
        page_id = create_or_get_page(
            token,
            title=title,
            description=f"Дубликат Claude (PR #26) для сравнения с «{name}»",
            apply=apply,
        )
        md = prepare_md(path.read_text(encoding="utf-8"), original_url=orig_url)
        if apply and page_id:
            write_body(token, page_id=page_id, md=md, pages=pages, apply=True)
            page = nc.get_page(token, page_id)
            urls[title] = page.get("url") or nc.notion_page_url(page_id)
            created[title] = page_id
        else:
            write_body(token, page_id=orig_id, md=md, pages=pages, apply=False)

    # Fill index body
    log(f"\n## Write index body")
    if apply and index_id:
        # Collect urls
        for title, pid in created.items():
            if title == INDEX_NAME:
                continue
            page = nc.get_page(token, pid)
            urls[title] = page.get("url") or nc.notion_page_url(pid)
        index_md = build_index_md(urls)
        write_body(token, page_id=index_id, md=index_md, pages=pages, apply=True)
        idx = nc.get_page(token, index_id)
        log(f"\nINDEX → {idx.get('url')}")
    else:
        log(build_index_md({f"{n}{SUFFIX}": "(dry-run)" for n in HUB_FILES}))

    # Persist id map for report
    out = ROOT / "docs/reports/notion-business-compare-ids.json"
    if apply:
        payload = {
            "created": created,
            "urls": urls,
            "originals": ORIGINALS,
            "note": "Claude duplicates for comparison; originals untouched",
        }
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        log(f"wrote {out}")

    log("\nDone." + ("" if apply else " DRY-RUN — добавьте --apply"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
