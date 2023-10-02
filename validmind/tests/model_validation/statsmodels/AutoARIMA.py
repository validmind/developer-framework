# Copyright © 2023 ValidMind Inc. All rights reserved.

from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller

from validmind.logging import get_logger
from validmind.vm_models import Metric

logger = get_logger(__name__)


class AutoARIMA(Metric):
    """
    **Purpose**: This validation test is designed to evaluate and rank ARIMA models, which are popular forecasting
    models used, amongst other things, for time series prediction tasks. The script automatically fits multiple ARIMA
    models (with varying orders of differencing, autoregression, and moving average parameters) for each variable in
    the provided dataset. It then ranks them based on their Bayesian Information Criterion (BIC) and Akaike Information
    Criterion (AIC) values. This allows efficient selection of the most suitable model for forecasting, based on these
    standard statistical measures.

    **Test Mechanism**: The metric works by generating a range of possible combinations of ARIMA model parameters
    within a predefined limit (max_p, max_d, max_q representing autoregressive, differencing, and moving average
    components respectively). It fits all these models on the provided time-series data. For each ARIMA model, it
    calculates and records the BIC and AIC value, which serve as performance measures for the model fit. Furthermore,
    prior to the parameter fitting, it runs an Augmented Dickey-Fuller test for stationarity on the series. If the
    series isn't stationary, it sends out a warning, as ARIMA models require the input series to be stationary.

    **Signs of High Risk**: If the p-value of the Augmented Dickey-Fuller test for any variable is greater than 0.05, a
    warning is logged indicating that the series might not be stationary, and this can lead to inaccurate results.
    Secondly, if there is consistent failure in fitting ARIMA models (evident through logged errors), it might indicate
    issues with the data or model stability.

    **Strengths**: This mechanism streamlines the potentially complex task of selecting the most suitable ARIMA model
    based on BIC and AIC criteria. It checks for and warns about non-stationarity in the data, a crucial assumption for
    ARIMA models. The exhaustive approach in checking all possible combinations of model parameters maximizes the
    potential for finding the best-fit model.

    **Limitations**: The approach can be computationally expensive given that it creates and fits multiple ARIMA models
    per variable. Secondly, a high p-value in the Augmented Dickey-Fuller test indicates a lack of stationarity, but it
    doesn't make any transformations on the data to rectify this. Additionally, model selection is purely based on BIC
    and AIC criteria, which might not yield the best predictive model in all scenarios. Also, it's limited to
    regression tasks on time series data and won't work effectively for other types of Machine Learning tasks.
    """

    name = "auto_arima"
    metadata = {
        "task_types": ["regression"],
        "tags": ["time_series_data", "forecasting", "model_selection", "statsmodels"],
    }

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
