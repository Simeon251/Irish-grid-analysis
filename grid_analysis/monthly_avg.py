import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_monthly_avg(cleaned_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = cleaned_df.copy()

    df["NI_Demand"] = pd.to_numeric(df.get("NI Demand", df.get("NI_Demand", np.nan)), errors="coerce")
    df["NI_Generation"] = pd.to_numeric(df.get("NI Generation", df.get("NI_Generation", np.nan)), errors="coerce")
    df["IE_Demand"] = pd.to_numeric(df.get("IE Demand", df.get("IE_Demand", np.nan)), errors="coerce")
    df["IE_Generation"] = pd.to_numeric(df.get("IE Generation", df.get("IE_Generation", np.nan)), errors="coerce")

    df["month"] = df.index.month

    ni_monthly_avg = (
        df.groupby("month")[["NI_Demand", "NI_Generation"]].mean().reindex(range(1, 13))
    )
    ni_monthly_avg.index.name = "Month"

    ie_monthly_avg = (
        df.groupby("month")[["IE_Demand", "IE_Generation"]].mean().reindex(range(1, 13))
    )
    ie_monthly_avg.index.name = "Month"

    plt.rcParams["figure.dpi"] = 120
    width = 0.35

    _bar_plot(
        ni_monthly_avg,
        col_a="NI_Demand",
        col_b="NI_Generation",
        label_a="NI Demand",
        label_b="NI Generation",
        color_a="tab:blue",
        color_b="tab:green",
        title="Northern Ireland (NI) Monthly Average: Demand and Generation",
        width=width,
    )
    _bar_plot(
        ie_monthly_avg,
        col_a="IE_Demand",
        col_b="IE_Generation",
        label_a="IE Demand",
        label_b="IE Generation",
        color_a="tab:orange",
        color_b="tab:green",
        title="Ireland (IE) Monthly Average: Demand and Generation",
        width=width,
    )

    return ni_monthly_avg, ie_monthly_avg


def _bar_plot(
    monthly_avg: pd.DataFrame,
    col_a: str,
    col_b: str,
    label_a: str,
    label_b: str,
    color_a: str,
    color_b: str,
    title: str,
    width: float,
) -> None:
    fig, ax = plt.subplots(figsize=(10, 4))
    months = monthly_avg.index
    ax.bar(months - width / 2, monthly_avg[col_a], width=width, label=label_a, color=color_a)
    ax.bar(months + width / 2, monthly_avg[col_b], width=width, label=label_b, color=color_b)
    ax.set_xticks(months)
    ax.set_xticklabels([str(m) for m in months])
    ax.set_xlabel("Month")
    ax.set_ylabel("MW (monthly mean)")
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    plt.show()
