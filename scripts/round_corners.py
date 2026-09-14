# scripts/round_corners.py
import sys
from PIL import Image, ImageChops, ImageDraw

SCALE = 4


def round_corners(src_path: str, dst_path: str, radius_ratio: float) -> None:
    img = Image.open(src_path).convert("RGBA")
    width, height = img.size
    radius = int(min(width, height) * radius_ratio)

    # 拡大したマスクを描いて縮小し、角のザラつきを抑える
    mask = Image.new("L", (width * SCALE, height * SCALE), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle(
        (0, 0, width * SCALE - 1, height * SCALE - 1),
        radius=radius * SCALE,
        fill=255,
    )
    mask = mask.resize((width, height), Image.LANCZOS)

    # 元画像の透明部分を保ったままマスクをかける
    alpha = ImageChops.multiply(img.getchannel("A"), mask)
    img.putalpha(alpha)
    img.save(dst_path)


def main() -> None:
    if len(sys.argv) < 3:
        print("usage: python scripts/round_corners.py <src> <dst> [radius_ratio]")
        sys.exit(1)

    radius_ratio = float(sys.argv[3]) if len(sys.argv) > 3 else 0.12
    round_corners(sys.argv[1], sys.argv[2], radius_ratio)


if __name__ == "__main__":
    main()
