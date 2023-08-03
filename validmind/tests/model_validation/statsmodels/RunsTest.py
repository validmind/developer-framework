# Copyright © 2023 ValidMind Inc. All rights reserved.

from statsmodels.sandbox.stats.runs import runstest_1samp

from validmind.vm_models import Metric


class RunsTest(Metric):
    """
    The runs test is a statistical test used to determine whether a given set
    of data has runs of positive and negative values that are longer than expected
    under the null hypothesis of randomness.
    """

    name = "runs_test"

    def run(self):
        """
        Calculates the run test for each of the dataset features
        """
        x_train = self.train_ds.df
        x_train = self.train_ds.df

        runs_test_values = {}
        for col in x_train.columns:
            runs_stat, runs_p_value = runstest_1samp(x_train[col].values)

            runs_test_values[col] = {
                "stat": runs_stat,
                "pvalue": runs_p_value,
            }

        return self.cache_results(runs_test_values)
