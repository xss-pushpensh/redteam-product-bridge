from src.attack_capture.simulator import AttackSimulator
from src.core.database import get_db

class FixVerifier:
    def verify(self, ticket_id: str, scenario_file: str) -> bool:
        with get_db() as conn:
            ticket = conn.execute("SELECT * FROM tickets WHERE id=?", (ticket_id,)).fetchone()
            if not ticket:
                raise ValueError(f"Ticket {ticket_id} not found")
            finding = conn.execute("SELECT * FROM findings WHERE id=?", (ticket["finding_id"],)).fetchone()

        sim = AttackSimulator(scenario_file)
        _, new_finding = sim.run()

        if new_finding.title != finding["title"]:
            with get_db() as conn:
                conn.execute("UPDATE tickets SET status='verified', verified_at=datetime('now') WHERE id=?", (ticket_id,))
            return True
        return False
