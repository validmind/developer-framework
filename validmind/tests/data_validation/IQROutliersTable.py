# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import pandas as pd

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class IQROutliersTable(Metric):
    """
    Determines and summarizes outliers in numerical features using the Interquartile Range method.

    ### Purpose

    The "Interquartile Range Outliers Table" (IQROutliersTable) metric is designed to identify and summarize outliers
    within numerical features of a dataset using the Interquartile Range (IQR) method. This exercise is crucial in the
    pre-processing of data because outliers can substantially distort statistical analysis and impact the performance
    of machine learning models.

    ### Test Mechanism

    The IQR, which is the range separating the first quartile (25th percentile) from the third quartile (75th
    percentile), is calculated for each numerical feature within the dataset. An outlier is defined as a data point
    falling below the "Q1 - 1.5 * IQR" or above "Q3 + 1.5 * IQR" range. The test computes the number of outliers and
    their summary statistics (minimum, 25th percentile, median, 75th percentile, and maximum values) for each numerical
    feature. If no specific features are chosen, the test applies to all numerical features in the dataset. The default
    outlier threshold is set to 1.5 but can be customized by the user.

    ### Signs of High Risk

    - A large number of outliers in multiple features.
    - Outliers significantly distanced from the mean value of variables.
    - Extremely high or low outlier values indicative of data entry errors or other data quality issues.

    ### Strengths

    - Provides a comprehensive summary of outliers for each numerical feature, helping pinpoint features with potential
    quality issues.
    - The IQR method is robust to extremely high or low outlier values as it is based on quartile calculations.
    - Can be customized to work on selected features and set thresholds for outliers.

    ### Limitations

    - Might cause false positives if the variable deviates from a normal or near-normal distribution, especially for
    skewed distributions.
    - Does not provide interpretation or recommendations for addressing outliers, relying on further analysis by users
    or data scientists.
    - Only applicable to numerical features, not categorical data.
    - Default thresholds may not be optimal for data with heavy pre-processing, manipulation, or inherently high
    kurtosis (heavy tails).
    """

    name = "iqr_outliers_table"
    required_inputs = ["dataset"]
    default_params = {"threshold": 1.5}
    tasks = ["classification", "regression"]
    tags = ["tabular_data", "numerical_data"]

    def run(self):

        # Select numerical features
        features = self.inputs.dataset.feature_columns_numeric

        # Select non-binary features
        features = [
            feature
            for feature in features
            if len(self.inputs.dataset.df[feature].unique()) > 2
        ]

        threshold = self.params["threshold"]

        df = self.inputs.dataset.df

        outliers_summary_table = self.detect_and_analyze_outliers(
            df, features, threshold
        )

        return self.cache_results(
            {"outliers_summary_table": outliers_summary_table.to_dict(orient="records")}
        )

    @staticmethod
    def compute_outliers(series, threshold=1.5):
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        return series[(series < lower_bound) | (series > upper_bound)]

    def detect_and_analyze_outliers(self, df, features, threshold=1.5):

        outliers_summary = []
        for feature in features:
            outliers_series = self.compute_outliers(df[feature], threshold)
            if not outliers_series.empty:
                outliers_summary.append(
                    {
                        "Variable": feature,
                        "Total Count of Outliers": outliers_series.count(),
                        "Mean Value of Variable": df[feature].mean(),
                        "Minimum Outlier Value": outliers_series.min(),
                        "Outlier Value at 25th Percentile": outliers_series.quantile(
                            0.25
                        ),
                        "Outlier Value at 50th Percentile": outliers_series.median(),
                        "Outlier Value at 75th Percentile": outliers_series.quantile(
                            0.75
                        ),
                        "Maximum Outlier Value": outliers_series.max(),
                    }
                )
        outliers_summary_table = pd.DataFrame(outliers_summary)
        return outliers_summary_table

    def summary(self, metric_value):
        outliers_summary_table = pd.DataFrame(metric_value["outliers_summary_table"])
        return ResultSummary(
            results=[
                ResultTable(
                    data=outliers_summary_table,
                    metadata=ResultTableMetadata(
                        title="Summary of Outliers Detected by IQR Method"
                    ),
                ),
            ]
        )
