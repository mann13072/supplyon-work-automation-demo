import csv
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from src.schema import BLOCKER_LABELS, ACTION_LABELS, OUTREACH_ACTIONS
from src.llm_optional import maybe_enrich_message

TEMPLATE_DIR = Path(__file__).parent.parent / "templates"
OUTPUT_DIR = Path(__file__).parent.parent / "outputs"

env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))

FAQ_CACHE = None


def _load_faq(faq_path: str = None):
    global FAQ_CACHE
    if FAQ_CACHE is not None:
        return FAQ_CACHE
    path = faq_path or (Path(__file__).parent.parent / "data" / "sample_faq.csv")
    faq = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row["segment"], row["language"])
            faq[key] = {
                "short_answer": row["short_answer"],
                "label": row["help_link_label"],
                "url": row["help_link_url"],
            }
    FAQ_CACHE = faq
    return faq


def _get_faq_snippet(segment: str, lang: str) -> str:
    faq = _load_faq()
    entry = faq.get((segment, lang)) or faq.get((segment, "en"))
    if not entry:
        return ""
    return f"> **{entry['label']}:** {entry['short_answer']}  \n  [Learn more]({entry['url']})"


def generate_all(
    df,
    output_dir: str = None,
    enable_llm: bool = False,
):
    base = Path(output_dir) if output_dir else OUTPUT_DIR
    email_dir = base / "generated_emails"
    note_dir = base / "generated_internal_notes"
    email_dir.mkdir(parents=True, exist_ok=True)
    note_dir.mkdir(parents=True, exist_ok=True)

    for f in email_dir.glob("*.md"):
        f.unlink()
    for f in note_dir.glob("*.md"):
        f.unlink()

    email_count = 0
    for _, row in df.iterrows():
        action = str(row.get("recommended_action", ""))
        contact_email = str(row.get("contact_email", "")).strip()
        template_key = str(row.get("template_key", ""))

        if action not in OUTREACH_ACTIONS:
            continue
        if not contact_email or contact_email.lower() in ("nan", "none", ""):
            continue
        if not template_key:
            continue

        supplier_id = str(row.get("supplier_id", ""))
        lang = str(row.get("preferred_language", "en"))
        segment = str(row.get("status_segment", ""))
        blocker = str(row.get("blocker_reason", ""))

        context = {
            "supplier_name": str(row.get("supplier_name", "")),
            "contact_name": str(row.get("contact_name", "Supplier Team")),
            "buyer_name": str(row.get("buyer_name", "")),
            "service_name": str(row.get("service_name", "")),
            "days_since_rollout": str(row.get("days_since_rollout", "")),
            "blocker_reason_human": BLOCKER_LABELS.get(blocker, blocker),
            "next_step_human": ACTION_LABELS.get(action, action),
            "faq_snippet": _get_faq_snippet(segment, lang),
        }

        tmpl = env.get_template(f"{template_key}.md")
        draft = tmpl.render(**context)

        if enable_llm:
            draft = maybe_enrich_message(
                draft,
                context,
                language=lang,
                mode="supplier_message",
            )

        filename = f"{supplier_id}_{action}.md"
        (email_dir / filename).write_text(draft, encoding="utf-8")
        email_count += 1

    # Generate escalation notes
    note_count = 0
    for _, row in df.iterrows():
        if not row.get("needs_human_escalation", False):
            continue

        supplier_id = str(row.get("supplier_id", ""))
        segment = str(row.get("status_segment", ""))
        blocker = str(row.get("blocker_reason", ""))
        action = str(row.get("recommended_action", ""))
        owner = str(row.get("assigned_owner_type", "onboarding_specialist"))

        if segment == "missing_master_data":
            reason = f"Supplier has missing master data (contact email missing). Cannot proceed with automated outreach."
            manual = "Reach out to supplier via alternative channel to obtain contact information and complete master data."
        elif segment == "overdue_escalation":
            reason = f"Supplier onboarding has been open for {row.get('days_since_rollout', '?')} days without completion. Case requires human intervention."
            manual = "Contact supplier directly to understand blockers and drive completion. Escalate internally if needed."
        elif segment == "technical_setup_pending":
            reason = f"Technical setup (EDI/M2M) is pending with high overall score ({row.get('overall_score', '?')}). Requires specialist involvement."
            manual = "Assign technical specialist to support EDI/M2M connection setup with the supplier."
        else:
            reason = f"Supplier case requires manual attention based on current status ({segment})."
            manual = "Review supplier case details and take appropriate action."

        context = {
            "supplier_name": str(row.get("supplier_name", "")),
            "buyer_name": str(row.get("buyer_name", "")),
            "status_segment": segment,
            "blocker_reason_human": BLOCKER_LABELS.get(blocker, blocker),
            "days_since_rollout": str(row.get("days_since_rollout", "")),
            "overall_score": str(row.get("overall_score", "")),
            "assigned_owner_type": owner,
            "escalation_reason": reason,
            "recommended_manual_step": manual,
        }

        lang = str(row.get("preferred_language", "en"))
        tmpl = env.get_template("internal_escalation_note.md")
        note = tmpl.render(**context)

        if enable_llm:
            note = maybe_enrich_message(
                note,
                context,
                language=lang,
                mode="internal_note",
            )

        filename = f"{supplier_id}_escalation.md"
        (note_dir / filename).write_text(note, encoding="utf-8")
        note_count += 1

    return email_count, note_count
