# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from statsmodels.stats.diagnostic import kstest_normal

from validmind.vm_models import Metric


@dataclass
class KolmogorovSmirnov(Metric):
    """
    The Kolmogorov-Smirnov metric is a statistical test used to determine
    whether a given set of data follows a normal distribution.
    """

    name = "kolmogorov_smirnov"

    def run(self):
        """
        Calculates KS for each of the dataset features
        """
        x_train = self.train_ds.df
        x_train = self.train_ds.df

        ks_values = {}
        for col in x_train.columns:
            ks_stat, p_value = kstest_normal(x_train[col].values, "norm")
            ks_values[col] = {"stat": ks_stat, "pvalue": p_value}

        return self.cache_results(ks_values)
