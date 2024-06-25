# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import matplotlib.pyplot as plt
import seaborn as sns

from validmind.vm_models import Figure, Metric


class SpreadPlot(Metric):
    """
    Visualizes the spread relationship between pairs of time-series variables in a dataset, thereby aiding in
    identification of potential correlations.

    **Purpose**:
    The SpreadPlot metric is intended to graphically illustrate and analyse the relationships between pairs of time
    series variables within a given dataset. This facilitated understanding helps in identifying and assessing
    potential time series correlations, like cointegration, between the variables.

    **Test Mechanism**:
    The SpreadPlot metric operates by computing and representing the spread between each pair of time series variables
    in the dataset. In particular, the difference between two variables is calculated and presented as a line graph.
    This method is iterated for each unique pair of variables in the dataset.

    **Signs of High Risk**:
    Potential indicators of high risk related to the SpreadPlot metric might include:

    - Large fluctuations in the spread over a given timespan
    - Unexpected patterns or trends that may signal a potential risk in the underlying correlations between the
    variables
    - Presence of significant missing data or extreme outlier values, which could potentially skew the spread and
    indicate high risk

    **Strengths**:
    The SpreadPlot metric provides several key advantages:

    - It allows for thorough visual examination and interpretation of the correlations between time-series pairs
    - It aids in revealing complex relationships like cointegration
    - It enhances interpretability by visualising the relationships, thereby helping in spotting outliers and trends
    - It is capable of handling numerous variable pairs from the dataset through a versatile and adaptable process

    **Limitations**:
    Despite its advantages, the SpreadPlot metric does have certain drawbacks:

    - It primarily serves as a visualisation tool and does not offer quantitative measurements or statistics to
    objectively determine relationships
    - It heavily relies on the quality and granularity of the data - missing data or outliers can notably disturb the
    interpretation of the relationships
    - It can become inefficient or difficult to interpret with a high number of variables due to the profuse number of
    plots
    - It might not completely capture intricate non-linear relationships between the variables
    """

    name = "spread_plot"
    required_inputs = ["dataset"]
    tasks = ["regression"]
    tags = ["time_series_data", "visualization"]

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
        df = self.inputs.dataset.df.dropna()

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
