# Copyright © 2023 ValidMind Inc. All rights reserved.

import matplotlib.pyplot as plt
import seaborn as sns

from validmind.vm_models import Figure, Metric


class ScatterPlot(Metric):
    """
    **Purpose**: The purpose of this metric, ScatterPlot, is to provide a visual analysis of the input dataset by
    generating a scatter plot matrix. This scatter plot matrix includes all columns (or features) in the dataset and is
    intended to reveal relationships, patterns, or outliers among different features. This visual representation can
    give both qualitative and quantitative insights into the multidimensional relationships in the dataset, which can
    be useful in understanding the suitability and effectiveness of selected features for model training.

    **Test Mechanism**: The ScatterPlot class utilizes the seaborn library to generate the scatter plot matrix. It
    first retrieves all columns from the input dataset, ensures that the specified columns exist in the dataset, and
    then creates a pairplot for these columns. It uses the kernel density estimate (kde) for a smoother, univariate
    distribution along the diagonal of the grid. The final plot is stored in an array of Figure objects, each
    encapsulating matplotlib figure instance for storage and later usage.

    **Signs of High Risk**: Signs of potential risk could be the appearance of non-linear or random patterns across
    different feature pairs indicating complex relationships not suitable for linear assumptions. Additionally, showing
    no clear patterns or clusters might indicate weak or non-existent correlations among features, posing a challenge
    for certain model types. Visualization of outliers may also be a sign of risk as outliers can negatively impact
    model performance.

    **Strengths**: The utilization of a scatter plot matrix for data analysis provides various strengths:
    1. It provides visual insight into the multidimensional relationships among multiple features.
    2. It helps to identify trends, correlations, and outliers that could impact model performance.
    3. As a diagnostic tool, it can suggest whether certain assumptions taken during model creation (like linearity)
    are valid.
    4. It is versatile and can be used for both classification and regression type tasks.

    **Limitations**: Scatter plot matrices, however, also present a few limitations:
    1. They can become highly cluttered and difficult to interpret as the number of features (columns) increases.
    2. They primarily reveal pairwise relationships and might not expose complex interactions involving more than two
    features.
    3. Since it is a visual tool, quantitative analysis might not be precise.
    4. Outliers, if not clearly visible, can be overlooked, affecting model performance.
    5. It assumes that the dataset fits into memory, which might not be the case for extremely large datasets.
    """

    name = "scatter_plot"
    required_inputs = ["dataset", "dataset.target_column"]
    metadata = {
        "task_types": ["classification", "regression"],
        "tags": ["tabular_data", "visualization"],
    }

    def run(self):
        columns = list(self.dataset.df.columns)

        df = self.dataset.df[columns]

        if not set(columns).issubset(set(df.columns)):
            raise ValueError("Provided 'columns' must exist in the dataset")

        sns.pairplot(data=df, diag_kind="kde")

        # Get the current figure
        fig = plt.gcf()

        figures = []
        figures.append(
            Figure(
                for_object=self,
                key=self.key,
                figure=fig,
            )
        )

        plt.close("all")

        return self.cache_results(
            figures=figures,
        )
