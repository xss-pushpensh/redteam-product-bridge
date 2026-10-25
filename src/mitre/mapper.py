import yaml
from typing import Optional
from src.core.models import Finding

class MitreMapper:
    def __init__(self, mapping_file: str = "config/mitre_mapping.yaml"):
        with open(mapping_file) as f:
            self.mapping = yaml.safe_load(f)

    def map(self, scenario: str) -> Optional[dict]:
        return self.mapping.get(scenario)

    def enrich_finding(self, finding: Finding, scenario: str) -> Finding:
        m = self.map(scenario)
        if m:
            finding.mitre_technique = m["technique"]
            finding.mitre_tactic = m["tactic"]
        return finding
