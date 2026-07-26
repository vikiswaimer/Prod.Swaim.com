#!/usr/bin/env python3
"""Синхронизация группы Активность (issue #22) в живую копию SBS в Notion.

- Хабы: Цели, Гипотезы (бывш. Идеи), Задачи, Рефлексия, Заметки, Календарь
- Новая страница: Аналитика
- Переименование Идеи → Гипотезы (+ child DB)
- Обновление Description в DB «Активность»
- Child database на страницах **сохраняются** (не удаляются)

  python3 scripts/notion_sync_activity.py --dry-run
  python3 scripts/notion_sync_activity.py --apply
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

ACTIVITY_DB_ID = "a2a207ca-d379-8344-9a0b-0152fb52fcc0"

PAGES = {
    "Цели": "f18207ca-d379-822c-beaa-8167847859f4",
    "Идеи": "4cf207ca-d379-82eb-baff-81b0dc1af094",  # → Гипотезы
    "Задачи": "57f207ca-d379-83e1-b273-011148ad0665",
    "Рефлексия": "2e9207ca-d379-83ba-8a69-01b6628af5af",
    "Заметки": "b7b207ca-d379-829b-b10b-815737f68e84",
    "Календарь": "6a2207ca-d379-8237-918b-81f8fdd53acd",
}

MD = {
    "Цели": CONTENT / "Активность/Цели--864823f3.md",
    "Идеи": CONTENT / "Активность/Идеи--8e1bd74e.md",
    "Задачи": CONTENT / "Активность/Задачи--c110a4ad.md",
    "Рефлексия": CONTENT / "Активность/Рефлексия--8b9172f7.md",
    "Заметки": CONTENT / "Активность/Заметки--85250681.md",
    "Календарь": CONTENT / "Активность/Календарь--76077d3c.md",
    "Аналитика": CONTENT / "Активность/Аналитика--a1f4c901.md",
}

DESCRIPTIONS = {
    "Цели": "Исходы (outcomes): baseline → target, недельный индикатор, критерий продолжить/изменить/остановить",
    "Гипотезы": "Проверяемые гипотезы: формула, статус, сигнал успеха, ссылка на Linear/GitHub",
    "Задачи": "Тонкий WIP продукта: исследование / эксперимент / поставка / долг (или зеркало Linear/GitHub)",
    "Аналитика": "Measure: MAU/DAU, retention, деньги и инструменты — простым языком",
    "Рефлексия": "Build → Measure → Learn: сила сигнала, pivot/persevere, следующий эксперимент",
    "Календарь": "Таймбокс обучения: интервью, тесты, запуски — не только встречи",
    "Заметки": "Опционально: сырое → в гипотезы; отдельная база часто шум",
}

IDEAS_CHILD_DB = "830207ca-d379-8223-9b27-01ad1f704d88"

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
    """Убрать H1 (title уже в Notion), CSV-ссылки на базы, git/examples."""
    md = re.sub(r"^#\s+[^\n]+\n+", "", md, count=1)
    md = re.sub(r"\n\[[^\]]+\]\([^)]+\.csv\)\s*$", "\n", md)
    md = re.sub(r"^\[[^\]]+\]\([^)]+\.csv\)\s*$", "", md, flags=re.M)
    md = re.sub(r"\[примером заполнения\]\([^)]+\)", "примером заполнения", md)
    md = re.sub(r"\(файл бывш\.[^)]*\)", "", md)
    md = re.sub(r"\(страница бывш\.[^)]*\)", "", md)
    md = re.sub(r"</?b>", "", md, flags=re.I)
    md = re.sub(r"</?strong>", "", md, flags=re.I)
    # Убрать пояснение про rename — в Notion страница уже Гипотезы
    md = re.sub(
        r"В Notion страницу базы можно назвать \*\*Гипотезы\*\*[^\n]*\n?",
        "",
        md,
    )
    return md.strip() + "\n"


def clear_keep_databases(token: str, page_id: str) -> tuple[int, list[str]]:
    """Удалить блоки кроме child_database / child_page. Возвращает (n_deleted, kept_ids)."""
    kids = nc.get_block_children(token, page_id)
    kept: list[str] = []
    deleted = 0
    for b in kids:
        if b.get("type") in ("child_database", "child_page"):
            kept.append(b["id"])
            continue
        nc.delete_block(token, b["id"])
        deleted += 1
        time.sleep(0.3)
    return deleted, kept


def sync_hub(
    token: str,
    *,
    page_id: str,
    md_path: Path,
    pages: dict[str, str],
    apply: bool,
    note_db_order: bool = True,
) -> int:
    md = prepare_md(md_path.read_text(encoding="utf-8"))
    if note_db_order:
        md = (
            "> Таблица базы раздела уже на этой странице — при необходимости "
            "перетащите её **под** гайд.\n\n"
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
    page = nc.get_page(token, page_id)
    title = nc.page_title(page)
    log(f"\n## {title} ({page_id})")
    log(f"blocks: {len(blocks)}")
    for line in nc.summarize_blocks(blocks)[:12]:
        log(f"  {line}")
    if len(blocks) > 12:
        log(f"  ... +{len(blocks) - 12} more")
    if not apply:
        log("DRY-RUN")
        return len(blocks)
    n, kept = clear_keep_databases(token, page_id)
    log(f"cleared {n} prose blocks; kept {len(kept)} db/page children")
    nc.append_children(token, page_id, blocks)
    log(f"appended {len(blocks)} OK → {page.get('url')}")
    return len(blocks)


def set_page_props(
    token: str,
    page_id: str,
    *,
    title: str | None = None,
    description: str | None = None,
) -> None:
    props: dict = {}
    if title is not None:
        props["Name"] = {
            "title": [{"type": "text", "text": {"content": title[:2000]}}]
        }
    if description is not None:
        props["Description"] = {
            "rich_text": [{"type": "text", "text": {"content": description[:2000]}}]
        }
    if not props:
        return
    nc._request("PATCH", f"/pages/{page_id}", token, body={"properties": props})
    time.sleep(0.3)


def rename_database(token: str, database_id: str, title: str) -> None:
    nc._request(
        "PATCH",
        f"/databases/{database_id}",
        token,
        body={"title": [{"type": "text", "text": {"content": title}}]},
    )
    time.sleep(0.3)


def ensure_hypothesis_schema(token: str, database_id: str, apply: bool) -> None:
    """Добавить поля Lean к DB гипотез (не трогаем Trust/Ease/Impact/Score)."""
    db = nc._request("GET", f"/databases/{database_id}", token)
    existing = set((db.get("properties") or {}).keys())
    wanted = {
        "Формулировка": {"rich_text": {}},
        "Как проверим": {"rich_text": {}},
        "Статус": {
            "select": {
                "options": [
                    {"name": "Черновик", "color": "default"},
                    {"name": "Уточнить", "color": "yellow"},
                    {"name": "К проверке", "color": "blue"},
                    {"name": "В работе", "color": "purple"},
                    {"name": "Вывод", "color": "green"},
                    {"name": "Отложена", "color": "orange"},
                    {"name": "Отброшена", "color": "red"},
                ]
            }
        },
        "Сигнал успеха": {"rich_text": {}},
        "Вывод": {"rich_text": {}},
        "Next step": {"rich_text": {}},
        "Ссылка": {"url": {}},
    }
    to_add = {k: v for k, v in wanted.items() if k not in existing}
    log(f"\n## Schema Гипотезы DB ({database_id})")
    log(f"existing: {sorted(existing)}")
    log(f"to_add: {sorted(to_add)}")
    if not to_add:
        log("schema already ok")
        return
    if not apply:
        log("DRY-RUN schema")
        return
    nc._request(
        "PATCH",
        f"/databases/{database_id}",
        token,
        body={"properties": to_add},
    )
    log("schema patched OK")
    time.sleep(0.4)


def find_analytics_page(token: str) -> str | None:
    body: dict = {"page_size": 50}
    while True:
        data = nc._request(
            "POST", f"/databases/{ACTIVITY_DB_ID}/query", token, body=body
        )
        for r in data.get("results") or []:
            if nc.page_title(r).strip() == "Аналитика":
                return r["id"]
        if not data.get("has_more"):
            break
        body["start_cursor"] = data["next_cursor"]
    return None


def create_analytics_page(token: str, apply: bool) -> str:
    existing = find_analytics_page(token)
    if existing:
        log(f"\n## Аналитика already exists ({existing})")
        if apply:
            set_page_props(
                token,
                existing,
                title="Аналитика",
                description=DESCRIPTIONS["Аналитика"],
            )
        return existing
    log("\n## Create Аналитика page in DB Активность")
    if not apply:
        log("DRY-RUN create")
        return "dry-run-analytics"
    page = nc._request(
        "POST",
        "/pages",
        token,
        body={
            "parent": {"database_id": ACTIVITY_DB_ID},
            "properties": {
                "Name": {
                    "title": [{"type": "text", "text": {"content": "Аналитика"}}]
                },
                "Description": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": DESCRIPTIONS["Аналитика"]},
                        }
                    ]
                },
            },
        },
    )
    pid = page["id"]
    log(f"created {pid} → {page.get('url')}")
    time.sleep(0.4)
    return pid


def update_page_map(analytics_id: str) -> None:
    data = json.loads(PAGE_MAP_PATH.read_text(encoding="utf-8"))
    pages = data.setdefault("pages", {})
    # rename key Идеи → Гипотезы (same id)
    ideas_id = pages.pop("Идеи", PAGES["Идеи"])
    pages["Гипотезы"] = ideas_id
    pages["Аналитика"] = analytics_id
    data["count"] = len(pages)
    PAGE_MAP_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    log(f"updated page map → {PAGE_MAP_PATH}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", default=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument(
        "--only",
        choices=[
            "hubs",
            "analytics",
            "rename",
            "schema",
            "tracks",
            "all",
        ],
        default="all",
    )
    args = ap.parse_args()
    apply = bool(args.apply)
    if apply:
        args.dry_run = False

    token = nc.get_token()
    pages = pilot.load_page_map(PAGE_MAP_PATH)
    # aliases for link resolution during this sync
    pages.setdefault("Гипотезы", PAGES["Идеи"])
    pages.setdefault("Идеи", PAGES["Идеи"])
    pilot.TITLE_ALIASES["гипотезы"] = "Гипотезы"
    pilot.TITLE_ALIASES["банк идей"] = "Гипотезы"
    pilot.TITLE_ALIASES["идеи"] = "Гипотезы"

    log(f"mode={'APPLY' if apply else 'DRY-RUN'} only={args.only}")

    if args.only in ("rename", "all"):
        log("\n## Rename Идеи → Гипотезы")
        if apply:
            set_page_props(
                token,
                PAGES["Идеи"],
                title="Гипотезы",
                description=DESCRIPTIONS["Гипотезы"],
            )
            rename_database(token, IDEAS_CHILD_DB, "Гипотезы")
            log("page + child DB renamed")
        else:
            log("DRY-RUN rename")

    if args.only in ("schema", "all"):
        ensure_hypothesis_schema(token, IDEAS_CHILD_DB, apply)

    analytics_id = pages.get("Аналитика") or find_analytics_page(token)
    if args.only in ("analytics", "all"):
        analytics_id = create_analytics_page(token, apply)
        if apply and analytics_id and analytics_id != "dry-run-analytics":
            sync_hub(
                token,
                page_id=analytics_id,
                md_path=MD["Аналитика"],
                pages={**pages, "Аналитика": analytics_id, "Гипотезы": PAGES["Идеи"]},
                apply=True,
                note_db_order=False,
            )

    if args.only in ("hubs", "all"):
        # refresh descriptions for all known rows
        desc_map = {
            PAGES["Цели"]: ("Цели", DESCRIPTIONS["Цели"]),
            PAGES["Идеи"]: ("Гипотезы", DESCRIPTIONS["Гипотезы"]),
            PAGES["Задачи"]: ("Задачи", DESCRIPTIONS["Задачи"]),
            PAGES["Рефлексия"]: ("Рефлексия", DESCRIPTIONS["Рефлексия"]),
            PAGES["Заметки"]: ("Заметки", DESCRIPTIONS["Заметки"]),
            PAGES["Календарь"]: ("Календарь", DESCRIPTIONS["Календарь"]),
        }
        for pid, (name, desc) in desc_map.items():
            log(f"\n## Description: {name}")
            if apply:
                # don't reset title for Идеи here if rename already ran — set Гипотезы
                title = "Гипотезы" if pid == PAGES["Идеи"] else name
                set_page_props(token, pid, title=title, description=desc)
                log("updated")
            else:
                log("DRY-RUN")

        link_pages = {
            **pages,
            "Гипотезы": PAGES["Идеи"],
            "Идеи": PAGES["Идеи"],
        }
        if analytics_id and analytics_id != "dry-run-analytics":
            link_pages["Аналитика"] = analytics_id

        for key, md_path in MD.items():
            if key == "Аналитика":
                continue
            sync_hub(
                token,
                page_id=PAGES[key if key != "Гипотезы" else "Идеи"],
                md_path=md_path,
                pages=link_pages,
                apply=apply,
            )

    if args.only in ("tracks", "all"):
        link_pages = {
            **pages,
            "Гипотезы": PAGES["Идеи"],
            "Идеи": PAGES["Идеи"],
        }
        if analytics_id and analytics_id != "dry-run-analytics":
            link_pages["Аналитика"] = analytics_id
        for name, (pid, md_path) in TRACKS.items():
            # tracks: full clear is OK? They may not have child DBs — check via sync_hub keep
            sync_hub(
                token,
                page_id=pid,
                md_path=md_path,
                pages=link_pages,
                apply=apply,
                note_db_order=False,
            )

    if apply and analytics_id and analytics_id != "dry-run-analytics":
        update_page_map(analytics_id)

    log("\nDone.")
    if not apply:
        log("Это был dry-run. Для записи: python3 scripts/notion_sync_activity.py --apply")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
