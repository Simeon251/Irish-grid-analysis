import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from .config import WEEKDAY_MAP, WEEKDAY_ORDER

ALL_HOURS = list(range(24))


def plot_daily_profiles(cleaned_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = cleaned_df.copy()

    df["NI_Demand"] = pd.to_numeric(df.get("NI Demand", df.get("NI_Demand", np.nan)), errors="coerce")
    df["IE_Demand"] = pd.to_numeric(df.get("IE Demand", df.get("IE_Demand", np.nan)), errors="coerce")

    if "hour" not in df.columns:
        df["hour"] = df.index.hour
    if "dayofweek" not in df.columns:
        df["dayofweek"] = df.index.dayofweek

    df["weekday_name"] = df["dayofweek"].map(WEEKDAY_MAP)

    ni_profiles = _hourly_by_weekday(df, "NI_Demand")
    ie_profiles = _hourly_by_weekday(df, "IE_Demand")

    sns.set_style("whitegrid")
    plt.rcParams["figure.dpi"] = 120

    _profile_plot(ni_profiles, ylabel="Mean NI Demand (MW)", title="Northern Ireland: Average Daily Demand Profile by Weekday")
    _profile_plot(ie_profiles, ylabel="Mean IE Demand (MW)", title="Ireland: Average Daily Demand Profile by Weekday")

    return ni_profiles, ie_profiles


def _hourly_by_weekday(df: pd.DataFrame, col: str) -> pd.DataFrame:
    grouped = (
        df.groupby(["weekday_name", "hour"])[col]
        .mean()
        .unstack(level="hour")
        .reindex(index=WEEKDAY_ORDER)
        .reindex(columns=ALL_HOURS)
    )
    return grouped


def _profile_plot(profiles: pd.DataFrame, ylabel: str, title: str) -> None:
    fig, ax = plt.subplots(figsize=(10, 4))
    for weekday in profiles.index:
        ax.plot(ALL_HOURS, profiles.loc[weekday].values, label=weekday, linewidth=1.6)
    ax.set_xticks(range(0, 24, 2))
    ax.set_xlabel("Hour of day (0-23)")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(title="Weekday", bbox_to_anchor=(1.02, 1), loc="upper left")
    ax.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()
    plt.show()
