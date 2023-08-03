# Copyright © 2023 ValidMind Inc. All rights reserved.

import pandas as pd
from statsmodels.tsa.stattools import coint

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


class EngleGrangerCoint(Metric):
    """
    Test for cointegration between pairs of time series variables in a given dataset using the Engle-Granger test.
    """

    type = "dataset"
    name = "engle_granger_coint"
    required_context = ["dataset"]
    default_params = {"threshold": 0.05}

    def run(self):
        threshold = self.params["threshold"]
        df = self.dataset.df.dropna()

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
