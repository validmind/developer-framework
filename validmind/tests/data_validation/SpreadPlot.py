# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import matplotlib.pyplot as plt
import seaborn as sns

from validmind.vm_models import Figure, Metric


class SpreadPlot(Metric):
    """
    Assesses potential correlations between pairs of time series variables through visualization to enhance
    understanding of their relationships.

    ### Purpose

    The SpreadPlot test aims to graphically illustrate and analyze the relationships between pairs of time series
    variables within a given dataset. This facilitated understanding helps in identifying and assessing potential time
    series correlations, such as cointegration, between the variables.

    ### Test Mechanism

    The SpreadPlot test computes and represents the spread between each pair of time series variables in the dataset.
    Specifically, the difference between two variables is calculated and presented as a line graph. This process is
    iterated for each unique pair of variables in the dataset, allowing for comprehensive visualization of their
    relationships.

    ### Signs of High Risk

    - Large fluctuations in the spread over a given timespan.
    - Unexpected patterns or trends that may signal potential risks in the underlying correlations between the
    variables.
    - Presence of significant missing data or extreme outlier values, which could potentially skew the spread and
    indicate high risk.

    ### Strengths

    - Allows for thorough visual examination and interpretation of the correlations between time-series pairs.
    - Aids in revealing complex relationships like cointegration.
    - Enhances interpretability by visualizing the relationships, thereby helping in spotting outliers and trends.
    - Capable of handling numerous variable pairs from the dataset through a versatile and adaptable process.

    ### Limitations

    - Primarily serves as a visualization tool and does not offer quantitative measurements or statistics to
    objectively determine relationships.
    - Heavily relies on the quality and granularity of the data—missing data or outliers can notably disturb the
    interpretation of relationships.
    - Can become inefficient or difficult to interpret with a high number of variables due to the profuse number of
    plots.
    - Might not completely capture intricate non-linear relationships between the variables.
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
