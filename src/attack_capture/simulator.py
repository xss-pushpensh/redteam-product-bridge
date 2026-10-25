import yaml
from datetime import datetime
from src.core.models import Attack, Finding

class AttackSimulator:
    def __init__(self, scenario_file: str):
        with open(scenario_file) as f:
            self.scenario = yaml.safe_load(f)

    def run(self):
        scenario_key = self.scenario["name"].lower().split()[0]
        attack = Attack(
            name=self.scenario["name"],
            scenario=scenario_key,
            target=self.scenario["target"],
        )
        finding = Finding(
            attack_id=attack.id,
            title=self.scenario["finding"]["title"],
            description=f"Simulated attack against {attack.target}",
            severity=self.scenario["finding"]["severity"],
            cvss_score=self.scenario["finding"]["cvss"],
            mitre_technique=self.scenario["finding"]["mitre"],
            mitre_tactic="Unknown",
            root_cause_type="unknown",
            root_cause_detail="pending",
            affected_component=self.scenario.get("affected_component", "/api/endpoint"),
        )
        attack.status = "completed"
        attack.completed_at = datetime.utcnow()
        return attack, finding
