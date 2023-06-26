import matplotlib.pyplot as plt
import seaborn as sns

from dataclasses import dataclass
from validmind.vm_models import Figure, Metric


@dataclass
class MissingValuesBarPlot(Metric):
    """
    Generates a visual analysis of missing values by plotting bar plots with colored bars and a threshold line.
    The input dataset is required.
    """

    name = "missing_values_bar_plot"
    required_context = ["dataset"]
    default_params = {"threshold": 80, "xticks_fontsize": 8}

    def run(self):
        threshold = self.params["threshold"]
        xticks_fontsize = self.params["xticks_fontsize"]

        figure = self.visualize_missing_values(threshold, xticks_fontsize)

        return self.cache_results(figures=figure)

    def visualize_missing_values(self, threshold, xticks_fontsize):
        # Calculate the percentage of missing values in each column
        missing_percentages = (
            self.dataset.df.isnull().sum() / len(self.dataset.df)
        ) * 100

        # Sort missing value percentages in ascending order
        missing_percentages_sorted = missing_percentages.sort_values(ascending=True)

        # Create a list to store the colors for each bar
        colors = []

        # Iterate through the missing percentages and assign colors based on the threshold
        for value in missing_percentages_sorted.values:
            if value < threshold:
                colors.append("grey")
            else:
                colors.append("lightcoral")

        # Create a bar plot of missing value percentages
        fig = plt.figure()
        ax = sns.barplot(
            x=missing_percentages_sorted.index,
            y=missing_percentages_sorted.values,
            palette=colors,
        )

        plt.xticks(rotation=90, ha="right", fontsize=xticks_fontsize)
        plt.xlabel("Columns")
        plt.ylabel("Missing Value Percentage (%)")
        plt.title("Missing Values")

        # Update y-axis labels to show one decimal place
        ax.set_yticklabels(["{:.1f}%".format(x) for x in ax.get_yticks()])

        # Draw a red line at the specified threshold
        plt.axhline(
            y=threshold,
            color="red",
            linestyle="--",
            label="Threshold: {}%".format(threshold),
        )

        plt.legend()
        plt.tight_layout()
        plt.close("all")

        figure = Figure(for_object=self, key=self.key, figure=fig)
        return [figure]
