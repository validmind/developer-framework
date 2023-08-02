# Copyright © 2023 ValidMind Inc. All rights reserved.

import pandas as pd
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.stattools import adfuller

from validmind.logging import get_logger
from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata

logger = get_logger(__name__)


class AutoAR(Metric):
    """
    Automatically detects the AR order of a time series using both BIC and AIC.
    """

    type = "dataset"
    name = "auto_ar"
    required_context = ["dataset"]
    default_params = {"max_ar_order": 3}

    def run(self):
        if "max_ar_order" not in self.params:
            raise ValueError("max_ar_order must be provided in params")

        max_ar_order = self.params["max_ar_order"]

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
