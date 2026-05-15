import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .config import WEEKDAY_MAP, WEEKDAY_ORDER


def plot_weekday_demand(cleaned_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = cleaned_df.copy()

    df["IE_Demand"] = pd.to_numeric(df.get("IE Demand", df.get("IE_Demand", np.nan)), errors="coerce")
    df["IE_Generation"] = pd.to_numeric(df.get("IE Generation", df.get("IE_Generation", np.nan)), errors="coerce")

    if "dayofweek" not in df.columns:
        df["dayofweek"] = df.index.dayofweek

    df["weekday"] = df["dayofweek"].map(WEEKDAY_MAP)

    ie_weekly_avg = (
        df.groupby("weekday")[["IE_Demand", "IE_Generation"]]
        .mean()
        .reindex(WEEKDAY_ORDER)
    )
    ie_weekly_avg.index.name = "Weekday"

    ie_weekday_counts = (
        df.groupby("weekday")[["IE_Demand", "IE_Generation"]]
        .count()
        .reindex(WEEKDAY_ORDER)
    )

    plt.rcParams["figure.dpi"] = 120

    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.bar(ie_weekly_avg.index, ie_weekly_avg["IE_Demand"], color="tab:blue")
    ax.set_xlabel("Weekday")
    ax.set_ylabel("Mean IE Demand (MW)")
    ax.set_title("Ireland: Average Demand by Weekday")
    ax.grid(axis="y", linestyle=":", alpha=0.6)
    plt.tight_layout()
    plt.show()

    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.bar(ie_weekly_avg.index, ie_weekly_avg["IE_Generation"], color="tab:green")
    ax.set_xlabel("Weekday")
    ax.set_ylabel("Mean IE Generation (MW)")
    ax.set_title("Ireland: Average Generation by Weekday")
    ax.grid(axis="y", linestyle=":", alpha=0.6)
    plt.tight_layout()
    plt.show()

    return ie_weekly_avg, ie_weekday_counts
