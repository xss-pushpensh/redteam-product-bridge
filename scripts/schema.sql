CREATE TABLE IF NOT EXISTS attacks (
    id TEXT PRIMARY KEY, name TEXT, scenario TEXT,
    started_at TIMESTAMP, completed_at TIMESTAMP,
    target TEXT, status TEXT, raw_log TEXT
);
CREATE TABLE IF NOT EXISTS findings (
    id TEXT PRIMARY KEY, attack_id TEXT, title TEXT, description TEXT,
    severity TEXT, cvss_score REAL, mitre_technique TEXT, mitre_tactic TEXT,
    root_cause_type TEXT, root_cause_detail TEXT, affected_component TEXT,
    created_at TIMESTAMP
);
CREATE TABLE IF NOT EXISTS tickets (
    id TEXT PRIMARY KEY, finding_id TEXT, external_id TEXT, platform TEXT,
    assignee TEXT, team TEXT, status TEXT, sla_deadline TIMESTAMP,
    created_at TIMESTAMP, fixed_at TIMESTAMP, verified_at TIMESTAMP
);
