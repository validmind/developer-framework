# Copyright © 2023 ValidMind Inc. All rights reserved.

import matplotlib.pyplot as plt
import seaborn as sns

from validmind.vm_models import Figure, Metric


class TabularDateTimeHistograms(Metric):
    """
    Generates a visual analysis of datetime data by plotting histograms of
    differences between consecutive dates. The input dataset can have multiple
    datetime variables if necessary. In this case, we produce a separate plot
    for each datetime variable.
    """

    name = "tabular_datetime_histograms"
    required_context = ["dataset"]

    def run(self):
        df = self.dataset.df

        # Extract datetime columns from the dataset
        datetime_columns = df.select_dtypes(include=["datetime64"]).columns.tolist()

        if len(datetime_columns) == 0:
            raise ValueError("No datetime columns found in the dataset")

        figures = []
        for col in datetime_columns:
            plt.figure()
            fig, _ = plt.subplots()

            # Calculate the difference between consecutive dates and convert to days
            date_diffs = df[col].sort_values().diff().dt.days.dropna()

            # Filter out 0 values
            date_diffs = date_diffs[date_diffs != 0]

            ax = sns.histplot(date_diffs, kde=False, bins=30)
            plt.title(f"{col}", weight="bold", fontsize=20)

            plt.xticks(fontsize=18)
            plt.yticks(fontsize=18)
            ax.set_xlabel("Days Between Consecutive Dates", fontsize=18)
            ax.set_ylabel("Frequency", fontsize=18)
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
