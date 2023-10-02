# Copyright © 2023 ValidMind Inc. All rights reserved.

import pandas as pd
from statsmodels.tsa.stattools import coint

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


class EngleGrangerCoint(Metric):
    """
    **Purpose**: The purpose of this metric is to use the Engle-Granger test to examine for cointegration between pairs
    of time series variables in a given dataset. This can be beneficial for assessing the extent to which two time
    series variables move together over time. Predictive regressions can be substantially more accurate if the
    variables involved are co-integrated.

    **Test Mechanism**: This test first prepares the input dataset by dropping any non-applicable values. It then
    iterates pairs of variables, applying the Engle-Granger cointegration test to each pair. The test yield a 'p'
    value, which is then compared to a pre-set threshold to determine whether the corresponding variables are
    cointegrated or not. If the 'p' value is less than or equal to the threshold, the decision is 'Cointegrated', if
    not, 'Not cointegrated'. The metric returns a summary table of the cointegration results for each pair of time
    series variables.

    **Signs of High Risk**: High risk can be indicated if a large number of variables that are expected to be
    cointegrated fail the test. Also, if a significant number of 'p' values obtained are near the threshold, it also
    poses a risk as minor data variations can skew the decision between 'Cointegrated' and 'Not cointegrated'.

    **Strengths**: This test is a powerful method for analysing the relationship between time series, particularly when
    it's important to know whether variables are moving together in a statistically significant manner. Objectively
    evaluating such relationships can drive better forecasting in many domains, especially in finance or economics
    where prediction models often depend on understanding how different variables move together over time.

    **Limitations**: Cointegration tests, such as the Engle-Granger, often assume that time series are integrated of
    the same order, which is not always true in multi-variate time series datasets. Non-stationary characteristics in
    the series or the presence of structural breaks might give falsely positive or negative cointegration results.
    Additionally, the method doesn't work very well with small sample sizes due to a lack of power. Thus, the test must
    be used with caution, and where possible, corroborated with other predictive indicators.
    """

    type = "dataset"
    name = "engle_granger_coint"
    required_inputs = ["dataset"]
    default_params = {"threshold": 0.05}
    metadata = {
        "task_types": ["regression"],
        "tags": ["time_series_data", "statistical_test", "forecasting"],
    }

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
