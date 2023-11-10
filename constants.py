from enum import Enum


class Metrics(str, Enum):
    CHARGING_SESSIONS = "Charging Sessions"
    TOTAL_KWH = "Total kWh"
    MEAN_KWH = "Mean kWh"


INPUT_FILE_PATH: str = "input/data.csv"
MONTHLY_RESULTS_FILE_PATH: str = "output/monthly_results_df.csv"
YEARLY_RESULTS_FILE_PATH: str = "output/yearly_results_df.csv"
CHARTS_EXPORTS_DIRECTORY_PATH: str = "charts_exports"

STANDARD_AGGREGATION_DICT: dict = {
    Metrics.CHARGING_SESSIONS.value: "sum",
    Metrics.TOTAL_KWH: "sum",
}

TIME_COLUMN = "_time"
ENERGY_QTY_COLUMN = "_value"
DRIVER_COLUMN = "driver"
YEAR_COLUMN = "year"
MONTH_COLUMN = "month"

REDUNDANT_COLUMNS = {
    "Unnamed: 0",
    "result",
    "table",
    "_start",
    "_stop",
    "_field",
    "_measurement",
}
EXPECTED_FINAL_COLUMNS = {TIME_COLUMN, ENERGY_QTY_COLUMN, DRIVER_COLUMN}
