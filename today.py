import os
import re
from pathlib import Path

import requests

USERNAME = os.getenv("USER_NAME", "Panduputran")
TOKEN = os.getenv("ACCESS_TOKEN")

QUERY = """
query($login: String!) {
  user(login: $login) {
    followers {
      totalCount
    }
    repositories(first: 100, ownerAffiliations: OWNER, privacy: PUBLIC) {
      totalCount
      nodes {
        stargazerCount
      }
    }
    contributionsCollection {
      contributionCalendar {
        totalContributions
      }
    }
  }
}
"""


def github_stats():
    if not TOKEN:
        raise RuntimeError("ACCESS_TOKEN is missing")

    response = requests.post(
        "https://api.github.com/graphql",
        json={
            "query": QUERY,
            "variables": {"login": USERNAME},
        },
        headers={"Authorization": f"Bearer {TOKEN}"},
        timeout=30,
    )
    response.raise_for_status()

    payload = response.json()

    if "errors" in payload:
        raise RuntimeError(payload["errors"])

    user = payload["data"]["user"]

    return {
        "followers": user["followers"]["totalCount"],
        "repositories": user["repositories"]["totalCount"],
        "stars": sum(
            repo["stargazerCount"]
            for repo in user["repositories"]["nodes"]
        ),
        "contributions": (
            user["contributionsCollection"]
            ["contributionCalendar"]
            ["totalContributions"]
        ),
    }


def main():
    # The current profile design is intentionally static.
    # This script is kept as the update entry point for future dynamic fields.
    stats = github_stats()

    print("GitHub statistics:")
    for name, value in stats.items():
        print(f"  {name}: {value:,}")

    # No SVG replacement is performed yet because the new profile
    # intentionally does not display GitHub Stats.
    print("Profile SVGs remain unchanged.")


if __name__ == "__main__":
    main()
