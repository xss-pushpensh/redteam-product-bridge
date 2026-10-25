import os
import uuid
import requests

class GitHubClient:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN", "")
        self.repo = os.getenv("GITHUB_REPO", "your-org/your-repo")
        self.base = "https://api.github.com"

    def create_issue(self, title: str, body: str, labels=None) -> dict:
        if not self.token:
            short = uuid.uuid4().hex[:8].upper()
            return {"number": f"DRY-{short}", "html_url": f"https://github.com/dry-run/DRY-{short}", "dry_run": True}
        headers = {"Authorization": f"token {self.token}"}
        data = {"title": title, "body": body, "labels": labels or ["security"]}
        r = requests.post(f"{self.base}/repos/{self.repo}/issues", json=data, headers=headers, timeout=10)
        r.raise_for_status()
        return r.json()
