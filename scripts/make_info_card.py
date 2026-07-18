from pathlib import Path
import json
import requests
from datetime import datetime

OUTPUT = Path("info-card.svg")
PROFILE = Path("data/profile.json")

BG = "#0d1117"
FG = "#c9d1d9"
GREEN = "#3fb950"
BLUE = "#58a6ff"
YELLOW = "#d29922"
RED = "#f85149"
GRAY = "#8b949e"

WIDTH = 900
HEIGHT = 420


DEFAULT_PROFILE = {
    "name": "Shavan Sanhotra",
    "username": "Shavan889",
    "location": "Mohali, India",
    "role": "MERN Stack Developer",
    "editor": "VS Code",
    "os": "Windows 11",
    "languages": [
        "JavaScript",
        "Python",
        "HTML",
        "CSS"
    ],
    "frameworks": [
        "React",
        "Node.js",
        "Express",
        "MongoDB"
    ],
    "tools": [
        "Git",
        "GitHub",
        "Postman",
        "Docker"
    ]
}


def load_profile():

    if PROFILE.exists():

        with open(PROFILE, "r", encoding="utf8") as f:
            return json.load(f)

    PROFILE.parent.mkdir(exist_ok=True)

    with open(PROFILE, "w", encoding="utf8") as f:
        json.dump(DEFAULT_PROFILE, f, indent=4)

    return DEFAULT_PROFILE


def github_stats(username):

    try:

        url = f"https://api.github.com/users/{username}"

        r = requests.get(url, timeout=15)

        if r.status_code != 200:
            return {}

        d = r.json()

        return {
            "repos": d["public_repos"],
            "followers": d["followers"],
            "following": d["following"]
        }

    except Exception:

        return {}


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
rx="18"
fill="{BG}"/>

<style>

text {{
font-family: Consolas, monospace;
fill:{FG};
font-size:16px;
}}

.title {{
font-size:20px;
font-weight:bold;
}}

.green {{
fill:{GREEN};
}}

.blue {{
fill:{BLUE};
}}

.yellow {{
fill:{YELLOW};
}}

.gray {{
fill:{GRAY};
}}

</style>

"""


def terminal_bar():

    return f"""
<circle cx="25" cy="25" r="7" fill="{RED}"/>
<circle cx="50" cy="25" r="7" fill="{YELLOW}"/>
<circle cx="75" cy="25" r="7" fill="{GREEN}"/>

<text
x="120"
y="30"
class="gray">

terminal

</text>

<line
x1="0"
y1="45"
x2="{WIDTH}"
y2="45"
stroke="#30363d"/>
"""
def ascii_logo():

    return [
        "        #####        ",
        "      #########      ",
        "     ###     ###     ",
        "    ###       ###    ",
        "    ###       ###    ",
        "    ###       ###    ",
        "    ###       ###    ",
        "     ###     ###     ",
        "      #########      ",
        "        #####        "
    ]


def render_logo():

    svg = []

    y = 90

    for line in ascii_logo():

        svg.append(f"""
<text
x="35"
y="{y}"
class="green"
xml:space="preserve">
{line}
</text>
""")

        y += 18

    return "".join(svg)


def render_profile(profile, stats):

    svg = []

    x = 260
    y = 90

    def row(label, value, color=""):

        nonlocal y

        cls = ""

        if color:
            cls = f'class="{color}"'

        svg.append(f"""
<text
x="{x}"
y="{y}">
<tspan class="green">$</tspan>
<tspan> {label}: </tspan>
<tspan {cls}>{value}</tspan>
</text>
""")

        y += 28


    row("Name", profile["name"], "blue")
    row("Username", profile["username"])
    row("Role", profile["role"])
    row("Location", profile["location"])
    row("OS", profile["os"])
    row("Editor", profile["editor"])

    row("Repositories", stats.get("repos", "-"))
    row("Followers", stats.get("followers", "-"))
    row("Following", stats.get("following", "-"))

    row("Updated", datetime.now().strftime("%d %b %Y"))


    return "".join(svg)


def render_skills(profile):

    svg = []

    y = 360

    svg.append(f"""
<text
x="35"
y="{y}"
class="title">
Skills
</text>
""")

    y += 28

    svg.append(f"""
<text
x="35"
y="{y}">
Languages :
{", ".join(profile["languages"])}
</text>
""")

    y += 24

    svg.append(f"""
<text
x="35"
y="{y}">
Frameworks :
{", ".join(profile["frameworks"])}
</text>
""")

    y += 24

    svg.append(f"""
<text
x="35"
y="{y}">
Tools :
{", ".join(profile["tools"])}
</text>
""")

    return "".join(svg)

def build_svg(profile, stats):

    svg = []

    svg.append(svg_header())
    svg.append(terminal_bar())
    svg.append(render_logo())
    svg.append(render_profile(profile, stats))
    svg.append(render_skills(profile))

    svg.append("""
</svg>
""")

    return "".join(svg)


def save_svg(svg):

    OUTPUT.write_text(svg, encoding="utf-8")


def main():

    profile = load_profile()

    stats = github_stats(profile["username"])

    svg = build_svg(profile, stats)

    save_svg(svg)

    print(f"Done!\nSaved -> {OUTPUT}")


if __name__ == "__main__":
    main()