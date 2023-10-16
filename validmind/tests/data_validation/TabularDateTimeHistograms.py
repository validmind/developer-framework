# Copyright © 2023 ValidMind Inc. All rights reserved.

import matplotlib.pyplot as plt
import seaborn as sns

from validmind.vm_models import Figure, Metric


class TabularDateTimeHistograms(Metric):
    """
    Generates histograms to provide graphical insight into the distribution of time intervals in model's datetime data.

    **Purpose**: The `TabularDateTimeHistograms` metric is designed to provide graphical insight into the distribution
    of time intervals in a machine learning model's datetime data. By plotting histograms of differences between
    consecutive date entries in all datetime variables, it enables an examination of the underlying pattern of time
    series data and identification of anomalies.

    **Test Mechanism**: This test operates by first identifying all datetime columns and extracting them from the
    dataset. For each datetime column, it next computes the differences (in days) between consecutive dates, excluding
    zero values, and visualizes these differences in a histogram. The seaborn library's histplot function is used to
    generate histograms, which are labeled appropriately and provide a graphical representation of the frequency of
    different day intervals in the dataset.

    **Signs of High Risk**:
    - If no datetime columns are detected in the dataset, this would lead to a ValueError. Hence, the absence of
    datetime columns signifies a high risk.
    - A severely skewed or irregular distribution depicted in the histogram may indicate possible complications with
    the data, such as faulty timestamps or abnormalities.

    **Strengths**:
    - The metric offers a visual overview of time interval frequencies within the dataset, supporting the recognition
    of inherent patterns.
    - Histogram plots can aid in the detection of potential outliers and data anomalies, contributing to an assessment
    of data quality.
    - The metric is versatile, compatible with a range of task types, including classification and regression, and can
    work with multiple datetime variables if present.

    **Limitations**:
    - A major weakness of this metric is its dependence on the visual examination of data, as it does not provide a
    measurable evaluation of the model.
    - The metric might overlook complex or multi-dimensional trends in the data.
    - The test is only applicable to datasets containing datetime columns and will fail if such columns are unavailable.
    - The interpretation of the histograms relies heavily on the domain expertise and experience of the reviewer.
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
