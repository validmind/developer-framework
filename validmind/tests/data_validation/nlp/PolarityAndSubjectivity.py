# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial


import pandas as pd
import plotly.express as px
from textblob import TextBlob

from validmind import tags, tasks


@tags("nlp", "text_data", "data_validation")
@tasks("nlp")
def PolarityAndSubjectivity(dataset):
    """
    Analyzes the polarity and subjectivity of text data within a dataset.

    This method processes a dataset containing textual data to compute the polarity and
    subjectivity scores using TextBlob, and returns a Plotly scatter plot visualizing
    these scores.

    Args:
        dataset (Dataset): A dataset object which must have a `df` attribute (a pandas DataFrame)
            and a `text_column` attribute indicating the name of the column containing text.

    Returns:
        plotly.graph_objs._figure.Figure: A Plotly scatter plot of polarity vs subjectivity.
    """

    # Function to calculate sentiment and subjectivity
    def analyze_sentiment(text):
        analysis = TextBlob(text)
        return analysis.sentiment.polarity, analysis.sentiment.subjectivity

    data = pd.DataFrame()
    # Apply the function to each row
    data[["polarity", "subjectivity"]] = dataset.df[dataset.text_column].apply(
        lambda x: pd.Series(analyze_sentiment(x))
    )

    # Create a Plotly scatter plot
    fig = px.scatter(
        data, x="polarity", y="subjectivity", title="Polarity vs Subjectivity"
    )
    fig.update_traces(textposition="top center")
    fig.update_layout(xaxis_title="Polarity", yaxis_title="Subjectivity")

    return fig
