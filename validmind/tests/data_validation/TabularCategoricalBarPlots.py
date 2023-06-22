import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from validmind.vm_models import Figure, Metric


class TabularCategoricalBarPlots(Metric):
    """
    Generates a visual analysis of categorical data by plotting bar plots.
    The input dataset can have multiple categorical variables if necessary.
    In this case, we produce a separate plot for each categorical variable.
    """

    name = "tabular_categorical_bar_plots"
    required_context = ["dataset"]

    def run(self):
        df = self.dataset.df

        # Extract categorical columns from the dataset
        categorical_columns = df.select_dtypes(include=[np.object]).columns.tolist()

        if len(categorical_columns) == 0:
            raise ValueError("No categorical columns found in the dataset")

        figures = []
        for col in categorical_columns:
            plt.figure()
            fig, _ = plt.subplots()
            ax = sns.countplot(data=df, x=col)
            plt.title(f"{col}", weight="bold", fontsize=20)

            plt.xticks(fontsize=18)
            plt.yticks(fontsize=18)
            ax.set_xlabel("")
            ax.set_ylabel("")
            figures.append(
                Figure(
                    for_object=self,
                    key=f"{self.key}:{col}",
                    figure=fig,
                )
            )

        plt.close("all")

        return self.cache_results(
            figures=figures,
        )
