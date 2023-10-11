# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from validmind.vm_models import Figure, Metric


@dataclass
class PiTPDHistogram(Metric):
    """
    Assesses credit risk prediction accuracy of a model by comparing actual and predicted defaults at a chosen point in
    time.

    **Purpose**: The PiTPDHistogram metric uses Probability of Default (PD) calculations for individual instances
    within both training and test data sets in order to assess a model's proficiency in predicting credit risk. A
    distinctive point in time (PiT) is chosen for these PD calculations, and the results for both actual and predicted
    defaults are presented in histogram form. This visualization is aimed at simplifying the understanding of model
    prediction accuracy.

    **Test Mechanism**: Instances are categorized into two groups - those for actual defaults and those for predicted
    defaults, with '1' indicating a default and '0' indicating non-default. PD is calculated for each instance, and
    based on these calculations, two histograms are created, one for actual defaults and one for predicted defaults. If
    the predicted default frequency matches that of the actual defaults, the model's performance is deemed effective.

    **Signs of High Risk**:
    - Discrepancies between the actual and predicted default histograms may suggest model inefficiency.
    - Variations in histogram shapes or divergences in default probability distributions could be concerning.
    - Significant mismatches in peak default probabilities could also be red flags.

    **Strengths**:
    - Provides a visual comparison between actual and predicted defaults, aiding in the understanding of model
    performance.
    - Helps reveal model bias and areas where the model's performance could be improved.
    - Easier to understand than purely numerical evaluations or other complicated visualization measures.

    **Limitations**:
    - The metric remains largely interpretive and subjective, as the extent and relevance of visual discrepancies often
    need to be evaluated manually, leading to potentially inconsistent results across different analyses.
    - This metric alone may not capture all the complexities and nuances of model performance.
    - The information provided is limited to a specific point in time, potentially neglecting the model's performance
    under various circumstances or different time periods.
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
