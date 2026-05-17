import sys
import json
from pathlib import Path

import config
from src.ingest import load_csv
from src.normalize import normalize
from src.classify import classify
from src.scoring import compute_scores
from src.decision_engine import decide_actions, split_queues
from src.template_engine import generate_all
from src.report_builder import build_kpi_summary, build_html_report


def main():
    input_path = config.DEFAULT_INPUT_PATH
    output_dir = config.ensure_output_dirs()
    enable_llm = config.ENABLE_LLM_ENRICHMENT and bool(config.OPENAI_API_KEY)

    print(f"SupplyOn Supplier Onboarding Acceleration Demo")
    print(f"{'='*50}")
    print(f"Input: {input_path}")
    print(f"Output: {output_dir}")
    print(f"AI Enrichment: {'enabled' if enable_llm else 'disabled'}")
    print()

    # 1. Load
    print("[1/9] Loading input data...")
    df = load_csv(input_path)
    print(f"       Loaded {len(df)} supplier rows")

    # 2. Normalize
    print("[2/9] Normalizing data...")
    df = normalize(df)

    # 3. Classify
    print("[3/9] Classifying suppliers...")
    df = classify(df)

    # 4. Score
    print("[4/9] Computing scores...")
    df = compute_scores(df)

    # 5. Decide actions
    print("[5/9] Deciding actions...")
    df = decide_actions(df)
    outreach, escalation = split_queues(df)

    # 6. Generate drafts and notes
    print("[6/9] Generating drafts and notes...")
    email_count, note_count = generate_all(
        df, output_dir=str(output_dir), enable_llm=enable_llm
    )

    # 7. Build reports
    print("[7/9] Building reports...")
    summary = build_kpi_summary(df)
    report_path = build_html_report(df, summary, output_dir=str(output_dir))

    # 8. Save outputs
    print("[8/9] Saving output files...")
    segmented_path = Path(output_dir) / "segmented_suppliers.csv"
    df.to_csv(segmented_path, index=False)

    outreach_path = Path(output_dir) / "outreach_queue.csv"
    outreach.to_csv(outreach_path, index=False)

    escalation_path = Path(output_dir) / "escalation_queue.csv"
    escalation.to_csv(escalation_path, index=False)

    kpi_path = Path(output_dir) / "kpi_summary.json"
    with open(kpi_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)

    # 9. Summary
    print("[9/9] Done!")
    print()
    print(f"{'='*50}")
    print(f"SUMMARY")
    print(f"{'='*50}")
    print(f"  Total suppliers processed:    {summary['total_suppliers']}")
    print(f"  Outreach drafts created:      {email_count}")
    print(f"  Escalation notes created:     {note_count}")
    print(f"  Completion rate:              {summary['completion_rate_pct']}%")
    print(f"  Overdue suppliers:            {summary['overdue_count']}")
    print(f"  AI enrichment used:           {'yes' if enable_llm else 'no'}")
    print()
    print(f"Outputs saved to: {output_dir}")
    print()
    print(f"To start the Streamlit UI, run:")
    print(f"  streamlit run app.py")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
