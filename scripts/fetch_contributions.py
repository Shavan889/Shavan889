from pathlib import Path
import json
import requests

USERNAME = "Shavan889"

OUTPUT = Path("data/contributions.json")

API = f"https://github-contributions-api.jogruber.de/v4/{USERNAME}"


def fetch():

    try:
        r = requests.get(API, timeout=20)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Request failed: {e}")


def save(data):

    OUTPUT.parent.mkdir(exist_ok=True)

    with open(
        OUTPUT,
        "w",
        encoding="utf8"
    ) as f:

      json.dump(
    data,
    f,
    indent=4,
    ensure_ascii=False
)
    

def extract_days(data):

    days = []

    if "contributions" in data:

        contrib = data["contributions"]

        if isinstance(contrib, list):

            for day in contrib:

                days.append({
                    "date": day.get("date"),
                    "count": day.get("count", 0),
                    "level": day.get("level", 0),
                })

    elif "years" in data:

        for year in data["years"]:

            for week in year.get("contributionWeeks", []):

                for day in week.get("contributionDays", []):

                    days.append(
                        {
                            "date": day.get("date"),
                            "count": day.get("contributionCount", 0),
                            "level": day.get("contributionLevel", "NONE"),
                        }
                    )

    return days


def normalize(days):

    normalized = []

    level_map = {
        "NONE": 0,
        "FIRST_QUARTILE": 1,
        "SECOND_QUARTILE": 2,
        "THIRD_QUARTILE": 3,
        "FOURTH_QUARTILE": 4,
    }

    for day in days:

        level = day["level"]

        if isinstance(level, str):
            level = level_map.get(level, 0)

        normalized.append(
            {
                "date": day["date"],
                "count": int(day["count"]),
                "level": int(level),
            }
        )

    return normalized

def main():

    print(f"Fetching contributions for {USERNAME}...")

    data = fetch()

    days = extract_days(data)

    days = normalize(days)

    result = {
        "username": USERNAME,
        "total_days": len(days),
        "days": days,
    }

    save(result)

    print("Done!")
    print(f"Saved -> {OUTPUT}")
    print(f"Days fetched: {len(days)}")


if __name__ == "__main__":
    main()