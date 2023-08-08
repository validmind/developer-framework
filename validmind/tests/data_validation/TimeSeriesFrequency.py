# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from validmind.vm_models import (
    Figure,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    TestResult,
    ThresholdTest,
)


@dataclass
class TimeSeriesFrequency(ThresholdTest):
    """
    Test that detect frequencies in the data
    """

    category = "data_quality"
    name = "time_series_frequency"
    required_context = ["dataset"]

    def summary(self, results, all_passed):
        """
        Example output:
        [
            {
                "values": {
                    "Variable": ["MORTGAGE30US", "GS10", "FEDFUNDS"],
                    "Frequency": ["Monthly", "Monthly", "Monthly"]
                },
                "passed": true
            }
        ]
        """
        first_result = results[0]
        variables = first_result.values["Variable"]
        frequencies = first_result.values["Frequency"]

        return ResultSummary(
            results=[
                ResultTable(
                    data=pd.DataFrame(
                        {"Variable": variables, "Frequency": frequencies}
                    ),
                    metadata=ResultTableMetadata(
                        title="Frequency of Time Series Variables"
                    ),
                )
            ]
        )

    def run(self):
        # Check if the index of dataframe is datetime
        is_datetime = pd.api.types.is_datetime64_any_dtype(self.dataset.df.index)
        if not is_datetime:
            raise ValueError("Dataset must be provided with datetime index")

        freq_df = self._identify_frequencies(self.dataset.df)
        n_frequencies = len(freq_df["Frequency"].unique())
        test_results = [
            TestResult(
                passed=n_frequencies == 1,
                values=freq_df.to_dict(orient="list"),
            )
        ]
        fig_frequency = self._frequency_plot(self.dataset.df)
        test_figures = []
        test_figures.append(
            Figure(
                for_object=self,
                key=f"{self.name}:frequencyplot",
                figure=fig_frequency,
                metadata={"type": "frequencyplot"},
            )
        )
        return self.cache_results(
            test_results,
            passed=all([r.passed for r in test_results]),
            figures=test_figures,
        )

    def _identify_frequencies(self, df):
        """
        Identify the frequency of each series in the DataFrame.
        :param df: Time-series DataFrame
        :return: DataFrame with two columns: 'Variable' and 'Frequency'
        """
        frequencies = []
        freq_dict = {
            "S": "Second",
            "T": "Minute",
            "min": "Minute",
            "H": "Hourly",
            "D": "Daily",
            "B": "Business day",
            "W": "Weekly",
            "MS": "Monthly",
            "M": "Monthly",
            "Q": "Quarterly",
            "A": "Yearly",
            "Y": "Yearly",
        }

        for column in df.columns:
            series = df[column].dropna()
            if not series.empty:
                freq = pd.infer_freq(series.index)
                label = freq_dict[freq] if freq in freq_dict.keys() else freq
            else:
                label = None

            frequencies.append({"Variable": column, "Frequency": label})

        freq_df = pd.DataFrame(frequencies)

        return freq_df

    def _frequency_plot(self, df):
        """
        Creates a frequency plot of time differences between consecutive entries in a DataFrame index.
        Args:
        df (pandas.DataFrame): The input DataFrame.
        Returns:
        A matplotlib Figure object representing the frequency plot of time differences.
        """

        # Calculate the time differences between consecutive entries
        time_diff = df.index.to_series().diff().dropna()

        # Convert the time differences to a suitable unit (e.g., days)
        time_diff_days = time_diff.dt.total_seconds() / (60 * 60 * 24)

        # Create a DataFrame with the time differences
        time_diff_df = pd.DataFrame({"Time Differences (Days)": time_diff_days})
        fig, ax = plt.subplots()
        # Plot the frequency distribution of the time differences
        sns.histplot(data=time_diff_df, bins=50, kde=False, ax=ax)

        plt.xticks(rotation=45, fontsize=18)
        plt.yticks(rotation=45, fontsize=18)
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.set_title(
            "Histogram of Time Differences (Days)",
            weight="bold",
            fontsize=20,
        )

        # Do this if you want to prevent the figure from being displayed
        plt.close("all")

        return fig
