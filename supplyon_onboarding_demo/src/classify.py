import pandas as pd
import numpy as np


_COMPLETION_VALUES = {"completed", "active", "activated", "registered_complete"}
_INVITED_VALUES = {"invited", "registration_invited", "pending_registration", "registration_not_started"}
_STARTED_VALUES = {"in_progress", "started", "registration_started", "registration_completed"}
_CONTRACT_HINTS = {
    "contract_issues", "unsigned_agreement", "signature_pending",
    "contract_pending", "contract_signature_pending",
}
_TECH_SETUP_HINTS = {
    "edi_mapping_pending", "edi_setup_pending", "technical_setup",
    "m2m_setup", "connection_validation", "integration_pending",
}
_EDI_TYPES = {"edi_m2m", "edi"}


def classify(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["status_segment"] = ""
    df["blocker_reason"] = ""

    for idx, row in df.iterrows():
        reg_status = str(row.get("registration_status", "")).strip().lower()
        substatus = str(row.get("substatus", "")).strip().lower()
        notes = str(row.get("notes", "")).strip().lower()
        contact_email = str(row.get("contact_email", "")).strip()
        connection_type = str(row.get("connection_type", "")).strip().lower()
        days_since_rollout = int(row.get("days_since_rollout", 0))
        days_in_current_status = int(row.get("days_in_current_status", 0))

        segment = ""
        blocker = ""

        # Rule 1: Completed
        if reg_status in _COMPLETION_VALUES:
            segment = "completed"
            blocker = "completed"
        # Rule 2: Missing master data
        elif not contact_email or contact_email.lower() in ("nan", "none", ""):
            segment = "missing_master_data"
            blocker = "missing_contact_or_master_data"
        # Rule 3: Overdue escalation (must come before contract/tech to catch long-stuck cases)
        elif days_since_rollout >= 28:
            segment = "overdue_escalation"
            blocker = "long_running_overdue_case"
        # Rule 4: Contract pending
        elif substatus in _CONTRACT_HINTS or any(h in notes for h in _CONTRACT_HINTS):
            segment = "contract_pending"
            blocker = "contract_signature_pending"
        # Rule 5: Technical setup pending
        elif (
            connection_type in _EDI_TYPES
            and (
                substatus in _TECH_SETUP_HINTS
                or any(h in notes for h in _TECH_SETUP_HINTS)
            )
        ):
            segment = "technical_setup_pending"
            blocker = "technical_connection_pending"
        # Rule 6: Invited no action
        elif reg_status in _INVITED_VALUES:
            segment = "invited_no_action"
            blocker = "no_response_after_invite"
        # Rule 7: Started incomplete (started and >=10 days stuck)
        elif reg_status in _STARTED_VALUES and days_in_current_status >= 10:
            segment = "started_incomplete"
            blocker = "incomplete_registration_steps"
        # Rule 8: In progress (started but <10 days stuck)
        elif reg_status in _STARTED_VALUES:
            segment = "in_progress"
            blocker = "incomplete_registration_steps"
        # Rule 9: Fallback not started
        else:
            segment = "not_started"
            blocker = "no_response_after_invite"

        df.at[idx, "status_segment"] = segment
        df.at[idx, "blocker_reason"] = blocker

    return df
