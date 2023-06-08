from validmind.vm_models import Metric


from statsmodels.stats.diagnostic import lilliefors


from dataclasses import dataclass


@dataclass
class Lilliefors(Metric):
    """
    The Lilliefors test is a statistical test used to determine
    whether a given set of data follows a normal distribution.
    """

    name = "lilliefors_test"

    def run(self):
        """
        Calculates Lilliefors test for each of the dataset features
        """
        x_train = self.train_ds.df
        x_train = self.train_ds.df

        lilliefors_values = {}
        for col in x_train.columns:
            l_stat, p_value = lilliefors(x_train[col].values)
            lilliefors_values[col] = {
                "stat": l_stat,
                "pvalue": p_value,
            }

        return self.cache_results(lilliefors_values)