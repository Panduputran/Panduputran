import datetime
import html
import os
from pathlib import Path

import requests
from dateutil.relativedelta import relativedelta

USERNAME = os.getenv("USER_NAME", "Panduputran")
TOKEN = os.getenv("ACCESS_TOKEN")
BIRTHDAY = datetime.datetime(2009, 4, 6)

ASCII_PATH = Path("ascii-art.txt")
DARK_SVG = Path("profile-dark.svg")
LIGHT_SVG = Path("profile-light.svg")


def github_request(query, variables=None):
    if not TOKEN:
        raise RuntimeError("ACCESS_TOKEN is not configured.")

    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": variables or {}},
        headers={"Authorization": f"Bearer {TOKEN}"},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()

    if "errors" in payload:
        raise RuntimeError(payload["errors"])

    return payload["data"]


def get_age():
    diff = relativedelta(datetime.datetime.now(), BIRTHDAY)
    return f"{diff.years} years, {diff.months} months, {diff.days} days"


def get_github_stats():
    query = """
    query($login: String!) {
      user(login: $login) {
        followers { totalCount }
        repositories(
          first: 100
          ownerAffiliations: OWNER
          privacy: PUBLIC
        ) {
          totalCount
          nodes { stargazerCount }
        }
        contributionsCollection {
          contributionCalendar { totalContributions }
        }
      }
    }
    """

    user = github_request(query, {"login": USERNAME})["user"]

    return {
        "repos": user["repositories"]["totalCount"],
        "stars": sum(r["stargazerCount"] for r in user["repositories"]["nodes"]),
        "followers": user["followers"]["totalCount"],
        "contributions": user["contributionsCollection"]["contributionCalendar"][
            "totalContributions"
        ],
    }


def esc(value):
    return html.escape(str(value))


def make_svg(stats, mode):
    bg = "#0d1117" if mode == "dark" else "#ffffff"
    fg = "#c9d1d9" if mode == "dark" else "#24292f"
    muted = "#8b949e" if mode == "dark" else "#57606a"
    accent = "#58a6ff" if mode == "dark" else "#0969da"
    label = "#ffa657" if mode == "dark" else "#953800"
    border = "#30363d" if mode == "dark" else "#d0d7de"

    ascii_lines = ASCII_PATH.read_text(encoding="utf-8").splitlines()

    left = []
    for i, line in enumerate(ascii_lines):
        left.append(
            f'<text x="38" y="{52 + i * 18}" fill="{fg}" '
            f'font-family="monospace" font-size="14">{esc(line)}</text>'
        )

    items = [
        ("Focus", "Web Development"),
        ("", "Artificial Intelligence"),
        ("", "Machine Learning"),
        ("", "Data Engineering"),
        ("", ""),
        ("Specialization", "Full Stack Development"),
        ("", "ETL Pipelines"),
        ("", "Backend Engineering"),
        ("", "Process Automation"),
        ("", ""),
        ("Currently", "Building scalable web applications"),
        ("", "Exploring AI Engineering"),
        ("", ""),
        ("Working With", "Laravel, React, Python, FastAPI"),
        ("", "PostgreSQL, Docker, Git"),
        ("", ""),
        ("Open To", "Internship"),
        ("", "Open Source Collaboration"),
        ("", ""),
        ("Location", "Bogor, Indonesia"),
        ("", ""),
        ("Age", get_age()),
        ("GitHub Repos", f'{stats["repos"]:,}'),
        ("GitHub Stars", f'{stats["stars"]:,}'),
        ("Followers", f'{stats["followers"]:,}'),
        ("Contributions", f'{stats["contributions"]:,}'),
        ("", ""),
        ("Portfolio", "panduputra.vercel.app"),
        ("GitHub", "github.com/Panduputran"),
        ("LinkedIn", "linkedin.com/in/panduputran"),
    ]

    right = []
    y = 52

    for key, value in items:
        if not key and not value:
            y += 12
            continue

        prefix = esc(key) if key else ".............................."
        color = label if key else muted

        right.append(
            f'<text x="610" y="{y}" fill="{color}" '
            f'font-family="monospace" font-size="14">{prefix}'
            f'.....................</text>'
        )
        right.append(
            f'<text x="795" y="{y}" fill="{accent}" '
            f'font-family="monospace" font-size="14">{esc(value)}</text>'
        )
        y += 18

    height = max(620, y + 30)

    return f"""
<svg xmlns="http://www.w3.org/2000/svg"
     width="1200" height="{height}" viewBox="0 0 1200 {height}">
  <rect width="1200" height="{height}" fill="{bg}"/>
  <rect x="16" y="16" width="1168" height="{height - 32}"
        rx="12" fill="{bg}" stroke="{border}"/>
  <text x="38" y="34" fill="{accent}"
        font-family="monospace" font-size="14">PANDU PUTRA / README</text>
  {''.join(left)}
  {''.join(right)}
</svg>
"""


def main():
    stats = get_github_stats()
    DARK_SVG.write_text(make_svg(stats, "dark"), encoding="utf-8")
    LIGHT_SVG.write_text(make_svg(stats, "light"), encoding="utf-8")
    print("Profile updated:", stats)


if __name__ == "__main__":
    main()
