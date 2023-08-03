# Copyright © 2023 ValidMind Inc. All rights reserved.

from statsmodels.stats.stattools import jarque_bera

from validmind.vm_models import Metric


class JarqueBera(Metric):
    """
    The Jarque-Bera test is a statistical test used to determine
    whether a given set of data follows a normal distribution.
    """

    name = "jarque_bera"

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
