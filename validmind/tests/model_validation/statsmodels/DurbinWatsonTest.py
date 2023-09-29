# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from statsmodels.stats.stattools import durbin_watson

from validmind.vm_models import Metric


@dataclass
class DurbinWatsonTest(Metric):
    """
    **Purpose**: The Durbin-Watson Test metric is utilized to detect autocorrelation (i.e., a set of data values are
    influenced by their predecessors) in time series data. This is especially important in regression tasks, where the
    independence of residuals is often assumed. If there is a significant autocorrelation, the predictions of the model
    may not be reliable.

    **Test Mechanism**: The Durbin-Watson Test metric generates a statistical value for each feature of the training
    dataset. This is done through the `durbin_watson` function from the `statsmodels` library in Python. The function
    is looped through all columns of the dataset, calculating and storing the Durbin-Watson (DB) value for each column.
    The results are then cached and made available for further analysis. A Durbin-Watson metric value close to 2
    suggests no autocorrelation, a value toward 0 indicates positive autocorrelation, and a value toward 4 shows
    negative autocorrelation.

    **Signs of High Risk**: If the Durbin-Watson value for any of the features is significantly different from 2, it
    indicates a high risk as it may point to significant autocorrelation issues within the dataset. Particularly, a
    value closer to '0' might hint at positive autocorrelation, while a value closer to '4' might suggest negative
    autocorrelation. These autocorrelation issues could lead to unreliable prediction models.

    **Strengths**: This metric is particularly powerful in identifying autocorrelation in the residuals of prediction
    models. With this metric, we can diagnose whether residuals have autocorrelation, which could violate the
    assumptions of various modeling techniques, particularly in regression analysis and time-series data modeling.

    **Limitations**: The Durbin-Watson Test has several limitations. First, it only detects linear autocorrelation and
    may miss other types of relationships. Second, it is significantly influenced by the order of data points, and
    shuffling the order can lead to entirely different results. Lastly, the test only checks for autocorrelation
    between a variable and its immediate preceding variable, essentially it's of order one, and cannot detect higher
    order autocorrelation.
    """

    name = "durbin_watson"
    metadata = {
        "task_types": ["regression"],
        "tags": ["time_series_data", "forecasting", "statistical_test", "statsmodels"],
    }

    def run(self):
        """
        Calculates DB for each of the dataset features
        """
        x_train = self.train_ds.df
        x_train = self.train_ds.df

        dw_values = {}
        for col in x_train.columns:
            dw_values[col] = durbin_watson(x_train[col].values)

        return self.cache_results(dw_values)
