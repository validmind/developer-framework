# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass
import matplotlib.pyplot as plt
import seaborn as sns

from validmind.logging import get_logger
from validmind.vm_models import Figure, Metric

logger = get_logger(__name__)


@dataclass
class RegressionFeatureSignificance(Metric):
    """
    This metric creates a plot of p-values for each model in the list.
    """

    name = "regression_feature_significance"
    default_params = {"fontsize": 10, "p_threshold": 0.05}

    def description(self):
        return """
        This section shows plots of feature p-values for each model.
        """

    def run(self):
        fontsize = self.params["fontsize"]
        p_threshold = self.params["p_threshold"]

        # Check models list is not empty
        if not self.models:
            raise ValueError("List of models must be provided in the models parameter")

        figures = self._plot_pvalues(self.models, fontsize, p_threshold)

        return self.cache_results(figures=figures)

    def _plot_pvalues(self, model_list, fontsize, p_threshold):
        # Initialize a list to store figures
        figures = []

        for i, fitted_model in enumerate(model_list):
            # Get the coefficients and p-values from the model
            coefficients = fitted_model.model.params
            pvalues = fitted_model.model.pvalues

            # Sort the variables by p-value in ascending order
            sorted_idx = pvalues.argsort()
            coefficients = coefficients.iloc[sorted_idx]
            pvalues = pvalues.iloc[sorted_idx]

            # Increase the height of the figure
            fig, ax = plt.subplots()

            # Create a horizontal bar plot with wider bars using Seaborn
            sns.barplot(x=pvalues, y=coefficients.index, ax=ax, color="skyblue")

            # Add a threshold line at p-value = p_threshold
            threshold_line = ax.axvline(x=p_threshold, color="red", linestyle="--")

            # Set labels and title
            ax.set_xlabel("P-value")
            ax.set_ylabel(None)
            ax.set_title(f"Feature Significance for Model {i + 1}")

            # Adjust the layout to prevent overlapping of variable names
            plt.tight_layout()

            # Set the fontsize of y-axis tick labels
            ax.set_yticklabels(ax.get_yticklabels(), fontsize=fontsize)

            # Add a legend for the threshold line
            legend_label = f"p_threshold {p_threshold}"
            ax.legend([threshold_line], [legend_label])

            # Add to the figures list
            figures.append(
                Figure(
                    for_object=self,
                    key=f"{self.key}:{i}",
                    figure=fig,
                    metadata={"model": str(fitted_model.model)},
                )
            )
            plt.close("all")
        return figures
