# Copyright © 2023 ValidMind Inc. All rights reserved.

from statsmodels.stats.diagnostic import acorr_ljungbox

from validmind.vm_models import Metric


class BoxPierce(Metric):
    """
    **Purpose:** The Box-Pierce test is a diagnostic tool employed to check if any form of autocorrelation (serial
    correlation) is present in the time series dataset, a set of data points indexed in time order, being tested.
    Autocorrelation is the similarity between observations as a function of the time lag between them. It evaluates the
    independence of residuals in regression types of tasks in Machine Learning. This is essentially a measure to
    establish the quality of a time-series model, ensuring the error terms in the model do not follow any specific
    pattern and are random.

    **Test Mechanism:** The Box-Pierce test calculates a test statistic and a corresponding p-value from the data
    features. The computed statistical test checks the null hypothesis that the data are independently distributed.
    This test is implemented by looping over each feature column in the time-series dataset and applying the
    `acorr_ljungbox` function from the statsmodels library, which returns both the Box-Pierce test statistic and its
    corresponding p-value. These values are cached as results.

    **Signs of High Risk:** A low p-value (typically less than 0.05) in the box-pierce test reflects evidence against
    the null hypothesis suggesting that there are autocorrelations in the dataset, pointing to a potentially high-risk
    situation in terms of model performance. Additionally, large Box-Pierce test statistic values may signal the
    presence of autocorrelation.

    **Strengths:** The Box-Pierce test is beneficial as it aids in detecting patterns or trends in data that are meant
    to be random, essentially ensuring the absence of autocorrelation. It can be implemented efficiently due to low
    computational complexity. Moreover, it can be widely applied for most types of regression problems.

    **Limitations:** This test assumes homoscedasticity and normality of residuals, assumptions which may not always
    hold true. It may have reduced power for detecting complex autocorrelation schemes, such as higher order or
    negative correlations. Also, it does not provide specific insights into the nature or patterns of the
    autocorrelation if detected; it is solely a general test for the existence of autocorrelation. Furthermore, if the
    time series data has a trend or seasonality, the Box-Pierce test could give misleading results. Lastly, it's worth
    stressing it's only applicable to time-series data, limiting its overall utility.
    """

    name = "box_pierce"
    metadata = {
        "task_types": ["regression"],
        "tags": ["time_series_data", "forecasting", "statistical_test", "statsmodels"],
    }

    def run(self):
        """
        Calculates Box-Pierce test for each of the dataset features
        """
        x_train = self.train_ds.df
        x_train = self.train_ds.df

        box_pierce_values = {}
        for col in x_train.columns:
            bp_results = acorr_ljungbox(
                x_train[col].values, boxpierce=True, return_df=True
            )
            box_pierce_values[col] = {
                "stat": bp_results.iloc[0]["lb_stat"],
                "pvalue": bp_results.iloc[0]["lb_pvalue"],
            }

        return self.cache_results(box_pierce_values)
