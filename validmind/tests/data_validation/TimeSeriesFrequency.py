# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import pandas as pd
import plotly.graph_objects as go

from validmind.vm_models import (
    Figure,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    ThresholdTest,
    ThresholdTestResult,
)


@dataclass
class TimeSeriesFrequency(ThresholdTest):
    """
    **Purpose**: The TimeSeriesFrequency test is designed to evaluate the consistency in the frequency of data points
    in a time series dataset. The metric inspects the intervals or duration between each data point in the dataset and
    helps to determine if there is a fixed pattern (e.g. daily, weekly, monthly). This is important in time-series
    analysis, as irregularities in the data frequency can lead to erroneous results or may affect the model's ability
    to identify trends and patterns.

    **Test Mechanism**: The test examines the dataframe index to verify that it's in datetime format. Afterwards, it
    identifies the frequency of each data series in the dataframe by employing pandas' `infer_freq` method, which
    infers the frequency of a given time series. It returns the frequency string as well as a dictionary that matches
    frequency strings to their respective labels. The frequencies of all variables in the dataset are then compared. If
    they all share one common frequency, the test passes; otherwise, it fails. A frequency plot that graphically
    depicts the time differences between consecutive entries in the dataframe index is also generated using Plotly.

    **Signs of High Risk**: One significant sign of high risk is if the test fails, i.e., when there are multiple
    unique frequencies in the dataset. This could indicate irregular time intervals between observations, which could
    disrupt pattern recognition or trend analysis that the model is designed to conduct. Also, missing or null
    frequencies can signify data inconsistencies or gaps in the data collection process.

    **Strengths**: This test provides a systematic way to check and visually represent the consistency of data
    frequency in a time series dataset. It increases reliability of the model by asserting that the timing and
    consistency of the observations are in line with the requirements of time series analysis. The visual plot
    generated provides an intuitive representation of the dataset's frequency distribution, catering to visual learners
    and aiding explanation and interpretation.

    **Limitations**: This test is restricted to time-series datasets; hence, it is not applicable to all kinds of
    datasets. Moreover, the `infer_freq` method may not always infer the correct frequency in the presence of missing
    or irregular data points. Lastly, in some cases, mixed frequencies might be acceptable depending on the context or
    the model being developed, but this test considers them a failing condition.
    """

    category = "data_quality"
    name = "time_series_frequency"
    required_inputs = ["dataset"]
    metadata = {
        "task_types": ["regression"],
        "tags": ["time_series_data"],
    }

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
            ThresholdTestResult(
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
                label = freq_dict.get(freq, freq)
            else:
                label = None

            frequencies.append({"Variable": column, "Frequency": label})

        freq_df = pd.DataFrame(frequencies)

        return freq_df

    def _frequency_plot(self, df):
        """
        Creates a frequency plot of time differences between consecutive entries in a DataFrame index using Plotly.
        Args:
        df (pandas.DataFrame): The input DataFrame.
        Returns:
        A Plotly Figure object representing the frequency plot of time differences.
        """
        # Calculate the time differences between consecutive entries
        time_diff = df.index.to_series().diff().dropna()

        # Convert the time differences to a suitable unit (e.g., days)
        time_diff_days = time_diff.dt.total_seconds() / (60 * 60 * 24)

        # Create a Plotly histogram
        fig = go.Figure(data=[go.Histogram(x=time_diff_days, nbinsx=50)])
        fig.update_layout(
            title="Histogram of Time Differences (Days)",
            xaxis_title="Days",
            yaxis_title="Frequency",
            font=dict(size=16),
        )

        return fig
