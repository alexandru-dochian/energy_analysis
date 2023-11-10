import pandas as pd
import constants as cts


def _exit_gracefully():
    emoji = "\u00f0\u009f\u0098\u0086".encode("latin-1").decode("utf-8")
    print(f"\nDone {emoji}\n")


def _write_csv(df: pd.DataFrame, target_path: str):
    head_lines: int = 20
    print(f"Printing first {head_lines} lines of aggregated results...")
    print(df.head(head_lines))
    df.to_csv(target_path, index=False)
    print(f"Writing aggregated results at [{target_path}]\n")


def _get_source_df() -> pd.DataFrame:
    print(f"Reading [{cts.INPUT_FILE_PATH}]...\n")
    df: pd.DataFrame = pd.read_csv(cts.INPUT_FILE_PATH, comment="#")
    df: pd.DataFrame = df.drop(columns=cts.REDUNDANT_COLUMNS, errors="ignore")

    assert (
        set(df.columns) == cts.EXPECTED_FINAL_COLUMNS
    ), f"Input csv structure has been changed. actual={df.columns.to_list()}"

    df[cts.TIME_COLUMN] = pd.to_datetime(df[cts.TIME_COLUMN])
    df[cts.MONTH_COLUMN] = df[cts.TIME_COLUMN].dt.month
    df[cts.YEAR_COLUMN] = df[cts.TIME_COLUMN].dt.year

    return df


def _write_aggregated_monthly_data(df: pd.DataFrame):
    monthly_results_df = (
        df.groupby(by=[cts.DRIVER_COLUMN, cts.MONTH_COLUMN, cts.YEAR_COLUMN])
        .agg({cts.ENERGY_QTY_COLUMN: ["count", "sum", "mean"]})
        .reset_index()
    )
    monthly_results_df.columns = [
        cts.DRIVER_COLUMN,
        cts.MONTH_COLUMN,
        cts.YEAR_COLUMN,
        cts.Metrics.CHARGING_SESSIONS.value,
        cts.Metrics.TOTAL_KWH.value,
        cts.Metrics.MEAN_KWH.value,
    ]
    _write_csv(monthly_results_df, cts.MONTHLY_RESULTS_FILE_PATH)


def _write_aggregated_yearly_data(df: pd.DataFrame):
    yearly_results_df = (
        df.groupby(by=[cts.DRIVER_COLUMN, cts.YEAR_COLUMN])
        .agg({cts.ENERGY_QTY_COLUMN: ["count", "sum", "mean"]})
        .reset_index()
    )

    yearly_results_df.columns = [
        cts.DRIVER_COLUMN,
        cts.YEAR_COLUMN,
        cts.Metrics.CHARGING_SESSIONS.value,
        cts.Metrics.TOTAL_KWH.value,
        cts.Metrics.MEAN_KWH.value,
    ]
    _write_csv(yearly_results_df, cts.YEARLY_RESULTS_FILE_PATH)


if __name__ == "__main__":
    df: pd.DataFrame = _get_source_df()
    _write_aggregated_monthly_data(df)
    _write_aggregated_yearly_data(df)
    _exit_gracefully()
