#!/usr/bin/env python3
"""Заменить контейнер «Пространство v2» в конце SBS на rich-пилот (Клиенты).

  python3 scripts/notion_sync_space_v2_rich.py --dry-run
  python3 scripts/notion_sync_space_v2_rich.py --apply

Архивирует старый контейнер (если есть) и создаёт новый в конце корня.
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

ROOT_DEFAULT = "dcf207ca-d379-82b8-9fa8-013434ecd77f"
OLD_TITLES = {"Пространство v2 (черновик)", "Пространство v2 — решения"}
NEW_TITLE = "Пространство v2 — решения"
GIT_ROOT = Path("content/small-business-space-ru/Пространство-v2")
REPORT_PATH = Path("docs/reports/notion-space-v2-page-map.json")
REPORT_MD = Path("docs/reports/space-v2-clients-rich.md")

HEADING_RE = re.compile(r"^(#{1,3})\s+(.*)$")
TODO_RE = re.compile(r"^[-*]\s+\[([ xX])\]\s+(.*)$")
BULLET_RE = re.compile(r"^[-*]\s+(.*)$")
NUM_RE = re.compile(r"^(\d+)\.\s+(.*)$")
QUOTE_RE = re.compile(r"^>\s?(.*)$")
FENCE_RE = re.compile(r"^```(\w*)\s*$")
TABLE_LINE_RE = re.compile(r"^\|(.+)\|\s*$")
SEP_RE = re.compile(r"^\s*\|?\s*:?-{3,}")


def plain(text: str) -> str:
    text = text.replace("**", "").replace("__", "").replace("`", "")
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text.strip()


def parse_md_table(lines: list[str], start: int) -> tuple[list[list[str]] | None, int]:
    rows: list[list[str]] = []
    i = start
    while i < len(lines) and TABLE_LINE_RE.match(lines[i]):
        raw = lines[i].strip()
        if "-" in raw and re.match(r"^\|?[\s\-:|]+$", raw):
            i += 1
            continue
        cells = [plain(c) for c in raw.strip("|").split("|")]
        rows.append(cells)
        i += 1
    if len(rows) < 2:
        return None, start
    return rows, i


def md_to_blocks(md: str) -> list[dict]:
    lines = md.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    blocks: list[dict] = []
    i = 0
    para: list[str] = []

    def flush() -> None:
        nonlocal para
        if not para:
            return
        blocks.append(nc.paragraph(plain(" ".join(para))))
        para = []

    while i < len(lines):
        line = lines[i]
        if not line.strip():
            flush()
            i += 1
            continue

        m_fence = FENCE_RE.match(line.strip())
        if m_fence:
            flush()
            lang = m_fence.group(1) or "plain text"
            if lang in ("text", "txt", ""):
                lang = "plain text"
            i += 1
            buf: list[str] = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            body = "\n".join(buf)
            # Notion code rich_text limit ~2000
            if len(body) > 1900:
                body = body[:1900] + "\n…"
            blocks.append(nc.code_block(body, language=lang if lang != "plain text" else "plain text"))
            continue

        table_rows, next_i = parse_md_table(lines, i)
        if table_rows is not None:
            flush()
            # Notion table max practical ~ rows; split if huge
            blocks.append(nc.table(table_rows, has_column_header=True))
            i = next_i
            continue

        if line.strip() == "---":
            flush()
            blocks.append(nc.divider())
            i += 1
            continue

        m_h = HEADING_RE.match(line)
        if m_h:
            flush()
            blocks.append(nc.heading(len(m_h.group(1)), plain(m_h.group(2))))
            i += 1
            continue

        m_q = QUOTE_RE.match(line)
        if m_q:
            flush()
            blocks.append(nc.quote(plain(m_q.group(1))))
            i += 1
            continue

        m_todo = TODO_RE.match(line)
        if m_todo:
            flush()
            blocks.append(nc.to_do(plain(m_todo.group(2)), checked=m_todo.group(1).lower() == "x"))
            i += 1
            continue

        m_b = BULLET_RE.match(line)
        if m_b:
            flush()
            blocks.append(nc.bulleted(plain(m_b.group(1))))
            i += 1
            continue

        m_n = NUM_RE.match(line)
        if m_n:
            flush()
            blocks.append(nc.numbered(plain(m_n.group(2))))
            i += 1
            continue

        para.append(line.strip())
        i += 1

    flush()
    return blocks


def find_child_page(token: str, parent_id: str, title: str) -> str | None:
    for b in nc.get_block_children(token, parent_id):
        if b.get("type") == "child_page" and (b.get("child_page") or {}).get("title") == title:
            return b["id"]
    return None


def archive_block(token: str, block_id: str) -> None:
    nc.delete_block(token, block_id)
    time.sleep(0.4)


def cleanup_root_markers(token: str, root: str) -> None:
    """Убрать хвостовые маркеры прошлой секции v2 (divider/heading/paragraph)."""
    kids = nc.get_block_children(token, root)
    for b in kids:
        t = b.get("type")
        if t == "child_page":
            title = (b.get("child_page") or {}).get("title") or ""
            if title in OLD_TITLES or title == NEW_TITLE:
                print(f"Archive leftover child_page: {title}")
                archive_block(token, b["id"])
            continue
        payload = b.get(t) or {}
        rts = payload.get("rich_text") or []
        text = "".join(x.get("plain_text", "") for x in rts).strip()
        if t == "heading_2" and "Пространство v2" in text:
            archive_block(token, b["id"])
        elif t == "paragraph" and (
            text.startswith("Новый каркас для теста")
            or text.startswith("Плотный формат:")
        ):
            archive_block(token, b["id"])


def build_parent_blocks(page_ids: dict[str, str]) -> list[dict]:
    return [
        nc.callout(
            "Не пустой canvas. Набор комплексных решений под боли фаундера / PM / предпринимателя: "
            "алгоритм + пример + визуал + антипаттерн. Модули v1 не заменяются — этот блок в конце для теста формата.",
            "🧪",
        ),
        nc.heading(2, "Единица ценности"),
        nc.numbered("Боль — человеческим языком"),
        nc.numbered("Симптомы — когда это про вас"),
        nc.numbered("Алгоритм — шаги"),
        nc.numbered("Пример — заполненный кейс"),
        nc.numbered("Визуал — схема / нормы / scorecard"),
        nc.numbered("Артефакты — шаблоны"),
        nc.numbered("Метрика успеха"),
        nc.numbered("Антипаттерн"),
        nc.heading(2, "Группы"),
        nc.table(
            [
                ["Группа", "Статус", "Смысл"],
                ["Клиенты", "✅ пилот", "Спрос, разговоры, воронка, приоритет"],
                ["Сейчас", "очередь", "Операционный пульс"],
                ["Продукт", "очередь", "Ценность и MVP-срез"],
                ["Рост", "очередь", "Эксперименты и каналы"],
                ["Деньги", "очередь", "Выживаемость и цена"],
                ["База", "очередь", "Память решений"],
            ]
        ),
        nc.heading(2, "С чего начать"),
        nc.numbered("Откройте «Клиенты» — первый полный пилот"),
        nc.numbered("Пройдите пакеты по боли, которая жжёт"),
        nc.numbered("Один пакет → одно действие на неделе"),
        nc.divider(),
        nc.paragraph("Страницы групп — ниже."),
    ]


PACKS = [
    ("01. Диагностика ICP", "01-диагностика-icp.md", "🎯"),
    ("02. Разговоры без самообмана", "02-разговоры-без-самообмана.md", "🗣️"),
    ("03. Воронка с нормами", "03-воронка-с-нормами.md", "📉"),
    ("04. Кого звать следующим", "04-кого-звать-следующим.md", "☎️"),
    ("05. Возражения и фидыбэк", "05-возражения-и-фидбек.md", "🛡️"),
]

QUEUE_GROUPS = [
    ("Сейчас", "🏠", "Сейчас/_index.md"),
    ("Продукт", "🎯", "Продукт/_index.md"),
    ("Рост", "📣", "Рост/_index.md"),
    ("Деньги", "💰", "Деньги/_index.md"),
    ("База", "🧠", "База/_index.md"),
]


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

    clients_index = (GIT_ROOT / "Клиенты/_index.md").read_text(encoding="utf-8")
    pack_files = {
        title: (GIT_ROOT / "Клиенты" / fname).read_text(encoding="utf-8")
        for title, fname, _ in PACKS
    }

    print(f"Parent title: {NEW_TITLE}")
    print(f"Packs: {len(PACKS)}")
    for title, fname, _ in PACKS:
        blocks = md_to_blocks(pack_files[title])
        print(f"  {title}: {len(blocks)} blocks from {fname}")

    if args.dry_run and not args.apply:
        print("DRY-RUN: Notion не менялся. Запустите с --apply")
        return 0

    # 1) архив старых контейнеров
    for title in list(OLD_TITLES | {NEW_TITLE}):
        existing = find_child_page(token, root, title)
        if existing:
            print(f"Archive old: {title} ({existing})")
            archive_block(token, existing)

    cleanup_root_markers(token, root)

    # 2) маркер + новый parent
    nc.append_children(
        token,
        root,
        [
            nc.divider(),
            nc.heading(2, "Пространство v2 — решения"),
            nc.paragraph(
                "Плотный формат: боль → пакет решения → пример → визуал. "
                "Пилот: группа Клиенты. Модули выше не заменяются."
            ),
        ],
    )

    # create parent with intro; groups as children after
    parent = nc.create_page(
        token,
        parent_page_id=root,
        title=NEW_TITLE,
        icon_emoji="🧪",
        children=build_parent_blocks({}),
    )
    parent_id = parent["id"]
    print(f"Parent: {nc.notion_page_url(parent_id)}")

    pages: dict[str, str] = {NEW_TITLE: parent_id}

    # 3) Клиенты hub + packs
    clients_page = nc.create_page(
        token,
        parent_page_id=parent_id,
        title="Клиенты",
        icon_emoji="👥",
        children=md_to_blocks(clients_index)[:90],
    )
    clients_id = clients_page["id"]
    pages["Клиенты"] = clients_id
    print(f"  Клиенты: {clients_id}")

    for title, fname, emoji in PACKS:
        md = pack_files[title]
        blocks = md_to_blocks(md)
        page = nc.create_page(
            token,
            parent_page_id=clients_id,
            title=title,
            icon_emoji=emoji,
            children=blocks[:100],
        )
        # leftover
        if len(blocks) > 100:
            nc.append_children(token, page["id"], blocks[100:])
        pages[title] = page["id"]
        print(f"    + {title}: {page['id']} ({len(blocks)} blocks)")

    # 4) queue groups
    for title, emoji, rel in QUEUE_GROUPS:
        md = (GIT_ROOT / rel).read_text(encoding="utf-8")
        page = nc.create_page(
            token,
            parent_page_id=parent_id,
            title=title,
            icon_emoji=emoji,
            children=md_to_blocks(md)[:80],
        )
        pages[title] = page["id"]
        print(f"  {title}: {page['id']}")

    report = {
        "issue": 30,
        "root_page_id": root,
        "parent_title": NEW_TITLE,
        "parent_page_id": parent_id,
        "parent_url": nc.notion_page_url(parent_id),
        "pages": pages,
        "git_path": "content/small-business-space-ru/Пространство-v2/",
        "pilot": "Клиенты",
        "replaced": "Пространство v2 (черновик)",
    }
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(
        f"""# Отчёт: Пространство v2 rich — пилот Клиенты

**Issue:** [#30](https://github.com/vikiswaimer/Prod.Swaim.com/issues/30)  
**Notion:** {nc.notion_page_url(parent_id)}

## Что сделано

- Старый контейнер «Пространство v2 (черновик)» заменён
- Новый формат: боль → пакет → пример → визуал
- Пилот **Клиенты**: 5 пакетов решений + сквозной кейс Studio North
- Остальные группы: карты болей (очередь)

## Пакеты Клиенты

1. Диагностика ICP  
2. Разговоры без самообмана  
3. Воронка с нормами  
4. Кого звать следующим  
5. Возражения и фидыбэк  

Карта id: `docs/reports/notion-space-v2-page-map.json`
""",
        encoding="utf-8",
    )
    print(f"Saved {REPORT_PATH}")
    print(f"Saved {REPORT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
