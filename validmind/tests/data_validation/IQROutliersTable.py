# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import numpy as np
import pandas as pd

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class IQROutliersTable(Metric):
    """
    **Purpose**: The "Interquartile Range Outliers Table" (IQROutliersTable) metric is used to detect and summarize
    outliers in numerical features of a dataset using the Interquartile Range (IQR) method. Outliers, values that
    deviate substantially from general patterns of the data, are crucial to be identified in data pre-processing as
    they can lead to serious problems in statistical analyses and may degrade the performance of machine learning
    models.

    **Test Mechanism**: This metric works by calculating the IQR (the range between the first quartile (25th
    percentile) and the third quartile (75th percentile)) of each numerical feature in a given dataset. An outlier is
    defined as a data point that falls below "Q1 - 1.5 * IQR" or above "Q3 + 1.5 * IQR". The number of outliers, as
    well as their minimum, 25th percentile, median, 75th percentile, and maximum values, are computed and collected for
    each numerical feature. If no specific features are selected, the metric will be applied to all numerical features
    in the dataset. Users can customize the outlier threshold. By default, it's 1.5, following the standard definition
    of outliers in statistical analysis.

    **Signs of High Risk**: High risk is indicated by a large number of outliers in multiple features, as well as
    outliers that are far from the mean value of variables, which suggest that they deviate significantly from the
    general patterns of the data. Additionally, extremely high or low outlier values might also point to data entry
    errors or other data quality issues.

    **Strengths**:
    1. This metric provides a comprehensive summary of outliers for each numerical feature in the dataset, which can
    help users identify features with potential quality issues.
    2. It's versatile and customizable, allowing users to select specific features and set a custom threshold for
    defining outliers.
    3. The IQR method is robust to the influence of extreme outlier values as it's based on quartile calculations.

    **Limitations**:
    1. This metric might generate false positives if the variable of interest does not follow a normal or near-normal
    distribution, specifically in case of skewed distributions.
    2. It does not provide interpretation or recommendations for handling outliers. The results need to be analyzed by
    users or data scientists.
    3. It only works on numerical features and cannot be used for categorical data.
    4. If the data has been heavily pre-processed or manipulated, or if it naturally has a high kurtosis (heavy tails),
    the set threshold may not work optimally for outlier detection.
    """

    name = "iqr_outliers_table"
    required_inputs = ["dataset"]
    default_params = {"features": None, "threshold": 1.5}
    metadata = {
        "task_types": ["classification", "regression"],
        "tags": ["tabular_data", "numerical_data"],
    }

    def run(self):
        features = self.params["features"]
        threshold = self.params["threshold"]

        df = self.dataset.df

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
