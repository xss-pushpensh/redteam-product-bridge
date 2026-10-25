import streamlit as st
import sqlite3
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
DB = os.getenv("DB_PATH", "./data/bridge.db")
st.set_page_config(page_title="RedTeam-Product Bridge", page_icon="🛡️", layout="wide")
st.title("🛡️ RedTeam-to-Product Bridge")
st.caption("Attack Simulation → MITRE Mapping → Root Cause → Remediation Ticket")

if not os.path.exists(DB):
    st.error(f"Database not found at {DB}. Run a simulation first.")
    st.stop()

conn = sqlite3.connect(DB)
findings = pd.read_sql("SELECT * FROM findings", conn)
tickets = pd.read_sql("SELECT * FROM tickets", conn)
attacks = pd.read_sql("SELECT * FROM attacks", conn)
conn.close()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Attacks", len(attacks))
col2.metric("Total Findings", len(findings))
col3.metric("Open Tickets", len(tickets[tickets["status"] == "open"]) if not tickets.empty else 0)
col4.metric("Critical Findings", len(findings[findings["severity"] == "critical"]) if not findings.empty else 0)

st.divider()
col_a, col_b = st.columns(2)
with col_a:
    st.subheader("Findings by Severity")
    if not findings.empty: st.bar_chart(findings["severity"].value_counts())
    else: st.info("No findings yet.")
with col_b:
    st.subheader("Findings by MITRE Technique")
    if not findings.empty: st.bar_chart(findings["mitre_technique"].value_counts())
    else: st.info("No findings yet.")

st.divider()
st.subheader("📋 Findings")
if not findings.empty: st.dataframe(findings[["severity", "title", "mitre_technique", "mitre_tactic", "root_cause_type", "affected_component"]], use_container_width=True)
else: st.info("No findings recorded.")

st.divider()
st.subheader("🎫 Remediation Tickets")
if not tickets.empty: st.dataframe(tickets[["external_id", "platform", "status", "sla_deadline"]], use_container_width=True)
else: st.info("No tickets created.")

with st.expander("🔍 Raw Attacks Log"):
    if not attacks.empty: st.dataframe(attacks, use_container_width=True)
    else: st.info("No attacks recorded.")
