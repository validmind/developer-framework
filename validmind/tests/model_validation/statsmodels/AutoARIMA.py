# Copyright © 2023 ValidMind Inc. All rights reserved.

from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller

from validmind.logging import get_logger
from validmind.vm_models import Metric

logger = get_logger(__name__)


class AutoARIMA(Metric):
    """
    Automatically fits multiple ARIMA models for each variable and ranks them by BIC and AIC.
    """

    name = "auto_arima"

    max_p = 3
    max_d = 2
    max_q = 3

    def run(self):
        x_train = self.train_ds.df

        results = []

        for col in x_train.columns:
            series = x_train[col].dropna()

            # Check for stationarity using the Augmented Dickey-Fuller test
            adf_test = adfuller(series)
            if adf_test[1] > 0.05:
                logger.warning(
                    f"Warning: {col} is not stationary. Results may be inaccurate."
                )

            arima_orders = []
            bic_values = []
            aic_values = []

            for p in range(self.max_p + 1):
                for d in range(self.max_d + 1):
                    for q in range(self.max_q + 1):
                        try:
                            model = ARIMA(series, order=(p, d, q))
                            model_fit = model.fit()

                            arima_orders.append((p, d, q))
                            bic_values.append(model_fit.bic)
                            aic_values.append(model_fit.aic)
                        except Exception as e:
                            logger.error(
                                f"Error fitting ARIMA({p}, {d}, {q}) model for {col}: {e}"
                            )

            result = {
                "Variable": col,
                "ARIMA Orders": arima_orders,
                "BIC": bic_values,
                "AIC": aic_values,
            }
            results.append(result)

        return self.cache_results(results)
