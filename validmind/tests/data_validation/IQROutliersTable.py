# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import numpy as np
import pandas as pd

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class IQROutliersTable(Metric):
    """
    Analyzes the distribution of outliers in numerical features using the Interquartile Range (IQR) method.
    The input dataset is required.
    """

    name = "iqr_outliers_table"
    required_inputs = ["dataset"]
    default_params = {"features": None, "threshold": 1.5}

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
