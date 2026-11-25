#!/usr/bin/env python3
"""将扩展打包为可上传 Edge/Chrome 商店的 zip（白名单策略）。

只打包扩展运行所必需的文件，避免把脚本、文档、源图混入商店包。
用法:
    python scripts/package.py
产物:
    dist/my-search-extension-<version>.zip
"""
import json
import os
import re
import sys
import zipfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
DIST_DIR = os.path.join(ROOT, "dist")

# 白名单：根目录必需文件
REQUIRED_FILES = ["manifest.json", "popup.html", "popup.js"]
# 白名单：需要递归打包的目录
INCLUDE_DIRS = ["_locales"]
# 只打包这四个扩展图标（不含 source.png / icon300.png）
ICON_RE = re.compile(r"^icon(16|32|48|128)\.png$")


def fail(msg):
    print(f"❌ {msg}", file=sys.stderr)
    sys.exit(1)


def collect_entries():
    entries = []

    for rel in REQUIRED_FILES:
        path = os.path.join(ROOT, rel)
        if not os.path.isfile(path):
            fail(f"缺少必需文件: {rel}")
        entries.append((path, rel))

    for rel_dir in INCLUDE_DIRS:
        base = os.path.join(ROOT, rel_dir)
        if not os.path.isdir(base):
            fail(f"缺少目录: {rel_dir}")
        for dirpath, _, filenames in os.walk(base):
            for name in filenames:
                full = os.path.join(dirpath, name)
                entries.append((full, os.path.relpath(full, ROOT)))

    assets = os.path.join(ROOT, "assets")
    if not os.path.isdir(assets):
        fail("缺少 assets/ 目录（请先运行 scripts/generate_icons.py）")

    icons = sorted(n for n in os.listdir(assets) if ICON_RE.match(n))
    if len(icons) < 4:
        fail("assets/ 中图标不全，需要 icon16/32/48/128.png")
    for name in icons:
        entries.append((os.path.join(assets, name), f"assets/{name}"))

    return entries


def main():
    manifest_path = os.path.join(ROOT, "manifest.json")
    with open(manifest_path, encoding="utf-8") as fp:
        manifest = json.load(fp)

    version = manifest.get("version")
    if not version:
        fail("manifest.json 缺少 version 字段")

    os.makedirs(DIST_DIR, exist_ok=True)
    out_path = os.path.join(DIST_DIR, f"my-search-extension-{version}.zip")

    entries = collect_entries()
    # manifest.json 放在 zip 首位，便于人工检查
    entries.sort(key=lambda item: (item[1] != "manifest.json", item[1]))

    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for src, arc in entries:
            zf.write(src, arc)

    size_kb = os.path.getsize(out_path) / 1024
    print(f"✅ 打包完成: {os.path.relpath(out_path, ROOT)} ({size_kb:.1f} KB, {len(entries)} 个文件)")
    for _, arc in entries:
        print(f"   - {arc}")


if __name__ == "__main__":
    main()