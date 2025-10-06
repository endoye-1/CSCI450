from typing import Dict, Any
from datetime import datetime, timedelta
import requests
from cli.metrics.base import MetricCalculator


class BusFactorMetric(MetricCalculator):
    def __init__(self) -> None:
        super().__init__("bus_factor")

    def calculate(self, url: str) -> Dict[str, Any]:
        # Only applies to GitHub repos
        if "github.com" not in url:
            return {"bus_factor": 0.0}

        try:
            owner, repo = url.rstrip("/").split("/")[-2:]
        except ValueError:
            # If we can't parse owner/repo, just return 0
            return {"bus_factor": 0.0}

        # We look about 6 months back
        since = (datetime.utcnow() - timedelta(days=180)).isoformat() + "Z"

        # A very simple call which is first page only (up to 100 commits)
        api = f"https://api.github.com/repos/{owner}/{repo}/commits?since={since}&per_page=100"

        try:
            r = requests.get(api, timeout=15)
            if r.status_code != 200:
                return {"bus_factor": 0.0}

            data = r.json()
            if not isinstance(data, list):
                return {"bus_factor": 0.0}

            authors = set()

            for c in data:
                # Prefer GitHub username if present
                author_login = (c.get("author") or {}).get("login")
                if author_login:
                    authors.add(author_login)
                    continue

                # Otherwise try commit author email as a fallback
                email = ((c.get("commit") or {}).get("author") or {}).get("email")
                if email:
                    authors.add(email)

            n = len(authors)

            # Map count to a simple score
            if n <= 0:
                score = 0.0
            elif n <= 2:
                score = 0.3
            elif n <= 5:
                score = 0.6
            else:
                score = 1.0

            return {"bus_factor": score}

        except Exception:
            return {"bus_factor": 0.0}
