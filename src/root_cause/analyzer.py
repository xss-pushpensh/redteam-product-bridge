from src.core.models import Finding

class RootCauseAnalyzer:
    def analyze(self, finding: Finding) -> dict:
        if finding.mitre_technique == "T1190":
            return {"type": "code", "detail": f"Missing input validation in {finding.affected_component}"}
        elif finding.mitre_technique == "T1078":
            return {"type": "code", "detail": f"Missing authorization check in {finding.affected_component}"}
        elif finding.mitre_technique == "T1068":
            return {"type": "config", "detail": f"Over-permissive configuration in {finding.affected_component}"}
        return {"type": "unknown", "detail": "Manual review required"}
