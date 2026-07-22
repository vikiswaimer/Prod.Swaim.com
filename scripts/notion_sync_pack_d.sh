#!/usr/bin/env bash
# Sync pack D (+ Instructions ИИ-блок) Git → Notion. Requires NOTION_TOKEN.
set -euo pipefail
cd "$(dirname "$0")/.."

APPLY="${1:-}"
FLAG=()
if [[ "$APPLY" == "--apply" ]]; then
  FLAG=(--apply)
  echo "MODE: apply"
else
  echo "MODE: dry-run (pass --apply to write)"
fi

python3 scripts/notion_smoke.py

sync() {
  local id="$1" md="$2" assets="${3:-}"
  local args=(--page-id "$id" --md "$md")
  if [[ -n "$assets" ]]; then
    args+=(--assets-dir "$assets")
  fi
  python3 scripts/notion_sync_pilot.py "${args[@]}" "${FLAG[@]}"
}

# Pack D + related user-facing pages
sync e45207ca-d379-83cb-af54-01ada6afeab0 \
  content/small-business-space-ru/Instructions/_index.md \
  content/small-business-space-ru/Instructions

sync a9f207ca-d379-831a-9185-0192f489348b \
  "content/small-business-space-ru/Other/Цифровая безопасность--ab1df728.md" \
  "content/small-business-space-ru/Other/Цифровая безопасность"

sync 1a2207ca-d379-8379-b2c9-010d04bba86a \
  "content/small-business-space-ru/Финансы/Финансовый отчет--c1992c57.md"

sync 329207ca-d379-837b-9966-81eee8afa61d \
  "content/small-business-space-ru/Быстрый старт/Развитие своего бизнеса--d23a7834.md"

sync 9b0207ca-d379-8305-9d71-013fc7eb2fd7 \
  "content/small-business-space-ru/Быстрый старт/Старт своего бизнеса--66c3ee00.md"

echo "Done."
