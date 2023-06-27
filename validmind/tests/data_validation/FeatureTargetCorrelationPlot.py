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
        features = (
            self.params["features"]
            if self.params["features"] is not None
            else self.dataset.df.columns
        )
        declutter = self.params["declutter"]
        fontsize = self.params["fontsize"]
        target_column = self.dataset.target_column

        figure = self.visualize_feature_target_correlation(
            features, target_column, declutter, fontsize
        )

        return self.cache_results(figures=figure)

    def visualize_feature_target_correlation(
        self, features, target_column, declutter, fontsize
    ):
        # Filter numerical features
        numerical_features = self.dataset.df.select_dtypes(include=["float64", "int64"])

        # Filter selected variables
        selected_features = numerical_features[features]

        # Perform check if all selected features are numerical
        if not set(features).issubset(selected_features.columns):
            raise ValueError("Selected features contain non-numerical columns.")

        # Add the target variable to the selected features DataFrame
        selected_features[target_column] = self.dataset.df[target_column]

        # Compute correlations with the target variable
        correlations = selected_features.corr()[target_column].drop(target_column)

        # Sort correlations in descending order
        correlations = correlations.sort_values(ascending=False)

        # Create the bar plot with adjusted width and ordered bars
        fig = plt.figure()
        ax = sns.barplot(
            x=correlations.values,
            y=correlations.index,
            palette="coolwarm_r",
            order=correlations.index,
        )
        plt.xticks(rotation=90, fontsize=fontsize)
        plt.yticks(fontsize=fontsize)

        plt.xlabel(None)
        plt.ylabel(None)
        plt.title(
            f"Correlation of Numerical Features vs Target Variable ({target_column})",
            fontsize=fontsize,
        )

        plt.tight_layout()

        if declutter:
            plt.ylabel(f"{len(correlations)} Numerical Features", fontsize=fontsize)
            ax.set_yticklabels([])
        else:
            for i, v in enumerate(correlations.values):
                ax.text(v + 0.01, i, str(round(v, 2)), va="center", fontsize=fontsize)

        plt.close("all")

        figure = Figure(for_object=self, key=self.key, figure=fig)
        return [figure]
