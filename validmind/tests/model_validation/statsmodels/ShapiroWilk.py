# Copyright © 2023 ValidMind Inc. All rights reserved.

from scipy import stats

from validmind.vm_models import Metric


class ShapiroWilk(Metric):
    """
    The Shapiro-Wilk test is a statistical test used to determine
    whether a given set of data follows a normal distribution.
    """

    name = "shapiro_wilk"

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
