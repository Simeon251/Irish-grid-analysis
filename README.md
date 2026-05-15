# Ireland Grid Analysis 2024

Analysis of electricity generation, demand, wind, and solar data for Ireland (IE) and Northern Ireland (NI) using 15-minute interval data throughout 2024.

## Project Structure

```
ireland-grid-analysis/
├── grid_analysis/
│   ├── config.py           # Shared paths and constants
│   ├── data_loader.py      # Load and clean raw Excel data
│   ├── monthly_stats.py    # Monthly demand/wind/solar statistics
│   ├── time_series.py      # Daily and weekly time series plots
│   ├── acf_analysis.py     # Autocorrelation (ACF) analysis
│   ├── monthly_avg.py      # Monthly average demand & generation plots
│   ├── hourly_profile.py   # Wind & solar profile by hour of day
│   ├── weekday_analysis.py # Demand & generation by weekday
│   ├── daily_profiles.py   # Daily demand profiles by weekday
│   ├── stat_tests.py       # Weekend vs weekday statistical tests
│   └── wind_penetration.py # Wind penetration rate distribution
├── main.py
├── requirements.txt
└── irish_grid_analysis_2024.ipynb
```

## Setup

```bash
pip install -r requirements.txt
```

## Usage

Place `System_Data_Qtr_Hourly_2024.xlsx` in the project root, then run:

```bash
python main.py
```

To also save the cleaned dataset:

```bash
python main.py --save-cleaned
```

## Analysis Covered

| # | Topic |
|---|-------|
| 1 | Data loading and cleaning |
| 2 | Monthly statistics (demand, wind, solar) |
| 3 | Daily and weekly time series |
| 4 | Autocorrelation (ACF) for wind and solar |
| 5 | Monthly average demand and generation |
| 6 | Average wind and solar generation by hour |
| 7 | Average demand and generation by weekday |
| 8 | Daily demand profiles by weekday |
| 9 | Weekend vs weekday statistical tests (Welch t-test, Mann-Whitney U) |
| 10 | Wind penetration rate distribution (NI vs IE) |

## Data

The input file `System_Data_Qtr_Hourly_2024.xlsx` contains 15-minute interval readings for:
- NI Generation, NI Demand, NI Wind Generation, NI Solar Generation
- IE Generation, IE Demand, IE Wind Generation, IE Solar Generation

The data file is excluded from version control — add your own copy to the project root before running.

## Requirements

- Python 3.10+
- pandas, numpy, matplotlib, seaborn, scipy, statsmodels, openpyxl
