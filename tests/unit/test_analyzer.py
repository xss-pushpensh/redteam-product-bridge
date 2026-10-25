from src.root_cause.analyzer import RootCauseAnalyzer
from src.core.models import Finding
def make_finding(technique: str) -> Finding:
    return Finding(attack_id="test-attack", title="Test", description="Test", severity="high", cvss_score=7.5, mitre_technique=technique, mitre_tactic="Test", root_cause_type="unknown", root_cause_detail="pending", affected_component="/api/test")
def test_ssrf_root_cause_is_code():
    rc = RootCauseAnalyzer().analyze(make_finding("T1190"))
    assert rc["type"] == "code"
def test_idor_root_cause_is_code():
    rc = RootCauseAnalyzer().analyze(make_finding("T1078"))
    assert rc["type"] == "code"
def test_privesc_root_cause_is_config():
    rc = RootCauseAnalyzer().analyze(make_finding("T1068"))
    assert rc["type"] == "config"
