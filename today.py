import os
from pathlib import Path
import requests

USERNAME = os.getenv("USER_NAME", "Panduputran")
TOKEN = os.getenv("ACCESS_TOKEN")

QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    repositories(first: 100, ownerAffiliations: OWNER, privacy: PUBLIC) {
      totalCount
      nodes { stargazerCount }
    }
    contributionsCollection {
      contributionCalendar { totalContributions }
    }
  }
}
"""

def main():
    if not TOKEN:
        raise RuntimeError("ACCESS_TOKEN is missing")

    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": QUERY, "variables": {"login": USERNAME}},
        headers={"Authorization": f"Bearer {TOKEN}"},
        timeout=30,
    )
    response.raise_for_status()
    user = response.json()["data"]["user"]

    stats = {
        "repo_data": user["repositories"]["totalCount"],
        "star_data": sum(r["stargazerCount"] for r in user["repositories"]["nodes"]),
        "follower_data": user["followers"]["totalCount"],
        "contrib_data": user["contributionsCollection"]["contributionCalendar"]["totalContributions"],
    }

    for filename in ("profile-dark.svg", "profile-light.svg"):
        path = Path(filename)
        text = path.read_text(encoding="utf-8")

        for element_id, value in stats.items():
            import re
            text = re.sub(
                rf'(<tspan[^>]*id="{element_id}"[^>]*>).*?(</tspan>)',
                rf'\1{value:,}\2',
                text,
                count=1,
            )

        path.write_text(text, encoding="utf-8")

    print("Updated:", stats)

if __name__ == "__main__":
    main()
