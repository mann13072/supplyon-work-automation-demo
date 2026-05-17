import pandas as pd


def compute_scores(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    priority_scores = []
    risk_scores = []

    for idx, row in df.iterrows():
        priority = 0
        risk = 0

        strategic = bool(row.get("strategic_supplier_flag", False))
        spend_tier = str(row.get("annual_spend_tier", "")).strip().lower()
        days_rollout = int(row.get("days_since_rollout", 0))
        blocker = str(row.get("blocker_reason", ""))
        reminder_count = int(row.get("reminder_count", 0))
        completed = str(row.get("status_segment", "")) == "completed"

        # Priority score
        if strategic:
            priority += 40
        if spend_tier == "high":
            priority += 30
        elif spend_tier == "medium":
            priority += 20
        elif spend_tier == "low":
            priority += 10
        priority = min(priority, 60)

        # Risk score
        if days_rollout >= 28:
            risk += 25
        elif days_rollout >= 14:
            risk += 15
        elif days_rollout >= 7:
            risk += 8

        blocker_risk = {
            "technical_connection_pending": 20,
            "contract_signature_pending": 15,
            "missing_contact_or_master_data": 10,
        }
        risk += blocker_risk.get(blocker, 0)

        if reminder_count >= 2:
            risk += 10

        if completed:
            risk -= 10

        risk = max(0, min(risk, 40))

        priority_scores.append(priority)
        risk_scores.append(risk)

    df["priority_score"] = priority_scores
    df["risk_score"] = risk_scores
    df["overall_score"] = df["priority_score"] + df["risk_score"]
    df["overall_score"] = df["overall_score"].clip(upper=100)

    df.loc[df["status_segment"] == "completed", "overall_score"] = 0

    return df
