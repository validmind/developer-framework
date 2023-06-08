from validmind.vm_models import Metric


from arch.unitroot import ZivotAndrews


from dataclasses import dataclass


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