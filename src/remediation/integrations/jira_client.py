import os
import uuid

class JiraClient:
    def __init__(self):
        self.url = os.getenv("JIRA_URL", "")
        self.user = os.getenv("JIRA_USER", "")
        self.token = os.getenv("JIRA_TOKEN", "")
        self.project = os.getenv("JIRA_PROJECT", "SEC")

    def _enabled(self) -> bool:
        return bool(self.url and self.user and self.token)

    def create_issue(self, finding) -> dict:
        if not self._enabled():
            short = uuid.uuid4().hex[:6].upper()
            return {"key": f"DRY-{self.project}-{short}", "self": f"https://dry-run/{short}", "dry_run": True}
        from jira import JIRA
        client = JIRA(server=self.url, basic_auth=(self.user, self.token))
        issue = client.create_issue(project=self.project, summary=f"[{finding.severity.upper()}] {finding.title}", description=finding.root_cause_detail, issuetype={"name": "Bug"}, labels=["security", finding.severity, finding.mitre_technique])
        return {"key": issue.key, "self": issue.self}
