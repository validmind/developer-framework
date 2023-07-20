# This software is proprietary and confidential. Unauthorized copying,
# modification, distribution or use of this software is strictly prohibited.
# Please refer to the LICENSE file in the root directory of this repository
# for more information.
#
# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from arch.unitroot import ZivotAndrews

from validmind.vm_models import Metric


@dataclass
class ZivotAndrewsArch(Metric):
    """
    Zivot-Andrews unit root test for
    establishing the order of integration of time series
    """

    name = "zivot_andrews"

    def run(self):
        """
        Calculates Zivot-Andrews metric for each of the dataset features
        """
        dataset = self.dataset.df

        za_values = {}
        for col in dataset.columns:
            za = ZivotAndrews(dataset[col].values)
            za_values[col] = {
                "stat": za.stat,
                "pvalue": za.pvalue,
                "usedlag": za.lags,
                "nobs": za.nobs,
            }

        return self.cache_results(za_values)
