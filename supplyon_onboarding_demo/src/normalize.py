import logging

import pandas as pd
import re

from src.schema import RAW_COLUMNS, CANONICAL_COLUMNS

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

logger = logging.getLogger(__name__)

RAW_TO_CANONICAL = dict(zip(RAW_COLUMNS, CANONICAL_COLUMNS))

GERMAN_SPEAKING_COUNTRIES = {"germany", "austria", "switzerland"}


def _map_language(val: str, country: str) -> str:
    cleaned = val.strip().lower() if val.strip() else ""
    if cleaned in ("en", "english", "eng"):
        return "en"
    if cleaned in ("de", "german", "deutsch", "ger"):
        return "de"
    if not cleaned and country.strip().lower() in GERMAN_SPEAKING_COUNTRIES:
        return "de"
    return "en"


def _normalize_status(val: str) -> str:
    cleaned = val.strip().lower().replace(" ", "_")
    cleaned = re.sub(r"[^a-z0-9_]", "", cleaned)
    return cleaned


def _parse_date(val: str):
    if not val.strip():
        return pd.NaT
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y", "%Y/%m/%d"):
        try:
            return pd.to_datetime(val.strip(), format=fmt)
        except (ValueError, TypeError):
            continue
    try:
        return pd.to_datetime(val.strip())
    except (ValueError, TypeError):
        logger.warning("Could not parse date: %s", val.strip()[:30])
        return pd.NaT


def normalize(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.rename(columns=RAW_TO_CANONICAL, inplace=True)

    str_cols = [
        "supplier_id", "supplier_name", "buyer_name", "buyer_region",
        "service_name", "country", "preferred_language", "contact_name",
        "contact_email", "duns_number", "registration_status", "substatus",
        "connection_type", "annual_spend_tier", "notes",
    ]
    for col in str_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    df["preferred_language"] = df.apply(
        lambda r: _map_language(r["preferred_language"], r["country"]), axis=1
    )

    status_cols = ["registration_status", "substatus", "connection_type"]
    for col in status_cols:
        if col in df.columns:
            df[col] = df[col].apply(_normalize_status)

    if "strategic_supplier_flag" in df.columns:
        df["strategic_supplier_flag"] = df["strategic_supplier_flag"].str.strip().str.lower().isin(
            ["true", "yes", "1", "t"]
        )

    tier_map = {
        "high": "high", "h": "high", "3": "high",
        "medium": "medium", "med": "medium", "m": "medium", "2": "medium",
        "low": "low", "l": "low", "1": "low",
    }
    if "annual_spend_tier" in df.columns:
        df["annual_spend_tier"] = (
            df["annual_spend_tier"]
            .str.strip()
            .str.lower()
            .map(tier_map)
            .fillna("low")
        )

    date_cols = ["rollout_date", "last_status_change_date", "last_contact_date"]
    for col in date_cols:
        if col in df.columns:
            df[col] = df[col].apply(_parse_date)

    now = pd.Timestamp.now().normalize()
    df["days_since_rollout"] = (now - df["rollout_date"]).dt.days.fillna(0).astype(int)
    df["days_in_current_status"] = (
        (now - df["last_status_change_date"]).dt.days.fillna(0).astype(int)
    )

    def _age_bucket(days):
        if days >= 28:
            return "28_plus_days"
        if days >= 14:
            return "14_27_days"
        if days >= 7:
            return "7_13_days"
        return "0_6_days"

    df["age_bucket"] = df["days_since_rollout"].apply(_age_bucket)

    for col in ["response_count", "reminder_count"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    mask_valid = df["contact_email"].apply(lambda v: bool(EMAIL_RE.match(str(v))) if v.strip() else False)
    df.loc[~mask_valid, "contact_email"] = ""

    df["contact_name"] = df["contact_name"].fillna("").replace("", "Supplier Team")

    return df
