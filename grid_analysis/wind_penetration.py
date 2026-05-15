import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def plot_wind_penetration(cleaned_df: pd.DataFrame) -> dict:
    df = cleaned_df.copy()

    df["NI_Wind"] = pd.to_numeric(df.get("NI Wind Generation", df.get("NI_Wind", np.nan)), errors="coerce")
    df["NI_Demand"] = pd.to_numeric(df.get("NI Demand", df.get("NI_Demand", np.nan)), errors="coerce")
    df["IE_Wind"] = pd.to_numeric(df.get("IE Wind Generation", df.get("IE_Wind", np.nan)), errors="coerce")
    df["IE_Demand"] = pd.to_numeric(df.get("IE Demand", df.get("IE_Demand", np.nan)), errors="coerce")

    df["NI_Wind_Penetration"] = (df["NI_Wind"] / df["NI_Demand"]) * 100
    df["IE_Wind_Penetration"] = (df["IE_Wind"] / df["IE_Demand"]) * 100

    for col in ["NI_Wind_Penetration", "IE_Wind_Penetration"]:
        df[col].replace([np.inf, -np.inf], np.nan, inplace=True)
        df[col] = df[col].mask(df[col] < 0, np.nan)

    ni_stats = df["NI_Wind_Penetration"].describe(percentiles=[0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99]).to_dict()
    ie_stats = df["IE_Wind_Penetration"].describe(percentiles=[0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99]).to_dict()

    plt.rcParams["figure.dpi"] = 120
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(10, 5))

    ni_clean = df["NI_Wind_Penetration"].dropna()
    ie_clean = df["IE_Wind_Penetration"].dropna()

    sns.histplot(ni_clean, bins=100, color="tab:blue", stat="density", alpha=0.25, label="NI histogram", ax=ax)
    sns.kdeplot(ni_clean, color="tab:blue", linewidth=1.5, label="NI KDE", ax=ax)
    sns.histplot(ie_clean, bins=100, color="yellow", stat="density", alpha=0.25, label="IE histogram", ax=ax)
    sns.kdeplot(ie_clean, color="tab:green", linewidth=1.5, label="IE KDE", ax=ax)

    ax.set_xlabel("Wind Penetration Rate (%)")
    ax.set_ylabel("Density")
    ax.set_title("Distribution of Wind Penetration Rates: NI vs IE (all timestamps)")
    ax.legend()
    ax.set_xlim(left=0)
    plt.tight_layout()
    plt.show()

    summary = {
        "NI_median": float(ni_stats.get("50%", np.nan)),
        "NI_95th_pct": float(ni_stats.get("95%", np.nan)),
        "IE_median": float(ie_stats.get("50%", np.nan)),
        "IE_95th_pct": float(ie_stats.get("95%", np.nan)),
        "NI_count": int(df["NI_Wind_Penetration"].count()),
        "IE_count": int(df["IE_Wind_Penetration"].count()),
    }
    print("\nWind Penetration Summary:")
    for k, v in summary.items():
        print(f"  {k}: {v:.2f}" if isinstance(v, float) else f"  {k}: {v}")
    return summary
