# Copyright © 2023 ValidMind Inc. All rights reserved.

import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

from validmind.logging import get_logger
from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata

logger = get_logger(__name__)


class AutoSeasonality(Metric):
    """
    Automatically detects the optimal seasonal order for a time series dataset
    using the seasonal_decompose method.
    """

    name = "auto_seasonality"
    required_context = ["dataset"]
    default_params = {"min_period": 1, "max_period": 4}

    def evaluate_seasonal_periods(self, series, min_period, max_period):
        seasonal_periods = []
        residual_errors = []

        for period in range(min_period, max_period + 1):
            try:
                sd = seasonal_decompose(series, model="additive", period=period)
                residual_error = np.abs(sd.resid.dropna()).mean()

                seasonal_periods.append(period)
                residual_errors.append(residual_error)
            except Exception as e:
                logger.error(f"Error evaluating period {period} for series: {e}")

        return seasonal_periods, residual_errors

    def run(self):
        # Parse input parameters
        if "min_period" not in self.params:
            raise ValueError("min_period must be provided in params")
        min_period = self.params["min_period"]

        if "max_period" not in self.params:
            raise ValueError("max_period must be provided in params")
        max_period = self.params["max_period"]

        df = self.dataset.df

        # Create an empty DataFrame to store the results
        summary_auto_seasonality = pd.DataFrame()

        for col_name, col in df.items():
            series = col.dropna()

            # Evaluate seasonal periods
            seasonal_periods, residual_errors = self.evaluate_seasonal_periods(
                series, min_period, max_period
            )

            for i, period in enumerate(seasonal_periods):
                decision = "Seasonality" if period > 1 else "No Seasonality"
                summary_auto_seasonality = pd.concat(
                    [
                        summary_auto_seasonality,
                        pd.DataFrame(
                            [
                                {
                                    "Variable": col_name,
                                    "Seasonal Period": period,
                                    "Residual Error": residual_errors[i],
                                    "Decision": decision,
                                }
                            ]
                        ),
                    ],
                    ignore_index=True,
                )

        # Convert the 'Seasonal Period' column to integer
        summary_auto_seasonality["Seasonal Period"] = summary_auto_seasonality[
            "Seasonal Period"
        ].astype(int)

        # Create a DataFrame to store the best seasonality period for each variable
        best_seasonality_period = pd.DataFrame()

        for variable in summary_auto_seasonality["Variable"].unique():
            temp_df = summary_auto_seasonality[
                summary_auto_seasonality["Variable"] == variable
            ]
            best_row = temp_df[
                temp_df["Residual Error"] == temp_df["Residual Error"].min()
            ]
            best_seasonality_period = pd.concat([best_seasonality_period, best_row])

        # Rename the 'Seasonal Period' column to 'Best Period'
        best_seasonality_period = best_seasonality_period.rename(
            columns={"Seasonal Period": "Best Period"}
        )

        # Convert the 'Best Period' column to integer
        best_seasonality_period["Best Period"] = best_seasonality_period[
            "Best Period"
        ].astype(int)

        return self.cache_results(
            {
                "auto_seasonality": summary_auto_seasonality.to_dict(orient="records"),
                "best_seasonality_period": best_seasonality_period.to_dict(
                    orient="records"
                ),
            }
        )

    def summary(self, metric_value):
        """
        Build one table for summarizing the auto seasonality results
        and another for the best seasonality period results
        """
        summary_auto_seasonality = metric_value["auto_seasonality"]
        best_seasonality_period = metric_value["best_seasonality_period"]

        return ResultSummary(
            results=[
                ResultTable(
                    data=summary_auto_seasonality,
                    metadata=ResultTableMetadata(title="Auto Seasonality Results"),
                ),
                ResultTable(
                    data=best_seasonality_period,
                    metadata=ResultTableMetadata(
                        title="Best Seasonality Period Results"
                    ),
                ),
            ]
        )
