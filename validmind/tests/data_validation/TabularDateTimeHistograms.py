# Copyright © 2023 ValidMind Inc. All rights reserved.

import matplotlib.pyplot as plt
import seaborn as sns

from validmind.vm_models import Figure, Metric


class TabularDateTimeHistograms(Metric):
    """
    **Purpose**: The purpose of `TabularDateTimeHistograms` metric is to visually analyze the datetime data within a
    given machine learning model dataset. It plots histograms for differences between consecutive dates across all
    datetime variables present in the dataset. This assists in the inspection and understanding of the frequency
    distribution of time intervals in the dataset, which can be useful in analysing patterns in the data over time.

    **Test Mechanism**: The test works by first extracting all the datetime columns from the dataset. For each of these
    datetime columns, the test then calculates the difference between consecutive dates and converts these differences
    into days. Zero values are filtered out to only plot data points that represent some amount of day difference.
    Histograms are created for each column using seaborn's histplot function and displayed with relevant labels. The
    histograms provide a visual representation of the frequency of occurrences of different day intervals in the
    dataset.

    **Signs of High Risk**: One high risk associated with this test is if no datetime columns are found in the data
    set, it would result in a ValueError. A potential sign of risk could also be a skewed or highly irregular
    distribution in the histogram, indicating potential issues in the data such as incorrect timestamps or anomalies.

    **Strengths**: The strengths of this metric include its ability to visually represent frequency distributions of
    time interval changes in the dataset, aiding in understanding inherent patterns. The histogram plots can also
    assist in identifying potential outliers and anomalies in the data, and can help assess data quality. The metric is
    applicable to various task types like classification, regression, and works with multiple datetime variables if
    available.

    **Limitations**: Limitations of using this metric mainly stem from its reliance on visual interpretation of the
    data. The metric does not provide a quantitative evaluation of the model and may not capture complexities or
    multidimensional patterns in data. The test can only be applied to datasets with datetime columns, and would fail
    in absence of them. Interpretation of the generated histograms also depends on the domain knowledge and experience
    of the investigator.
    """

    name = "tabular_datetime_histograms"
    required_inputs = ["dataset"]

    metadata = {
        "task_types": ["classification", "regression"],
        "tags": ["tabular_data", "visualization"],
    }

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
