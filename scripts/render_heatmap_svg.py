from pathlib import Path
import json
from datetime import datetime

INPUT = Path("data/contributions.json")
OUTPUT = Path("contrib-heatmap.svg")

CELL = 12
GAP = 3

LEFT = 40
TOP = 35

COLS = 53
ROWS = 7

WIDTH = LEFT + COLS * (CELL + GAP) + 20
HEIGHT = TOP + ROWS * (CELL + GAP) + 40

BG = "#0d1117"
BORDER = "#30363d"
TEXT = "#8b949e"

LEVELS = {
    0: "#161b22",
    1: "#0e4429",
    2: "#006d32",
    3: "#26a641",
    4: "#39d353",
}


def load():

    if not INPUT.exists():
        raise FileNotFoundError(INPUT)

    with open(INPUT, "r", encoding="utf8") as f:
        return json.load(f)


def svg_header():

    return f"""<?xml version="1.0" encoding="UTF-8"?>

<svg
xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<rect
width="100%"
height="100%"
rx="12"
fill="{BG}"/>

<style>

text {{
font-family: Consolas, monospace;
font-size:11px;
fill:{TEXT};
}}

rect.cell {{
stroke:{BORDER};
stroke-width:.4;
rx:2;
}}

</style>

"""


def month_labels():

    return [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]


def weekday_labels():

    return [
        "Mon",
        "Wed",
        "Fri",
    ]

def draw_months():

    svg = []

    labels = month_labels()

    step = COLS / 12

    for i, month in enumerate(labels):

        x = LEFT + int(i * step) * (CELL + GAP)

        svg.append(f"""
<text
x="{x}"
y="18">
{month}
</text>
""")

    return "".join(svg)


def draw_weekdays():

    svg = []

    labels = weekday_labels()

    rows = [1, 3, 5]

    for label, row in zip(labels, rows):

        y = TOP + row * (CELL + GAP) + CELL - 2

        svg.append(f"""
<text
x="5"
y="{y}">
{label}
</text>
""")

    return "".join(svg)


def build_grid(days):

    svg = []

    for index, day in enumerate(days[: COLS * ROWS]):

        col = index // ROWS
        row = index % ROWS

        x = LEFT + col * (CELL + GAP)
        y = TOP + row * (CELL + GAP)

        level = int(day.get("level", 0))

        color = LEVELS.get(level, LEVELS[0])

        date = day.get("date", "")
        count = day.get("count", 0)

        delay = round(index * 0.01, 2)

        svg.append(f"""
<rect
class="cell"
x="{x}"
y="{y}"
width="{CELL}"
height="{CELL}"
fill="{color}">

<title>{date} • {count} contributions</title>

<animate
attributeName="opacity"
from="0"
to="1"
dur="0.25s"
begin="{delay}s"
fill="freeze"/>

<animate
attributeName="transform"
type="scale"
from="0"
to="1"
dur="0.20s"
begin="{delay}s"
additive="sum"
fill="freeze"/>

</rect>
""")

    return "".join(svg)

def draw_legend():

    svg = []

    x = WIDTH - 140
    y = HEIGHT - 18

    svg.append(f"""
<text
x="{x - 35}"
y="{y + 10}">
Less
</text>
""")

    for i in range(5):

        svg.append(f"""
<rect
class="cell"
x="{x + i * (CELL + 4)}"
y="{y}"
width="{CELL}"
height="{CELL}"
fill="{LEVELS[i]}"/>
""")

    svg.append(f"""
<text
x="{x + 5 * (CELL + 4) + 8}"
y="{y + 10}">
More
</text>
""")

    return "".join(svg)


def build_svg(days):

    svg = []

    svg.append(svg_header())

    svg.append(f"""
<text
x="20"
y="18"
style="font-size:16px;font-weight:bold;fill:#c9d1d9;">
GitHub Contribution Heatmap
</text>
""")

    svg.append(draw_months())
    svg.append(draw_weekdays())
    svg.append(build_grid(days))
    svg.append(draw_legend())

    svg.append(f"""
<text
x="20"
y="{HEIGHT - 10}"
style="font-size:10px;fill:{TEXT};">
Generated automatically using Python
</text>
""")

    svg.append("</svg>")

    return "".join(svg)


def save_svg(svg):

    OUTPUT.write_text(svg, encoding="utf-8")


def main():

    print("Loading contribution data...")

    data = load()

    days = data.get("days", [])

    if not days:
        raise RuntimeError(
            "No contribution data found."
        )

    svg = build_svg(days)

    save_svg(svg)

    print("Done!")
    print(f"Saved -> {OUTPUT}")
    print(f"Rendered {len(days)} contribution days")


if __name__ == "__main__":
    main()