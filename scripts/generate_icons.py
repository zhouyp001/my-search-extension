#!/usr/bin/env python3
"""从 assets/source.png 生成扩展所需图标。

用法:
    python scripts/generate_icons.py
    python scripts/generate_icons.py --source path/to/logo.png --sizes 16,32,48,128,300

依赖:
    pip install Pillow
"""
import argparse
import os
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("❌ 需要 Pillow：pip install Pillow")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

DEFAULT_SOURCE = os.path.join(PROJECT_ROOT, "assets", "source.png")
DEFAULT_OUT = os.path.join(PROJECT_ROOT, "assets")
DEFAULT_SIZES = "16,32,48,128,300"


def parse_sizes(raw):
    sizes = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        if "x" in part:
            w, h = part.lower().split("x")
            sizes.append((int(w), int(h)))
        else:
            sizes.append(int(part))
    return sizes


def generate(source, out_dir, sizes):
    if not os.path.isfile(source):
        sys.exit(f"❌ 找不到源图: {source}")

    os.makedirs(out_dir, exist_ok=True)
    img = Image.open(source).convert("RGBA")
    print(f"🔍 源图: {source} ({img.width}x{img.height})")

    for size in sizes:
        if isinstance(size, tuple):
            w, h = size
            name = f"icon{w}x{h}.png"
        else:
            w = h = size
            name = f"icon{w}.png"

        resized = img.resize((w, h), Image.Resampling.LANCZOS)
        out_path = os.path.join(out_dir, name)
        resized.save(out_path, "PNG")
        print(f"✅ {os.path.relpath(out_path, PROJECT_ROOT)} ({w}x{h})")

    print("🎉 图标生成完成")


def main():
    parser = argparse.ArgumentParser(description="生成扩展图标")
    parser.add_argument("--source", default=DEFAULT_SOURCE, help="源图路径")
    parser.add_argument("--out", default=DEFAULT_OUT, help="输出目录")
    parser.add_argument("--sizes", default=DEFAULT_SIZES, help="尺寸列表，如 16,32,48,128,300 或 440x280")
    args = parser.parse_args()

    generate(args.source, args.out, parse_sizes(args.sizes))


if __name__ == "__main__":
    main()