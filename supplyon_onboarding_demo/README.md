# SupplyOn Supplier Onboarding Acceleration Demo

A local demonstration prototype that automates supplier onboarding acceleration workflows for SupplyOn-style rollout operations.

> **Note:** This is a demonstration prototype. All data is synthetic. This is not an official SupplyOn integration.

## What This Demonstrates

1. Ingest supplier rollout export data (CSV)
2. Normalize messy supplier onboarding fields
3. Classify suppliers by onboarding stage and likely blocker
4. Score suppliers by urgency and business priority
5. Recommend the next best action
6. Generate English and German follow-up drafts
7. Generate internal escalation notes
8. Produce summary KPIs and reports
9. Present everything in a Streamlit dashboard

## Project Structure

```
supplyon_onboarding_demo/
  README.md              - This file
  requirements.txt       - Python dependencies
  .env.example           - Environment variable template
  app.py                 - Streamlit UI
  run_demo.py            - CLI entry point
  config.py              - Configuration and environment loading
  data/                  - Sample datasets
    sample_supplier_rollout.csv
    sample_faq.csv
    sample_status_rules.csv
  outputs/               - Generated files (after running)
    segmented_suppliers.csv
    outreach_queue.csv
    escalation_queue.csv
    kpi_summary.json
    generated_emails/
    generated_internal_notes/
    reports/
  src/                   - Core logic modules
    ingest.py
    schema.py
    normalize.py
    classify.py
    scoring.py
    decision_engine.py
    template_engine.py
    llm_optional.py
    report_builder.py
  templates/             - Markdown email and note templates
  docs/                  - Documentation
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment (Optional)

```bash
cp .env.example .env
```

Edit `.env` to set your OpenAI API key if you want AI enrichment (not required for basic operation).

## Running

### CLI Mode

```bash
python run_demo.py
```

This processes the sample dataset and writes all outputs to the `outputs/` directory.

### Streamlit UI Mode

```bash
streamlit run app.py
```

This opens an interactive dashboard in your browser.

## Outputs

After running, the `outputs/` directory contains:

- `segmented_suppliers.csv` — All suppliers with segments, scores, and actions
- `outreach_queue.csv` — Suppliers ready for automated outreach
- `escalation_queue.csv` — Suppliers requiring human intervention
- `kpi_summary.json` — Aggregate KPI data
- `generated_emails/*.md` — Draft follow-up emails per supplier
- `generated_internal_notes/*.md` — Escalation notes per case
- `reports/executive_summary.html` — Standalone HTML report

## Deterministic Mode vs AI Enrichment

By default, the system works entirely with deterministic business logic — no API key needed.

If you add an `OPENAI_API_KEY` to your `.env` file and enable enrichment (checkbox in UI or `ENABLE_LLM_ENRICHMENT=true` in `.env`), the system will optionally improve wording in generated drafts while preserving all factual content. The AI never changes segments, scores, actions, or statuses.

## Requirements

- Python 3.8+
- Dependencies: pandas, streamlit, python-dotenv, jinja2, plotly, openai (optional)
