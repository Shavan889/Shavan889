from pathlib import Path
import html
import numpy as np
from PIL import Image

INPUT = Path("source-prepped.png")
OUTPUT = Path("avi-ascii.svg")

RAMP = " .`:-=+*cs#%@"

COLS = 100
ROWS = 53

FONT_SIZE = 12
CHAR_W = 7.2
LINE_H = 13

FG = "#d4d4d4"
BG = "#0d1117"


def load():
    img = Image.open(INPUT).convert("L")
    img = img.resize((COLS, ROWS), Image.Resampling.LANCZOS)
    return np.asarray(img)


def ascii_rows(gray):
    rows = []

    for y in range(ROWS):

        s = ""

        for x in range(COLS):

            p = gray[y, x]

            idx = int((p / 255) * (len(RAMP) - 1))

            s += RAMP[idx]

        rows.append(s)

    return rows


def header(w, h):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="{w}"
     height="{h}"
     viewBox="0 0 {w} {h}">

<rect width="100%" height="100%" fill="{BG}"/>

<style>
text {{
    font-family: Consolas, 'Courier New', monospace;
    font-size: {FONT_SIZE}px;
    fill: {FG};
    white-space: pre;
}}
</style>
"""
def svg_defs():
    out = ["<defs>"]

    for i in range(ROWS):
        y = 8 + i * LINE_H
        delay = i * 0.04

        out.append(f"""
<clipPath id="clip{i}">
    <rect x="0"
          y="{y - LINE_H + 2}"
          width="0"
          height="{LINE_H + 4}">
        <animate attributeName="width"
                 from="0"
                 to="{COLS * CHAR_W + 30}"
                 dur="0.7s"
                 begin="{delay:.2f}s"
                 fill="freeze"/>
    </rect>
</clipPath>
""")

    out.append("</defs>")
    return "\n".join(out)


def svg_text(rows):

    out = []

    y = 18

    for i, line in enumerate(rows):

        safe = html.escape(line)

        out.append(f"""
<text
x="10"
y="{y}"
clip-path="url(#clip{i})"
font-family="Consolas, monospace"
font-size="{FONT_SIZE}"
fill="{FG}"
xml:space="preserve">
{safe}
</text>
""")

        y += LINE_H

    return "".join(out)


def svg_cursor():

    total = ROWS * 0.04 + 0.7

    cursor = f"""
<rect
id="cursor"
x="10"
y="6"
width="8"
height="{LINE_H}"
fill="{FG}">

<animate
attributeName="x"
values="
10;
{COLS * CHAR_W};
10;
{COLS * CHAR_W};
10;
{COLS * CHAR_W};
10;
{COLS * CHAR_W};
10;
{COLS * CHAR_W};
10;
{COLS * CHAR_W};
10;
{COLS * CHAR_W};
"
dur="{total}s"
fill="freeze"/>

<animate
attributeName="y"
values="
6;
19;
32;
45;
58;
71;
84;
97;
110;
123;
136;
149;
162;
175;
188;
201;
214;
227;
240;
253;
266;
279;
292;
305;
318;
331;
344;
357;
370;
383;
396;
409;
422;
435;
448;
461;
474;
487;
500;
513;
526;
539;
552;
565;
578;
591;
604;
617;
630;
643;
656;
669;
682
"
dur="{total}s"
fill="freeze"/>

<animate
attributeName="opacity"
values="1;0;1;0;1;0;1"
dur="0.8s"
repeatCount="indefinite"/>

</rect>
"""

    return cursor

def build_svg(rows):

    width = int(COLS * CHAR_W + 20)
    height = int(ROWS * LINE_H + 20)

    svg = []

    svg.append(header(width, height))
    svg.append(svg_defs())
    svg.append(svg_text(rows))
    svg.append(svg_cursor())

    svg.append("\n</svg>")

    return "".join(svg)


def save_svg(svg):

    OUTPUT.write_text(svg, encoding="utf-8")


def main():

    if not INPUT.exists():
        raise FileNotFoundError(
            f"Input image not found: {INPUT}"
        )

    gray = load()

    rows = ascii_rows(gray)

    svg = build_svg(rows)

    save_svg(svg)

    print(f"SVG saved to {OUTPUT}")


if __name__ == "__main__":
    main()