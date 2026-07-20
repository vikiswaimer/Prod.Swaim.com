#!/usr/bin/env python3
"""Общий клиент Notion API для Prod.Swaim (token из env)."""

from __future__ import annotations

import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

NOTION_VERSION = "2022-06-28"
API = "https://api.notion.com/v1"


def get_token() -> str:
    for key in ("NOTION_TOKEN", "NotionToken", "NOTION_API_KEY", "NOTION_SECRET"):
        val = os.environ.get(key, "").strip()
        if val:
            return val
    print(
        "Токен не найден в env (NOTION_TOKEN / NotionToken).\n"
        "Секреты Cursor подхватываются обычно только в НОВОМ Cloud Agent run.\n"
        "См. docs/notion-integration.md",
        file=sys.stderr,
    )
    sys.exit(2)


def _request(
    method: str,
    path: str,
    token: str,
    *,
    body: dict | None = None,
    raw_body: bytes | None = None,
    headers: dict | None = None,
    form: list[tuple[str, Any]] | None = None,
) -> Any:
    url = path if path.startswith("http") else f"{API}{path}"
    hdrs = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
    }
    data = None
    if form is not None:
        # multipart for file upload send
        import uuid

        boundary = f"----CursorForm{uuid.uuid4().hex}"
        hdrs["Content-Type"] = f"multipart/form-data; boundary={boundary}"
        chunks: list[bytes] = []
        for name, value in form:
            chunks.append(f"--{boundary}\r\n".encode())
            if isinstance(value, tuple):
                filename, content, ctype = value
                chunks.append(
                    (
                        f'Content-Disposition: form-data; name="{name}"; '
                        f'filename="{filename}"\r\n'
                        f"Content-Type: {ctype}\r\n\r\n"
                    ).encode()
                )
                chunks.append(content)
                chunks.append(b"\r\n")
            else:
                chunks.append(
                    f'Content-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode()
                )
        chunks.append(f"--{boundary}--\r\n".encode())
        data = b"".join(chunks)
    elif raw_body is not None:
        data = raw_body
        if headers:
            hdrs.update(headers)
    elif body is not None:
        data = json.dumps(body).encode()
        hdrs["Content-Type"] = "application/json"
    if headers and form is None and raw_body is None:
        hdrs.update(headers)

    req = urllib.request.Request(url, data=data, method=method, headers=hdrs)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read()
            if not raw:
                return {}
            return json.loads(raw.decode())
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code} {method} {path}: {err}") from e


def search(token: str, query: str = "", *, filter_type: str | None = None) -> list[dict]:
    body: dict[str, Any] = {"page_size": 50}
    if query:
        body["query"] = query
    if filter_type:
        body["filter"] = {"property": "object", "value": filter_type}
    results: list[dict] = []
    while True:
        data = _request("POST", "/search", token, body=body)
        results.extend(data.get("results") or [])
        if not data.get("has_more"):
            break
        body["start_cursor"] = data["next_cursor"]
        if len(results) >= 200:
            break
    return results


def get_page(token: str, page_id: str) -> dict:
    return _request("GET", f"/pages/{page_id}", token)


def get_block_children(token: str, block_id: str) -> list[dict]:
    results: list[dict] = []
    params = "page_size=100"
    path = f"/blocks/{block_id}/children?{params}"
    while True:
        data = _request("GET", path, token)
        results.extend(data.get("results") or [])
        if not data.get("has_more"):
            break
        path = f"/blocks/{block_id}/children?page_size=100&start_cursor={data['next_cursor']}"
    return results


def delete_block(token: str, block_id: str) -> None:
    _request("DELETE", f"/blocks/{block_id}", token)


def append_children(token: str, parent_id: str, children: list[dict]) -> None:
    # Notion limit: 100 children per request
    for i in range(0, len(children), 100):
        chunk = children[i : i + 100]
        _request(
            "PATCH",
            f"/blocks/{parent_id}/children",
            token,
            body={"children": chunk},
        )
        time.sleep(0.35)


def clear_page_blocks(token: str, page_id: str) -> int:
    kids = get_block_children(token, page_id)
    for b in kids:
        delete_block(token, b["id"])
        time.sleep(0.35)
    return len(kids)


def page_title(page: dict) -> str:
    props = page.get("properties") or {}
    for prop in props.values():
        if prop.get("type") == "title":
            parts = prop.get("title") or []
            return "".join(p.get("plain_text", "") for p in parts)
    return ""


def rich(
    text: str,
    *,
    bold: bool = False,
    italic: bool = False,
    code: bool = False,
    link: str | None = None,
) -> list[dict]:
    if not text:
        return []
    # Notion rich_text item limit ~2000 chars
    chunks: list[dict] = []
    for i in range(0, len(text), 1900):
        ann: dict[str, Any] = {
            "bold": bool(bold),
            "italic": bool(italic),
            "strikethrough": False,
            "underline": False,
            "code": bool(code),
            "color": "default",
        }
        item: dict[str, Any] = {
            "type": "text",
            "text": {"content": text[i : i + 1900]},
            "annotations": ann,
        }
        if link:
            item["text"]["link"] = {"url": link}
        chunks.append(item)
    return chunks


def rich_page_mention(page_id: str) -> dict:
    return {
        "type": "mention",
        "mention": {"type": "page", "page": {"id": page_id}},
        "annotations": {
            "bold": False,
            "italic": False,
            "strikethrough": False,
            "underline": False,
            "code": False,
            "color": "default",
        },
    }


def notion_page_url(page_id: str) -> str:
    compact = page_id.replace("-", "")
    return f"https://www.notion.so/{compact}"


def paragraph_rt(rich_text: list[dict]) -> dict:
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": rich_text}}


def heading_rt(level: int, rich_text: list[dict]) -> dict:
    key = {1: "heading_1", 2: "heading_2", 3: "heading_3"}[level]
    return {"object": "block", "type": key, key: {"rich_text": rich_text}}


def bulleted_rt(rich_text: list[dict]) -> dict:
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": rich_text},
    }


def numbered_rt(rich_text: list[dict]) -> dict:
    return {
        "object": "block",
        "type": "numbered_list_item",
        "numbered_list_item": {"rich_text": rich_text},
    }


def quote_rt(rich_text: list[dict]) -> dict:
    return {"object": "block", "type": "quote", "quote": {"rich_text": rich_text}}


def to_do_rt(rich_text: list[dict], *, checked: bool = False) -> dict:
    return {
        "object": "block",
        "type": "to_do",
        "to_do": {"rich_text": rich_text, "checked": checked},
    }


def paragraph(text: str, **ann) -> dict:
    return paragraph_rt(rich(text, **ann))


def heading(level: int, text: str) -> dict:
    return heading_rt(level, rich(text))


def bulleted(text: str, *, italic: bool = False) -> dict:
    return bulleted_rt(rich(text, italic=italic))


def numbered(text: str, *, italic: bool = False) -> dict:
    return numbered_rt(rich(text, italic=italic))


def quote(text: str) -> dict:
    return quote_rt(rich(text))


def divider() -> dict:
    return {"object": "block", "type": "divider", "divider": {}}


def callout(
    text: str,
    emoji: str = "💡",
    *,
    children: list[dict] | None = None,
    rich_text: list[dict] | None = None,
) -> dict:
    payload: dict[str, Any] = {
        "rich_text": rich_text if rich_text is not None else rich(text),
        "icon": {"type": "emoji", "emoji": emoji},
    }
    if children:
        payload["children"] = children
    return {"object": "block", "type": "callout", "callout": payload}


def to_do(text: str, *, checked: bool = False) -> dict:
    return to_do_rt(rich(text), checked=checked)


def image_external(url: str) -> dict:
    return {
        "object": "block",
        "type": "image",
        "image": {"type": "external", "external": {"url": url}},
    }


def image_file_upload(upload_id: str) -> dict:
    return {
        "object": "block",
        "type": "image",
        "image": {"type": "file_upload", "file_upload": {"id": upload_id}},
    }


def upload_local_file(token: str, path: Path) -> str:
    """Direct upload ≤20MB → returns file_upload id."""
    data = path.read_bytes()
    ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    created = _request(
        "POST",
        "/file_uploads",
        token,
        body={"filename": path.name, "content_type": ctype},
    )
    upload_id = created["id"]
    send_url = created.get("upload_url") or f"{API}/file_uploads/{upload_id}/send"
    _request(
        "POST",
        send_url,
        token,
        form=[("file", (path.name, data, ctype))],
    )
    return upload_id


def summarize_blocks(blocks: list[dict], *, depth: int = 0) -> list[str]:
    lines: list[str] = []
    pad = "  " * depth
    for b in blocks:
        t = b.get("type")
        payload = b.get(t) or {}
        rts = payload.get("rich_text") or []
        parts: list[str] = []
        for x in rts:
            parts.append(x.get("plain_text") or (x.get("text") or {}).get("content") or "")
        plain = "".join(parts)[:80]
        extra = ""
        link_n = sum(1 for x in rts if (x.get("text") or {}).get("link"))
        if link_n:
            extra += f" links={link_n}"
        if t == "image":
            img = payload
            extra += f" {img.get('type')}"
        if t == "callout":
            icon = payload.get("icon") or {}
            if icon.get("type") == "emoji":
                extra += f" icon={icon.get('emoji', '')}"
            else:
                extra += f" icon_type={icon.get('type')}"
            kids = payload.get("children") or []
            if kids:
                extra += f" children={len(kids)}"
        if t == "to_do":
            extra += f" checked={payload.get('checked')}"
        lines.append(f"{pad}{t}{extra}: {plain}")
        kids = payload.get("children") or []
        if kids and depth < 2:
            lines.extend(summarize_blocks(kids, depth=depth + 1))
    return lines
