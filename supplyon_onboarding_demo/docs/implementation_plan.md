# SupplyOn-Tailored Supplier Onboarding Acceleration Demo Prototype

## Purpose of This Document

This document is a build-ready implementation specification for a junior engineer or agent.

The goal is not to brainstorm or outline possibilities. The goal is to describe exactly what to build, how to structure it, what files to create, what logic to implement, what outputs to generate, and how to verify that the prototype works.

This is a demonstration prototype for presentation to a representative from SupplyOn or a similar company. It is not a production integration. It must be realistic enough to prove capability, but simple enough to build quickly and run locally.

This spec assumes:

- no direct SupplyOn API access
- no real supplier data
- no LLM API key required for the first usable version
- a local Python-based prototype
- a Streamlit interface for demo purposes
- synthetic but realistic supplier onboarding rollout data

The implementation must be complete enough that another agent can build it without making product decisions on its own.

---

## Project Goal

Build a local prototype that demonstrates a supplier onboarding acceleration workflow tailored to SupplyOn-style onboarding and rollout operations.

The prototype must show how a system can:

1. ingest supplier rollout export data
2. normalize messy supplier onboarding fields
3. classify suppliers by onboarding stage and likely blocker
4. score suppliers by urgency and business priority
5. recommend the next best action
6. generate English and German follow-up drafts
7. generate internal escalation notes
8. produce summary KPIs and reports
9. present all of this in a simple local Streamlit app
10. run fully without an LLM key, but optionally improve drafts if a key is provided later

The main pitch is:

"I can build operational workflow automation that identifies stuck suppliers, drafts the right follow-up, and helps onboarding teams move suppliers through activation faster."

---

## Non-Goals

Do not build any of the following in v1:

- real SupplyOn integration
- authentication
- multi-user login
- production database
- background job queues
- email sending infrastructure
- CRM integration
- ticketing integration
- advanced admin panels
- deployment automation
- cloud infrastructure
- model training
- autonomous decision-making by AI

The prototype must remain local, lightweight, and deterministic at its core.

---

## Deliverable Definition

The final deliverable is a self-contained local project folder named:

`supplyon_onboarding_demo`

This folder must contain:

- runnable Python code
- a sample synthetic supplier rollout dataset
- deterministic workflow logic
- optional LLM enrichment support
- a Streamlit UI
- generated output artifacts
- a README explaining setup and execution
- a short demo script
- this implementation plan copied into the project docs

The prototype must be usable in two ways:

1. command-line execution
2. local Streamlit UI execution

Both modes must work without an API key.

---

## Exact Folder Structure

Create the project with this exact structure:

```text
supplyon_onboarding_demo/
  README.md
  requirements.txt
  .env.example
  app.py
  run_demo.py
  config.py
  data/
    sample_supplier_rollout.csv
    sample_faq.csv
    sample_status_rules.csv
  outputs/
    segmented_suppliers.csv
    outreach_queue.csv
    escalation_queue.csv
    kpi_summary.json
    generated_emails/
    generated_internal_notes/
    reports/
  src/
    __init__.py
    ingest.py
    schema.py
    normalize.py
    classify.py
    scoring.py
    decision_engine.py
    template_engine.py
    llm_optional.py
    report_builder.py
    demo_seed_notes.md
  templates/
    email_invited_no_action_en.md
    email_invited_no_action_de.md
    email_started_incomplete_en.md
    email_started_incomplete_de.md
    email_missing_data_en.md
    email_missing_data_de.md
    email_contract_blocked_en.md
    email_contract_blocked_de.md
    email_technical_guidance_en.md
    email_technical_guidance_de.md
    internal_escalation_note.md
    dashboard_intro.md
  docs/
    implementation_plan.md
    demo_script.md
    dataset_design.md
```

Notes:

- `outputs/` contains generated files only.
- `src/` contains the implementation logic.
- `templates/` contains all deterministic markdown templates.
- `docs/implementation_plan.md` must be a copy of this plan.
- `outputs/generated_emails/` stores one generated markdown file per outreach item.
- `outputs/generated_internal_notes/` stores one generated markdown file per escalation item.
- `outputs/reports/` stores at least one static HTML summary report.

---

## High-Level Workflow

The system must execute the following operational flow:

1. Read a supplier rollout CSV file.
2. Normalize input columns into a canonical schema.
3. Clean obvious formatting problems.
4. Derive timing and language fields.
5. Classify each supplier into one onboarding segment.
6. Determine the likely blocker reason.
7. Compute urgency and business priority scores.
8. Decide the recommended next action.
9. Generate supplier-facing follow-up drafts where appropriate.
10. Generate internal escalation notes where human action is required.
11. Create KPI aggregates and report views.
12. Save all outputs to disk.
13. Show the processed workflow in Streamlit.

This workflow must remain deterministic in its business logic.

AI, when enabled later, is allowed only to improve wording, personalization, and summaries. AI must not choose segments, actions, scores, or factual statuses.

---

## Product Positioning Inside The Prototype

This prototype must look tailored to SupplyOn-style supplier onboarding operations.

Use terminology such as:

- supplier onboarding
- rollout
- supplier activation
- registration
- onboarding status
- supplier master data
- connection type
- EDI/M2M
- escalation
- onboarding specialist
- account owner

However, clearly state in the README and UI that:

- this is a demonstration prototype
- all data is synthetic
- it is not an official SupplyOn integration

---

## Data Model

### Canonical Internal Supplier Fields

After normalization, every supplier row must use the same internal schema.

These fields are required:

```text
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
rollout_date: date
last_status_change_date: date
last_contact_date: date | null
registration_status: str
substatus: str
connection_type: str
strategic_supplier_flag: bool
annual_spend_tier: str
response_count: int
reminder_count: int
notes: str
```

### Derived Fields

The workflow must derive these fields during processing:

```text
days_since_rollout: int
days_in_current_status: int
age_bucket: str
status_segment: str
blocker_reason: str
priority_score: int
risk_score: int
overall_score: int
recommended_action: str
needs_human_escalation: bool
template_key: str
```

### Required Controlled Values

Use these exact segment names:

1. `not_started`
2. `invited_no_action`
3. `started_incomplete`
4. `missing_master_data`
5. `contract_pending`
6. `technical_setup_pending`
7. `overdue_escalation`
8. `completed`

Use these exact blocker values:

1. `no_response_after_invite`
2. `missing_contact_or_master_data`
3. `incomplete_registration_steps`
4. `contract_signature_pending`
5. `technical_connection_pending`
6. `long_running_overdue_case`
7. `completed`

Use these exact action values:

1. `send_reminder_1`
2. `send_reminder_2`
3. `send_missing_data_request`
4. `send_contract_help`
5. `send_technical_guidance`
6. `route_to_onboarding_specialist`
7. `route_to_account_owner`
8. `no_action_completed`

These constants must be centralized in `src/schema.py`.

---

## Input Dataset Specification

### Main Dataset File

Create:

`data/sample_supplier_rollout.csv`

The dataset must contain between 40 and 60 rows.

Recommended target:

- 50 rows total

This is large enough to look realistic in charts and tables, but still easy for a junior implementer to inspect manually.

### Dataset Coverage Requirements

The synthetic dataset must include:

1. at least 6 countries
2. English and German suppliers
3. at least 8 overdue suppliers
4. at least 6 missing master data cases
5. at least 6 started-but-incomplete cases
6. at least 5 strategic suppliers
7. multiple connection types
8. at least 3 already completed suppliers
9. at least 3 large suppliers with high urgency but low response counts
10. some intentionally messy fields

### Required Raw Input Columns

The sample CSV should include these raw columns:

```text
Supplier ID
Supplier Name
Buyer Name
Buyer Region
Service Name
Country
Preferred Language
Contact Name
Contact Email
DUNS Number
Rollout Date
Last Status Change Date
Last Contact Date
Registration Status
Substatus
Connection Type
Strategic Supplier Flag
Annual Spend Tier
Response Count
Reminder Count
Notes
```

### Intentional Messiness In Sample Data

The dataset must deliberately include realistic data-quality problems:

- empty preferred language fields
- empty contact names
- some empty contact emails
- inconsistent whitespace
- different casing in statuses
- mixed but parseable date formats
- some notes with free-text hints such as "waiting for signature" or "EDI mapping pending"

This is important because the demo should prove that the workflow can handle operationally messy data.

---

## Supporting Data Files

### FAQ File

Create:

`data/sample_faq.csv`

Required columns:

```text
faq_key
segment
language
short_answer
help_link_label
help_link_url
```

Populate it with FAQ rows relevant to:

- invitation reminders
- incomplete registration steps
- missing data requests
- contract signing help
- technical setup guidance

Each FAQ entry must exist in English and German where relevant.

### Status Rules File

Create:

`data/sample_status_rules.csv`

Required columns:

```text
rule_id
registration_status
substatus
min_days
max_days
strategic_override
derived_segment
recommended_action
```

Even if the code still contains explicit logic, this CSV must exist because:

- it demonstrates that rules can later become editable by operations teams
- it gives the demo a more credible workflow-design feel

In v1, the code may use a hybrid approach:

- fixed core logic in Python
- this CSV present as a visible rules artifact

---

## Required Output Files

Each demo run must generate these exact outputs:

1. `outputs/segmented_suppliers.csv`
2. `outputs/outreach_queue.csv`
3. `outputs/escalation_queue.csv`
4. `outputs/kpi_summary.json`
5. `outputs/generated_emails/*.md`
6. `outputs/generated_internal_notes/*.md`
7. `outputs/reports/executive_summary.html`

### Output File Definitions

#### `segmented_suppliers.csv`

Contains all suppliers after normalization, derived fields, segment assignment, score assignment, and recommended action.

This is the master processed file.

#### `outreach_queue.csv`

Contains only suppliers who should receive or be prepared for supplier-facing outreach.

Required columns:

- supplier_id
- supplier_name
- buyer_name
- preferred_language
- status_segment
- blocker_reason
- overall_score
- recommended_action
- template_key

#### `escalation_queue.csv`

Contains only suppliers who require human intervention.

Required columns:

- supplier_id
- supplier_name
- buyer_name
- status_segment
- blocker_reason
- overall_score
- recommended_action
- strategic_supplier_flag
- assigned_owner_type

#### `kpi_summary.json`

Must contain at least:

- total suppliers
- completed suppliers
- incomplete suppliers
- completion rate
- suppliers by segment
- escalations count
- overdue count
- English outreach count
- German outreach count
- average days since rollout
- top blocker reasons
- top 10 highest-risk suppliers

#### Generated Email Files

For every supplier in the outreach queue with a valid contact email, create one markdown file:

`outputs/generated_emails/<supplier_id>_<action>.md`

Example:

`outputs/generated_emails/SUP-001_send_reminder_1.md`

#### Generated Internal Note Files

For every escalated supplier, create one markdown file:

`outputs/generated_internal_notes/<supplier_id>_escalation.md`

#### Executive HTML Report

Create:

`outputs/reports/executive_summary.html`

This report is important for showing the prototype even if Streamlit is not open.

---

## Module-By-Module Implementation Spec

### `config.py`

Responsibilities:

1. load environment variables
2. expose default paths
3. expose feature flags
4. validate output directories

Use these variables:

```text
OPENAI_API_KEY=
DEFAULT_INPUT_PATH=data/sample_supplier_rollout.csv
DEFAULT_OUTPUT_DIR=outputs
DEFAULT_LANGUAGE_FALLBACK=en
ENABLE_LLM_ENRICHMENT=false
```

Requirements:

- use `python-dotenv`
- provide defaults if `.env` is not present
- create output directories if missing
- do not crash if `OPENAI_API_KEY` is empty

### `src/schema.py`

Responsibilities:

1. define raw column names
2. define canonical internal column names
3. define constants for segments
4. define constants for actions
5. define constants for blocker reasons
6. define lists of required fields

Implementation guidance:

- use plain constants or dataclasses
- keep this module very simple
- do not import Streamlit here
- do not put business logic here

### `src/ingest.py`

Responsibilities:

1. load the CSV file into pandas
2. validate that required raw columns exist
3. preserve original columns
4. return a DataFrame

Rules:

- accept an optional input path
- raise a readable error if columns are missing
- do not normalize or classify in this file

### `src/normalize.py`

Responsibilities:

1. map raw column names to canonical names
2. trim whitespace
3. normalize text values
4. normalize language handling
5. convert dates
6. derive timing fields
7. create age buckets

Required normalization rules:

1. strip leading/trailing whitespace from all string fields
2. normalize `registration_status`, `substatus`, and `connection_type` to lowercase snake_case where possible
3. convert `Strategic Supplier Flag` into a boolean
4. normalize `Annual Spend Tier` to one of:
   - `high`
   - `medium`
   - `low`
5. parse dates into pandas datetime
6. calculate `days_since_rollout` relative to the current date
7. calculate `days_in_current_status` using `last_status_change_date`
8. derive `age_bucket` using:
   - `0_6_days`
   - `7_13_days`
   - `14_27_days`
   - `28_plus_days`

Language rules:

1. if preferred language is already English-like, map to `en`
2. if preferred language is German-like, map to `de`
3. if preferred language is missing and country is Germany, Austria, or Switzerland, set `de`
4. otherwise use `en`

Missing-value handling:

1. preserve blank `contact_email` values because they matter for escalation logic
2. for draft rendering only, allow fallback contact name `"Supplier Team"`
3. do not silently fill missing status fields with fake values

### `src/classify.py`

Responsibilities:

1. assign one segment per supplier
2. assign one blocker reason per supplier
3. flag human escalation where needed

Apply rules in a clear priority order. The order matters.

Use this exact priority order:

1. completion check
2. missing contact/master data check
3. contract-related blocker check
4. technical setup blocker check
5. overdue escalation check
6. invited no action check
7. started incomplete check
8. fallback not started

Detailed classification rules:

#### Rule 1: Completed

If `registration_status` clearly indicates completion, then:

- `status_segment = completed`
- `blocker_reason = completed`
- `needs_human_escalation = false`

Recognize completion-like values such as:

- completed
- active
- activated
- registered_complete

Map all such values into the single internal completed segment.

#### Rule 2: Missing Master Data

If contact email is empty, or if essential contact/master-data fields are missing in a way that prevents outreach, then:

- `status_segment = missing_master_data`
- `blocker_reason = missing_contact_or_master_data`
- `needs_human_escalation = true`

Minimum trigger in v1:

- missing contact email

Optional additional trigger:

- missing supplier name or missing supplier id should raise an error earlier rather than classifying

#### Rule 3: Contract Pending

If `substatus` or `notes` suggests contract signature problems, then:

- `status_segment = contract_pending`
- `blocker_reason = contract_signature_pending`

Look for phrases like:

- signature pending
- waiting for signature
- contract pending
- unsigned agreement

#### Rule 4: Technical Setup Pending

If connection type is EDI/M2M and notes or substatus suggest technical setup dependency, then:

- `status_segment = technical_setup_pending`
- `blocker_reason = technical_connection_pending`

Look for phrases like:

- edi mapping pending
- technical setup
- m2m setup
- connection validation
- integration pending

#### Rule 5: Overdue Escalation

If the supplier is not completed and `days_since_rollout >= 28`, then:

- `status_segment = overdue_escalation`
- `blocker_reason = long_running_overdue_case`
- `needs_human_escalation = true`

This rule must override ordinary reminder logic.

#### Rule 6: Invited No Action

If supplier has invitation status and no progress has been made:

- if `days_since_rollout` is between 7 and 27 inclusive, and no narrower blocker exists, then:
  - `status_segment = invited_no_action`
  - `blocker_reason = no_response_after_invite`

Use invitation-style statuses such as:

- invited
- registration_invited
- pending_registration

#### Rule 7: Started Incomplete

If onboarding was started but is not complete and the status has stalled for at least 10 days:

- `status_segment = started_incomplete`
- `blocker_reason = incomplete_registration_steps`

Use clues like:

- in_progress
- started
- registration_started
- incomplete

and:

- `days_in_current_status >= 10`

#### Rule 8: Fallback Not Started

If no other rule applies and the supplier is not completed, then:

- `status_segment = not_started`
- `blocker_reason = no_response_after_invite`

### `src/scoring.py`

Responsibilities:

1. compute priority score
2. compute risk score
3. compute overall score

Use this exact scoring logic.

#### Priority Score

Start at `0`.

Add:

- `40` if strategic supplier flag is true
- `30` if annual spend tier is `high`
- `20` if annual spend tier is `medium`
- `10` if annual spend tier is `low`

Cap `priority_score` at `60`.

#### Risk Score

Start at `0`.

Add:

- `25` if `days_since_rollout >= 28`
- `15` if `days_since_rollout >= 14` and `< 28`
- `8` if `days_since_rollout >= 7` and `< 14`
- `20` if blocker is `technical_connection_pending`
- `15` if blocker is `contract_signature_pending`
- `10` if blocker is `missing_contact_or_master_data`
- `10` if reminder count is `>= 2`

Subtract:

- `10` if status is completed

Cap `risk_score` at `40`.

#### Overall Score

`overall_score = min(100, priority_score + risk_score)`

This split is intentionally simple and demo-friendly.

### `src/decision_engine.py`

Responsibilities:

1. convert segment + score into next action
2. assign template keys
3. split suppliers into outreach and escalation queues
4. assign a human owner type for escalated cases

Use these exact decision rules:

#### Completed

If segment is `completed`:

- `recommended_action = no_action_completed`
- `template_key = ""`
- `needs_human_escalation = false`

#### Missing Master Data

If segment is `missing_master_data`:

- if contact email is missing:
  - `recommended_action = route_to_onboarding_specialist`
  - `template_key = ""`
  - `needs_human_escalation = true`
- else:
  - `recommended_action = send_missing_data_request`
  - `template_key = email_missing_data_<lang>`

#### Invited No Action

If segment is `invited_no_action`:

- if reminder count is `0`:
  - `recommended_action = send_reminder_1`
- if reminder count is `1` or more:
  - `recommended_action = send_reminder_2`

Template key:

- `email_invited_no_action_en`
- `email_invited_no_action_de`

#### Started Incomplete

If segment is `started_incomplete`:

- if connection type is `edi_m2m` or similar normalized value:
  - `recommended_action = send_technical_guidance`
  - use technical template
- otherwise:
  - `recommended_action = send_missing_data_request`
  - use missing data template

#### Contract Pending

If segment is `contract_pending`:

- `recommended_action = send_contract_help`
- use contract template

#### Technical Setup Pending

If segment is `technical_setup_pending`:

- if `overall_score >= 60`:
  - `recommended_action = route_to_onboarding_specialist`
  - `template_key = ""`
  - `needs_human_escalation = true`
- else:
  - `recommended_action = send_technical_guidance`
  - use technical template

#### Overdue Escalation

If segment is `overdue_escalation`:

- if strategic supplier flag is true:
  - `recommended_action = route_to_account_owner`
  - `assigned_owner_type = account_owner`
- else:
  - `recommended_action = route_to_onboarding_specialist`
  - `assigned_owner_type = onboarding_specialist`

Both cases:

- `needs_human_escalation = true`
- `template_key = ""`

#### Not Started

If segment is `not_started`:

- `recommended_action = send_reminder_1`
- use invited-no-action template

### `src/template_engine.py`

Responsibilities:

1. load markdown templates
2. populate templates with structured values
3. optionally call the LLM enrichment layer
4. write final output files to disk

Use `jinja2` for template rendering.

Every supplier-facing template must support these placeholders:

- `{{ supplier_name }}`
- `{{ contact_name }}`
- `{{ buyer_name }}`
- `{{ service_name }}`
- `{{ days_since_rollout }}`
- `{{ blocker_reason_human }}`
- `{{ next_step_human }}`
- `{{ faq_snippet }}`

Every internal escalation note must support:

- `{{ supplier_name }}`
- `{{ buyer_name }}`
- `{{ status_segment }}`
- `{{ blocker_reason_human }}`
- `{{ days_since_rollout }}`
- `{{ overall_score }}`
- `{{ assigned_owner_type }}`
- `{{ recommended_manual_step }}`

Rules:

1. if no API key exists, render deterministic templates only
2. if API key exists and AI toggle is on, first create deterministic draft, then optionally enrich wording
3. never allow AI to change factual fields
4. if enrichment fails, fall back to deterministic draft silently but log the failure in the terminal or app

### `src/llm_optional.py`

Responsibilities:

1. detect whether AI enrichment is possible
2. enrich drafts only if enabled and key present
3. keep AI output constrained

Behavior requirements:

- if no key is present, return original deterministic draft unchanged
- if enrichment is disabled, return original deterministic draft unchanged
- if API call fails, return original deterministic draft unchanged

Expose at least one function:

`maybe_enrich_message(draft_text, context_dict, language, mode)`

`mode` can be:

- `supplier_message`
- `internal_note`

Prompt requirements:

1. preserve all facts exactly
2. do not invent dates or statuses
3. do not change the recommended action
4. keep the tone concise and operational
5. preserve English or German depending on input

### `src/report_builder.py`

Responsibilities:

1. create KPI summary data
2. create a static HTML report
3. prepare chart-ready aggregates

The static HTML report must include these sections:

1. prototype overview
2. processing timestamp
3. summary KPI cards
4. supplier counts by segment
5. blocker reason distribution
6. outreach queue preview
7. escalation queue preview
8. example supplier-facing draft
9. example internal escalation note
10. short explanation of business value

The business value section should explain in plain language:

- this reduces manual follow-up work
- this surfaces stuck suppliers earlier
- this prioritizes high-impact supplier cases
- this gives a path from export-based workflow to deeper integration later

### `run_demo.py`

Responsibilities:

1. run the full workflow from the command line
2. write all outputs
3. print a short terminal summary

Execution order must be:

1. load config
2. load input data
3. normalize data
4. classify suppliers
5. score suppliers
6. decide actions
7. generate drafts and notes
8. build reports
9. save all output files
10. print summary

Terminal summary must show:

- total suppliers processed
- number of outreach drafts created
- number of escalation notes created
- whether AI enrichment was used
- output path

### `app.py`

Responsibilities:

1. run a Streamlit UI
2. let the user load sample data or upload another CSV
3. trigger the workflow
4. display KPIs, tables, charts, and draft previews
5. allow downloads of outputs

---

## Streamlit UI Specification

Build the app in this exact page order.

### 1. Header

Show:

- title: `Supplier Onboarding Acceleration Demo`
- subtitle: `SupplyOn-tailored prototype using synthetic supplier rollout data`

Add a small info box stating:

- not an official SupplyOn integration
- all data shown is synthetic

### 2. Sidebar

Include:

- optional CSV uploader
- checkbox or toggle: `Use AI enrichment if API key available`
- language filter
- segment filter
- minimum score slider
- `Run workflow` button

### 3. KPI Overview

Display at least these metrics:

- total suppliers
- completion rate
- outreach items
- escalations
- overdue suppliers
- average rollout age

### 4. Supplier Segmentation Table

Display a table sorted by `overall_score` descending.

Required visible columns:

- supplier_name
- buyer_name
- status_segment
- blocker_reason
- preferred_language
- days_since_rollout
- overall_score
- recommended_action

### 5. Outreach Queue Section

Display:

- outreach queue table
- row selector or dropdown
- preview panel for the selected generated supplier email

### 6. Escalation Queue Section

Display:

- escalation queue table
- row selector or dropdown
- preview panel for the selected internal escalation note

### 7. Charts Section

Include:

- bar chart: suppliers by segment
- bar chart: blockers by reason
- chart of suppliers by days-since-rollout bucket

Use Plotly for these charts.

### 8. Generated Files Section

Provide download access or file listing for:

- segmented_suppliers.csv
- outreach_queue.csv
- escalation_queue.csv
- kpi_summary.json
- executive_summary.html

The UI should be clean and practical, not overdesigned.

---

## Template Requirements

Create the following markdown templates:

1. `email_invited_no_action_en.md`
2. `email_invited_no_action_de.md`
3. `email_started_incomplete_en.md`
4. `email_started_incomplete_de.md`
5. `email_missing_data_en.md`
6. `email_missing_data_de.md`
7. `email_contract_blocked_en.md`
8. `email_contract_blocked_de.md`
9. `email_technical_guidance_en.md`
10. `email_technical_guidance_de.md`
11. `internal_escalation_note.md`
12. `dashboard_intro.md`

### Supplier-Facing Template Rules

Every supplier-facing template must:

- stay under 180 words
- sound professional and operational
- mention the buyer name
- mention the relevant service
- describe the issue clearly
- ask for one concrete next step
- include a short help or FAQ reference
- avoid legal language
- avoid vague AI-sounding wording

### Internal Escalation Note Rules

The escalation note must include:

- supplier name
- buyer name
- current segment
- blocker reason
- how long the case has been open
- why it was escalated
- who should handle it
- suggested next human step

### Language Requirements

Support:

- English
- German

No other languages are required in v1.

---

## Human-Readable Label Mapping

Inside the code, create helper mappings from internal machine labels to display text.

Examples:

- `no_response_after_invite` -> `No response after invitation`
- `missing_contact_or_master_data` -> `Missing contact or master data`
- `contract_signature_pending` -> `Contract signature pending`
- `technical_connection_pending` -> `Technical connection pending`
- `long_running_overdue_case` -> `Overdue onboarding case`

Also map actions to readable descriptions:

- `send_reminder_1` -> `Send first reminder`
- `send_reminder_2` -> `Send second reminder`
- `send_missing_data_request` -> `Request missing onboarding information`
- `send_contract_help` -> `Send contract support guidance`
- `send_technical_guidance` -> `Send technical setup guidance`
- `route_to_onboarding_specialist` -> `Route to onboarding specialist`
- `route_to_account_owner` -> `Route to account owner`
- `no_action_completed` -> `No action needed`

These mappings are needed for the UI, markdown drafts, and report readability.

---

## Detailed Action Logic Summary

This section exists so the implementer cannot misunderstand the decision tree.

### Supplier-facing outreach should be created only if:

- the supplier has a contact email
- the action is one of:
  - `send_reminder_1`
  - `send_reminder_2`
  - `send_missing_data_request`
  - `send_contract_help`
  - `send_technical_guidance`

### Internal escalation notes should be created if:

- `needs_human_escalation = true`
- or the action is:
  - `route_to_onboarding_specialist`
  - `route_to_account_owner`

### Supplier-facing outreach must never be created for:

- completed suppliers
- suppliers with missing contact emails
- purely escalated cases with no outreach action

### Strategic supplier behavior

Strategic suppliers must escalate faster in edge cases.

In this v1 prototype, that means:

- all overdue strategic suppliers go to `route_to_account_owner`
- comparable non-strategic overdue suppliers go to `route_to_onboarding_specialist`

This rule must be visible in the output so it is obvious in the demo.

---

## CLI Execution Requirements

The command:

```powershell
python run_demo.py
```

must:

1. complete successfully
2. process the sample CSV
3. create all output files
4. print a readable terminal summary

If the project uses a virtual environment, the README may recommend one, but the code must not depend on IDE-specific behavior.

---

## Optional AI Enrichment Behavior

The system must be designed so that AI enhancement is easy to enable later.

### Required behavior without API key

If there is no OpenAI API key:

- app still works
- CLI still works
- deterministic templates are generated
- no crashes occur

### Required behavior with API key

If an API key is later added:

- the same deterministic message is built first
- that message may be lightly rewritten for clarity and personalization
- no underlying facts may change

### Prompt Design Constraints

The prompt must tell the model:

- do not change facts
- do not invent statuses
- do not change the recommended action
- do not add claims about integration or compliance
- preserve the exact language
- keep the tone short and operational

The implementer should not make prompt design decisions beyond this.

---

## Report Specification

### `outputs/reports/executive_summary.html`

This must be a standalone HTML file that can be opened in a browser without the Streamlit app.

It should contain:

1. title and context
2. processing timestamp
3. KPI summary cards
4. segment table or chart
5. blocker summary
6. top-priority supplier preview
7. outreach queue preview
8. escalation queue preview
9. one sample English outreach draft
10. one sample German outreach draft
11. one sample internal escalation note
12. a short "why this matters" section

The report does not need advanced CSS. Basic clean styling is enough.

---

## Demo Script For Presentation

Create `docs/demo_script.md`.

It must instruct the presenter to show the prototype in this order:

1. Explain the problem:
   - supplier onboarding gets stuck
   - manual follow-up is repetitive
   - not all suppliers matter equally
2. Show the sample dataset:
   - synthetic data
   - realistic onboarding statuses and blockers
3. Run the CLI workflow:
   - show that outputs are generated automatically
4. Open Streamlit:
   - show KPI overview
5. Show segmentation:
   - suppliers grouped by stage and blocker
6. Show one English outreach draft
7. Show one German outreach draft
8. Show one strategic supplier escalation note
9. Show the HTML executive summary
10. Close with:
   - can start from CSV exports
   - can later connect to APIs, ticketing, or LLM-based assistants

This matters because the prototype is not only code. It is a sales demonstration asset.

---

## README Requirements

Create a useful `README.md`.

It must include:

1. project purpose
2. what the prototype demonstrates
3. setup steps
4. dependency installation
5. how to run CLI mode
6. how to run Streamlit mode
7. explanation of outputs
8. explanation of deterministic mode vs optional AI enrichment
9. note that all data is synthetic
10. note that this is not a live SupplyOn integration

The README must be simple enough that a junior person can follow it without assumptions.

---

## Required Python Dependencies

Use the minimum set of libraries needed.

Recommended `requirements.txt`:

- `pandas`
- `streamlit`
- `python-dotenv`
- `jinja2`
- `plotly`
- `openai`

Do not add:

- SQLAlchemy
- FastAPI
- Django
- Celery
- Redis
- authentication libraries
- test frameworks unless the implementer has extra time

Keep the stack minimal.

---

## Recommended Implementation Order

The junior implementer must follow this order exactly.

### Phase 1: Skeleton

1. create the root folder
2. create the full folder structure
3. create empty files
4. write `requirements.txt`
5. write `.env.example`
6. write `src/schema.py`

### Phase 2: Data

7. create `data/sample_supplier_rollout.csv`
8. create `data/sample_faq.csv`
9. create `data/sample_status_rules.csv`
10. write `docs/dataset_design.md` explaining how the synthetic data is structured

### Phase 3: Core Logic

11. implement `src/ingest.py`
12. implement `src/normalize.py`
13. implement `src/classify.py`
14. implement `src/scoring.py`
15. implement `src/decision_engine.py`

### Phase 4: Templates And Outputs

16. create all markdown templates
17. implement `src/template_engine.py` in deterministic mode only
18. implement `src/report_builder.py`
19. implement `run_demo.py`

### Phase 5: Validate Core Flow

20. run the CLI workflow
21. verify all output files are created
22. inspect at least 5 generated drafts manually
23. inspect at least 5 escalated cases manually

### Phase 6: UI

24. implement `app.py`
25. connect the backend processing to Streamlit
26. add KPI cards, tables, and charts
27. add preview sections
28. add output download access

### Phase 7: Optional AI Layer

29. implement `src/llm_optional.py`
30. add AI toggle to the UI
31. ensure graceful fallback when no key exists

### Phase 8: Documentation

32. write `README.md`
33. write `docs/demo_script.md`
34. copy this plan into `docs/implementation_plan.md`

This order is important. The implementer must not start with the UI before the backend works.

---

## Acceptance Criteria

The prototype is only complete if all conditions below are true.

### Core Execution

1. `python run_demo.py` runs successfully without an API key.
2. The workflow reads the sample CSV and creates all required outputs.
3. No production integration is required for execution.

### Data Processing

4. All rows are normalized into the canonical schema.
5. All rows receive a status segment.
6. All rows receive a blocker reason.
7. All rows receive scores and a recommended action.

### Message Generation

8. At least one English supplier draft is generated.
9. At least one German supplier draft is generated.
10. At least one internal escalation note is generated.
11. Suppliers without contact email do not receive supplier-facing drafts.

### Business Logic

12. Completed suppliers receive `no_action_completed`.
13. Overdue strategic suppliers route to account owner.
14. Overdue non-strategic suppliers route to onboarding specialist.
15. Technical EDI/M2M cases can become technical setup pending.
16. Contract cases can become contract pending.

### UI

17. `streamlit run app.py` opens a working local app.
18. The UI shows KPIs, tables, charts, and draft previews.
19. The UI works without an API key.

### Reporting

20. The static HTML report is created.
21. The report can be opened locally in a browser.

### Optional AI

22. If AI is disabled, deterministic output still works.
23. If AI is enabled but no key exists, the app does not crash.
24. If AI is enabled and a valid key exists later, enriched drafts are generated while preserving facts.

---

## Manual Test Cases

The implementer must validate these exact scenarios.

1. A completed supplier becomes `completed` and generates no outreach.
2. A supplier invited 8 days ago with 0 reminders becomes `invited_no_action` and gets `send_reminder_1`.
3. A supplier invited 15 days ago with no progress becomes `invited_no_action` or `overdue_escalation` according to the implemented threshold logic, but this logic must be consistent with the code and documentation.
4. A supplier open for 28 or more days becomes `overdue_escalation`.
5. A supplier with blank contact email becomes `missing_master_data` and escalates.
6. A supplier with notes indicating signature issues becomes `contract_pending`.
7. A supplier with EDI/M2M setup notes becomes `technical_setup_pending`.
8. A strategic overdue supplier routes to `route_to_account_owner`.
9. A non-strategic overdue supplier routes to `route_to_onboarding_specialist`.
10. A German supplier with missing language but country Germany defaults to `de`.
11. A US supplier with missing language defaults to `en`.
12. AI toggle off generates deterministic drafts only.
13. AI toggle on with no key falls back safely.

Important implementation note:

The threshold logic must be kept internally consistent. If the implementer adjusts the 14-day invite logic to preserve cleaner separation between `invited_no_action` and `overdue_escalation`, they must update both code and docs together. However, they should prefer the logic already defined in this spec and avoid inventing new behavior.

---

## Edge Cases And Failure Behavior

Handle these situations explicitly.

### Missing Input File

If the input CSV path is invalid:

- show a readable error
- do not show a Python traceback unless in debug mode

### Missing Required Columns

If the CSV is missing required columns:

- raise a clear validation error naming the missing columns

### Empty Dataset

If the CSV has zero rows:

- show a readable error or warning
- do not attempt message generation

### Invalid Dates

If a date cannot be parsed:

- attempt safe coercion
- if coercion fails, leave it null and log the issue
- rows with unusable rollout dates may be excluded or flagged, but the behavior must be documented in code comments

### Missing Contact Name

If contact name is missing:

- use `"Supplier Team"` for rendering only

### Missing Contact Email

If contact email is missing:

- do not generate supplier-facing outreach
- escalate internally

---

## Design Principles The Implementer Must Follow

1. Keep business logic deterministic.
2. Keep AI optional and secondary.
3. Prefer simple pandas pipelines over abstract architecture.
4. Keep files readable and beginner-friendly.
5. Do not over-engineer the prototype.
6. Use comments only where logic is not obvious.
7. Make outputs demo-friendly, not just technically correct.
8. Make naming operational and understandable.

---

## Final Instruction To The Implementer

When building this prototype:

- do not improvise the product scope
- do not add infrastructure that was not requested
- do not replace deterministic action logic with AI
- do not skip the synthetic data design
- do not skip documentation
- do not skip the HTML report
- do not skip German support
- do not stop after the CLI works; the Streamlit UI is required

The target outcome is not just "some code." The target outcome is a demoable, credible workflow prototype that can be shown to a company representative as evidence of workflow-automation capability.
