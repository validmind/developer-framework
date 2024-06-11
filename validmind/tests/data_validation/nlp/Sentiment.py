# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial


import matplotlib.pyplot as plt
import nltk
import seaborn as sns
from nltk.sentiment import SentimentIntensityAnalyzer

from validmind import tags, tasks


@tags("nlp", "text_data", "data_validation")
@tasks("nlp")
def Sentiment(dataset):
    """
    Analyzes the sentiment of text data within a dataset using the VADER sentiment analysis tool.

    This method initializes the VADER SentimentIntensityAnalyzer and applies it to each text entry
    in the specified column of the dataset's dataframe. It returns a KDE plot visualizing the distribution
    of sentiment scores across the dataset.

    Args:
        dataset (Dataset): A dataset object which must have a `df` attribute (a pandas DataFrame)
            and a `text_column` attribute indicating the name of the column containing text.

    Returns:
        matplotlib.figure.Figure: A KDE plot visualizing the distribution of sentiment scores.
    """
    nltk.download("vader_lexicon", quiet=True)
    # Initialize VADER
    sia = SentimentIntensityAnalyzer()

    # Function to get VADER sentiment scores
    def get_vader_sentiment(text):
        sentiment_score = sia.polarity_scores(text)
        return sentiment_score["compound"]

    # Apply the function to each row
    vader_sentiment = dataset.df[dataset.text_column].apply(get_vader_sentiment)

    fig = plt.figure()
    ax = sns.kdeplot(
        x=vader_sentiment,
        fill=True,
        common_norm=False,
        palette="crest",
        alpha=0.5,
        linewidth=0,
    )
    ax.set_title(f"Sentiment score of {dataset.text_column} ")
    ax.set_xlabel("Sentiment score")

    plt.close("all")

    return fig
