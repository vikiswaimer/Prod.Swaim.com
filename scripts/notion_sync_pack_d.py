#!/usr/bin/env python3
"""Синхронизация пакета D (issue #8) в живую копию SBS в Notion.

Точечно:
  - Instructions (+ блок «Работа с ИИ»)
  - Развитие своего бизнеса (примечание про пароли)
  - Пароли (новый текст; пустая архивная БД без демо-секретов)
  - Финансовый отчёт (текст + схема налога %; без демо-строки)
  - Оценка (очистка демо-строки)
  - Задачи: Untitled → «Пример задачи…»
  - INV-0001 помечен как пример

  python3 scripts/notion_sync_pack_d.py --dry-run
  python3 scripts/notion_sync_pack_d.py --apply
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import notion_client as nc  # noqa: E402
import notion_sync_pilot as pilot  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PAGE_MAP = ROOT / "docs/reports/notion-sbs-page-map.json"

PAGES = {
    "Instructions": "e45207ca-d379-83cb-af54-01ada6afeab0",
    "Развитие своего бизнеса": "329207ca-d379-837b-9966-81eee8afa61d",
    "Пароли": "a9f207ca-d379-831a-9185-0192f489348b",
    "Финансовый отчет": "1a2207ca-d379-8379-b2c9-010d04bba86a",
    "Оценка": "c79207ca-d379-83b0-841d-81d040e09089",
    "Задачи": "57f207ca-d379-83e1-b273-011148ad0665",
    "Счет-фактуры": "ba9207ca-d379-821c-b9fb-01f8546447d2",
}

# child DB ids (finance DB пересоздаётся при sync — актуальный id после apply)
FIN_DB_ID = "3a3207ca-d379-81d9-a7b3-e250f7328fda"  # было 18c207ca-… до pack-d sync
EVAL_DB_ID = "7d8207ca-d379-8317-9eff-817522e99b89"
TASKS_DB_ID = "331207ca-d379-8357-88f5-01bbb91f40b5"
INV_DB_ID = "df8207ca-d379-8252-854c-01cfd787b9f9"
PASSWORDS_DB_ID = "3a3207ca-d379-81c7-b6ad-dde481d961cb"


def log(msg: str) -> None:
    print(msg, flush=True)


def prepare_md(md: str) -> str:
    """Убрать отсылки к Git/docs из пользовательского контента (пакет D)."""
    import re

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
    return md


def sync_full_page(
    token: str,
    *,
    page_id: str,
    md_path: Path,
    assets_dir: Path | None,
    pages: dict[str, str],
    apply: bool,
) -> int:
    md = prepare_md(md_path.read_text(encoding="utf-8"))
    blocks = pilot.md_to_blocks(
        md,
        assets_dir=assets_dir,
        token=token if apply else None,
        upload=apply,
        pages=pages,
        nest_aside_images=False,
    )
    page = nc.get_page(token, page_id)
    title = nc.page_title(page)
    log(f"\n## {title} ({page_id})")
    log(f"blocks: {len(blocks)}")
    for line in nc.summarize_blocks(blocks)[:20]:
        log(f"  {line}")
    if len(blocks) > 20:
        log(f"  ... +{len(blocks) - 20} more")
    if not apply:
        log("DRY-RUN")
        return len(blocks)
    n = nc.clear_page_blocks(token, page_id)
    log(f"cleared {n}")
    nc.append_children(token, page_id, blocks)
    log(f"appended {len(blocks)} OK → {page.get('url')}")
    return len(blocks)


def query_all(token: str, database_id: str) -> list[dict]:
    results: list[dict] = []
    body: dict = {"page_size": 50}
    while True:
        data = nc._request("POST", f"/databases/{database_id}/query", token, body=body)
        results.extend(data.get("results") or [])
        if not data.get("has_more"):
            break
        body["start_cursor"] = data["next_cursor"]
    return results


def archive_page(token: str, page_id: str) -> None:
    nc._request("PATCH", f"/pages/{page_id}", token, body={"archived": True})


def set_title(token: str, page_id: str, title_prop: str, title: str) -> None:
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


def sync_passwords(token: str, pages: dict[str, str], apply: bool) -> None:
    page_id = PAGES["Пароли"]
    md_path = ROOT / "content/small-business-space-ru/Other/Пароли--ab1df728.md"
    md = prepare_md(md_path.read_text(encoding="utf-8"))
    # убрать CSV-ссылку — в Notion останется child_database
    import re

    md = re.sub(r"\n?\[Таблица[^\]]*\]\([^)]+\)\n?", "\n", md)
    blocks = pilot.md_to_blocks(
        md,
        assets_dir=ROOT / "content/small-business-space-ru/Other/Пароли",
        token=token if apply else None,
        upload=False,
        pages=pages,
    )
    log(f"\n## Пароли ({page_id})")
    log(f"text blocks: {len(blocks)}")
    for line in nc.summarize_blocks(blocks):
        log(f"  {line}")
    if not apply:
        log("DRY-RUN: БД Password manager будет пересоздана пустой")
        return

    # Полная замена: демо-пароли из шаблона убираем
    n = nc.clear_page_blocks(token, page_id)
    log(f"cleared {n} (включая старую Password manager)")
    # текст + пустая БД
    nc.append_children(token, page_id, blocks)
    nc._request(
        "POST",
        "/databases",
        token,
        body={
            "parent": {"type": "page_id", "page_id": page_id},
            "title": [{"type": "text", "text": {"content": "Password manager"}}],
            "properties": {
                "Account": {"title": {}},
                "Email/Username": {"rich_text": {}},
                "Website": {"url": {}},
                "Password": {"rich_text": {}},
            },
        },
    )
    log("recreated empty Password manager DB")
    # title страницы
    set_title(token, page_id, "Name", "Пароли (не ядро шаблона)")
    # усилить «не ядро» в первом абзаце
    kids = nc.get_block_children(token, page_id)
    if kids and kids[0].get("type") == "paragraph":
        nc._request(
            "PATCH",
            f"/blocks/{kids[0]['id']}",
            token,
            body={
                "paragraph": {
                    "rich_text": nc.rich(
                        "Этот раздел — не ядро шаблона. Рекомендация: не храните рабочие "
                        "пароли и секреты в Notion и в копии шаблона. Это риск при шаринге "
                        "пространства, экспорте и работе с ИИ."
                    )
                }
            },
        )
    log(nc.get_page(token, page_id).get("url"))


def sync_finance_report(token: str, pages: dict[str, str], apply: bool) -> None:
    """Intro + новая БД: Tax rate % и Taxes — editable; без демо-строки и без 30%."""
    page_id = PAGES["Финансовый отчет"]
    md_path = ROOT / "content/small-business-space-ru/Финансы/Финансовый отчет--c1992c57.md"
    md = prepare_md(md_path.read_text(encoding="utf-8"))
    import re

    md = re.sub(r"\n?---\n?", "\n", md)
    md = re.sub(r"\n?\[[^\]]*\]\([^)]+\.csv\)\n?", "\n", md)
    blocks = pilot.md_to_blocks(
        md,
        assets_dir=None,
        token=None,
        upload=False,
        pages=pages,
    )
    log(f"\n## Финансовый отчет ({page_id})")
    for line in nc.summarize_blocks(blocks):
        log(f"  {line}")

    try:
        db = nc._request("GET", f"/databases/{FIN_DB_ID}", token)
        props = db.get("properties") or {}
        log(f"old props: {list(props.keys())}")
        rows = query_all(token, FIN_DB_ID)
        log(f"old rows: {[nc.page_title(r) for r in rows]}")
    except RuntimeError as e:
        log(f"old finance DB unavailable (ok if recreating): {e}")

    if not apply:
        log("DRY-RUN: recreate DB — Tax rate % + Taxes (числа), Profit формулы, 0 строк")
        return

    n = nc.clear_page_blocks(token, page_id)
    log(f"full clear {n}")
    nc.append_children(token, page_id, blocks)

    # Taxes — число (✏️), считаете сами или от ставки; Profit — формулы.
    created = nc._request(
        "POST",
        "/databases",
        token,
        body={
            "parent": {"type": "page_id", "page_id": page_id},
            "title": [{"type": "text", "text": {"content": "Финансовый отчет"}}],
            "properties": {
                "Date": {"title": {}},
                "Income": {"number": {"format": "dollar"}},
                "Expenses": {"number": {"format": "dollar"}},
                "✏️ Tax rate %": {"number": {"format": "number"}},
                "✏️ Taxes": {"number": {"format": "dollar"}},
                "⛔️ Profit": {
                    "formula": {
                        "expression": (
                            'prop("Income") - prop("Expenses") - '
                            'if(empty(prop("✏️ Taxes")), 0, prop("✏️ Taxes"))'
                        )
                    }
                },
                "⛔️ Profit %": {
                    "formula": {
                        "expression": (
                            'if(empty(prop("Income")) or prop("Income") == 0, 0, '
                            'floor(((prop("Income") - prop("Expenses") - '
                            'if(empty(prop("✏️ Taxes")), 0, prop("✏️ Taxes"))) '
                            '/ prop("Income")) * 100) * 0.01)'
                        )
                    }
                },
            },
        },
    )
    log(f"created finance DB {created['id']}")
    log(nc.get_page(token, page_id).get("url"))


def sync_evaluation(token: str, apply: bool) -> None:
    log(f"\n## Оценка DB ({EVAL_DB_ID})")
    rows = query_all(token, EVAL_DB_ID)
    log(f"rows before: {[(r['id'], nc.page_title(r)) for r in rows]}")
    if not apply:
        log("DRY-RUN: archive demo rows")
        return
    for r in rows:
        title = nc.page_title(r) or ""
        # очищаем демо-цифры: архивируем строки с данными
        props = r.get("properties") or {}
        income = (props.get("Income") or {}).get("number")
        expenses = (props.get("Expenses") or {}).get("number")
        if income is not None or expenses is not None or title.strip():
            archive_page(token, r["id"])
            log(f"archived demo row {title!r} {r['id']}")
            time.sleep(0.35)
    log("Оценка: демо очищены")


def sync_tasks(token: str, apply: bool) -> None:
    log(f"\n## Задачи DB ({TASKS_DB_ID})")
    rows = query_all(token, TASKS_DB_ID)
    for r in rows:
        log(f"  row {r['id']} title={nc.page_title(r)!r}")
    if not apply:
        log("DRY-RUN: rename empty/Untitled → Пример задачи")
        return
    for r in rows:
        title = (nc.page_title(r) or "").strip()
        if title and title.lower() not in ("untitled",):
            continue
        set_title(token, r["id"], "Название", "Пример задачи (удалите или замените)")
        # тело страницы
        kids = nc.get_block_children(token, r["id"])
        if not kids:
            nc.append_children(
                token,
                r["id"],
                [
                    nc.paragraph(
                        "Демо-запись из шаблона. Создайте свои задачи или удалите эту, "
                        "чтобы база оставалась чистой."
                    )
                ],
            )
        log(f"renamed task {r['id']}")
        time.sleep(0.35)


def sync_invoice(token: str, apply: bool) -> None:
    log(f"\n## Счет-фактуры / INV-0001 ({INV_DB_ID})")
    rows = query_all(token, INV_DB_ID)
    target = None
    for r in rows:
        t = nc.page_title(r)
        log(f"  row {r['id']} title={t!r}")
        if t and t.startswith("INV-0001"):
            target = r
    if not target:
        log("INV-0001 not found")
        return
    if not apply:
        log("DRY-RUN: rename + demo callout")
        return
    set_title(token, target["id"], "Name", "INV-0001 (пример)")
    # prepend notice: append at end with callout if not present
    kids = nc.get_block_children(token, target["id"])
    already = False
    for b in kids:
        t = b.get("type")
        payload = b.get(t) or {}
        plain = "".join(
            x.get("plain_text", "") for x in (payload.get("rich_text") or [])
        )
        if "демо" in plain.lower() or "пример" in plain.lower():
            already = True
            break
    if not already:
        # Вставим callout в начало: append в конец, затем... оставим сверху через
        # удаление пустого первого paragraph и вставку after — упрощённо append в конец.
        nc.append_children(
            token,
            target["id"],
            [
                nc.callout(
                    "Это демо-счёт для понимания структуры. Замените данными или "
                    "удалите после дублирования шаблона. Tax — ваша ставка, не фиксированные 30%.",
                    "💡",
                )
            ],
        )
    log(f"updated INV {target['id']}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", default=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument(
        "--only",
        choices=[
            "instructions",
            "development",
            "passwords",
            "finance",
            "evaluation",
            "tasks",
            "invoice",
            "all",
        ],
        default="all",
    )
    args = ap.parse_args()
    apply = bool(args.apply)
    if apply:
        args.dry_run = False

    token = nc.get_token()
    pages = pilot.load_page_map(PAGE_MAP)
    log(f"mode={'APPLY' if apply else 'DRY-RUN'} page_map={len(pages)}")

    only = args.only
    if only in ("all", "instructions"):
        sync_full_page(
            token,
            page_id=PAGES["Instructions"],
            md_path=ROOT / "content/small-business-space-ru/Instructions/_index.md",
            assets_dir=ROOT / "content/small-business-space-ru/Instructions",
            pages=pages,
            apply=apply,
        )
    if only in ("all", "development"):
        sync_full_page(
            token,
            page_id=PAGES["Развитие своего бизнеса"],
            md_path=ROOT
            / "content/small-business-space-ru/Быстрый старт/Развитие своего бизнеса--d23a7834.md",
            assets_dir=None,
            pages=pages,
            apply=apply,
        )
    if only in ("all", "passwords"):
        sync_passwords(token, pages, apply)
    if only in ("all", "finance"):
        sync_finance_report(token, pages, apply)
    if only in ("all", "evaluation"):
        sync_evaluation(token, apply)
    if only in ("all", "tasks"):
        sync_tasks(token, apply)
    if only in ("all", "invoice"):
        sync_invoice(token, apply)

    log("\nDONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
