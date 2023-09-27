# Copyright © 2023 ValidMind Inc. All rights reserved.

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


class AutoStationarity(Metric):
    """
    **Purpose**: This test, AutoStationarity, is used to automatically detect and evaluate the stationarity of each
    time series in a Dataframe, using the Augmented Dickey-Fuller (ADF) test. Stationarity is a crucial property in
    time series data, which indicates that a series' statistical features such as mean and variance are constant over
    time. This property is an underlying assumption for many time-series models.

    **Test Mechanism**: The test performs the Augmented Dickey-Fuller test on each time series in a provided DataFrame
    to determine if the time series is stationary. A loop is ran over each column (time series) of the DataFrame. For
    each series, the ADF test is performed up to a maximum order of differencing (default value 5, configurable via
    params). The p-value of the ADF test is compared against a predefined threshold (default value 0.05, configurable
    via params). If the p-value is less than the threshold, the series is considered stationary at the current order of
    differencing.

    **Signs of High Risk**: The high risk or failure in the model's performance may be indicated by a significant
    number of series failing to achieve stationarity up to the maximum order of differencing. This might suggest that
    the series are not well-modeled by a stationary process and other modeling strategies might be needed.

    **Strengths**: By automating the ADF test, this metric allows for the mass analysis of stationarity across a
    multitude of time series, greatly increasing the efficiency and reliability of the analysis. The use of the ADF
    test, a commonly accepted method for testing stationarity, gives credibility to the results. Furthermore, the
    implementation of max order and threshold parameters allows users to specify their preferred level of strictness in
    the tests.

    **Limitations**: The Augmented Dickey-Fuller test and stationarity check generally have limitations. They rely on
    the assumption that the series are well-modeled by an autoregressive process, which may not be the case for all
    time series. The stationarity check is also sensitive to the choice of the threshold value for the significance
    level. Too high or too low threshold may lead to erroneous conclusions about stationary properties. There is also a
    risk of over-differencing if the maximum order is set too high, leading to unnecessary cycles.
    """

    type = "dataset"
    name = "auto_stationarity"
    required_inputs = ["dataset"]
    default_params = {"max_order": 5, "threshold": 0.05}
    metadata = {
        "task_types": ["regression"],
        "tags": [
            "time_series_data",
            "statsmodels",
            "forecasting",
            "statistical_test",
            "stationarity",
        ],
    }

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
