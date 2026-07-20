#!/usr/bin/env python3
"""Smoke-check доступа к Notion API через NOTION_TOKEN.

Без токена печатает чеклист из docs/notion-integration.md и выходит с кодом 2.
С токеном: GET /v1/users/me и опционально GET /v1/pages/{NOTION_ROOT_PAGE_ID}.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

NOTION_VERSION = "2022-06-28"
API = "https://api.notion.com/v1"


def request(method: str, path: str, token: str) -> dict:
    req = urllib.request.Request(
        f"{API}{path}",
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def main() -> int:
    token = os.environ.get("NOTION_TOKEN", "").strip()
    if not token:
        print(
            "NOTION_TOKEN не задан.\n"
            "1) Создайте Internal Integration: https://www.notion.so/my-integrations\n"
            "2) Подключите её к корневой странице шаблона (⋯ → Connections)\n"
            "3) Добавьте секрет в Cursor Cloud secrets / env как NOTION_TOKEN\n"
            "Подробности: docs/notion-integration.md"
        )
        return 2

    try:
        me = request("GET", "/users/me", token)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code} /users/me: {body}")
        return 1

    bot = me.get("bot") or {}
    owner = bot.get("owner") or {}
    print("OK /users/me")
    print(f"  type={me.get('type')} name={me.get('name')}")
    print(f"  owner={owner.get('type')} workspace={bool(bot.get('workspace_name') or owner)}")

    page_id = os.environ.get("NOTION_ROOT_PAGE_ID", "").strip()
    if page_id:
        # Notion page ids в URL часто без дефисов — API принимает оба вида
        try:
            page = request("GET", f"/pages/{page_id}", token)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            print(f"HTTP {e.code} /pages/{page_id}: {body}")
            print(
                "Частая причина: integration не добавлена в Connections этой страницы."
            )
            return 1
        title = page.get("properties", {}).get("title") or page.get("properties", {})
        print(f"OK /pages/{page_id} object={page.get('object')} archived={page.get('archived')}")
        print(f"  url={page.get('url')}")
        print(f"  properties_keys={list(page.get('properties', {}).keys())[:8]}")
        _ = title
    else:
        print("NOTION_ROOT_PAGE_ID не задан — пропуск проверки страницы.")

    print("Smoke OK. Можно переходить к точечным правкам страниц.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
