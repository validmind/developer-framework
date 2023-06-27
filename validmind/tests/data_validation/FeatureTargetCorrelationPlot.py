import matplotlib.pyplot as plt
import seaborn as sns

from dataclasses import dataclass
from validmind.vm_models import Figure, Metric


@dataclass
class FeatureTargetCorrelationPlot(Metric):
    """
    Generates a visual analysis of correlations between features and target by plotting a bar plot.
    The input dataset is required.
    """

    name = "feature_target_correlation_plot"
    required_context = ["dataset"]
    default_params = {"features": None, "declutter": False, "fontsize": 13}

    def run(self):
        features = self.params["features"]

        if features is None:
            features = self.dataset.df.columns.to_list()
        else:
            features = self.params["features"]

        declutter = self.params["declutter"]
        fontsize = self.params["fontsize"]
        target_column = self.dataset.target_column

        # Filter DataFrame based on features and target_column
        df = self.dataset.df[features + [target_column]]

        figure = self.visualize_feature_target_correlation(
            df, target_column, declutter, fontsize
        )

        return self.cache_results(figures=figure)

    def visualize_feature_target_correlation(
        self, df, target_column, declutter, fontsize
    ):
        # Compute correlations with the target variable
        correlations = df.corr().iloc[:, 0].drop(target_column)

        # Sort correlations in descending order based on the first column
        correlations = correlations.sort_values(ascending=False)

        # Create the bar plot with adjusted width and ordered bars
        fig, ax = plt.subplots()
        sns.barplot(
            x=correlations.values,
            y=correlations.index,
            palette="coolwarm_r",
            ax=ax,
        )

        plt.xticks(fontsize=fontsize)
        plt.yticks(fontsize=fontsize)

        plt.xlabel(None)
        plt.ylabel(None)
        plt.title(
            f"Correlation of Features vs Target Variable ({target_column})",
            fontsize=fontsize,
        )

        plt.tight_layout()

        if declutter:
            ax.set_yticklabels([])
            plt.ylabel(f"{len(correlations)} Features", fontsize=fontsize)
        else:
            for i, v in enumerate(correlations.values):
                ax.text(v + 0.01, i, str(round(v, 2)), va="center", fontsize=fontsize)

        plt.close("all")

        figure = Figure(for_object=self, key=self.key, figure=fig)
        return [figure]
