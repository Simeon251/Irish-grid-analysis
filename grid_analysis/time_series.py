import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def plot_daily_weekly(cleaned_df: pd.DataFrame) -> None:
    df = cleaned_df.copy()

    cols_map = {
        "IE Demand": "IE_Demand",
        "IE Generation": "IE_Generation",
        "IE Wind Generation": "IE_Wind",
        "IE Solar Generation": "IE_Solar",
        "NI Demand": "NI_Demand",
        "NI Generation": "NI_Generation",
        "NI Wind Generation": "NI_Wind",
        "NI Solar Generation": "NI_Solar",
    }
    for orig, new in cols_map.items():
        if orig in df.columns:
            df[new] = pd.to_numeric(df[orig], errors="coerce")

    if "IE_Generation" not in df.columns and {"IE_Wind", "IE_Solar"}.issubset(df.columns):
        df["IE_Generation"] = df[["IE_Wind", "IE_Solar"]].sum(axis=1)
    if "NI_Generation" not in df.columns and {"NI_Wind", "NI_Solar"}.issubset(df.columns):
        df["NI_Generation"] = df[["NI_Wind", "NI_Solar"]].sum(axis=1)

    ie_daily = df[["IE_Demand", "IE_Generation"]].resample("D").mean()
    ni_daily = df[["NI_Demand", "NI_Generation"]].resample("D").mean()
    ie_weekly = df[["IE_Demand", "IE_Generation"]].resample("W-MON").mean()
    ni_weekly = df[["NI_Demand", "NI_Generation"]].resample("W-MON").mean()

    sns.set_style("whitegrid")
    plt.rcParams["figure.dpi"] = 120

    _line_plot(
        ie_daily,
        cols=["IE_Demand", "IE_Generation"],
        labels=["IE Demand", "IE Generation"],
        colors=["tab:blue", "tab:green"],
        title="Ireland (IE) Daily Average: Demand vs Generation",
        ylabel="MW (daily mean)",
    )
    _line_plot(
        ni_daily,
        cols=["NI_Demand", "NI_Generation"],
        labels=["NI Demand", "NI Generation"],
        colors=["tab:blue", "tab:green"],
        title="Northern Ireland (NI) Daily Average: Demand vs Generation",
        ylabel="MW (daily mean)",
    )
    _line_plot(
        ie_weekly,
        cols=["IE_Demand", "IE_Generation"],
        labels=["IE Demand (weekly)", "IE Generation (weekly)"],
        colors=["tab:blue", "tab:green"],
        title="Ireland (IE) Weekly Average: Demand vs Generation",
        ylabel="MW (weekly mean)",
        xlabel="Week starting",
        lw=1.5,
    )
    _line_plot(
        ni_weekly,
        cols=["NI_Demand", "NI_Generation"],
        labels=["NI Demand (weekly)", "NI Generation (weekly)"],
        colors=["tab:blue", "tab:green"],
        title="Northern Ireland (NI) Weekly Average: Demand vs Generation",
        ylabel="MW (weekly mean)",
        xlabel="Week starting",
        lw=1.5,
    )


def _line_plot(
    df: pd.DataFrame,
    cols: list[str],
    labels: list[str],
    colors: list[str],
    title: str,
    ylabel: str,
    xlabel: str = "Date",
    lw: float = 1.0,
) -> None:
    fig, ax = plt.subplots(figsize=(12, 3.5))
    for col, label, color in zip(cols, labels, colors):
        ax.plot(df.index, df[col], label=label, color=color, linewidth=lw)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(loc="upper right")
    ax.tick_params(axis="x", rotation=30)
    plt.tight_layout()
    plt.show()
