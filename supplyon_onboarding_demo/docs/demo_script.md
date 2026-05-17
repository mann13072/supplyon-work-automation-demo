# Demo Script — Supplier Onboarding Acceleration Prototype

## Presentation Order

### 1. Explain the Problem (2 minutes)

"Supplier onboarding often gets stuck at various stages — suppliers don't respond to invitations, master data is missing, contracts aren't signed, or technical setups are pending. Onboarding teams spend hours on manual follow-up, and not all suppliers are equally important. We need a way to identify stuck suppliers, prioritize by urgency and business value, and automate the routine follow-up work."

### 2. Show the Sample Dataset (1 minute)

Open `data/sample_supplier_rollout.csv` and show:
- 60 suppliers across multiple countries (Germany, Austria, France, Japan, etc.)
- Various onboarding statuses (invited, started, in_progress, completed)
- Some intentionally messy fields (missing emails, inconsistent casing, empty names)
- Notes with real-world hints like "waiting for signature" or "EDI mapping pending"

### 3. Run the CLI Workflow (1 minute)

```bash
python run_demo.py
```

Show the terminal output:
- 9-step workflow executes automatically
- All outputs are generated
- Summary shows totals and completion rate

### 4. Open the Streamlit UI (2 minutes)

```bash
streamlit run app.py
```

First show the KPI overview:
- Total suppliers, completion rate, outreach items, escalations, overdue count, average rollout age

### 5. Show Supplier Segmentation (1 minute)

Scroll to the segmentation table:
- Suppliers sorted by overall score (descending)
- Each row shows: supplier name, buyer, segment, blocker, language, days since rollout, score, action
- Point out that high-priority, high-risk suppliers appear at the top

### 6. Show an English Outreach Draft (1 minute)

Navigate to the Outreach Queue section:
- Select an English supplier draft from the dropdown
- Read the professional email template with personalized fields filled in
- Show how the FAQ snippet is included for self-service

### 7. Show a German Outreach Draft (1 minute)

Select a German supplier draft:
- Full German localization of the same template
- Culturally appropriate tone and terminology
- Demonstrates multi-language support without AI

### 8. Show a Strategic Supplier Escalation Note (1 minute)

Navigate to the Escalation Queue section:
- Select an escalated supplier note (preferably a strategic/overdue one)
- Note the `assigned_owner_type = account_owner` for strategic suppliers
- Show the escalation reason and suggested next step

### 9. Show the HTML Executive Summary (1 minute)

Open `outputs/reports/executive_summary.html` in a browser:
- Standalone report, no server needed
- KPI cards, segment breakdown, blocker analysis
- Sample outreach draft and escalation note
- "Why This Matters" section

### 10. Close With These Points (30 seconds)

"This prototype shows how we can:
- Start from standard CSV exports that onboarding teams already use
- Automatically classify, prioritize, and draft follow-up for every supplier
- Surface the cases that need human attention before they become crises
- Later connect to APIs, ticketing systems, or LLM-based assistants"

## Key Talking Points

- **Deterministic core:** Business logic is rules-based, predictable, and auditable
- **AI optional:** If enabled, AI only improves wording — it never makes decisions
- **Data quality:** The system handles messy real-world data gracefully
- **Multi-language:** English and German support built in from day one
- **Scalable approach:** From CSV to API integration later
