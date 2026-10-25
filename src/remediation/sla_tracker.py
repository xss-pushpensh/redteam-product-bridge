from datetime import datetime
from src.core.database import get_db

def find_overdue_tickets():
    with get_db() as conn:
        rows = conn.execute("SELECT t.*, f.severity, f.title FROM tickets t JOIN findings f ON f.id = t.finding_id WHERE t.status='open' AND t.sla_deadline < datetime('now')").fetchall()
    return rows

def escalate_overdue():
    overdue = find_overdue_tickets()
    if not overdue:
        print(f"[{datetime.utcnow()}] No overdue tickets.")
        return []
    for r in overdue:
        with get_db() as conn:
            conn.execute("UPDATE tickets SET status='escalated' WHERE id=?", (r["id"],))
        print(f"[OVERDUE-ESCALATED] {r['external_id']} — {r['title']} ({r['severity']})")
    return overdue

if __name__ == "__main__":
    escalate_overdue()
