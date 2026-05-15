import numpy as np
import pandas as pd

from .config import CLEANED_OUTPUT_PATH, DATA_PATH, EXPECTED_NONNEG_COLS


def load_raw(path=None) -> pd.DataFrame:
    xlsx_path = path or DATA_PATH
    raw = pd.read_excel(xlsx_path, engine="openpyxl")
    print(f"Loaded dataset with {len(raw)} rows and {len(raw.columns)} columns.")
    return raw


def clean_data(raw: pd.DataFrame, save: bool = False) -> tuple[pd.DataFrame, dict]:
    raw = raw.copy()

    raw["DateTime_raw"] = raw["DateTime"]
    raw["DateTime_parsed"] = pd.to_datetime(raw["DateTime_raw"], errors="coerce")

    if "GMT Offset" in raw.columns:
        raw["GMT_Offset"] = pd.to_numeric(raw["GMT Offset"], errors="coerce")
    else:
        raw["GMT_Offset"] = np.nan

    raw["timestamp_local"] = raw["DateTime_parsed"] + pd.to_timedelta(
        raw["GMT_Offset"].fillna(0), unit="h"
    )
    raw.loc[raw["GMT_Offset"].isna(), "timestamp_local"] = raw.loc[
        raw["GMT_Offset"].isna(), "DateTime_parsed"
    ]

    raw = raw.sort_values("timestamp_local").reset_index(drop=True)
    raw.index = pd.DatetimeIndex(raw["timestamp_local"], name="timestamp_local")

    raw["hour"] = raw.index.hour
    raw["date"] = raw.index.date
    raw["dayofweek"] = raw.index.dayofweek
    raw["month"] = raw.index.month
    raw["year"] = raw.index.year

    missing_counts = raw.isna().sum()

    expected_full_index = pd.date_range(
        start=raw.index.min(),
        end=raw.index.max(),
        freq="15min",
        name="timestamp_local",
    )
    missing_timestamps = expected_full_index.difference(raw.index)

    raw["is_duplicate_timestamp"] = raw.index.duplicated(keep=False)
    n_duplicate_rows = int(raw["is_duplicate_timestamp"].sum())

    time_deltas_min = (
        raw.index.to_series().diff().dt.total_seconds().div(60)
    )
    irregular_gap_count = int((time_deltas_min.fillna(15) != 15).sum())

    existing_nonneg_cols = [c for c in EXPECTED_NONNEG_COLS if c in raw.columns]
    negatives_report = {}
    for col in existing_nonneg_cols:
        numeric = pd.to_numeric(raw[col], errors="coerce")
        neg_mask = numeric < 0
        n_neg = int(neg_mask.sum())
        sample_neg_ts = list(raw.index[neg_mask][:10])
        negatives_report[col] = {"count_negative": n_neg, "example_timestamps": sample_neg_ts}
        raw[f"{col}_was_negative"] = neg_mask
        raw[col] = numeric.mask(neg_mask, np.nan)

    cleaning_summary = {
        "n_rows": int(len(raw)),
        "missing_counts": missing_counts.to_dict(),
        "n_missing_timestamps_expected": int(len(missing_timestamps)),
        "n_duplicate_rows": n_duplicate_rows,
        "n_irregular_gaps": irregular_gap_count,
        "negatives_report": negatives_report,
    }

    cleaned_df = raw.copy()

    if save:
        cleaned_df.to_excel(CLEANED_OUTPUT_PATH, index=True)
        print(f"Cleaned dataset saved to {CLEANED_OUTPUT_PATH}")

    return cleaned_df, cleaning_summary
