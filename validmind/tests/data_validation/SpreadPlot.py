# Copyright © 2023 ValidMind Inc. All rights reserved.

import matplotlib.pyplot as plt
import seaborn as sns

from validmind.vm_models import Figure, Metric


class SpreadPlot(Metric):
    """
    **Purpose**:
    The purpose of the SpreadPlot metric is to visually explore and understand the relationships between pairs of time
    series variables in the given dataset. This understanding aids in identifying and assessing potential time series
    relationships, such as cointegration, between variables.

    **Test Mechanism**:
    The test mechanism for this metric involves calculating and plotting the spread between each pair of time series
    variables in the dataset. More specifically, the difference between two variables is computed and then plotted as a
    line graph. This process is repeated for all unique pairs of variables in the dataset.

    **Signs of High Risk**:
    Signs of high risk related to this metric include the presence of large fluctuations in the spread over time,
    unexpected patterns, or trends that might signal a potential risk in the underlying relationships between the
    variables. Also, the presence of significant missing data or extreme outlier values could potentially distort the
    spread, indicating a high risk.

    **Strengths**:
    The key strengths of using the SpreadPlot metric include:
    1. Enables detailed visual inspection and interpretation of the relationships between time-series pairs.
    2. Facilitates uncovering complex relationships like cointegration.
    3. Enhances interpretability by visualizing the relationships, aiding in identifying outliers and trends.
    4. Capable of handling multiple variable pairs from a dataset with a flexible and adaptable process.

    **Limitations**:
    Despite its strengths, the SpreadPlot metric also comes with certain limitations:
    1. It's primarily a visualization tool and does not provide quantitative measurements or statistics to objectively
    assess relationships.
    2. Highly dependent on the quality and granularity of the data – missing data or outliers can significantly affect
    the interpretation of the relationships.
    3. Can become inefficient or challenging to interpret with a large number of variables due to the large number of
    plots.
    4. Might not fully capture complex non-linear relationships between variables.
    """

    name = "spread_plot"
    required_inputs = ["dataset"]
    metadata = {
        "task_types": ["regression"],
        "tags": ["time_series_data", "visualization"],
    }

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
