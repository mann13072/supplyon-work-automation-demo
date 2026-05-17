import pandas as pd

from src.schema import OUTREACH_ACTIONS


def decide_actions(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    recommended_actions = []
    template_keys = []
    needs_escalation = []
    assigned_owners = []

    for idx, row in df.iterrows():
        segment = str(row.get("status_segment", ""))
        lang = str(row.get("preferred_language", "en"))
        contact_email = str(row.get("contact_email", "")).strip()
        reminder_count = int(row.get("reminder_count", 0))
        connection_type = str(row.get("connection_type", "")).strip().lower()
        overall_score = int(row.get("overall_score", 0))
        strategic = bool(row.get("strategic_supplier_flag", False))

        action = ""
        tkey = ""
        escalation = False
        owner = ""

        if segment == "completed":
            action = "no_action_completed"
            tkey = ""
            escalation = False

        elif segment == "missing_master_data":
            if not contact_email or contact_email.lower() in ("nan", "none", ""):
                action = "route_to_onboarding_specialist"
                tkey = ""
                escalation = True
                owner = "onboarding_specialist"
            else:
                action = "send_missing_data_request"
                tkey = f"email_missing_data_{lang}"

        elif segment == "invited_no_action":
            if reminder_count == 0:
                action = "send_reminder_1"
            else:
                action = "send_reminder_2"
            tkey = f"email_invited_no_action_{lang}"

        elif segment == "started_incomplete":
            if connection_type in ("edi_m2m", "edi"):
                action = "send_technical_guidance"
                tkey = f"email_technical_guidance_{lang}"
            else:
                action = "send_missing_data_request"
                tkey = f"email_missing_data_{lang}"

        elif segment == "contract_pending":
            action = "send_contract_help"
            tkey = f"email_contract_blocked_{lang}"

        elif segment == "technical_setup_pending":
            if overall_score >= 60:
                action = "route_to_onboarding_specialist"
                tkey = ""
                escalation = True
                owner = "onboarding_specialist"
            else:
                action = "send_technical_guidance"
                tkey = f"email_technical_guidance_{lang}"

        elif segment == "overdue_escalation":
            if strategic:
                action = "route_to_account_owner"
                owner = "account_owner"
            else:
                action = "route_to_onboarding_specialist"
                owner = "onboarding_specialist"
            escalation = True
            tkey = ""

        elif segment == "not_started":
            action = "send_reminder_1"
            tkey = f"email_invited_no_action_{lang}"

        else:
            action = "no_action_completed"
            tkey = ""
            escalation = False

        recommended_actions.append(action)
        template_keys.append(tkey)
        needs_escalation.append(escalation)
        assigned_owners.append(owner)

    df["recommended_action"] = recommended_actions
    df["template_key"] = template_keys
    df["needs_human_escalation"] = needs_escalation
    df["assigned_owner_type"] = assigned_owners

    return df


def split_queues(df: pd.DataFrame):
    outreach = df[
        (df["recommended_action"].isin(OUTREACH_ACTIONS))
        & (df["contact_email"].str.strip() != "")
        & (~df["contact_email"].str.lower().isin(["nan", "none"]))
    ].copy()

    outreach_cols = [
        "supplier_id", "supplier_name", "buyer_name",
        "preferred_language", "status_segment", "blocker_reason",
        "overall_score", "recommended_action", "template_key",
    ]
    outreach = outreach[[c for c in outreach_cols if c in outreach.columns]]

    escalation = df[df["needs_human_escalation"] == True].copy()

    escalation_cols = [
        "supplier_id", "supplier_name", "buyer_name",
        "status_segment", "blocker_reason", "overall_score",
        "recommended_action", "strategic_supplier_flag", "assigned_owner_type",
    ]
    escalation = escalation[[c for c in escalation_cols if c in escalation.columns]]

    return outreach, escalation
