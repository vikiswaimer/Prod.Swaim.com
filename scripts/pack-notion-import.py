#!/usr/bin/env python3
"""Упаковка content/small-business-space-ru → ZIP для импорта в Notion (Markdown & CSV + картинки).

Notion ZIP-importer ожидает папку с .md/.csv и относительными ассетами рядом
(как в экспорте: Page.md + Page/image.png). Хеш-суффиксы --xxxxxxxx убираем,
чтобы заголовки страниц были читаемыми; ссылки и пути к картинкам обновляем.
"""

from __future__ import annotations

import argparse
import re
import shutil
import urllib.parse
import zipfile
from pathlib import Path

HASH_SUFFIX = re.compile(r"--([0-9a-fA-F]{8})(?=\.[^.]+$)")
MD_LINK = re.compile(r"(!?\[[^\]]*\])\(([^)]+)\)")
HTML_SRC = re.compile(r'(<img[^>]+src=["\'])([^"\']+)(["\'])', re.I)
IMG_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}


def strip_hash(name: str) -> str:
    return HASH_SUFFIX.sub("", name)


def rewrite_href(href: str) -> str:
    """Переписать относительный href: убрать hash в сегментах пути к .md/.csv."""
    if not href or href.startswith(("http://", "https://", "data:", "mailto:", "#")):
        return href
    raw, frag = href, ""
    if "#" in href:
        raw, frag = href.split("#", 1)
        frag = "#" + frag
    decoded = urllib.parse.unquote(raw)
    parts = Path(decoded).parts
    if not parts:
        return href
    new_parts = []
    for i, part in enumerate(parts):
        if i == len(parts) - 1 and Path(part).suffix.lower() in {".md", ".csv"}:
            new_parts.append(strip_hash(part))
        else:
            new_parts.append(part)
    new_path = str(Path(*new_parts)) if new_parts[0] != ".." else "/".join(new_parts)
    # сохранить URL-encoding пробелов как %20 (Notion/markdown friendly)
    encoded = "/".join(urllib.parse.quote(p, safe="") if p != ".." else ".." for p in Path(new_path).parts)
    # Path("a/b").parts на posix ок; для путей начинающихся с .. Path ломает — fallback:
    if new_path.startswith(".."):
        encoded = "/".join(
            ".." if p == ".." else urllib.parse.quote(p, safe="") for p in new_path.split("/")
        )
    return encoded + frag


def rewrite_file_text(text: str) -> str:
    def link_sub(m: re.Match[str]) -> str:
        return f"{m.group(1)}({rewrite_href(m.group(2))})"

    def src_sub(m: re.Match[str]) -> str:
        return f"{m.group(1)}{rewrite_href(m.group(2))}{m.group(3)}"

    text = MD_LINK.sub(link_sub, text)
    text = HTML_SRC.sub(src_sub, text)
    return text


def prepare_tree(src: Path, dst: Path, *, include_git_nav: bool) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)

    # 1) Сначала каталоги и ассеты (картинки/svg) — имена папок без изменений
    for path in sorted(src.rglob("*")):
        rel = path.relative_to(src)
        if path.is_dir():
            (dst / rel).mkdir(parents=True, exist_ok=True)

    # 2) Файлы
    for path in sorted(src.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(src)

        # Git-навигация: по умолчанию не тащим в Notion (ссылки на docs/ и INDEX шумят)
        if not include_git_nav and rel.as_posix() in {"00-index.md", "INDEX.md"}:
            continue
        if rel.parts[0] == "examples" and not include_git_nav:
            # пример продукта полезен — оставляем examples/
            pass

        # Instructions: Notion-конвенция Page.md + Page/assets
        if rel.as_posix() == "Instructions/_index.md":
            text = rewrite_file_text(path.read_text(encoding="utf-8"))
            # картинки лежат в Instructions/ → префикс Instructions/
            text = re.sub(
                r'(src=["\'])(paper\.png|Thunder\.png|Folder\.png|archive\.png|Group_416\.jpg|Group_415\.jpg)(["\'])',
                r"\1Instructions/\2\3",
                text,
            )
            text = re.sub(
                r'(!\[[^\]]*\]\()(Group_416\.jpg|Group_415\.jpg)(\))',
                r"\1Instructions/\2\3",
                text,
            )
            # убрать git-only ссылку на docs
            text = text.replace(
                "Подробнее: [позиционирование](../../../docs/positioning.md) (в репозитории).",
                "Подробнее о позиционировании — в Git-копии `docs/positioning.md` (после импорта в Notion ссылку можно заменить на страницу пространства).",
            )
            (dst / "Instructions.md").write_text(text, encoding="utf-8")
            continue

        out_name = strip_hash(path.name) if path.suffix.lower() in {".md", ".csv"} else path.name
        out_rel = rel.parent / out_name
        out_path = dst / out_rel
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if path.suffix.lower() in {".md", ".csv"}:
            raw = path.read_text(encoding="utf-8")
            if path.suffix.lower() == ".md":
                raw = rewrite_file_text(raw)
            out_path.write_text(raw, encoding="utf-8")
        else:
            shutil.copy2(path, out_path)


def validate_images(root: Path) -> tuple[int, int, list[str]]:
    ok = bad = 0
    missing: list[str] = []
    for md in root.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        srcs = [m.group(2) for m in MD_LINK.finditer(text) if m.group(1).startswith("!")]
        srcs += [m.group(2) for m in HTML_SRC.finditer(text)]
        for href in srcs:
            if href.startswith(("http://", "https://", "data:")):
                continue
            target = (md.parent / urllib.parse.unquote(href.split("#")[0])).resolve()
            if target.exists():
                ok += 1
            else:
                bad += 1
                missing.append(f"{md.relative_to(root)} -> {href}")
    return ok, bad, missing


def zip_dir(src_dir: Path, zip_path: Path, arc_root: str) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(src_dir.rglob("*")):
            if path.is_file():
                arc = f"{arc_root}/{path.relative_to(src_dir).as_posix()}"
                zf.write(path, arcname=arc)


def pack_subset(src_prepared: Path, dst: Path, rel_paths: list[str]) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)
    for rel in rel_paths:
        src_item = src_prepared / rel
        if not src_item.exists():
            raise FileNotFoundError(rel)
        out = dst / rel
        if src_item.is_dir():
            shutil.copytree(src_item, out)
        else:
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_item, out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--src",
        type=Path,
        default=Path("content/small-business-space-ru"),
    )
    ap.add_argument(
        "--out-dir",
        type=Path,
        default=Path("import"),
    )
    ap.add_argument(
        "--work-dir",
        type=Path,
        default=Path("/tmp/notion-import-build"),
    )
    ap.add_argument(
        "--include-git-nav",
        action="store_true",
        help="Включить 00-index.md и INDEX.md",
    )
    ap.add_argument(
        "--also-mini",
        action="store_true",
        help="Дополнительно собрать мини-ZIP (Instructions + картинки) для пробы импорта",
    )
    args = ap.parse_args()

    src = args.src.resolve()
    work = args.work_dir.resolve()
    prepared = work / "Small Business Space v 1.0 [RU]"
    prepare_tree(src, prepared, include_git_nav=args.include_git_nav)

    ok, bad, missing = validate_images(prepared)
    print(f"image refs: ok={ok} bad={bad}")
    for m in missing:
        print("MISSING", m)
    if bad:
        raise SystemExit(1)

    n_img = sum(1 for p in prepared.rglob("*") if p.suffix.lower() in IMG_EXTS)
    n_md = len(list(prepared.rglob("*.md")))
    n_csv = len(list(prepared.rglob("*.csv")))
    print(f"files: md={n_md} csv={n_csv} images={n_img}")

    full_zip = args.out_dir / "ProdSwaim-Notion-import.zip"
    zip_dir(prepared, full_zip, prepared.name)
    print(f"wrote {full_zip} ({full_zip.stat().st_size // 1024} KiB)")

    if args.also_mini:
        mini_prepared = work / "mini" / "Instructions smoke test"
        pack_subset(
            prepared,
            mini_prepared,
            [
                "Instructions.md",
                "Instructions",
            ],
        )
        ok2, bad2, missing2 = validate_images(mini_prepared)
        print(f"mini image refs: ok={ok2} bad={bad2}")
        for m in missing2:
            print("MISSING", m)
        if bad2:
            raise SystemExit(1)
        mini_zip = args.out_dir / "ProdSwaim-Notion-import-mini-Instructions.zip"
        zip_dir(mini_prepared, mini_zip, mini_prepared.name)
        print(f"wrote {mini_zip} ({mini_zip.stat().st_size // 1024} KiB)")


if __name__ == "__main__":
    main()
