import matplotlib.pyplot as plt
import numpy as np

from dataclasses import dataclass
from validmind.vm_models import Figure, Metric


@dataclass
class BivariateBarPlots(Metric):
    """
    Generates a visual analysis of categorical data by plotting bivariate bar plots.
    The input dataset and variable_pairs are required.
    """

    name = "bivariate_bar_plots"
    required_context = ["dataset"]
    default_params = {"variable_pairs": None, "loan_status_filter": None}

    def plot_bivariate_bar(self, variable_pairs, loan_status_filter):
        figures = []
        for x, hue in variable_pairs.items():
            df = self.dataset.df
            if loan_status_filter:
                df = df[df["loan_status"].isin(loan_status_filter)]

            means = df.groupby([x, hue])["loan_status"].mean().unstack().reset_index()
            hue_categories = means.columns[1:]

            n = len(hue_categories)
            width = 1 / (n + 1)

            plt.figure()

            color_palette = {
                category: color
                for category, color in zip(
                    hue_categories, plt.cm.get_cmap("tab10").colors
                )
            }

            for i, hue_category in enumerate(hue_categories):
                plt.bar(
                    np.arange(len(means)) + i * width,
                    means[hue_category],
                    color=color_palette[hue_category],
                    alpha=0.7,
                    label=hue_category,
                    width=width,
                )

            plt.title(x + " by " + hue)
            plt.xlabel(x)
            plt.ylabel("Loan Default Ratio")
            plt.xticks(ticks=np.arange(len(means)), labels=means[x], rotation=90)
            plt.legend()
            plt.show()

            figures.append(
                Figure(
                    for_object=self, key=f"{self.key}:{x}_{hue}", figure=plt.figure()
                )
            )

        plt.close("all")

        return figures

    def run(self):
        variable_pairs = self.params["variable_pairs"]
        loan_status_filter = self.params["loan_status_filter"]

        figures = self.plot_bivariate_bar(variable_pairs, loan_status_filter)

        return self.cache_results(figures=figures)
