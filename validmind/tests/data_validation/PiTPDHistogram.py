# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from validmind.vm_models import Figure, Metric


@dataclass
class PiTPDHistogram(Metric):
    """
    Probability of Default (PD) Histogram
    """

    name = "pit_pd_histogram"
    required_context = ["dataset"]
    default_parameters = {"title": "Histogram of PiT Probability of Default"}

    def description(self):
        return """
        This metric calculates the probability of default (PD) for each instance in the training and test datasets,
        and creates histograms to visualize the distributions of PD for the positive and negative classes.
        """

    @staticmethod
    def plot_pit_pd_histogram(
        df,
        default_column,
        predicted_default_column,
        default_probabilities_column,
        title,
        point_in_time_date,
    ):
        fig = make_subplots(
            rows=1, cols=2, subplot_titles=("Observed Default", "Predicted Default")
        )

        observed_data_0 = df[df[default_column] == 0][default_probabilities_column]
        observed_data_1 = df[df[default_column] == 1][default_probabilities_column]

        predicted_data_0 = df[df[predicted_default_column] == 0][
            default_probabilities_column
        ]
        predicted_data_1 = df[df[predicted_default_column] == 1][
            default_probabilities_column
        ]

        fig.add_trace(
            go.Histogram(x=observed_data_0, opacity=0.75, name="Observed Default = 0"),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Histogram(x=observed_data_1, opacity=0.75, name="Observed Default = 1"),
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Histogram(
                x=predicted_data_0, opacity=0.75, name="Predicted Default = 0"
            ),
            row=1,
            col=2,
        )
        fig.add_trace(
            go.Histogram(
                x=predicted_data_1, opacity=0.75, name="Predicted Default = 1"
            ),
            row=1,
            col=2,
        )

        title += f" (PiT: {point_in_time_date.strftime('%d %b %Y')})"
        fig.update_layout(barmode="overlay", title_text=title)

        return fig

    def run(self):
        df = self.dataset
        default_column = self.params["default_column"]
        predicted_default_column = self.params["predicted_default_column"]
        default_probabilities_column = self.params["default_probabilities_column"]
        point_in_time_column = self.params["point_in_time_column"]

        title = self.params["title"]

        point_in_time_date = pd.to_datetime(df[point_in_time_column].iloc[0])

        fig = self.plot_pit_pd_histogram(
            df,
            default_column,
            predicted_default_column,
            default_probabilities_column,
            title,
            point_in_time_date,
        )

        return self.cache_results(
            metric_value={
                "prob_histogram": {
                    "observed_probs": list(
                        df[df[default_column] == 1][default_probabilities_column]
                    ),
                    "predicted_probs": list(
                        df[df[predicted_default_column] == 1][
                            default_probabilities_column
                        ]
                    ),
                },
            },
            figures=[
                Figure(
                    for_object=self,
                    key="prob_histogram",
                    figure=fig,
                )
            ],
        )