import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_hourly_wind_solar(cleaned_df: pd.DataFrame) -> pd.DataFrame:
    df = cleaned_df.copy()

    df["NI_Wind"] = pd.to_numeric(df.get("NI Wind Generation", df.get("NI_Wind", np.nan)), errors="coerce")
    df["NI_Solar"] = pd.to_numeric(df.get("NI Solar Generation", df.get("NI_Solar", np.nan)), errors="coerce")

    if "hour" not in df.columns:
        df["hour"] = df.index.hour

    hourly_mean = df.groupby("hour")[["NI_Wind", "NI_Solar"]].mean().reindex(range(24))

    plt.rcParams["figure.dpi"] = 120
    width = 0.6

    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.bar(hourly_mean.index, hourly_mean["NI_Wind"], color="tab:blue", width=width)
    ax.set_xticks(range(24))
    ax.set_xlabel("Hour of day (0-23)")
    ax.set_ylabel("Mean NI Wind Generation (MW)")
    ax.set_title("Northern Ireland: Average Wind Generation by Hour of Day")
    ax.grid(axis="y", linestyle=":", alpha=0.6)
    plt.tight_layout()
    plt.show()

    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.bar(hourly_mean.index, hourly_mean["NI_Solar"], color="gold", width=width, edgecolor="orange")
    ax.set_xticks(range(24))
    ax.set_xlabel("Hour of day (0-23)")
    ax.set_ylabel("Mean NI Solar Generation (MW)")
    ax.set_title("Northern Ireland: Average Solar Generation by Hour of Day")
    ax.grid(axis="y", linestyle=":", alpha=0.6)
    plt.tight_layout()
    plt.show()

    return hourly_mean
