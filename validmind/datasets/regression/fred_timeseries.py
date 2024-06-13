# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import os

import pandas as pd

current_path = os.path.dirname(os.path.abspath(__file__))
mortgage30us_path = os.path.join(current_path, "datasets", "fred", "MORTGAGE30US.csv")
fedfunds_path = os.path.join(current_path, "datasets", "fred", "FEDFUNDS.csv")
gs10_path = os.path.join(current_path, "datasets", "fred", "GS10.csv")
unrate_path = os.path.join(current_path, "datasets", "fred", "UNRATE.csv")

target_column = "MORTGAGE30US"
feature_columns = ["FEDFUNDS", "GS10", "UNRATE"]


def get_common_date_range(dfs):
    start_dates = [df.index.min() for df in dfs]
    end_dates = [df.index.max() for df in dfs]

    common_start_date = max(start_dates)
    common_end_date = min(end_dates)

    return common_start_date, common_end_date


def align_date_range(dfs, start_date, end_date):
    return [df.loc[start_date:end_date] for df in dfs]


def load_data():
    mortgage30us = pd.read_csv(
        mortgage30us_path, parse_dates=["DATE"], index_col="DATE"
    )
    fedfunds = pd.read_csv(fedfunds_path, parse_dates=["DATE"], index_col="DATE")
    gs10 = pd.read_csv(gs10_path, parse_dates=["DATE"], index_col="DATE")
    unrate = pd.read_csv(unrate_path, parse_dates=["DATE"], index_col="DATE")

    # Resample mortgage30us to monthly frequency
    mortgage30us = mortgage30us.resample("MS").last()

    # Get the common date range
    common_start_date, common_end_date = get_common_date_range(
        [mortgage30us, fedfunds, gs10, unrate]
    )

    # Align the date range for all dataframes
    mortgage30us, fedfunds, gs10, unrate = align_date_range(
        [mortgage30us, fedfunds, gs10, unrate], common_start_date, common_end_date
    )

    # Combine into a single DataFrame
    df = pd.concat([mortgage30us, fedfunds, gs10, unrate], axis=1, join="inner")
    df.columns = [target_column] + feature_columns

    return df


# Convert data back to levels
def convert_to_levels(diff_df, original_df, target_column):
    """
    Convert differenced data back to original levels.
    """
    previous_values = original_df[target_column].shift(1).dropna()
    levels_df = diff_df.add(previous_values, axis=0)
    return levels_df


def get_demo_test_config(test_suite=None):

    default_config = {}

    default_config["validmind.data_validation.TimeSeriesDescription"] = {
        "inputs": {
            "dataset": "raw_ds",
        }
    }
    default_config["validmind.data_validation.TimeSeriesLinePlot"] = {
        "inputs": {
            "dataset": "raw_ds",
        }
    }
    default_config["validmind.data_validation.TimeSeriesMissingValues"] = {
        "inputs": {
            "dataset": "raw_ds",
        }
    }
    default_config["validmind.data_validation.SeasonalDecompose"] = {
        "inputs": {
            "dataset": "raw_ds",
        }
    }
    default_config[
        "validmind.data_validation.TimeSeriesDescriptiveStatistics:train_diff_data"
    ] = {
        "inputs": {
            "dataset": "train_diff_ds",
        }
    }
    default_config[
        "validmind.data_validation.TimeSeriesDescriptiveStatistics:test_diff_data"
    ] = {
        "inputs": {
            "dataset": "test_diff_ds",
        }
    }
    default_config["validmind.data_validation.TimeSeriesOutliers:train_diff_data"] = {
        "inputs": {
            "dataset": "train_diff_ds",
        },
        "params": {"zscore_threshold": 4},
    }
    default_config["validmind.data_validation.TimeSeriesOutliers:test_diff_data"] = {
        "inputs": {
            "dataset": "test_diff_ds",
        },
        "params": {"zscore_threshold": 4},
    }
    default_config["validmind.data_validation.TimeSeriesHistogram:train_diff_data"] = {
        "inputs": {
            "dataset": "train_diff_ds",
        },
        "params": {"nbins": 100},
    }
    default_config["validmind.data_validation.TimeSeriesHistogram:test_diff_data"] = {
        "inputs": {
            "dataset": "test_diff_ds",
        },
        "params": {"nbins": 100},
    }
    default_config["validmind.data_validation.DatasetSplit"] = {
        "inputs": {
            "datasets": ["train_diff_ds", "test_diff_ds"],
        }
    }
    default_config["validmind.model_validation.ModelMetadataComparison"] = {
        "inputs": {
            "models": ["random_forests_model", "gradient_boosting_model"],
        }
    }
    default_config[
        "validmind.model_validation.sklearn.RegressionErrorsComparison:train_data"
    ] = {
        "inputs": {
            "datasets": ["train_ds", "train_ds"],
            "models": ["random_forests_model", "gradient_boosting_model"],
        }
    }
    default_config[
        "validmind.model_validation.sklearn.RegressionErrorsComparison:test_data"
    ] = {
        "inputs": {
            "datasets": ["test_ds", "test_ds"],
            "models": ["random_forests_model", "gradient_boosting_model"],
        }
    }
    default_config[
        "validmind.model_validation.sklearn.RegressionR2SquareComparison:train_data"
    ] = {
        "inputs": {
            "datasets": ["train_ds", "train_ds"],
            "models": ["random_forests_model", "gradient_boosting_model"],
        }
    }
    default_config[
        "validmind.model_validation.sklearn.RegressionR2SquareComparison:test_data"
    ] = {
        "inputs": {
            "datasets": ["test_ds", "test_ds"],
            "models": ["random_forests_model", "gradient_boosting_model"],
        }
    }
    default_config[
        "validmind.model_validation.TimeSeriesR2SquareBySegments:train_data"
    ] = {
        "inputs": {
            "datasets": ["train_ds", "train_ds"],
            "models": ["random_forests_model", "gradient_boosting_model"],
        }
    }
    default_config[
        "validmind.model_validation.TimeSeriesR2SquareBySegments:test_data"
    ] = {
        "inputs": {
            "datasets": ["test_ds", "test_ds"],
            "models": ["random_forests_model", "gradient_boosting_model"],
        },
        "params": {
            "segments": {
                "start_date": ["2012-11-01", "2018-02-01"],
                "end_date": ["2018-01-01", "2023-03-01"],
            }
        },
    }
    default_config[
        "validmind.model_validation.TimeSeriesPredictionsPlot:train_data"
    ] = {
        "inputs": {
            "datasets": ["train_ds", "train_ds"],
            "models": ["random_forests_model", "gradient_boosting_model"],
        }
    }
    default_config["validmind.model_validation.TimeSeriesPredictionsPlot:test_data"] = {
        "inputs": {
            "datasets": ["test_ds", "test_ds"],
            "models": ["random_forests_model", "gradient_boosting_model"],
        }
    }
    default_config[
        "validmind.model_validation.TimeSeriesPredictionWithCI:random_forests_model"
    ] = {
        "inputs": {
            "dataset": "test_ds",
            "model": "random_forests_model",
        }
    }
    default_config[
        "validmind.model_validation.TimeSeriesPredictionWithCI:gradient_boosting_model"
    ] = {
        "inputs": {
            "dataset": "test_ds",
            "model": "gradient_boosting_model",
        }
    }
    default_config["validmind.model_validation.ModelPredictionResiduals:train_data"] = {
        "inputs": {
            "datasets": ["train_ds", "train_ds"],
            "models": ["random_forests_model", "gradient_boosting_model"],
        }
    }
    default_config["validmind.model_validation.ModelPredictionResiduals:test_data"] = {
        "inputs": {
            "datasets": ["test_ds", "test_ds"],
            "models": ["random_forests_model", "gradient_boosting_model"],
        }
    }
    default_config[
        "validmind.model_validation.sklearn.FeatureImportanceComparison:train_data"
    ] = {
        "inputs": {
            "datasets": ["train_ds", "train_ds"],
            "models": ["random_forests_model", "gradient_boosting_model"],
        }
    }
    default_config[
        "validmind.model_validation.sklearn.FeatureImportanceComparison:test_data"
    ] = {
        "inputs": {
            "datasets": ["test_ds", "test_ds"],
            "models": ["random_forests_model", "gradient_boosting_model"],
        }
    }
    default_config[
        "validmind.model_validation.sklearn.PermutationFeatureImportance:random_forests_model"
    ] = {
        "inputs": {
            "dataset": "test_ds",
            "model": "random_forests_model",
        }
    }
    default_config[
        "validmind.model_validation.sklearn.PermutationFeatureImportance:gradient_boosting_model"
    ] = {
        "inputs": {
            "dataset": "test_ds",
            "model": "gradient_boosting_model",
        }
    }

    return default_config
