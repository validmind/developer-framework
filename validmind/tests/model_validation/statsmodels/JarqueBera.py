# Copyright © 2023 ValidMind Inc. All rights reserved.

from statsmodels.stats.stattools import jarque_bera

from validmind.vm_models import Metric


class JarqueBera(Metric):
    """
    **Purpose**: The purpose of the Jarque-Bera test as implemented in this metric is to determine if the features in
    the dataset of a given Machine Learning model follows a normal distribution. This is essential in understanding the
    distribution and behavior of the model's features, as numerous statistical methods assume normal distribution of
    the data.

    **Test Mechanism**: The test mechanism involves computing the Jarque-Bera statistic and the associated p-value,
    skew and kurtosis for each feature in the dataset. Necessary variables like the Jarque-Bera statistic, p-value,
    skew and kurtosis are computed using the 'jarque_bera' function from the 'statsmodels' library in python and stored
    in a dictionary. The jarque_bera function evaluates the skewness and kurtosis of the input dataset to determine if
    it follows a normal distribution. A significant p-value (usually less than 0.05) suggests that the feature does not
    possess normal distribution.

    **Signs of High Risk**: High risk associated with this test would be a significantly high Jarque-Bera statistic and
    a low p-value (typically < 0.05). These indicate that the data deviates significantly from a normal distribution,
    thereby implying that a machine learning model may not function as intended as many models expect feature data to
    be normally distributed.

    **Strengths**: The strength of this test lies in its ability to provide insights into the shape of the data
    distribution. It helps determine whether a given set of data follows a normal distribution or not, enabling risk
    assessment, especially for models that assume normal distribution of data. By measuring skewness and kurtosis, it
    also provides extra insights on the nature and magnitude of distribution deviation.

    **Limitations**: The Jarque-Bera test only checks for normality of the data distribution and will not provide
    insights about other types of distributions. Datasets which are not normally distributed but may follow some other
    distribution, may lead to incorrect risk assessments. Additionally, this test is very sensitive to large sample
    sizes, often rejecting the null hypothesis (that data is normally distributed) for even slight deviations in larger
    datasets.
    """

    name = "jarque_bera"
    metadata = {
        "task_types": ["classification", "regression"],
        "tags": [
            "tabular_data",
            "data_distribution",
            "statistical_test",
            "statsmodels",
        ],
    }

    def run(self):
        """
        Calculates JB for each of the dataset features
        """
        x_train = self.train_ds.df
        x_train = self.train_ds.df

        jb_values = {}
        for col in x_train.columns:
            jb_stat, jb_pvalue, jb_skew, jb_kurtosis = jarque_bera(x_train[col].values)

            jb_values[col] = {
                "stat": jb_stat,
                "pvalue": jb_pvalue,
                "skew": jb_skew,
                "kurtosis": jb_kurtosis,
            }

        return self.cache_results(jb_values)
