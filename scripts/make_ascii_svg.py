from pathlib import Path

import numpy as np
from PIL import Image

# Bright -> Dark
RAMP = " .`:-=+*cs#%@"

INPUT_IMAGE = Path("source-prepped.png")
OUTPUT_SVG = Path("avi-ascii.svg")

# Number of characters
COLS = 100
ROWS = 53

FONT_SIZE = 12
FONT_FAMILY = "Consolas, Courier New, monospace"

TEXT_COLOR = "#d4d4d4"
BACKGROUND = "#0d1117"


def resize_image(image: Image.Image):
    image = image.convert("L")
    image = image.resize((COLS, ROWS))
    return image


def pixel_to_char(value):
    index = int((value / 255) * (len(RAMP) - 1))
    return RAMP[index]


def image_to_ascii(image):
    pixels = np.array(image)

    rows = []

    for row in pixels:
        line = ""

        for pixel in row:
            line += pixel_to_char(pixel)

        rows.append(line)

    return rows


def build_svg(lines):
    width = COLS * 8
    height = ROWS * 14 + 20

    svg = []

    svg.append(
        f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{width}"
height="{height}"
viewBox="0 0 {width} {height}">
'''
    )

    svg.append(
        f'''
<rect width="100%" height="100%" fill="{BACKGROUND}"/>
'''
    )

    svg.append(
        f'''
<text
font-family="{FONT_FAMILY}"
font-size="{FONT_SIZE}"
fill="{TEXT_COLOR}"
xml:space="preserve">
'''
    )

    y = 18

    for line in lines:
        svg.append(
            f'<tspan x="10" y="{y}">{line}</tspan>\n'
        )
        y += 13

    svg.append("</text>")
    svg.append("</svg>")

    return "".join(svg)


def main():
    if not INPUT_IMAGE.exists():
        raise FileNotFoundError("source-prepped.png not found.")

    image = Image.open(INPUT_IMAGE)

    image = resize_image(image)

    ascii_rows = image_to_ascii(image)

    svg = build_svg(ascii_rows)

    OUTPUT_SVG.write_text(svg, encoding="utf-8")

    print("Done!")
    print(f"Saved -> {OUTPUT_SVG}")


if __name__ == "__main__":
    main()