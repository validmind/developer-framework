# Copyright © 2023 ValidMind Inc. All rights reserved.

import matplotlib.pyplot as plt
import seaborn as sns

from validmind.vm_models import Figure, Metric


class SpreadPlot(Metric):
    """
    This class provides a metric to visualize the spread between pairs of time series variables in a given dataset. By plotting the spread of each pair of variables in separate figures, users can assess the relationship between the variables and determine if any cointegration or other time series relationships exist between them.
    """

    name = "spread_plot"
    required_context = ["dataset"]

    @staticmethod
    def plot_spread(series1, series2, ax=None):
        """
        Plot the spread between two time series variables.
        :param series1: Pandas Series with time-series data for the first variable
        :param series2: Pandas Series with time-series data for the second variable
        :param ax: Axis object for the spread plot
        """
        spread = series1 - series2

        if ax is None:
            _, ax = plt.subplots()

        sns.lineplot(data=spread, ax=ax)

        return ax

    def run(self):
        df = self.dataset.df.dropna()

        figures = []
        columns = df.columns
        num_vars = len(columns)

        for i in range(num_vars):
            for j in range(i + 1, num_vars):
                var1 = columns[i]
                var2 = columns[j]

                series1 = df[var1]
                series2 = df[var2]

                fig, ax = plt.subplots()
                fig.suptitle(
                    f"Spread between {var1} and {var2}",
                    fontsize=20,
                    weight="bold",
                    y=0.95,
                )

                self.plot_spread(series1, series2, ax=ax)

                ax.set_xlabel("")
                ax.tick_params(axis="both", labelsize=18)

                # Do this if you want to prevent the figure from being displayed
                plt.close("all")

                figures.append(
                    Figure(
                        for_object=self,
                        key=f"{self.key}:{var1}_{var2}",
                        figure=fig,
                    )
                )

        return self.cache_results(figures=figures)
