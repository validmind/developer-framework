# This software is proprietary and confidential. Unauthorized copying,
# modification, distribution or use of this software is strictly prohibited.
# Please refer to the LICENSE file in the root directory of this repository
# for more information.
#
# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from statsmodels.tsa.stattools import kpss

from validmind.vm_models import Metric


@dataclass
class KPSS(Metric):
    """
    Kwiatkowski-Phillips-Schmidt-Shin (KPSS) unit root test for
    establishing the order of integration of time series
    """

    name = "kpss"

    def run(self):
        """
        Calculates KPSS for each of the dataset features
        """
        dataset = self.dataset.df

        kpss_values = {}
        for col in dataset.columns:
            kpss_stat, pvalue, usedlag, critical_values = kpss(dataset[col].values)
            kpss_values[col] = {
                "stat": kpss_stat,
                "pvalue": pvalue,
                "usedlag": usedlag,
                "critical_values": critical_values,
            }

        return self.cache_results(kpss_values)
