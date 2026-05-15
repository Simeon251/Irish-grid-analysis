import argparse

from grid_analysis import (
    compute_monthly_stats,
    load_raw,
    clean_data,
    plot_acf_all,
    plot_daily_profiles,
    plot_daily_weekly,
    plot_hourly_wind_solar,
    plot_monthly_avg,
    plot_wind_penetration,
    plot_weekday_demand,
    weekend_vs_weekday_tests,
)
from grid_analysis.config import DATA_PATH


def main(save_cleaned: bool = False) -> None:
    print("=" * 60)
    print("Irish Grid Analysis 2024")
    print("=" * 60)

    print("\n--- Q1: Load & Clean ---")
    raw = load_raw(DATA_PATH)
    cleaned_df, summary = clean_data(raw, save=save_cleaned)
    print(f"Rows: {summary['n_rows']}  |  Missing timestamps: {summary['n_missing_timestamps_expected']}"
          f"  |  Duplicates: {summary['n_duplicate_rows']}")

    print("\n--- Q2: Monthly Statistics ---")
    ie_tidy, ni_tidy = compute_monthly_stats(cleaned_df)

    print("\n--- Q3: Daily & Weekly Time Series ---")
    plot_daily_weekly(cleaned_df)

    print("\n--- Q4: Autocorrelation (ACF) ---")
    plot_acf_all(cleaned_df)

    print("\n--- Q5: Monthly Average Demand & Generation ---")
    ni_monthly_avg, ie_monthly_avg = plot_monthly_avg(cleaned_df)

    print("\n--- Q6: Hourly Wind & Solar Profile (NI) ---")
    hourly_mean = plot_hourly_wind_solar(cleaned_df)

    print("\n--- Q7: Weekday Demand & Generation (IE) ---")
    ie_weekly_avg, ie_weekday_counts = plot_weekday_demand(cleaned_df)

    print("\n--- Q8: Daily Demand Profiles by Weekday ---")
    ni_profiles, ie_profiles = plot_daily_profiles(cleaned_df)

    print("\n--- Q9: Weekend vs Weekday Statistical Tests ---")
    test_results = weekend_vs_weekday_tests(cleaned_df)

    print("\n--- Q10: Wind Penetration Distribution ---")
    penetration_summary = plot_wind_penetration(cleaned_df)

    print("\n" + "=" * 60)
    print("Analysis complete.")
    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Irish Grid Analysis 2024 pipeline")
    parser.add_argument(
        "--save-cleaned",
        action="store_true",
        help="Save the cleaned dataset to Excel after loading",
    )
    args = parser.parse_args()
    main(save_cleaned=args.save_cleaned)
