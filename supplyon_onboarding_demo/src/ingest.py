import pandas as pd

from src.schema import RAW_COLUMNS


def load_csv(input_path: str) -> pd.DataFrame:
    df = pd.read_csv(input_path, dtype=str, keep_default_na=False)

    missing = [c for c in RAW_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(
            f"Missing required columns: {', '.join(missing)}"
        )

    if df.empty:
        raise ValueError("The input CSV file contains zero rows.")

    return df
