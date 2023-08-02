# Copyright © 2023 ValidMind Inc. All rights reserved.

import numpy as np
import pandas as pd
from dataclasses import dataclass
from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class IQROutliersTable(Metric):
    """
    Detects the outliers in numerical features using the Interquartile Range (IQR) method.
    The input dataset is required.
    """

    name = "iqr_outliers_table"
    required_context = ["dataset"]
    default_params = {"features": None, "threshold": 1.5}

    def run(self):
        num_features = self.params["num_features"]
        threshold = self.params["threshold"]

        df = self.dataset.df

        outliers_table = self.detect_outliers(df, num_features, threshold)

        return self.cache_results(
            {
                "outliers_table": outliers_table,
            }
        )

    @staticmethod
    def compute_outliers(series, threshold=1.5):
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        return series[(series < lower_bound) | (series > upper_bound)]

    def detect_outliers(self, df, features=None, threshold=1.5):
        if features is None:
            features = df.select_dtypes(include=[np.number]).columns.tolist()

        outliers = []
        for feature in features:
            outliers_series = self.compute_outliers(df[feature], threshold)
            for index, outlier in outliers_series.items():
                outliers.append(
                    {"Feature": feature, "Index": index, "OutlierValue": outlier}
                )

        outliers_table = pd.DataFrame(outliers)
        return outliers_table

    def summary(self, metric_value):
        outliers_table = metric_value["outliers_table"]
        return ResultSummary(
            results=[
                ResultTable(
                    data=outliers_table,
                    metadata=ResultTableMetadata(
                        title="Outliers Detected by IQR Method"
                    ),
                )
            ]
        )
