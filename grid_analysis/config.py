from pathlib import Path

DATA_PATH = Path("System_Data_Qtr_Hourly_2024.xlsx")
CLEANED_OUTPUT_PATH = Path("System_Data_Qtr_Hourly_2025_cleaned.xlsx")

EXPECTED_NONNEG_COLS = [
    "NI Generation",
    "NI Demand",
    "NI Wind Generation",
    "NI Solar Generation",
    "IE Generation",
    "IE Demand",
    "IE Wind Generation",
    "IE Solar Generation",
]

WEEKDAY_ORDER = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
WEEKDAY_MAP = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}
