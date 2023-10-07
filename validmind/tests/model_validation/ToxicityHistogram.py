# Copyright © 2023 ValidMind Inc. All rights reserved.

import itertools
from dataclasses import dataclass

import evaluate
import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp

from validmind.vm_models import Figure, Metric


@dataclass
class ToxicityHistogram(Metric):
    """
    toxicity Histogram
    """

    name = "toxicity_histogram"
    default_params = {"text_columns": None}

    def description(self):
        return """
        Toxicity detailed description coming soon...!
        """

    def _get_datasets_from_model(self):
        # Check model attributes
        if not hasattr(self, "model"):
            raise AttributeError("The 'model' attribute is missing.")

        y_true = list(itertools.chain.from_iterable(self.model.y_test_true))
        y_pred = self.model.y_test_predict
        input_text = self.model.test_ds.df[self.model.test_ds.text_column]

        # Ensure consistency in lengths
        if not len(y_true) == len(y_pred) == len(input_text):
            raise ValueError(
                "Inconsistent lengths among input text, true summaries, and predicted summaries."
            )

        return input_text, y_true, y_pred

    def toxicity_histograms(self, df):
        """
        Compute toxicity scores for texts and then plot histograms for all columns of df.

        Parameters:
        - df (pd.DataFrame): The dataframe containing texts.
        """

        # Extract necessary parameters
        toxicity = evaluate.load("toxicity")

        # Get all columns of df
        text_columns = df.columns.tolist()

        # Determine the number of rows required based on the number of text columns
        num_rows = (len(text_columns) + 1) // 2  # +1 to handle odd number of columns

        # Create a subplot layout
        fig = sp.make_subplots(rows=num_rows, cols=2, subplot_titles=text_columns)

        subplot_height = 350  # Height of each subplot
        total_height = num_rows * subplot_height + 200  # 200 for padding, titles, etc.

        for idx, col in enumerate(text_columns, start=1):
            row = (idx - 1) // 2 + 1
            col_idx = (idx - 1) % 2 + 1  # to place subplots in two columns

            # Get list of texts from dataframe
            texts = df[col].tolist()

            # Compute toxicity for texts
            toxicity_scores = toxicity.compute(predictions=texts)["toxicity"]

            # Add traces to the corresponding subplot without legend
            fig.add_trace(
                go.Histogram(x=toxicity_scores, showlegend=False), row=row, col=col_idx
            )

            # Update xaxes and yaxes titles only for the first subplot
            if idx == 1:
                fig.update_xaxes(title_text="Toxicity Score", row=row, col=col_idx)
                fig.update_yaxes(title_text="Frequency", row=row, col=col_idx)

        # Update layout
        fig.update_layout(
            title_text="Histograms of Toxicity Scores", height=total_height
        )

        return fig

    def run(self):
        input_text, y_true, y_pred = self._get_datasets_from_model()

        # Create a DataFrame with results and user-friendly column names
        df = pd.DataFrame(
            {
                "Input Text": input_text,
                "Target Text": y_true,
                "Predicted Summaries": y_pred,
            }
        )

        fig = self.toxicity_histograms(df)

        return self.cache_results(
            figures=[Figure(for_object=self, key=self.key, figure=fig)]
        )
