# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from validmind.vm_models import Figure, Metric


@dataclass
class PiTPDHistogram(Metric):
    """
    **Purpose**: The PiTPDHistogram metric is used to compute the Probability of Default (PD) for each instance in both
    the training and test datasets in order to evaluate the model's performance in credit risk estimation. The PD is
    examined at a specific point in time (PiT). The resulting distributions for the actual and predicted default
    classes are then visualized in a histogram, making it easier to understand the model's prediction accuracy.

    **Test Mechanism**: This metric sorts instances into either observed (actual) or predicted default classes, with a
    default being represented by '1' and non-default as '0'. Using these classes, the probability of default is
    computed for each instance and plotted in a histogram. Two histograms are generated: one for the observed defaults
    and another one for the predicted defaults. If the distribution of predicted defaults closely matches the
    distribution of observed defaults, this would indicate good model performance.

    **Signs of High Risk**: Discrepancies between the two histograms (observed and predicted defaults) would suggest
    model risk. This may include differences in the shapes of the histograms, divergences in the spread of default
    probabilities, or significant mismatches in the peak default probabilities. These disparities signal that the model
    may not be accurately predicting defaults, which could pose a high risk especially in the field of credit risk
    analysis.

    **Strengths**: This metric excels in its visual interpretation of model performance. By comparing two histograms
    side by side, it allows for a convenient comparison between the observed and predicted defaults. This visualization
    can reveal model biases and illuminate areas where the model's performance may fall short, which might not be as
    evident in purely numerical evaluations or more complex visualization measures.

    **Limitations**: Despite its strengths, the PiTPDHistogram metric is largely interpretive and subjective.
    Determining risk based on visual discrepancies requires a certain level of human judgement and may vary between
    different analysts. If used solely, this metric might overlook other nuances in model performance that are better
    captured by more quantitative or diversified metrics. Furthermore, the information provided is limited to a
    specific point in time, which might not fully reflect the model's performance over different periods or under
    changing conditions.
    """

    name = "pit_pd_histogram"
    required_context = ["dataset"]
    default_params = {"title": "Histogram of PiT Probability of Default"}
    metadata = {
        "task_types": ["classification"],
        "tags": ["tabular_data", "visualization", "credit_risk"],
    }

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
