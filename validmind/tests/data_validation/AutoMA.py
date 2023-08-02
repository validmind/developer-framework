# Copyright © 2023 ValidMind Inc. All rights reserved.

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller

from validmind.logging import get_logger
from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata

logger = get_logger(__name__)


class AutoMA(Metric):
    """
    Automatically detects the MA order of a time series using both BIC and AIC.
    """

    type = "dataset"
    name = "auto_ma"
    required_context = ["dataset"]
    default_params = {"max_ma_order": 3}

    def run(self):
        if "max_ma_order" not in self.params:
            raise ValueError("max_ma_order must be provided in params")

        max_ma_order = self.params["max_ma_order"]

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
