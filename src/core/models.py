from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
import uuid

class Attack(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    scenario: str
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    target: str
    status: str = "running"
    raw_log: Optional[str] = None

class Finding(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    attack_id: str
    title: str
    description: str
    severity: str
    cvss_score: float
    mitre_technique: str
    mitre_tactic: str
    root_cause_type: str
    root_cause_detail: str
    affected_component: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Ticket(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    finding_id: str
    external_id: Optional[str] = None
    platform: str = "github"
    assignee: Optional[str] = None
    team: Optional[str] = None
    status: str = "open"
    sla_deadline: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    fixed_at: Optional[datetime] = None
    verified_at: Optional[datetime] = None
