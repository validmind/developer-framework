# Copyright © 2023 ValidMind Inc. All rights reserved.

from scipy import stats

from validmind.vm_models import Metric


class ShapiroWilk(Metric):
    """
    **Purpose**: The Shapiro-Wilk metric is used to assess if a given set of data adheres to the standard normal
    distribution. This is integral in machine learning modeling as the normality of data can significantly affect model
    performance. In particular, it is used on different features of the dataset in both classification and regression
    tasks.

    **Test Mechanism**: By implementing the Shapiro-Wilk test for each feature column in the training dataset, we
    determine if the data in these columns conform to the normal distribution. The test returns a statistic and a
    p-value, where the p-value is used to decipher whether to accept or reject the null hypothesis (the data being
    tested is normally distributed).

    **Signs of High Risk**: A lower p-value, typically below 0.05, indicates a high risk as it rejects the null
    hypothesis, meaning that the data is not normally distributed. For ML models that assume normality of data, this
    could lead to poor performance or inaccurate predictions.

    **Strengths**: The Shapiro-Wilk test is known for its precision, making it especially useful on small to
    moderate-sized datasets. It also works on both classification and regression tasks, providing more versatility in
    its usage. Since it tests each feature column separately, it can give an alert if any particular feature does not
    conform to normality.

    **Limitations**: Since Shapiro-Wilk test is quite sensitive, it often rejects the null hypothesis (i.e., data is
    normally distributed) even for slight deviations, particularly for large datasets. This means the test can consider
    data as non-normal even if it's approximately normally distributed, potentially leading to 'false alarms' of high
    risk. Additionally, handling of missing data or outliers needs to be carefully managed before testing as these can
    highly influence the results. Lastly, it is not ideally suited for data with strong skewness or kurtosis.
    """

    name = "shapiro_wilk"
    metadata = {
        "task_types": ["classification", "regression"],
        "tags": ["tabular_data", "data_distribution", "statistical_test"],
    }

    def run(self):
        """
        Calculates Shapiro-Wilk test for each of the dataset features.
        """
        x_train = self.train_ds.df
        x_train = self.train_ds.df

        sw_values = {}
        for col in x_train.columns:
            sw_stat, sw_pvalue = stats.shapiro(x_train[col].values)

            sw_values[col] = {
                "stat": sw_stat,
                "pvalue": sw_pvalue,
            }

        return self.cache_results(sw_values)
