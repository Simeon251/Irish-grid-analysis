import pandas as pd


def compute_monthly_stats(cleaned_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    ie_cols = {
        "IE Demand": "IE_Demand",
        "IE Wind Generation": "IE_Wind",
        "IE Solar Generation": "IE_Solar",
    }
    ni_cols = {
        "NI Demand": "NI_Demand",
        "NI Wind Generation": "NI_Wind",
        "NI Solar Generation": "NI_Solar",
    }

    available_ie = {k: v for k, v in ie_cols.items() if k in cleaned_df.columns}
    available_ni = {k: v for k, v in ni_cols.items() if k in cleaned_df.columns}

    work = cleaned_df.copy()
    for orig, new in {**available_ie, **available_ni}.items():
        work[new] = pd.to_numeric(work[orig], errors="coerce")

    work["month"] = work.index.month
    agg_funcs = ["mean", "max", "min"]

    ie_monthly = (
        work[list(available_ie.values()) + ["month"]]
        .groupby("month")
        .agg(agg_funcs)
    )
    ie_monthly.columns = ["_".join(col).strip() for col in ie_monthly.columns.values]
    ie_monthly = ie_monthly.sort_index()

    ni_monthly = (
        work[list(available_ni.values()) + ["month"]]
        .groupby("month")
        .agg(agg_funcs)
    )
    ni_monthly.columns = ["_".join(col).strip() for col in ni_monthly.columns.values]
    ni_monthly = ni_monthly.sort_index()

    ie_tidy = _tidy_table(ie_monthly, "IE")
    ni_tidy = _tidy_table(ni_monthly, "NI")

    print("\nIreland Monthly Summary:\n")
    print(ie_tidy.to_string(index=False))
    print("\nNorthern Ireland Monthly Summary:\n")
    print(ni_tidy.to_string(index=False))

    return ie_tidy, ni_tidy


def _tidy_table(monthly_df: pd.DataFrame, prefix: str) -> pd.DataFrame:
    cols_order = []
    for var in ["Demand", "Wind", "Solar"]:
        base = f"{prefix}_{var}"
        for agg in ["mean", "max", "min"]:
            candidate = f"{base}_{agg}"
            if candidate in monthly_df.columns:
                cols_order.append(candidate)

    tidy = monthly_df[cols_order].copy()
    rename_map = {"_".join(c.split("_")[1:]): c for c in tidy.columns}
    tidy = tidy.rename(columns={v: k for k, v in rename_map.items()})
    tidy = tidy.reset_index().rename(columns={"month": "Month"})
    tidy["Month"] = tidy["Month"].astype(int)
    return tidy
