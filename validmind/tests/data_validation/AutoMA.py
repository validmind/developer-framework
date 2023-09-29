# Copyright © 2023 ValidMind Inc. All rights reserved.

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller

from validmind.logging import get_logger
from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata

logger = get_logger(__name__)


class AutoMA(Metric):
    """
    **Purpose**: The primary role of the `AutoMA` metric is to automatically determine the optimal Moving Average (MA)
    order for each variable in the time series dataset. The decision of MA order is based on minimizing BIC (Bayesian
    Information Criterion) and AIC (Akaike Information Criterion); both are statistical tools for model choice. Before
    the fitting process begins, a stationarity test (Augmented Dickey-Fuller test) is conducted on each series.

    **Test Mechanism**: First, the `AutoMA` algorithm checks whether the `max_ma_order` parameter is provided. It then
    loops over all variables in the dataset, performing the Dickey-Fuller test for stationarity. For each variable (if
    stationary), it fits an ARIMA model for orders running from 0 to `max_ma_order`. The output is a list showing BIC
    and AIC values of the ARIMA models with different orders. For each variable, the MA order that offers the smallest
    BIC is selected as the *best MA order*. The final results include a table summarizing the auto MA analysis and a
    table listing the best MA order for each variable.

    **Signs of High Risk**:
    - If a series is non-stationary (p-value>0.05 in the Dickey-Fuller test), the result might be inaccurate.
    - Any error while fitting the ARIMA models, especially with higher MA order, could indicate possible risks and
    might require further investigation.

    **Strengths**:
    - This metric is beneficial for automating the selection process of the MA order for time series forecasting, thus
    saving time and effort usually required in manual hyperparameter tuning.
    - It applies both BIC and AIC, enhancing the chance of selecting the most suitable model.
    - It checks for stationarity of the series prior to model fitting, ensuring that the underlying assumptions of the
    MA model are met.

    **Limitations**:
    - If the time series is not stationary, the metric would provide inaccurate results. This limitation necessitates
    pre-processing steps to stabilize the series before ARIMA model fitting.
    - This metric uses a rudimentary model selection approach based on BIC and does not consider other possible model
    selection strategies, which might be more appropriate depending on the specific dataset.
    - The 'max_ma_order' parameter must be manually set, which may not always guarantee the best performance,
    especially if set too low.
    - The computation time raises with the increase in `max_ma_order`, thus the metric can be computationally expensive
    for larger values.
    """

    type = "dataset"
    name = "auto_ma"
    required_inputs = ["dataset"]
    default_params = {"max_ma_order": 3}
    metadata = {
        "task_types": ["regression"],
        "tags": ["time_series_data", "statsmodels", "forecasting", "statistical_test"],
    }

    def run(self):
        if "max_ma_order" not in self.params:
            raise ValueError("max_ma_order must be provided in params")

        max_ma_order = int(self.params["max_ma_order"])

        df = self.dataset.df

        # Create empty DataFrames to store the results
        summary_ma_analysis = pd.DataFrame()
        best_ma_order = pd.DataFrame()

        for col in df.columns:
            series = df[col].dropna()

            # Check for stationarity using the Augmented Dickey-Fuller test
            adf_test = adfuller(series)
            if adf_test[1] > 0.05:
                logger.warning(
                    f"Warning: {col} is not stationary. Results may be inaccurate."
                )

            for ma_order in range(0, max_ma_order + 1):
                try:
                    model = ARIMA(series, order=(0, 0, ma_order))
                    model_fit = model.fit()

                    # Append the result of each MA order directly into the DataFrame
                    summary_ma_analysis = pd.concat(
                        [
                            summary_ma_analysis,
                            pd.DataFrame(
                                [
                                    {
                                        "Variable": col,
                                        "MA Order": ma_order,
                                        "BIC": model_fit.bic,
                                        "AIC": model_fit.aic,
                                    }
                                ]
                            ),
                        ],
                        ignore_index=True,
                    )
                except Exception as e:
                    logger.error(f"Error fitting MA({ma_order}) model for {col}: {e}")

            # Find the best MA Order for this variable based on the minimum BIC
            variable_summary = summary_ma_analysis[
                summary_ma_analysis["Variable"] == col
            ]
            best_bic_row = variable_summary[
                variable_summary["BIC"] == variable_summary["BIC"].min()
            ]
            best_ma_order = pd.concat([best_ma_order, best_bic_row])

        # Convert the 'MA Order' column to integer
        summary_ma_analysis["MA Order"] = summary_ma_analysis["MA Order"].astype(int)
        best_ma_order["MA Order"] = best_ma_order["MA Order"].astype(int)

        return self.cache_results(
            {
                "auto_ma_analysis": summary_ma_analysis.to_dict(orient="records"),
                "best_ma_order": best_ma_order.to_dict(orient="records"),
            }
        )

    def summary(self, metric_value):
        """
        Build one table for summarizing the auto MA results
        and another for the best MA Order results
        """
        summary_ma_analysis = metric_value["auto_ma_analysis"]
        best_ma_order = metric_value["best_ma_order"]

        return ResultSummary(
            results=[
                ResultTable(
                    data=summary_ma_analysis,
                    metadata=ResultTableMetadata(title="Auto MA Analysis Results"),
                ),
                ResultTable(
                    data=best_ma_order,
                    metadata=ResultTableMetadata(title="Best MA Order Results"),
                ),
            ]
        )
