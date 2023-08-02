# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from arch.unitroot import DFGLS

from validmind.vm_models import Metric


@dataclass
class DFGLSArch(Metric):
    """
    Dickey-Fuller GLS unit root test for
    establishing the order of integration of time series
    """

    name = "dickey_fuller_gls"

    def run(self):
        """
        Calculates Dickey-Fuller GLS metric for each of the dataset features
        """
        dataset = self.dataset.df

        dfgls_values = {}
        for col in dataset.columns:
            dfgls_out = DFGLS(dataset[col].values)
            dfgls_values[col] = {
                "stat": dfgls_out.stat,
                "pvalue": dfgls_out.pvalue,
                "usedlag": dfgls_out.lags,
                "nobs": dfgls_out.nobs,
            }

        return self.cache_results(dfgls_values)
