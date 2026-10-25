import typer
from rich import print
from src.attack_capture.simulator import AttackSimulator
from src.mitre.mapper import MitreMapper
from src.root_cause.analyzer import RootCauseAnalyzer
from src.remediation.ticket_creator import TicketCreator
from src.remediation.verifier import FixVerifier
from src.core.database import get_db

app = typer.Typer(help="RedTeam-to-Product Bridge CLI")

@app.command()
def simulate(scenario: str = typer.Option(..., help="Path to scenario YAML")):
    print(f"[bold cyan][*] Running scenario:[/] {scenario}")
    sim = AttackSimulator(scenario)
    attack, finding = sim.run()
    mapper = MitreMapper()
    finding = mapper.enrich_finding(finding, attack.scenario)
    analyzer = RootCauseAnalyzer()
    rc = analyzer.analyze(finding)
    finding.root_cause_type = rc["type"]
    finding.root_cause_detail = rc["detail"]
    print(f"[bold green][+] Finding:[/] {finding.title} ({finding.severity})")
    print(f"[bold yellow][*] MITRE:[/] {finding.mitre_technique} — {finding.mitre_tactic}")
    print(f"[bold yellow][*] Root Cause:[/] {finding.root_cause_type} — {finding.root_cause_detail}")
    creator = TicketCreator()
    ticket = creator.create(finding)
    with get_db() as conn:
        conn.execute("INSERT OR REPLACE INTO attacks VALUES (?,?,?,?,?,?,?,?)", (attack.id, attack.name, attack.scenario, attack.started_at, attack.completed_at, attack.target, attack.status, attack.raw_log))
        conn.execute("INSERT OR REPLACE INTO findings VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (finding.id, finding.attack_id, finding.title, finding.description, finding.severity, finding.cvss_score, finding.mitre_technique, finding.mitre_tactic, finding.root_cause_type, finding.root_cause_detail, finding.affected_component, finding.created_at))
        conn.execute("INSERT OR REPLACE INTO tickets VALUES (?,?,?,?,?,?,?,?,?,?,?)", (ticket.id, ticket.finding_id, ticket.external_id, ticket.platform, ticket.assignee, ticket.team, ticket.status, ticket.sla_deadline, ticket.created_at, ticket.fixed_at, ticket.verified_at))
    print(f"[bold green][+] Ticket created:[/] {ticket.external_id}")
    print(f"[bold green][+] Ticket ID:[/] {ticket.id}")
    print(f"[bold green][+] SLA deadline:[/] {ticket.sla_deadline}")

@app.command()
def list_findings():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM findings").fetchall()
        if not rows: print("[yellow]No findings yet.[/]"); return
        for r in rows: print(f"[{r['severity']}] {r['title']} — {r['mitre_technique']}")

@app.command()
def list_tickets():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM tickets").fetchall()
        if not rows: print("[yellow]No tickets yet.[/]"); return
        for r in rows: print(f"{r['external_id']} — {r['status']} — SLA {r['sla_deadline']}")

@app.command()
def verify(ticket_id: str = typer.Option(..., help="Ticket UUID"), scenario: str = typer.Option(..., help="Path to original scenario YAML")):
    print(f"[bold cyan][*] Verifying ticket:[/] {ticket_id}")
    verifier = FixVerifier()
    fixed = verifier.verify(ticket_id, scenario)
    if fixed: print("[bold green][+] Fix VERIFIED — vulnerability no longer reproduces.[/]")
    else: print("[bold red][-] Still vulnerable — ticket remains open.[/]")

@app.command()
def check_sla():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM tickets WHERE status='open' AND sla_deadline < datetime('now')").fetchall()
        if not rows: print("[bold green][+] No overdue tickets.[/]"); return
        for r in rows: print(f"[bold red][OVERDUE][/] {r['external_id']} — SLA {r['sla_deadline']}")

if __name__ == "__main__":
    app()
