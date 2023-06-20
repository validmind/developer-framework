import matplotlib.pyplot as plt
import seaborn as sns

from dataclasses import dataclass
from validmind.vm_models import Figure, Metric


@dataclass
class BivariateHistograms(Metric):
    """
    Generates a visual analysis of categorical data by plotting bivariate histograms.
    The input dataset and variable_pairs are required.
    """

    name = "bivariate_histograms"
    required_context = ["dataset"]
    default_params = {"variable_pairs": None, "status_filter": None}

    def plot_bivariate_histogram(self, variable_pairs, status_filter):
        status_var = self.dataset.target_column
        figures = []
        palette = {0: (0.5, 0.5, 0.5, 0.8), 1: "tab:red"}

        for x, y in variable_pairs.items():
            df = self.dataset.df
            if status_filter:
                df = df[df[status_var] == status_filter]

            fig, axes = plt.subplots(2, 1)

            for ax, var in zip(axes, [x, y]):
                for status, color in palette.items():
                    subset = df[df[status_var] == status]
                    sns.histplot(
                        subset[var],
                        ax=ax,
                        color=color,
                        edgecolor=None,
                        kde=True,
                        label="Category 1" if status else "Category 2",
                    )

                ax.set_title(f"Histogram of {var} by {status_var}")
                ax.set_xlabel(var)
                ax.legend()

            plt.tight_layout()
            plt.show()

            figures.append(
                Figure(for_object=self, key=f"{self.key}:{x}_{y}", figure=plt.figure())
            )

        plt.close("all")

        return figures

    def run(self):
        variable_pairs = self.params["variable_pairs"]
        status_filter = self.params["status_filter"]

        figures = self.plot_bivariate_histogram(variable_pairs, status_filter)

        return self.cache_results(figures=figures)
