# Copyright © 2023 ValidMind Inc. All rights reserved.

import pandas as pd
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.stattools import adfuller

from validmind.logging import get_logger
from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata

logger = get_logger(__name__)


class AutoAR(Metric):
    """
    **Purpose**:
    The purpose of this test, referred to as AutoAR, is to automatically detect the Autoregressive (AR) order of a time
    series using both Bayesian information criterion (BIC) and Akaike information criterion (AIC) for regression tasks.
    The AR order specifies the number of previous terms in the series to use to predict the current term. The goal is
    to select the appropriate AR model that best captures the trend and seasonality in the time series data.

    **Test Mechanism**:
    The test iterates over a range of possible AR orders up to a specified maximum. For each order, an autoregressive
    model is fitted, and the BIC and AIC are computed. Both these statistical measures penalize models for complexity
    (higher number of parameters), favoring simpler models that fit the data well. Additionally, the Augmented
    Dickey-Fuller test is conducted to check stationarity of the time series; non-stationary series might produce
    inaccurate results. The test results, including AR order, BIC, and AIC, are added into a dataframe for easy
    comparison. Subsequently, the AR order with minimum BIC is determined as the "best" order for each variable.

    **Signs of High Risk**:
    - If a time series is not stationary (Augmented Dickey-Fuller test p-value > 0.05), it may lead to inaccurate
    results.
    - Issues with the model fitting process, such as computational or convergence problems, suggest a high risk.
    - If the chosen AR order is consistently at the maximum specified order, this could suggest insufficiency of the
    maximum set limit.

    **Strengths**:
    - The test automatically determines the optimal AR order, reducing potential bias involved in manual selection.
    - The method attempts to balance goodness-of-fit against model simplicity, preventing overfitting.
    - It factors in stationarity of the time series, essential for reliable AR modeling.
    - The test consolidates the results into a clear, easily interpreted table.

    **Limitations**:
    - The test requires stationary input time series.
    - Assumes linear relationship between the series and its lags.
    - Finding the best model is limited to the maximum AR order provided in the parameters. A low max_ar_order may
    yield suboptimal results.
    - AIC and BIC may not always select the same model as the best; interpretation may need to consider the goal and
    the trade-offs.
    """

    type = "dataset"
    name = "auto_ar"
    required_inputs = ["dataset"]
    default_params = {"max_ar_order": 3}
    metadata = {
        "task_types": ["regression"],
        "tags": ["time_series_data", "statsmodels", "forecasting", "statistical_test"],
    }

    def run(self):
        if "max_ar_order" not in self.params:
            raise ValueError("max_ar_order must be provided in params")

        max_ar_order = int(self.params["max_ar_order"])

        df = self.dataset.df

        # Create empty DataFrames to store the results
        summary_ar_analysis = pd.DataFrame()
        best_ar_order = pd.DataFrame()

        for col in df.columns:
            series = df[col].dropna()

            # Check for stationarity using the Augmented Dickey-Fuller test
            adf_test = adfuller(series)
            if adf_test[1] > 0.05:
                logger.warning(
                    f"Warning: {col} is not stationary. Results may be inaccurate."
                )

            for ar_order in range(0, max_ar_order + 1):
                try:
                    model = AutoReg(series, lags=ar_order, old_names=False)
                    model_fit = model.fit()

                    # Append the result of each AR order directly into the DataFrame
                    summary_ar_analysis = pd.concat(
                        [
                            summary_ar_analysis,
                            pd.DataFrame(
                                [
                                    {
                                        "Variable": col,
                                        "AR Order": ar_order,
                                        "BIC": model_fit.bic,
                                        "AIC": model_fit.aic,
                                    }
                                ]
                            ),
                        ],
                        ignore_index=True,
                    )
                except Exception as e:
                    logger.error(f"Error fitting AR({ar_order}) model for {col}: {e}")

            # Find the best AR Order for this variable based on the minimum BIC
            variable_summary = summary_ar_analysis[
                summary_ar_analysis["Variable"] == col
            ]
            best_bic_row = variable_summary[
                variable_summary["BIC"] == variable_summary["BIC"].min()
            ]
            best_ar_order = pd.concat([best_ar_order, best_bic_row])

        # Convert the 'AR Order' column to integer
        summary_ar_analysis["AR Order"] = summary_ar_analysis["AR Order"].astype(int)
        best_ar_order["AR Order"] = best_ar_order["AR Order"].astype(int)

        return self.cache_results(
            {
                "auto_ar_analysis": summary_ar_analysis.to_dict(orient="records"),
                "best_ar_order": best_ar_order.to_dict(orient="records"),
            }
        )

    def summary(self, metric_value):
        """
        Build one table for summarizing the auto AR results
        and another for the best AR Order results
        """
        summary_ar_analysis = metric_value["auto_ar_analysis"]
        best_ar_order = metric_value["best_ar_order"]

        return ResultSummary(
            results=[
                ResultTable(
                    data=summary_ar_analysis,
                    metadata=ResultTableMetadata(title="Auto AR Analysis Results"),
                ),
                ResultTable(
                    data=best_ar_order,
                    metadata=ResultTableMetadata(title="Best AR Order Results"),
                ),
            ]
        )
