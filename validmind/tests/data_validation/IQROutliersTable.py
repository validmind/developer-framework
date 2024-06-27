# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import numpy as np
import pandas as pd

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class IQROutliersTable(Metric):
    """
    Determines and summarizes outliers in numerical features using Interquartile Range method.

    **Purpose**: The "Interquartile Range Outliers Table" (IQROutliersTable) metric has been designed for identifying
    and summarizing outliers within numerical features of a dataset using the Interquartile Range (IQR) method. The
    purpose of this exercise is crucial in the pre-processing of data as outliers can substantially distort the
    statistical analysis and debilitate the performance of machine learning models.

    **Test Mechanism**: The IQR, which is the range separating the first quartile (25th percentile) from the third
    quartile (75th percentile), is calculated for each numerical feature within the dataset. An outlier is defined as a
    data point falling below the "Q1 - 1.5 * IQR" or above "Q3 + 1.5 * IQR" range. The metric then computes the number
    of outliers along with their minimum, 25th percentile, median, 75th percentile, and maximum values for each
    numerical feature. If no specific features are chosen, the metric will apply to all numerical features in the
    dataset. The default outlier threshold is set to 1.5, following the standard definition of outliers in statistical
    analysis, although it can be customized by the user.

    **Signs of High Risk**:
    - High risk is indicated by a large number of outliers in multiple features.
    - Outliers that are significantly distanced from the mean value of variables could potentially signal high risk.
    - Data entry errors or other data quality issues could be manifested through extremely high or low outlier values.

    **Strengths**:
    - It yields a comprehensive summary of outliers for each numerical feature within the dataset. This enables the
    user to pinpoint features with potential quality issues.
    - The IQR method is not overly affected by extremely high or low outlier values as it is based on quartile
    calculations.
    - The versatility of this metric grants the ability to customize the method to work on selected features and set a
    defined threshold for outliers.

    **Limitations**:
    - The metric might cause false positives if the variable of interest veers away from a normal or near-normal
    distribution, notably in the case of skewed distributions.
    - It does not extend to provide interpretation or recommendations for tackling outliers and relies on the user or a
    data scientist to conduct further analysis of the results.
    - As it only functions on numerical features, it cannot be used for categorical data.
    - For data that has undergone heavy pre-processing, was manipulated, or inherently possesses a high kurtosis (heavy
    tails), the pre-set threshold may not be optimal for outlier detection.
    """

    name = "iqr_outliers_table"
    required_inputs = ["dataset"]
    default_params = {"features": None, "threshold": 1.5}
    tasks = ["classification", "regression"]
    tags = ["tabular_data", "numerical_data"]

    def run(self):
        features = self.params["features"]
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

    def detect_and_analyze_outliers(self, df, features=None, threshold=1.5):
        if features is None:
            features = df.select_dtypes(include=[np.number]).columns.tolist()

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
