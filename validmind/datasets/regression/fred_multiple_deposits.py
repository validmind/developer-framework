# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import os
import pandas as pd
import numpy as np
import pymc as pm
import arviz as az

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

current_path = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(current_path, "datasets/fred")
deposits_file = os.path.join(dataset_path, "DPSACBW027NBOG.csv")
fed_funds_file = os.path.join(dataset_path, "FEDFUNDS.csv")
tb3ms_file = os.path.join(dataset_path, "TB3MS.csv")
gs10_file = os.path.join(dataset_path, "GS10.csv")
gs30_file = os.path.join(dataset_path, "GS30.csv")

start_year = "2010"
end_year = "2022"


def load_data():
    # Load the data from the CSV files
    deposits = pd.read_csv(deposits_file, parse_dates=["DATE"], index_col="DATE")
    fed_funds = pd.read_csv(fed_funds_file, parse_dates=["DATE"], index_col="DATE")
    tb3ms = pd.read_csv(tb3ms_file, parse_dates=["DATE"], index_col="DATE")
    gs10 = pd.read_csv(gs10_file, parse_dates=["DATE"], index_col="DATE")
    gs30 = pd.read_csv(gs30_file, parse_dates=["DATE"], index_col="DATE")

    # Select historical data
    fed_funds = fed_funds.loc[start_year:end_year]
    tb3ms = tb3ms.loc[start_year:end_year]
    gs10 = gs10.loc[start_year:end_year]
    gs30 = gs30.loc[start_year:end_year]
    deposits = deposits.loc[start_year:end_year]

    # Resample the deposits data to a monthly frequency
    deposits = deposits.resample("MS").mean()

    # Create multiple deposits with synthetic seasonality
    deposits_1 = _add_synthetic_seasonality(deposits, amplitude=100, period=12)
    deposits_2 = _add_synthetic_seasonality(deposits, amplitude=200, period=12)
    deposits_3 = _add_synthetic_seasonality(deposits, amplitude=300, period=12)
    deposits_4 = _add_synthetic_seasonality(deposits, amplitude=400, period=12)
    deposits_5 = _add_synthetic_seasonality(deposits, amplitude=500, period=12)

    return (
        deposits_1,
        deposits_2,
        deposits_3,
        deposits_4,
        deposits_5,
        fed_funds,
        tb3ms,
        gs10,
        gs30,
    )


def fit_pymc_seasonality_model(df, target_column, n_order):
    """
    Fits a linear model with seasonality using PyMC3.

    Parameters:
    t: array-like
        Time variable.
    y: array-like
        Observed data.
    fourier_features: DataFrame
        Fourier features for seasonality.
    coords: dict
        Coordinates for the model.

    Returns:
    linear_seasonality_prior: prior predictive samples
    linear_seasonality_trace: trace of the posterior samples
    linear_seasonality_posterior: posterior predictive samples
    """

    pymc_df, t, y, y_max, fourier_features, coords = _process_df_for_pymc(
        df, target_column, n_order
    )

    with pm.Model(check_bounds=False, coords=coords) as linear_with_seasonality:
        alpha = pm.Normal("alpha", mu=0, sigma=0.5)
        beta = pm.Normal("beta", mu=0, sigma=0.5)
        sigma = pm.HalfNormal("sigma", sigma=0.1)
        beta_fourier = pm.Normal(
            "beta_fourier", mu=0, sigma=0.1, dims="fourier_features"
        )

        seasonality = pm.Deterministic(
            "seasonality", pm.math.dot(beta_fourier, fourier_features.to_numpy().T)
        )
        trend = pm.Deterministic("trend", alpha + beta * t)
        mu = trend + seasonality

        pm.Normal("likelihood", mu=mu, sigma=sigma, observed=y)

        # Sample the prior
        linear_seasonality_prior = pm.sample_prior_predictive()

    # Sample the posterior
    with linear_with_seasonality:
        linear_seasonality_trace = pm.sample(return_inferencedata=True)
        linear_seasonality_posterior = pm.sample_posterior_predictive(
            trace=linear_seasonality_trace
        )

    # Extract the prior samples
    prior_likelihood = (
        az.extract(linear_seasonality_prior, group="prior_predictive", num_samples=100)[
            "likelihood"
        ]
        * y_max
    )
    prior_seasonality = (
        az.extract(linear_seasonality_prior, group="prior", num_samples=100)[
            "seasonality"
        ]
        * 100
    )

    # Extract the posterior samples
    posterior_likelihood = (
        az.extract(
            linear_seasonality_posterior, group="posterior_predictive", num_samples=100
        )["likelihood"]
        * y_max
    )
    posterior_seasonality = (
        az.extract(linear_seasonality_trace, group="posterior", num_samples=100)[
            "seasonality"
        ]
        * 10000
    )

    return (
        pymc_df,
        prior_likelihood,
        prior_seasonality,
        posterior_likelihood,
        posterior_seasonality,
    )


def _process_df_for_pymc(df, target_column, n_order):
    pymc_df = df.copy()

    pymc_df["Month"] = pymc_df.index
    t = (pymc_df["Month"] - pd.Timestamp("1900-01-01")).dt.days.to_numpy()
    t_min = np.min(t)
    t_max = np.max(t)
    t = (t - t_min) / (t_max - t_min)

    y = pymc_df[target_column].to_numpy()
    y_max = np.max(y)
    y = y / y_max

    periods = (pymc_df["Month"] - pd.Timestamp("1900-01-01")).dt.days / 365.25

    fourier_features = pd.DataFrame(
        {
            f"{func}_order_{order}": getattr(np, func)(2 * np.pi * periods * order)
            for order in range(1, n_order + 1)
            for func in ("sin", "cos")
        }
    )

    coords = {"fourier_features": np.arange(2 * n_order)}

    return pymc_df, t, y, y_max, fourier_features, coords


def process_and_train_random_forest(df, posterior_seasonality, target_column):

    preprocessed_df = df.copy()

    # Extract the posterior predictive mean for seasonality
    seasonality_posterior_mean = posterior_seasonality.mean(axis=1)

    # Adjust the target variable by removing the seasonality component
    preprocessed_df[target_column] = (
        preprocessed_df[target_column] - seasonality_posterior_mean
    )

    # Train a random forest model
    train_df, test_df = train_test_split(preprocessed_df, test_size=0.20)

    X_train = train_df.drop(target_column, axis=1)
    y_train = train_df[target_column]
    X_test = test_df.drop(target_column, axis=1)
    y_test = test_df[target_column]

    model = RandomForestRegressor(random_state=0)
    model.fit(X_train, y_train)
    s1 = model.score(X_train, y_train)
    s2 = model.score(X_test, y_test)
    print("R² of Support Vector Regressor on training set: {:.3f}".format(s1))
    print("R² of Support Vector Regressor on test set: {:.3f}".format(s2))

    return model, train_df, test_df


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
