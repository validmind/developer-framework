# Copyright © 2023 ValidMind Inc. All rights reserved.

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

from validmind.vm_models import Figure, Metric


class ACFandPACFPlot(Metric):
    """
    Plots ACF and PACF for a given time series dataset.
    """

    name = "acf_pacf_plot"
    required_context = ["dataset"]

    def run(self):
        # Check if index is datetime
        if not pd.api.types.is_datetime64_any_dtype(self.dataset.df.index):
            raise ValueError("Index must be a datetime type")

        columns = list(self.dataset.df.columns)

        df = self.dataset.df.dropna()

        if not set(columns).issubset(set(df.columns)):
            raise ValueError("Provided 'columns' must exist in the dataset")

        figures = []

        for col in df.columns:
            series = df[col]

            # Create subplots
            fig, (ax1, ax2) = plt.subplots(1, 2)
            width, _ = fig.get_size_inches()
            fig.set_size_inches(width, 5)

            plot_acf(series, ax=ax1)
            plot_pacf(series, ax=ax2)

            # Get the current y-axis limits
            ymin, ymax = ax1.get_ylim()
            # Set new limits - adding a bit of space
            ax1.set_ylim([ymin, ymax + 0.05 * (ymax - ymin)])

            ymin, ymax = ax2.get_ylim()
            ax2.set_ylim([ymin, ymax + 0.05 * (ymax - ymin)])

            ax1.tick_params(axis="both", labelsize=18)
            ax2.tick_params(axis="both", labelsize=18)
            ax1.set_title(f"ACF for {col}", weight="bold", fontsize=20)
            ax2.set_title(f"PACF for {col}", weight="bold", fontsize=20)
            ax1.set_xlabel("Lag", fontsize=18)
            ax2.set_xlabel("Lag", fontsize=18)
            figures.append(
                Figure(
                    for_object=self,
                    key=f"{self.key}:{col}",
                    figure=fig,
                )
            )

            # Do this if you want to prevent the figure from being displayed
            plt.close("all")

        return self.cache_results(figures=figures)
