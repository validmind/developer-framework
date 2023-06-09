import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from validmind.vm_models import Figure, Metric


class TabularNumericalHistograms(Metric):
    """
    Generates a visual analysis of numerical data by plotting the histogram.
    The input dataset can have multiple numerical variables if necessary.
    In this case, we produce a separate plot for each numerical variable.
    """

    name = "tabular_numerical_histograms"
    required_context = ["dataset"]

    def run(self):
        df = self.dataset.df

        # Extract numerical columns from the dataset
        numerical_columns = df.select_dtypes(include=[np.number]).columns.tolist()

        if len(numerical_columns) == 0:
            raise ValueError("No numerical columns found in the dataset")

        figures = []
        for col in numerical_columns:
            plt.figure()
            fig, _ = plt.subplots()
            ax = sns.histplot(data=df, x=col, kde=True)
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
