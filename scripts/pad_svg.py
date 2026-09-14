# scripts/pad_svg.py
import re
import sys


def pad_svg(src_path: str, dst_path: str, pad_top: int) -> None:
    with open(src_path, encoding="utf-8") as f:
        svg = f.read()

    # viewBox の高さを取得して余白分だけ広げる
    match = re.search(r'viewBox="0 0 (\d+(?:\.\d+)?) (\d+(?:\.\d+)?)"', svg)
    if match is None:
        raise ValueError("viewBox が見つかりません")

    view_width = match.group(1)
    view_height = float(match.group(2))
    new_height = view_height + pad_top

    svg = svg.replace(
        match.group(0),
        f'viewBox="0 0 {view_width} {new_height:g}"',
    )

    # height 属性も同じだけ広げる
    svg = re.sub(
        r'height="\d+(?:\.\d+)?"',
        f'height="{new_height:g}"',
        svg,
        count=1,
    )

    # 中身を下方向にずらして上に余白を作る
    svg = re.sub(
        r"<g ",
        f'<g transform="translate(0 {pad_top})" ',
        svg,
        count=1,
    )

    with open(dst_path, "w", encoding="utf-8") as f:
        f.write(svg)


def main() -> None:
    if len(sys.argv) < 4:
        print("usage: python scripts/pad_svg.py <src> <dst> <pad_top>")
        sys.exit(1)

    pad_svg(sys.argv[1], sys.argv[2], int(sys.argv[3]))


if __name__ == "__main__":
    main()
