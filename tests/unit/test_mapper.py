from src.mitre.mapper import MitreMapper
def test_ssrf_maps_to_t1190():
    mapper = MitreMapper()
    result = mapper.map("ssrf")
    assert result["technique"] == "T1190"
    assert result["tactic"] == "Initial Access"
def test_idor_maps_to_t1078():
    mapper = MitreMapper()
    result = mapper.map("idor")
    assert result["technique"] == "T1078"
def test_unknown_returns_none():
    mapper = MitreMapper()
    assert mapper.map("unknown_scenario") is None
