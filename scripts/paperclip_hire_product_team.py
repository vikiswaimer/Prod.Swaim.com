#!/usr/bin/env python3
"""Идемпотентный найм продуктовой команды в Paperclip.

Читает docs/paperclip-hires.json. Создаёт отсутствующих агентов, паузит HOLD.
Не будит всю команду.

Env:
  PAPERCLIP_API_KEY          обязателен
  PAPERCLIP_API_BASE_URL     по умолчанию https://paperclip.inc
                             (локально: http://127.0.0.1:3100)

Коды выхода:
  0 — ок (созданы / уже были)
  2 — нет ключа
  3 — API ошибка
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "docs" / "paperclip-hires.json"


def api_base() -> str:
    raw = os.environ.get("PAPERCLIP_API_BASE_URL", "https://paperclip.inc").rstrip("/")
    if raw.endswith("/api"):
        return raw
    return f"{raw}/api"


def request(method: str, path: str, key: str, body: dict | None = None) -> tuple[int, object]:
    url = f"{api_base()}{path}"
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8") or "null"
            return resp.status, json.loads(raw)
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            parsed: object = json.loads(raw)
        except json.JSONDecodeError:
            parsed = {"error": raw}
        return exc.code, parsed


def unwrap_list(payload: object) -> list:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for k in ("agents", "companies", "data", "items"):
            if isinstance(payload.get(k), list):
                return payload[k]
    return []


def name_key(name: str) -> str:
    return " ".join(name.lower().split())


def find_company_id(key: str) -> str | None:
    code, payload = request("GET", "/companies", key)
    if code == 401:
        print("unauthorized: проверьте PAPERCLIP_API_KEY", file=sys.stderr)
        return None
    if code >= 400:
        print(f"GET /companies → {code} {payload}", file=sys.stderr)
        return None
    companies = unwrap_list(payload)
    if not companies:
        print("компаний нет — создайте company в UI Paperclip", file=sys.stderr)
        return None
    if len(companies) > 1:
        print(f"компаний {len(companies)}; берём первую: {companies[0].get('name') or companies[0].get('id')}")
    cid = companies[0].get("id")
    return str(cid) if cid else None


def existing_by_name(agents: list) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for a in agents:
        n = a.get("name") or ""
        if n:
            out[name_key(n)] = a
    return out


def adapter_config(spec_agent: dict) -> dict:
    enabled = bool(spec_agent.get("heartbeatEnabled"))
    interval = int(spec_agent.get("heartbeatIntervalSec") or 3600)
    return {
        "heartbeatSchedule": {
            "enabled": enabled,
            "intervalSec": interval,
            "maxConcurrentRuns": 1,
        }
    }


def main() -> int:
    key = os.environ.get("PAPERCLIP_API_KEY", "").strip()
    if not key:
        print(
            "нет PAPERCLIP_API_KEY — найм в Paperclip не выполнен.\n"
            "Канон: docs/reports/paperclip-product-team.md и docs/paperclip-hires.json\n"
            "Инжект ключа в Cloud env, затем: python3 scripts/paperclip_hire_product_team.py",
            file=sys.stderr,
        )
        return 2

    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    company_id = find_company_id(key)
    if not company_id:
        return 3

    code, payload = request("GET", f"/companies/{company_id}/agents", key)
    if code >= 400:
        print(f"GET agents → {code} {payload}", file=sys.stderr)
        return 3

    agents = unwrap_list(payload)
    by_name = existing_by_name(agents)
    print(f"компания {company_id}: уже {len(agents)} агент(ов)")
    for a in agents:
        print(f"  - {a.get('name')}  role={a.get('role')}  status={a.get('status')}  id={a.get('id')}")

    created_ids: dict[str, str] = {}
    for spec_agent in spec["agents"]:
        names = [spec_agent["name"], *spec_agent.get("aliases", [])]
        found = None
        for n in names:
            found = by_name.get(name_key(n))
            if found:
                break
        if found:
            created_ids[spec_agent["slug"]] = str(found["id"])
            print(f"есть: {found.get('name')} ({spec_agent['slug']})")
            want_pause = not spec_agent.get("heartbeatEnabled")
            status = (found.get("status") or "").lower()
            if want_pause and status not in {"paused", "terminated", "pending_approval"}:
                pcode, pres = request("POST", f"/agents/{found['id']}/pause", key, {})
                print(f"  pause → {pcode} {pres if pcode >= 400 else 'ok'}")
            continue

        if spec_agent.get("optional") and spec_agent["slug"] == "ceo" and not CREATE_CEO:
            print("пропуск optional CEO (нет в org — передайте --create-ceo, если нужен ИИ-root)")
            continue

        reports_to = None
        parent_slug = spec_agent.get("reportsToSlug")
        if parent_slug:
            reports_to = created_ids.get(parent_slug)
            if not reports_to:
                parent = next((x for x in spec["agents"] if x["slug"] == parent_slug), None)
                if parent:
                    for n in [parent["name"], *parent.get("aliases", [])]:
                        hit = by_name.get(name_key(n))
                        if hit:
                            reports_to = str(hit["id"])
                            break

        body = {
            "name": spec_agent["name"],
            "role": spec_agent["role"],
            "title": spec_agent.get("title"),
            "reportsTo": reports_to,
            "capabilities": spec_agent.get("capabilities"),
            "budgetMonthlyCents": spec_agent.get("budgetMonthlyCents"),
            "adapterType": "http",
            "adapterConfig": adapter_config(spec_agent),
            "runtimeConfig": {
                "loop": spec_agent.get("capabilities"),
                "schedule": {
                    "enabled": bool(spec_agent.get("heartbeatEnabled")),
                    "intervalSec": int(spec_agent.get("heartbeatIntervalSec") or 3600),
                },
            },
        }
        if spec_agent.get("permissions"):
            body["permissions"] = spec_agent["permissions"]

        hcode, hres = request("POST", f"/companies/{company_id}/agents", key, body)
        print(f"create {spec_agent['name']} → {hcode}")
        if hcode >= 400:
            print(f"  {hres}", file=sys.stderr)
            return 3
        agent_obj = hres.get("agent") if isinstance(hres, dict) and "agent" in hres else hres
        if isinstance(agent_obj, dict) and agent_obj.get("id"):
            created_ids[spec_agent["slug"]] = str(agent_obj["id"])
            by_name[name_key(spec_agent["name"])] = agent_obj
        if not spec_agent.get("heartbeatEnabled") and isinstance(agent_obj, dict) and agent_obj.get("id"):
            request("POST", f"/agents/{agent_obj['id']}/pause", key, {})

    print("готово. HOLD-роли на паузе; ACTIVE — Discovery (+ редкий Product Lead). Не wakeup пачкой.")
    return 0


CREATE_CEO = False

if __name__ == "__main__":
    CREATE_CEO = "--create-ceo" in sys.argv
    raise SystemExit(main())
