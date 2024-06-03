# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import os

import numpy as np
import pandas as pd

current_path = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(current_path, "datasets/fred")
deposits_file = os.path.join(dataset_path, "DPSACBW027NBOG.csv")
fed_funds_file = os.path.join(dataset_path, "FEDFUNDS.csv")
tb3ms_file = os.path.join(dataset_path, "TB3MS.csv")
gs10_file = os.path.join(dataset_path, "GS10.csv")
gs30_file = os.path.join(dataset_path, "GS30.csv")

period = 12
start_year = "2010"
end_year = "2022"
target_column = "DPSACBW027NBOG"


def load_data():
    deposits = pd.read_csv(deposits_file, parse_dates=["DATE"], index_col="DATE")
    fed_funds = pd.read_csv(fed_funds_file, parse_dates=["DATE"], index_col="DATE")
    tb3ms = pd.read_csv(tb3ms_file, parse_dates=["DATE"], index_col="DATE")
    gs10 = pd.read_csv(gs10_file, parse_dates=["DATE"], index_col="DATE")
    gs30 = pd.read_csv(gs30_file, parse_dates=["DATE"], index_col="DATE")

    # Select historical data
    deposits = deposits.loc[start_year:end_year]

    # Resample the deposits data to a monthly frequency
    deposits = deposits.resample("MS").mean()

    fed_funds = fed_funds.loc[start_year:end_year]
    tb3ms = tb3ms.loc[start_year:end_year]
    gs10 = gs10.loc[start_year:end_year]
    gs30 = gs30.loc[start_year:end_year]

    # Add synthetic seasonality to the time series
    deposits_seasonality = _add_synthetic_seasonality(
        deposits, amplitude=100, period=period
    )

    return deposits, deposits_seasonality, fed_funds, tb3ms, gs10, gs30


def _add_synthetic_seasonality(time_series, amplitude=10, period=12, method="additive"):
    """
    Add synthetic seasonality to a time series.

    Parameters:
    - time_series: pandas Series or single-column DataFrame
    - amplitude: Amplitude of the seasonality
    - frequency: Frequency of the seasonality
    - method: Method to add seasonality ('additive' or 'multiplicative')

    Returns:
    - DataFrame with synthetic seasonality added
    """
    # Ensure the time_series is a pandas Series
    if isinstance(time_series, pd.DataFrame):
        if time_series.shape[1] == 1:
            time_series = (
                time_series.squeeze()
            )  # Convert single column DataFrame to Series
        else:
            raise ValueError(
                "time_series must be a single column DataFrame or a Series"
            )
    elif not isinstance(time_series, pd.Series):
        raise ValueError(
            "time_series must be a pandas Series or a single column DataFrame"
        )

    # Create a time index based on the length of the time series
    time_index = np.arange(len(time_series))

    # Generate the synthetic seasonality component
    seasonality = amplitude * np.sin(2 * np.pi * time_index / period)

    # Apply the synthetic seasonality to the original time series
    if method == "additive":
        synthetic_series = time_series + seasonality
    elif method == "multiplicative":
        synthetic_series = time_series * (1 + seasonality)
    else:
        raise ValueError("method must be either 'additive' or 'multiplicative'")

    # Create a DataFrame to hold the synthetic series with the original index
    synthetic_df = pd.DataFrame(synthetic_series, columns=[time_series.name])
    synthetic_df.index = time_series.index

    return synthetic_df
