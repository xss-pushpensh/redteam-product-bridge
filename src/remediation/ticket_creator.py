from datetime import datetime, timedelta
import yaml
from src.core.models import Finding, Ticket
from src.remediation.integrations.github_client import GitHubClient

class TicketCreator:
    def __init__(self):
        with open("config/sla_policy.yaml") as f:
            self.sla = yaml.safe_load(f)
        self.github = GitHubClient()

    def build_body(self, finding: Finding) -> str:
        return f"""## Security Finding\n\n**Severity:** {finding.severity} (CVSS {finding.cvss_score})\n**MITRE ATT&CK:** {finding.mitre_technique} — {finding.mitre_tactic}\n**Affected Component:** {finding.affected_component}\n**Root Cause Type:** {finding.root_cause_type}\n\n### Description\n{finding.description}\n\n### Root Cause\n{finding.root_cause_detail}\n\n### Remediation\n1. Fix the root cause in `{finding.affected_component}`\n2. Add regression test\n3. Re-run the attack simulation to verify\n\n### SLA\nFix within **{self.sla.get(finding.severity, 30)} days**.\n"""

    def create(self, finding: Finding) -> Ticket:
        body = self.build_body(finding)
        title = f"[{finding.severity.upper()}] {finding.title}"
        issue = self.github.create_issue(title, body, labels=["security", finding.severity])
        sla_days = self.sla.get(finding.severity, 30)
        return Ticket(finding_id=finding.id, external_id=str(issue.get("number")), platform="github", status="open", sla_deadline=datetime.utcnow() + timedelta(days=sla_days))
