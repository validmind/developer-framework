import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from dataclasses import dataclass
from validmind.vm_models import Figure, Metric


@dataclass
class IQROutliersPlots(Metric):
    """
    Generates a visual analysis of the outliers for numeric variables.
    The input dataset is required.
    """

    name = "iqr_outliers_plots"
    required_context = ["dataset"]
    default_params = {"threshold": 1.5, "num_features": None}

    def run(self):
        df = self.dataset.df
        num_features = self.params["num_features"]
        threshold = self.params["threshold"]

        # If num_features is None, use all numeric columns.
        # Otherwise, only use the columns provided in num_features.
        if num_features is None:
            df = df.select_dtypes(include=[np.number])
        else:
            df = df[num_features]

        return self.detect_and_visualize_outliers(df, threshold)

    @staticmethod
    def compute_outliers(series, threshold=1.5):
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        return series[(series < lower_bound) | (series > upper_bound)]

    def detect_and_visualize_outliers(self, df, threshold):
        num_cols = df.columns.tolist()

        figures = []

        for col in num_cols:
            fig, ax = plt.subplots(1, 2)

            # Compute outliers
            outliers = self.compute_outliers(df[col], threshold)

            # Plot the boxplot without outliers
            sns.boxplot(x=df[col], color="skyblue", orient="h", fliersize=0, ax=ax[0])

            # Overplot the outliers
            ax[0].scatter(outliers, [0.0] * len(outliers), color="r", alpha=0.5)

            # Add title and legend
            ax[0].set_title(f"Boxplot for {col}")
            ax[0].set_xlabel("")  # Remove x label
            ax[0].set_yticks([])  # Remove y ticks
            red_dot = plt.Line2D([], [], color="r", marker="o", linestyle="None")
            ax[0].legend([red_dot], ["Outliers"])

            # Plot the histogram
            sns.histplot(df[col].dropna(), kde=True, ax=ax[1])
            ax[1].set_title(f"Histogram for {col}")
            ax[1].set_xlabel("")
            ax[1].set_ylabel("")

            plt.tight_layout()
            figures.append(Figure(for_object=self, key=f"{self.key}:{col}", figure=fig))

            plt.close("all")

        return self.cache_results(figures=figures)
