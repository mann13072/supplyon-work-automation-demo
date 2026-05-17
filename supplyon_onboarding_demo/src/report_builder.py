import json
from datetime import datetime
from pathlib import Path

from src.schema import BLOCKER_LABELS, ACTION_LABELS, OUTREACH_ACTIONS


def build_kpi_summary(df):
    total = len(df)
    completed = len(df[df["status_segment"] == "completed"])
    incomplete = total - completed
    completion_rate = round(completed / total * 100, 1) if total else 0

    by_segment = df["status_segment"].value_counts().to_dict()
    for s in [
        "not_started", "invited_no_action", "started_incomplete",
        "missing_master_data", "contract_pending", "technical_setup_pending",
        "overdue_escalation", "completed",
    ]:
        by_segment.setdefault(s, 0)

    escalation_count = int(df["needs_human_escalation"].sum())
    overdue_count = int((df["days_since_rollout"] >= 28).sum())

    outreach_df = df[df["recommended_action"].isin([
        "send_reminder_1", "send_reminder_2", "send_missing_data_request",
        "send_contract_help", "send_technical_guidance",
    ])]
    has_email = outreach_df["contact_email"].str.strip().ne("") & ~outreach_df["contact_email"].str.lower().isin(["nan", "none"])
    outreach_en = int((outreach_df[has_email]["preferred_language"] == "en").sum())
    outreach_de = int((outreach_df[has_email]["preferred_language"] == "de").sum())

    avg_days = round(df["days_since_rollout"].mean(), 1)

    top_blockers = df["blocker_reason"].value_counts().head(5).to_dict()

    top_risk = df[df["status_segment"] != "completed"].nlargest(10, "overall_score")[
        ["supplier_id", "supplier_name", "status_segment", "overall_score"]
    ].to_dict(orient="records")

    summary = {
        "total_suppliers": total,
        "completed_suppliers": completed,
        "incomplete_suppliers": incomplete,
        "completion_rate_pct": completion_rate,
        "suppliers_by_segment": {k: int(v) for k, v in by_segment.items()},
        "escalations_count": escalation_count,
        "overdue_count": overdue_count,
        "english_outreach_count": outreach_en,
        "german_outreach_count": outreach_de,
        "average_days_since_rollout": avg_days,
        "top_blocker_reasons": {BLOCKER_LABELS.get(k, k): int(v) for k, v in top_blockers.items()},
        "top_10_highest_risk_suppliers": top_risk,
        "processed_at": datetime.now().isoformat(),
    }
    return summary


def build_html_report(df, summary, output_dir: str = None):
    base = Path(output_dir) if output_dir else (Path(__file__).parent.parent / "outputs")
    reports_dir = base / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    outreach = df[
        (df["recommended_action"].isin(OUTREACH_ACTIONS))
        & (df["contact_email"].str.strip() != "")
        & (~df["contact_email"].str.lower().isin(["nan", "none"]))
    ].head(10)

    escalation = df[df["needs_human_escalation"] == True].head(10)

    by_segment = summary["suppliers_by_segment"]
    segment_rows = "".join(
        f"<tr><td>{s}</td><td>{v}</td></tr>"
        for s, v in sorted(by_segment.items())
    )

    blocker_rows = "".join(
        f"<tr><td>{k}</td><td>{v}</td></tr>"
        for k, v in summary["top_blocker_reasons"].items()
    )

    outreach_rows = "".join(
        f"<tr><td>{r['supplier_id']}</td><td>{r['supplier_name']}</td>"
        f"<td>{r['status_segment']}</td><td>{BLOCKER_LABELS.get(r['blocker_reason'], r['blocker_reason'])}</td>"
        f"<td>{ACTION_LABELS.get(r['recommended_action'], r['recommended_action'])}</td>"
        f"<td>{r['overall_score']}</td></tr>"
        for _, r in outreach.iterrows()
    )

    escalation_rows = "".join(
        f"<tr><td>{r['supplier_id']}</td><td>{r['supplier_name']}</td>"
        f"<td>{r['status_segment']}</td><td>{BLOCKER_LABELS.get(r['blocker_reason'], r['blocker_reason'])}</td>"
        f"<td>{r['assigned_owner_type']}</td>"
        f"<td>{r['overall_score']}</td></tr>"
        for _, r in escalation.iterrows()
    )

    sample_draft = ""
    email_dir = base / "generated_emails"
    if email_dir.exists():
        files = list(email_dir.glob("*.md"))
        if files:
            sample_draft = f"<pre style='white-space:pre-wrap'>{files[0].read_text(encoding='utf-8')[:500]}...</pre>"

    sample_note = ""
    note_dir = base / "generated_internal_notes"
    if note_dir.exists():
        files = list(note_dir.glob("*.md"))
        if files:
            sample_note = f"<pre style='white-space:pre-wrap'>{files[0].read_text(encoding='utf-8')[:500]}...</pre>"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Supplier Onboarding Acceleration - Executive Summary</title>
<style>
body {{ font-family: -apple-system, sans-serif; max-width: 1100px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
h1, h2, h3 {{ color: #333; }}
.kpi-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 20px 0; }}
.kpi-card {{ background: white; border-radius: 8px; padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
.kpi-card .value {{ font-size: 28px; font-weight: bold; color: #1a73e8; }}
.kpi-card .label {{ font-size: 13px; color: #666; margin-top: 4px; }}
table {{ width: 100%; border-collapse: collapse; background: white; margin: 16px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
th, td {{ padding: 10px 12px; text-align: left; border-bottom: 1px solid #eee; }}
th {{ background: #f8f9fa; font-weight: 600; }}
pre {{ background: #f0f0f0; padding: 12px; border-radius: 6px; font-size: 13px; overflow-x: auto; }}
.section {{ background: white; border-radius: 8px; padding: 20px; margin: 20px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
.tag {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; }}
.tag-escalation {{ background: #fce8e6; color: #c5221f; }}
.tag-ok {{ background: #e6f4ea; color: #137333; }}
.footer {{ text-align: center; color: #888; font-size: 13px; margin: 40px 0; }}
</style>
</head>
<body>
<h1>Supplier Onboarding Acceleration</h1>
<p><strong>Executive Summary</strong> — Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
<p><em>SupplyOn-tailored prototype using synthetic supplier rollout data. Not an official SupplyOn integration.</em></p>

<div class="kpi-grid">
<div class="kpi-card"><div class="value">{summary['total_suppliers']}</div><div class="label">Total Suppliers</div></div>
<div class="kpi-card"><div class="value">{summary['completion_rate_pct']}%</div><div class="label">Completion Rate</div></div>
<div class="kpi-card"><div class="value">{summary['overdue_count']}</div><div class="label">Overdue Suppliers</div></div>
<div class="kpi-card"><div class="value">{summary['escalations_count']}</div><div class="label">Escalations</div></div>
<div class="kpi-card"><div class="value">{summary['english_outreach_count'] + summary['german_outreach_count']}</div><div class="label">Outreach Items</div></div>
<div class="kpi-card"><div class="value">{summary['average_days_since_rollout']}d</div><div class="label">Avg Rollout Age</div></div>
</div>

<div class="section">
<h2>Suppliers by Segment</h2>
<table><tr><th>Segment</th><th>Count</th></tr>{segment_rows}</table>
</div>

<div class="section">
<h2>Top Blocker Reasons</h2>
<table><tr><th>Blocker</th><th>Count</th></tr>{blocker_rows}</table>
</div>

<div class="section">
<h2>Top Priority Outreach Queue (First 10)</h2>
<table><tr><th>ID</th><th>Supplier</th><th>Segment</th><th>Blocker</th><th>Action</th><th>Score</th></tr>{outreach_rows}</table>
</div>

<div class="section">
<h2>Escalation Queue (First 10)</h2>
<table><tr><th>ID</th><th>Supplier</th><th>Segment</th><th>Blocker</th><th>Assigned To</th><th>Score</th></tr>{escalation_rows}</table>
</div>

<div class="section">
<h2>Sample Outreach Draft</h2>
{sample_draft}
</div>

<div class="section">
<h2>Sample Escalation Note</h2>
{sample_note}
</div>

<div class="section">
<h2>Why This Matters</h2>
<ul>
<li>Reduces manual follow-up work by automatically classifying suppliers and drafting targeted communications</li>
<li>Surfaces stuck suppliers earlier so onboarding teams can intervene before cases become critical</li>
<li>Prioritizes high-impact supplier cases based on strategic importance and urgency</li>
<li>Provides a clear path from CSV-export-based workflows to deeper API and ticketing integration later</li>
</ul>
</div>

<div class="footer">
Prototype built for demonstration purposes. All data is synthetic.<br>
Not a live SupplyOn integration.
</div>
</body>
</html>"""

    filepath = reports_dir / "executive_summary.html"
    filepath.write_text(html, encoding="utf-8")
    return str(filepath)
