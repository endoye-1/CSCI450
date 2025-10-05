from typing import Dict, Any
import requests
from cli.metrics.base import MetricCalculator


class RampUpMetric(MetricCalculator):
    def __init__(self) -> None:

    # This name is used by the base class to add "<name>_latency"
        super().__init__("ramp_up")

    def calculate(self, url: str) -> Dict[str, Any]:
        text = self._fetch_readme_text(url)
        if not text:
            return {"ramp_up": 0.0}

    # Making everything lowercase so checks are easy
        t = text.lower()

        score = 0.0

    # Super basic checks. Each check adds to the score and installing hint
        if ("pip install" in t) or ("requirements.txt" in t) or ("installation" in t):
            score += 0.4

    # Quickstart/Usage hint
        if ("quickstart" in t) or ("usage" in t) or ("how to run" in t):
            score += 0.3

    # Code block hint
        if "```" in text:
            score += 0.2

    # Links/docs hint
        if ("http://" in t) or ("https://" in t) or ("docs" in t):
            score += 0.1

    # Cap at 1.0
        if score > 1.0:
            score = 1.0

        return {"ramp_up": score}


    def _fetch_readme_text(self, url: str) -> str:
        try:
            if "github.com" in url:
                owner, repo = url.rstrip("/").split("/")[-2:]
                raw_urls = [
                    f"https://raw.githubusercontent.com/{owner}/{repo}/main/README.md",
                    f"https://raw.githubusercontent.com/{owner}/{repo}/master/README.md",
                ]
                for raw in raw_urls:
                    r = requests.get(raw, timeout=10)
                    if r.status_code == 200 and r.text.strip():
                        return r.text

            if "huggingface.co" in url:
                path = url.split("huggingface.co/")[-1].strip("/")
                raw = f"https://huggingface.co/{path}/raw/main/README.md"
                r = requests.get(raw, timeout=10)
                if r.status_code == 200 and r.text.strip():
                    return r.text
        except Exception:
            pass

        return ""
