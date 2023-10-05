# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import matplotlib.pyplot as plt
import seaborn as sns

from validmind.vm_models import Figure, Metric


@dataclass
class BivariateScatterPlots(Metric):
    """
    Generates bivariate scatterplots to visually inspect relationships between pairs of predictor variables in machine
    learning classification tasks.

    **Purpose**: This metric is intended for visual inspection and monitoring of relationships between pairs of
    variables in a machine learning model targeting classification tasks. It is especially useful for understanding how
    predictor variables (features) behave in relation to each other and how they are distributed for different classes
    of the target variable, which could inform feature selection, model-building strategies, and even alert to possible
    biases and irregularities in the data.

    **Test Mechanism**: This metric operates by creating a scatter plot for each pair of the selected features in the
    dataset. If the parameters "features_pairs" are not specified, an error will be thrown. The metric offers
    flexibility by allowing the user to filter on a specific target class - specified by the "target_filter" parameter
    - for more granified insights. Each scatterplot is then color-coded based on the category of the target variable
    for better visual differentiation. The seaborn scatterplot library is used for generating the plots.

    **Signs of High Risk**:
    - Visual patterns which might suggest non-linear relationships, substantial skewness, multicollinearity,
    clustering, or isolated outlier points in the scatter plot.
    - Such issues could affect the assumptions and performance of some models, especially the ones assuming linearity
    like linear regression or logistic regression.

    **Strengths**:
    - Scatterplots are simple and intuitive for users to understand, providing a visual tool to pinpoint complex
    relationships between two variables.
    - They are useful for outlier detection, identification of variable associations and trends, including non-linear
    patterns which can be overlooked by other linear-focused metrics or tests.
    - The implementation also supports visualizing binary or multi-class classification datasets.

    **Limitations**:
    - Scatterplots are limited to bivariate analysis - the relationship of two variables at a time - and might not
    reveal the full picture in higher dimensions or where interactions are present.
    - They are not ideal for very large datasets as points will overlap and render the visualization less informative.
    - Scatterplots are more of an exploratory tool rather than a formal statistical test, so they don't provide any
    quantitative measure of model quality or performance.
    - Interpretation of scatterplots relies heavily on the domain knowledge and judgment of the viewer, which can
    introduce subjective bias.
    """

    name = "bivariate_scatter_plots"
    required_inputs = ["dataset"]
    default_params = {"features_pairs": None, "target_filter": None}
    metadata = {
        "task_types": ["classification"],
        "tags": [
            "tabular_data",
            "categorical_data",
            "binary_classification",
            "multiclass_classification",
            "visualization",
        ],
    }

    def plot_bivariate_scatter(self, features_pairs, target_filter):
        status_var = self.dataset.target_column
        figures = []
        for x, y in features_pairs.items():
            df = self.dataset.df
            if target_filter is not None:
                df = df[df[status_var] == target_filter]

            plt.figure()

            # Scatterplot using seaborn, with color variation based on 'status_var'
            # Create color mapping with rgba values, last value is alpha (transparency)
            palette = {0: (0.8, 0.8, 0.8, 0.8), 1: "tab:red"}
            plot = sns.scatterplot(
                data=df, x=x, y=y, hue=status_var, palette=palette, alpha=1
            )

            # Change legend labels
            legend_labels = [
                "Category 1" if t.get_text() == "1" else "Category 2"
                for t in plot.legend_.texts[1:]
            ]
            plot.legend_.texts[1:] = legend_labels

            plt.title(x + " and " + y)
            plt.xlabel(x)
            plt.ylabel(y)
            plt.show()

            figures.append(
                Figure(for_object=self, key=f"{self.key}:{x}_{y}", figure=plt.figure())
            )

        plt.close("all")

        return figures

    def run(self):
        features_pairs = self.params["features_pairs"]
        target_filter = self.params["target_filter"]

        if features_pairs is None:
            raise ValueError(
                "The features_pairs parameter is required for this metric."
            )

        figures = self.plot_bivariate_scatter(features_pairs, target_filter)

        return self.cache_results(figures=figures)
