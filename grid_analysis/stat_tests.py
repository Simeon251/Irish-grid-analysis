import numpy as np
import pandas as pd
from scipy import stats


def weekend_vs_weekday_tests(cleaned_df: pd.DataFrame) -> dict:
    df = cleaned_df.copy()

    df["NI_Demand"] = pd.to_numeric(df.get("NI Demand", df.get("NI_Demand", np.nan)), errors="coerce")
    df["IE_Demand"] = pd.to_numeric(df.get("IE Demand", df.get("IE_Demand", np.nan)), errors="coerce")
    df["NI_Solar"] = pd.to_numeric(df.get("NI Solar Generation", df.get("NI_Solar", np.nan)), errors="coerce")
    df["IE_Solar"] = pd.to_numeric(df.get("IE Solar Generation", df.get("IE_Solar", np.nan)), errors="coerce")

    if "dayofweek" not in df.columns:
        df["dayofweek"] = df.index.dayofweek

    weekend_mask = df["dayofweek"].isin([5, 6])
    weekday_mask = df["dayofweek"].isin([0, 1, 2, 3, 4])

    results = {}
    for col in ["NI_Demand", "IE_Demand", "NI_Solar", "IE_Solar"]:
        wkend = df.loc[weekend_mask, col].dropna().values
        wkday = df.loc[weekday_mask, col].dropna().values

        t_stat, t_p = _welch(wkend, wkday)
        mw_stat, mw_p = _mannwhitney(wkend, wkday)

        results[col] = {
            "weekend_mean": float(np.nanmean(wkend)) if len(wkend) > 0 else np.nan,
            "weekday_mean": float(np.nanmean(wkday)) if len(wkday) > 0 else np.nan,
            "n_weekend": int(len(wkend)),
            "n_weekday": int(len(wkday)),
            "welch_tstat": t_stat,
            "welch_pval": t_p,
            "mw_stat": mw_stat,
            "mw_pval": mw_p,
        }

    _print_results(results)
    return results


def _welch(a: np.ndarray, b: np.ndarray) -> tuple[float, float]:
    if len(a) == 0 or len(b) == 0:
        return np.nan, np.nan
    t, p = stats.ttest_ind(a, b, equal_var=False, nan_policy="omit")
    return float(t), float(p)


def _mannwhitney(a: np.ndarray, b: np.ndarray) -> tuple[float, float]:
    if len(a) == 0 or len(b) == 0:
        return np.nan, np.nan
    u, p = stats.mannwhitneyu(a, b, alternative="two-sided")
    return float(u), float(p)


def _print_results(results: dict) -> None:
    print(f"\n{'Variable':<15} {'Weekend mean':>14} {'Weekday mean':>13} {'Welch p':>10} {'MW p':>10}")
    print("-" * 65)
    for col, r in results.items():
        print(
            f"{col:<15} {r['weekend_mean']:>14.2f} {r['weekday_mean']:>13.2f}"
            f" {r['welch_pval']:>10.4f} {r['mw_pval']:>10.4f}"
        )
