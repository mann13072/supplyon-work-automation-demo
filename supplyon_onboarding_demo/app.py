import json
import sys
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px

sys.path.insert(0, str(Path(__file__).parent))

import config
from src.ingest import load_csv
from src.normalize import normalize
from src.classify import classify
from src.scoring import compute_scores
from src.decision_engine import decide_actions, split_queues
from src.template_engine import generate_all
from src.report_builder import build_kpi_summary, build_html_report
from src.schema import BLOCKER_LABELS, ACTION_LABELS

st.set_page_config(
    page_title="Supplier Onboarding Acceleration Demo",
    page_icon="📋",
    layout="wide",
)

st.markdown("""
<style>
.kpi-card {
    background: #f0f2f6;
    border-radius: 8px;
    padding: 16px;
    text-align: center;
}
.kpi-card .value {
    font-size: 32px;
    font-weight: bold;
    color: #1a73e8;
}
.kpi-card .label {
    font-size: 13px;
    color: #555;
    margin-top: 4px;
}
</style>
""", unsafe_allow_html=True)

st.title("Supplier Onboarding Acceleration Demo")
st.caption("SupplyOn-tailored prototype using synthetic supplier rollout data")
st.info("⚠️ This is a demonstration prototype. All data shown is synthetic. Not an official SupplyOn integration.")

# Sidebar
st.sidebar.header("Controls")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV (optional)", type=["csv"],
    help="Upload your own supplier rollout CSV. Uses sample data if empty."
)

enable_llm = st.sidebar.checkbox(
    "Use AI enrichment if API key available",
    value=False,
    help="Requires OPENAI_API_KEY in .env file"
)

lang_filter = st.sidebar.multiselect(
    "Language filter", ["en", "de"], default=["en", "de"]
)

segment_filter = st.sidebar.multiselect(
    "Segment filter",
    [
        "not_started", "invited_no_action", "started_incomplete",
        "missing_master_data", "contract_pending", "technical_setup_pending",
        "overdue_escalation", "completed",
    ],
    default=[
        "not_started", "invited_no_action", "started_incomplete",
        "missing_master_data", "contract_pending", "technical_setup_pending",
        "overdue_escalation",
    ],
)

min_score = st.sidebar.slider("Minimum overall score", 0, 100, 0)

if st.sidebar.button("Run Workflow", type="primary", use_container_width=True):
    with st.spinner("Processing..."):
        try:
            input_path = config.DEFAULT_INPUT_PATH
            if uploaded_file:
                tmp = Path(config.ensure_output_dirs()) / "_uploaded.csv"
                tmp.write_bytes(uploaded_file.getvalue())
                input_path = str(tmp)

            df = load_csv(input_path)
            df = normalize(df)
            df = classify(df)
            df = compute_scores(df)
            df = decide_actions(df)

            use_llm = enable_llm and bool(config.OPENAI_API_KEY)
            output_dir = config.ensure_output_dirs()
            email_count, note_count = generate_all(
                df, output_dir=str(output_dir), enable_llm=use_llm
            )

            outreach, escalation = split_queues(df)
            summary = build_kpi_summary(df)
            report_path = build_html_report(df, summary, output_dir=str(output_dir))

            segmented_path = Path(output_dir) / "segmented_suppliers.csv"
            df.to_csv(segmented_path, index=False)
            outreach_path = Path(output_dir) / "outreach_queue.csv"
            outreach.to_csv(outreach_path, index=False)
            escalation_path = Path(output_dir) / "escalation_queue.csv"
            escalation.to_csv(escalation_path, index=False)

            st.session_state["df"] = df
            st.session_state["outreach"] = outreach
            st.session_state["escalation"] = escalation
            st.session_state["summary"] = summary
            st.session_state["output_dir"] = str(output_dir)
            st.session_state["email_count"] = email_count
            st.session_state["note_count"] = note_count
            st.session_state["ran"] = True
            st.success("Workflow completed successfully!")
        except Exception as e:
            st.error(f"Error: {e}")
else:
    # Try to load from last run
    output_dir = config.ensure_output_dirs()
    out_path = Path(output_dir) / "segmented_suppliers.csv"
    if out_path.exists() and "df" not in st.session_state:
        df = pd.read_csv(out_path, dtype=str)
        summary_path = Path(output_dir) / "kpi_summary.json"
        if summary_path.exists():
            with open(summary_path) as f:
                summary = json.load(f)
        else:
            summary = build_kpi_summary(df)
    outreach_path = Path(output_dir) / "outreach_queue.csv"
    if outreach_path.exists():
        outreach = pd.read_csv(outreach_path, dtype=str)
    else:
        outreach = pd.DataFrame()
    escalation_path = Path(output_dir) / "escalation_queue.csv"
    if escalation_path.exists():
        escalation = pd.read_csv(escalation_path, dtype=str)
    else:
        escalation = pd.DataFrame()

        st.session_state["df"] = df
        st.session_state["outreach"] = outreach
        st.session_state["escalation"] = escalation
        st.session_state["summary"] = summary
        st.session_state["output_dir"] = str(output_dir)
        st.session_state["ran"] = True

if "ran" not in st.session_state:
    st.info("👈 Click 'Run Workflow' in the sidebar to process the sample data.")
    st.stop()

df = st.session_state["df"]
outreach = st.session_state["outreach"]
escalation = st.session_state["escalation"]
summary = st.session_state["summary"]

# Apply filters
if lang_filter:
    df = df[df["preferred_language"].isin(lang_filter)]
if segment_filter:
    df = df[df["status_segment"].isin(segment_filter)]
df = df[df["overall_score"].astype(float) >= min_score]

# KPI Overview
st.header("📊 KPI Overview")
k1, k2, k3, k4, k5, k6 = st.columns(6)

filtered_total = len(df)
filtered_completed = len(df[df["status_segment"] == "completed"])
filtered_completion_rate = round(filtered_completed / filtered_total * 100, 1) if filtered_total else 0
filtered_escalations = int(df["needs_human_escalation"].sum())
filtered_overdue = int((df["days_since_rollout"].astype(float) >= 28).sum())
filtered_outreach = len(df[df["recommended_action"].isin([
    "send_reminder_1", "send_reminder_2", "send_missing_data_request",
    "send_contract_help", "send_technical_guidance",
])])
filtered_avg_days = round(df["days_since_rollout"].astype(float).mean(), 1) if filtered_total else 0

with k1:
    st.markdown(f"<div class='kpi-card'><div class='value'>{filtered_total}</div><div class='label'>Total Suppliers</div></div>", unsafe_allow_html=True)
with k2:
    st.markdown(f"<div class='kpi-card'><div class='value'>{filtered_completion_rate}%</div><div class='label'>Completion Rate</div></div>", unsafe_allow_html=True)
with k3:
    st.markdown(f"<div class='kpi-card'><div class='value'>{filtered_outreach}</div><div class='label'>Outreach Items</div></div>", unsafe_allow_html=True)
with k4:
    st.markdown(f"<div class='kpi-card'><div class='value'>{filtered_escalations}</div><div class='label'>Escalations</div></div>", unsafe_allow_html=True)
with k5:
    st.markdown(f"<div class='kpi-card'><div class='value'>{filtered_overdue}</div><div class='label'>Overdue</div></div>", unsafe_allow_html=True)
with k6:
    st.markdown(f"<div class='kpi-card'><div class='value'>{filtered_avg_days}d</div><div class='label'>Avg Rollout Age</div></div>", unsafe_allow_html=True)

# Supplier Segmentation Table
st.header("📋 Supplier Segmentation")
cols = ["supplier_name", "buyer_name", "status_segment", "blocker_reason",
        "preferred_language", "days_since_rollout", "overall_score", "recommended_action"]
display_cols = [c for c in cols if c in df.columns]
seg_table = df[display_cols].sort_values("overall_score", ascending=False).copy()
seg_table["blocker_reason"] = seg_table["blocker_reason"].map(BLOCKER_LABELS).fillna(seg_table["blocker_reason"])
seg_table["recommended_action"] = seg_table["recommended_action"].map(ACTION_LABELS).fillna(seg_table["recommended_action"])
st.dataframe(seg_table, use_container_width=True, hide_index=True)

# Outreach Queue
st.header("📧 Outreach Queue")
if outreach.empty:
    st.info("No outreach items in the current view.")
else:
    out_cols = ["supplier_id", "supplier_name", "buyer_name", "status_segment",
                "blocker_reason", "overall_score", "recommended_action"]
    out_display = outreach[[c for c in out_cols if c in outreach.columns]].copy()
    out_display["blocker_reason"] = out_display["blocker_reason"].map(BLOCKER_LABELS).fillna(out_display["blocker_reason"])
    out_display["recommended_action"] = out_display["recommended_action"].map(ACTION_LABELS).fillna(out_display["recommended_action"])
    st.dataframe(out_display, use_container_width=True, hide_index=True)

    email_dir = Path(st.session_state["output_dir"]) / "generated_emails"
    email_files = sorted(email_dir.glob("*.md"))
    if email_files:
        email_options = {f.name: f for f in email_files}
        selected = st.selectbox("Preview generated email:", list(email_options.keys()))
        st.markdown(email_options[selected].read_text(encoding="utf-8"))
    else:
        st.info("No generated email files found.")

# Escalation Queue
st.header("🚨 Escalation Queue")
if escalation.empty:
    st.info("No escalation items in the current view.")
else:
    esc_cols = ["supplier_id", "supplier_name", "buyer_name", "status_segment",
                "blocker_reason", "overall_score", "assigned_owner_type"]
    esc_display = escalation[[c for c in esc_cols if c in escalation.columns]].copy()
    esc_display["blocker_reason"] = esc_display["blocker_reason"].map(BLOCKER_LABELS).fillna(esc_display["blocker_reason"])
    st.dataframe(esc_display, use_container_width=True, hide_index=True)

    note_dir = Path(st.session_state["output_dir"]) / "generated_internal_notes"
    note_files = sorted(note_dir.glob("*.md"))
    if note_files:
        note_options = {f.name: f for f in note_files}
        selected = st.selectbox("Preview escalation note:", list(note_options.keys()))
        st.markdown(note_options[selected].read_text(encoding="utf-8"))
    else:
        st.info("No generated escalation notes found.")

# Charts
st.header("📈 Charts")

c1, c2 = st.columns(2)
with c1:
    seg_counts = df["status_segment"].value_counts().reset_index()
    seg_counts.columns = ["segment", "count"]
    fig = px.bar(seg_counts, x="segment", y="count",
                 title="Suppliers by Segment", color="segment",
                 color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    blocker_counts = df["blocker_reason"].value_counts().reset_index()
    blocker_counts.columns = ["blocker", "count"]
    blocker_counts["blocker"] = blocker_counts["blocker"].map(BLOCKER_LABELS).fillna(blocker_counts["blocker"])
    fig = px.bar(blocker_counts, x="blocker", y="count",
                 title="Blocker Reasons", color="blocker",
                 color_discrete_sequence=px.colors.qualitative.Set1)
    st.plotly_chart(fig, use_container_width=True)

age_counts = df["age_bucket"].value_counts().reset_index()
age_counts.columns = ["bucket", "count"]
bucket_order = ["0_6_days", "7_13_days", "14_27_days", "28_plus_days"]
age_counts["bucket"] = pd.Categorical(age_counts["bucket"], categories=bucket_order, ordered=True)
age_counts = age_counts.sort_values("bucket")
fig = px.bar(age_counts, x="bucket", y="count",
             title="Suppliers by Days-Since-Rollout Bucket",
             color="bucket",              color_discrete_sequence=px.colors.qualitative.Set3)
st.plotly_chart(fig, use_container_width=True)

# Generated Files
st.header("📁 Generated Files")
output_dir = st.session_state["output_dir"]

file_links = {
    "segmented_suppliers.csv": "segmented_suppliers.csv",
    "outreach_queue.csv": "outreach_queue.csv",
    "escalation_queue.csv": "escalation_queue.csv",
    "kpi_summary.json": "kpi_summary.json",
    "executive_summary.html": "reports/executive_summary.html",
}

for label, rel_path in file_links.items():
    full = Path(output_dir) / rel_path
    if full.exists():
        with open(full, "rb") as f:
            st.download_button(
                label=f"📥 {label}",
                data=f,
                file_name=label,
                mime="application/octet-stream",
                use_container_width=True,
            )
