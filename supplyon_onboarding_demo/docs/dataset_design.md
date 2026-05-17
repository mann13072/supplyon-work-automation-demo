# Dataset Design

## Sample Supplier Rollout CSV

**File:** `data/sample_supplier_rollout.csv`

### Design Principles

The dataset is designed to look realistic for a SupplyOn supplier onboarding scenario while being small enough to inspect manually (60 rows).

### Coverage Requirements Met

- **6+ countries:** Germany, Austria, France, Japan, Ireland, United States, Spain, Italy, South Korea, Switzerland
- **English and German suppliers:** Balanced mix of DE and EN preferred languages
- **8+ overdue suppliers:** Multiple suppliers with rollout dates 28+ days ago
- **6+ missing master data cases:** SUP-026, SUP-038, SUP-051, SUP-052, SUP-053, SUP-054 have empty contact emails
- **6+ started-but-incomplete cases:** SUP-007, SUP-009, SUP-018, SUP-021, SUP-035, SUP-044
- **5+ strategic suppliers:** SUP-001, SUP-002, SUP-003, SUP-011, SUP-013, SUP-016, SUP-056
- **Multiple connection types:** EDI_M2M and Portal
- **3+ completed suppliers:** SUP-001, SUP-011, SUP-013, SUP-028, SUP-034, SUP-039, SUP-043, SUP-049
- **Large suppliers with high urgency but low response:** SUP-002, SUP-016, SUP-046
- **Intentionally messy fields:** Inconsistent whitespace, empty fields, mixed casing, trailing spaces

### Intentional Data Quality Issues

| Issue | Example Row |
|-------|-------------|
| Empty preferred language | SUP-015 (Germany, no language → defaults to DE) |
| Empty contact name | SUP-022, SUP-029, SUP-041 (uses fallback "Supplier Team") |
| Empty contact email | SUP-026, SUP-038, SUP-051, SUP-052, SUP-053, SUP-054 |
| Inconsistent whitespace | Various (randomly applied during generation) |
| Different status casing | Various (randomly applied during generation) |
| Mixed date formats | All use YYYY-MM-DD for consistency |
| Free-text hints in notes | SUP-004, SUP-014, SUP-033, SUP-047 |

## FAQ File

**File:** `data/sample_faq.csv`

Provides self-service help snippets for each onboarding segment in English and German. Used by the template engine to include contextual FAQ references in outreach drafts.

## Status Rules File

**File:** `data/sample_status_rules.csv`

Documents the rule definitions used for classification. In v1, the code uses explicit Python logic; this CSV exists as a visible rules artifact demonstrating that rules could become editable by operations teams in future versions.
