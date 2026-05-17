# Demo Seed Notes

This file exists as a reference for the demo presenter.

## Key Scenarios to Highlight

### 1. Strategic Overdue → Account Owner
SUP-016 (Siemens AG) is a strategic supplier with high spend and 32 days overdue → routes to account owner.
SUP-002 (Bosch GmbH) is strategic, 55 days overdue → routes to account owner.

### 2. Missing Contact Email → Escalation
SUP-026 (Schaeffler Paravan), SUP-038 (Bühler Motor), SUP-051 to SUP-054 all have no contact email → missing_master_data → escalated to onboarding specialist.

### 3. Contract Blocker
SUP-014 (ThyssenKrupp AG) and SUP-033 (WITTE Automotive) have contract signature issues → contract_pending segment.
SUP-055 (BKM Industrie) and SUP-056 (Dold GmbH, strategic) also have contract blockers.

### 4. Technical EDI/M2M Setup
SUP-004 (Continental AG) has EDI mapping pending → technical_setup_pending segment.
SUP-031 (Brose), SUP-037 (Mubea), SUP-047 (SMS) also have EDI/technical blockers.

### 5. German Language Default
SUP-015 (BASF SE) has empty language field but country is Germany → defaults to DE.

### 6. Completed Supplier
SUP-001 (Schaeffler AG) is completed → overall_score=0, no outreach, not in top-risk list.
SUP-043 (Kaco GmbH) is completed → no action needed.

### 7. Started Incomplete
SUP-007 (Valeo GmbH) has been in registration_started/incomplete for 12 days → started_incomplete.

### 8. Supplier-Facing Outreach
SUP-046 (Primetals Technologies, Austria) is invited, 12 days, high spend, no response → send_reminder_1 (DE template).
SUP-020 (Grupo Antolin, Spain) is invited, 12 days, medium spend → send_reminder_1 (EN template).
