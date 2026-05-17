import logging

logger = logging.getLogger(__name__)


def maybe_enrich_message(
    draft_text: str,
    context_dict: dict,
    language: str = "en",
    mode: str = "supplier_message",
) -> str:
    return draft_text
