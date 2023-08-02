# Copyright © 2023 ValidMind Inc. All rights reserved.

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


class AutoStationarity(Metric):
    """
    Automatically detects stationarity for each time series in a DataFrame
    using the Augmented Dickey-Fuller (ADF) test.
    """

    type = "dataset"
    name = "auto_stationarity"
    required_context = ["dataset"]
    default_params = {"max_order": 5, "threshold": 0.05}

    def run(self):
        if "max_order" not in self.params:
            raise ValueError("max_order must be provided in params")
        max_order = self.params["max_order"]

        if "threshold" not in self.params:
            raise ValueError("threshold must be provided in params")
        threshold = self.params["threshold"]

        df = self.dataset.df.dropna()

        # Create an empty DataFrame to store the results
        summary_stationarity = pd.DataFrame()
        best_integration_order = pd.DataFrame()  # New DataFrame

        # Loop over each column in the input DataFrame and perform stationarity tests
        for col in df.columns:
            is_stationary = False
            order = 0

            while not is_stationary and order <= max_order:
                series = df[col]

                if order == 0:
                    adf_result = adfuller(series)
                else:
                    adf_result = adfuller(np.diff(series, n=order - 1))

                adf_pvalue = adf_result[1]
                adf_pass_fail = adf_pvalue < threshold
                adf_decision = "Stationary" if adf_pass_fail else "Non-stationary"

                # Append the result of each test directly into the DataFrame
                summary_stationarity = pd.concat(
                    [
                        summary_stationarity,
                        pd.DataFrame(
                            [
                                {
                                    "Variable": col,
                                    "Integration Order": order,
                                    "Test": "ADF",
                                    "p-value": adf_pvalue,
                                    "Threshold": threshold,
                                    "Pass/Fail": "Pass" if adf_pass_fail else "Fail",
                                    "Decision": adf_decision,
                                }
                            ]
                        ),
                    ],
                    ignore_index=True,
                )

                if adf_pass_fail:
                    is_stationary = True
                    best_integration_order = pd.concat(
                        [
                            best_integration_order,
                            pd.DataFrame(
                                [
                                    {
                                        "Variable": col,
                                        "Best Integration Order": order,
                                        "Test": "ADF",
                                        "p-value": adf_pvalue,
                                        "Threshold": threshold,
                                        "Decision": adf_decision,
                                    }
                                ]
                            ),
                        ],
                        ignore_index=True,
                    )

                order += 1

        # Convert the 'Integration Order' and 'Best Integration Order' column to integer
        summary_stationarity["Integration Order"] = summary_stationarity[
            "Integration Order"
        ].astype(int)
        best_integration_order["Best Integration Order"] = best_integration_order[
            "Best Integration Order"
        ].astype(int)

        return self.cache_results(
            {
                "stationarity_analysis": summary_stationarity.to_dict(orient="records"),
                "best_integration_order": best_integration_order.to_dict(
                    orient="records"
                ),
            }
        )

    def summary(self, metric_value):
        """
        Build one table for summarizing the stationarity results
        and another for the best integration order results
        """
        summary_stationarity = metric_value["stationarity_analysis"]
        best_integration_order = metric_value["best_integration_order"]

        return ResultSummary(
            results=[
                ResultTable(
                    data=summary_stationarity,
                    metadata=ResultTableMetadata(title="Stationarity Analysis Results"),
                ),
                ResultTable(
                    data=best_integration_order,
                    metadata=ResultTableMetadata(
                        title="Best Integration Order Results"
                    ),
                ),
            ]
        )
