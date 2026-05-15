import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf

MAX_LAGS = 10 * 24 * 4  # 10 days at 15-min resolution = 960 lags


def plot_acf_all(cleaned_df: pd.DataFrame) -> None:
    df = cleaned_df.copy()

    df["NI_Wind"] = pd.to_numeric(df.get("NI Wind Generation", df.get("NI_Wind", np.nan)), errors="coerce")
    df["NI_Solar"] = pd.to_numeric(df.get("NI Solar Generation", df.get("NI_Solar", np.nan)), errors="coerce")
    df["IE_Wind"] = pd.to_numeric(df.get("IE Wind Generation", df.get("IE_Wind", np.nan)), errors="coerce")
    df["IE_Solar"] = pd.to_numeric(df.get("IE Solar Generation", df.get("IE_Solar", np.nan)), errors="coerce")

    series_config = [
        ("NI_Wind", "tab:red", "NI Wind Generation"),
        ("NI_Solar", "tab:green", "NI Solar Generation"),
        ("IE_Wind", "tab:brown", "IE Wind Generation"),
        ("IE_Solar", "tab:orange", "IE Solar Generation"),
    ]

    plt.rcParams["figure.dpi"] = 120
    plt.rcParams["figure.figsize"] = (10, 3.6)

    for col, color, label in series_config:
        s = _prepare(df[col])
        if len(s) == 0:
            print(f"Skipping {label}: no valid data.")
            continue
        plt.figure()
        plot_acf(s, lags=MAX_LAGS, alpha=0.05, zero=True, color=color)
        plt.title(f"ACF: {label} (lags up to 10 days)")
        plt.xlabel("Lag (15-minute intervals; 96 = 1 day)")
        plt.ylabel("Autocorrelation")
        plt.tight_layout()
        plt.show()


def _prepare(series: pd.Series) -> pd.Series:
    s = series.dropna().astype(float)
    return s - s.mean() if len(s) > 0 else s
