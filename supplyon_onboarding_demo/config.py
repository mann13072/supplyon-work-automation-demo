import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent
DEFAULT_INPUT_PATH = os.getenv(
    "DEFAULT_INPUT_PATH",
    str(BASE_DIR / "data" / "sample_supplier_rollout.csv"),
)
DEFAULT_OUTPUT_DIR = os.getenv(
    "DEFAULT_OUTPUT_DIR",
    str(BASE_DIR / "outputs"),
)
DEFAULT_LANGUAGE_FALLBACK = os.getenv("DEFAULT_LANGUAGE_FALLBACK", "en")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ENABLE_LLM_ENRICHMENT = os.getenv("ENABLE_LLM_ENRICHMENT", "false").lower() == "true"


def ensure_output_dirs(output_dir: str = None):
    base = Path(output_dir or DEFAULT_OUTPUT_DIR)
    for sub in ["", "generated_emails", "generated_internal_notes", "reports"]:
        (base / sub).mkdir(parents=True, exist_ok=True)
    return base
