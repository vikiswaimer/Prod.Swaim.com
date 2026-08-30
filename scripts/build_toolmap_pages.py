#!/usr/bin/env python3
"""Prepare a GitHub Pages artifact for toolmap landing deployment.

Resulting routes:
- /                -> landing (A Cartograph)
- /map.html        -> interactive tool map
- /playbook.html   -> playbook stub
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def _replace_once(text: str, old: str, new: str, file_path: Path) -> str:
    if old not in text:
        raise ValueError(f"Pattern not found in {file_path}: {old}")
    return text.replace(old, new)


def _patch_file(path: Path, replacements: list[tuple[str, str]]) -> None:
    text = path.read_text(encoding="utf-8")
    for old, new in replacements:
        text = _replace_once(text, old, new, path)
    path.write_text(text, encoding="utf-8")


def build(toolmap_dir: Path, output_dir: Path) -> None:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    shutil.copytree(toolmap_dir, output_dir)

    # Keep map page available explicitly at /map.html.
    map_html = (output_dir / "index.html").read_text(encoding="utf-8")
    (output_dir / "map.html").write_text(map_html, encoding="utf-8")

    # Make landing variant A the homepage without changing source files.
    landing_a = (toolmap_dir / "landing" / "a-cartograph.html").read_text(encoding="utf-8")
    landing_a = landing_a.replace('href="a-cartograph.css"', 'href="landing/a-cartograph.css"')
    landing_a = landing_a.replace('href="../index.html"', 'href="map.html"')
    landing_a = landing_a.replace('href="../playbook.html"', 'href="playbook.html"')
    landing_a = landing_a.replace('href="index.html">Другие направления</a>', 'href="landing/index.html">Другие направления</a>')
    landing_a = landing_a.replace('src="../config.local.js"', 'src="config.local.js"')
    landing_a = landing_a.replace('src="landing-track.js"', 'src="landing/landing-track.js"')
    (output_dir / "index.html").write_text(landing_a, encoding="utf-8")

    _patch_file(
        output_dir / "playbook.html",
        [('href="index.html">← назад к map</a>', 'href="map.html">← назад к map</a>')],
    )

    # Keep links from landing hub/variants pointing to /map.html.
    _patch_file(
        output_dir / "landing" / "index.html",
        [('href="../index.html">живая map</a>', 'href="../map.html">живая map</a>')],
    )
    _patch_file(
        output_dir / "landing" / "a-cartograph.html",
        [('href="../index.html"', 'href="../map.html"')],
    )
    _patch_file(
        output_dir / "landing" / "b-foundry.html",
        [('href="../index.html"', 'href="../map.html"')],
    )
    _patch_file(
        output_dir / "landing" / "c-blueprint.html",
        [('href="../index.html"', 'href="../map.html"')],
    )

    # GitHub Pages build has no local config file by default.
    config_local = output_dir / "config.local.js"
    if not config_local.exists():
        shutil.copyfile(output_dir / "config.example.js", config_local)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build toolmap artifact for GitHub Pages")
    parser.add_argument("--toolmap-dir", default="toolmap", help="Path to toolmap source directory")
    parser.add_argument("--output-dir", default="dist/toolmap-pages", help="Path to output directory")
    args = parser.parse_args()

    toolmap_dir = Path(args.toolmap_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    build(toolmap_dir=toolmap_dir, output_dir=output_dir)
    print(f"Built Pages artifact: {output_dir}")


if __name__ == "__main__":
    main()
