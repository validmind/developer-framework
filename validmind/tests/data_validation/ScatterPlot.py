# Copyright © 2023 ValidMind Inc. All rights reserved.

import matplotlib.pyplot as plt
import seaborn as sns

from validmind.vm_models import Figure, Metric


class ScatterPlot(Metric):
    """
    Generates a visual analysis of data by plotting a scatter plot matrix for all columns
    in the dataset. The input dataset can have multiple columns (features) if necessary.
    """

    name = "scatter_plot"
    required_context = ["dataset", "dataset.target_column"]

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
