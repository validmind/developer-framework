# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import pandas as pd
from statsmodels.tsa.stattools import coint

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


class EngleGrangerCoint(Metric):
    """
    Validates co-integration in pairs of time series data using the Engle-Granger test and classifies them as
    'Cointegrated' or 'Not cointegrated'.

    **Purpose**: The intent of this Engle-Granger cointegration test is to explore and quantify the degree of
    co-movement between pairs of time series variables in a dataset. This is particularly useful in enhancing the
    accuracy of predictive regressions whenever the underlying variables are co-integrated, i.e., they move together
    over time.

    **Test Mechanism**: The test first drops any non-applicable values from the input dataset and then iterates over
    each pair of variables to apply the Engle-Granger cointegration test. The test generates a 'p' value, which is then
    compared against a pre-specified threshold (0.05 by default). The pair is labeled as 'Cointegrated' if the 'p'
    value is less than or equal to the threshold or 'Not cointegrated' otherwise. A summary table is returned by the
    metric showing cointegration results for each variable pair.

    **Signs of High Risk**:
    - A high risk might be indicated if a significant number of variables that were hypothesized to be cointegrated do
    not pass the test.
    - Another sign of high risk is if a considerable number of 'p' values are close to the threshold. This is a risk
    because minor fluctuations in the data can switch the decision between 'Cointegrated' and 'Not cointegrated'.

    **Strengths**:
    - The Engle-Granger cointegration test provides an effective way to analyze relationships between time series,
    particularly in contexts where it's essential to check if variables are moving together in a statistically
    significant manner.
    - It is useful in various domains, especially finance or economics. Here, predictive models often hinge on
    understanding how different variables move together over time.

    **Limitations**:
    - The Engle-Granger cointegration test assumes that the time series are integrated of the same order, which isn't
    always true in multivariate time series datasets.
    - The presence of non-stationary characteristics in the series or structural breaks can result in falsely positive
    or negative cointegration results.
    - The test may not perform well for small sample sizes due to lack of statistical power. Therefore, it should be
    used with caution, and whenever possible, supplemented with other predictive indicators for a more robust model
    evaluation.
    """

    type = "dataset"
    name = "engle_granger_coint"
    required_inputs = ["dataset"]
    default_params = {"threshold": 0.05}
    tasks = ["regression"]
    tags = ["time_series_data", "statistical_test", "forecasting"]

    def run(self):
        threshold = self.params["threshold"]
        df = self.inputs.dataset.df.dropna()

        # Create an empty DataFrame to store the results
        summary_cointegration = pd.DataFrame()

        columns = df.columns
        num_vars = len(columns)

        for i in range(num_vars):
            for j in range(i + 1, num_vars):
                var1 = columns[i]
                var2 = columns[j]

                # Perform the Engle-Granger cointegration test
                _, p_value, _ = coint(df[var1], df[var2])

                # Determine the decision based on the p-value and the significance level
                decision = (
                    "Cointegrated" if p_value <= threshold else "Not cointegrated"
                )
                pass_fail = "Pass" if p_value <= threshold else "Fail"

                # Append the result of each test directly into the DataFrame
                summary_cointegration = pd.concat(
                    [
                        summary_cointegration,
                        pd.DataFrame(
                            [
                                {
                                    "Variable 1": var1,
                                    "Variable 2": var2,
                                    "Test": "Engle-Granger",
                                    "p-value": p_value,
                                    "Threshold": threshold,
                                    "Pass/Fail": pass_fail,
                                    "Decision": decision,
                                }
                            ]
                        ),
                    ],
                    ignore_index=True,
                )

        return self.cache_results(
            {
                "cointegration_analysis": summary_cointegration.to_dict(
                    orient="records"
                ),
            }
        )

    def summary(self, metric_value):
        """
        Build one table for summarizing the cointegration results
        """
        summary_cointegration = metric_value["cointegration_analysis"]

        return ResultSummary(
            results=[
                ResultTable(
                    data=summary_cointegration,
                    metadata=ResultTableMetadata(
                        title="Cointegration Analysis Results"
                    ),
                ),
            ]
        )
