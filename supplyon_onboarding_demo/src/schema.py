from dataclasses import dataclass
from typing import List, Set

OUTREACH_ACTIONS: Set[str] = {
    "send_reminder_1", "send_reminder_2",
    "send_missing_data_request", "send_contract_help",
    "send_technical_guidance",
}

RAW_COLUMNS = [
    "Supplier ID",
    "Supplier Name",
    "Buyer Name",
    "Buyer Region",
    "Service Name",
    "Country",
    "Preferred Language",
    "Contact Name",
    "Contact Email",
    "DUNS Number",
    "Rollout Date",
    "Last Status Change Date",
    "Last Contact Date",
    "Registration Status",
    "Substatus",
    "Connection Type",
    "Strategic Supplier Flag",
    "Annual Spend Tier",
    "Response Count",
    "Reminder Count",
    "Notes",
]

CANONICAL_COLUMNS = [
    "supplier_id",
    "supplier_name",
    "buyer_name",
    "buyer_region",
    "service_name",
    "country",
    "preferred_language",
    "contact_name",
    "contact_email",
    "duns_number",
    "rollout_date",
    "last_status_change_date",
    "last_contact_date",
    "registration_status",
    "substatus",
    "connection_type",
    "strategic_supplier_flag",
    "annual_spend_tier",
    "response_count",
    "reminder_count",
    "notes",
]

SEGMENTS = [
    "not_started",
    "invited_no_action",
    "in_progress",
    "started_incomplete",
    "missing_master_data",
    "contract_pending",
    "technical_setup_pending",
    "overdue_escalation",
    "completed",
]

BLOCKER_REASONS = [
    "no_response_after_invite",
    "missing_contact_or_master_data",
    "incomplete_registration_steps",
    "contract_signature_pending",
    "technical_connection_pending",
    "long_running_overdue_case",
    "completed",
]

ACTIONS = [
    "send_reminder_1",
    "send_reminder_2",
    "send_missing_data_request",
    "send_contract_help",
    "send_technical_guidance",
    "route_to_onboarding_specialist",
    "route_to_account_owner",
    "no_action_completed",
]

BLOCKER_LABELS = {
    "no_response_after_invite": "No response after invitation",
    "missing_contact_or_master_data": "Missing contact or master data",
    "incomplete_registration_steps": "Incomplete registration steps",
    "contract_signature_pending": "Contract signature pending",
    "technical_connection_pending": "Technical connection pending",
    "long_running_overdue_case": "Overdue onboarding case",
    "completed": "Completed",
}

ACTION_LABELS = {
    "send_reminder_1": "Send first reminder",
    "send_reminder_2": "Send second reminder",
    "send_missing_data_request": "Request missing onboarding information",
    "send_contract_help": "Send contract support guidance",
    "send_technical_guidance": "Send technical setup guidance",
    "route_to_onboarding_specialist": "Route to onboarding specialist",
    "route_to_account_owner": "Route to account owner",
    "no_action_completed": "No action needed",
}

AGE_BUCKETS = ["0_6_days", "7_13_days", "14_27_days", "28_plus_days"]


@dataclass
class SupplierRecord:
    supplier_id: str
    supplier_name: str
    buyer_name: str
    buyer_region: str
    service_name: str
    country: str
    preferred_language: str
    contact_name: str
    contact_email: str
    duns_number: str
    rollout_date: str
    last_status_change_date: str
    last_contact_date: str
    registration_status: str
    substatus: str
    connection_type: str
    strategic_supplier_flag: bool
    annual_spend_tier: str
    response_count: int
    reminder_count: int
    notes: str
