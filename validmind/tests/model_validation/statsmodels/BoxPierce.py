# Copyright © 2023 ValidMind Inc. All rights reserved.

from statsmodels.stats.diagnostic import acorr_ljungbox

from validmind.vm_models import Metric


class BoxPierce(Metric):
    """
    The Box-Pierce test is a statistical test used to determine
    whether a given set of data has autocorrelations
    that are different from zero.
    """

    name = "box_pierce"

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
