# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

"""
Metrics functions for any Pandas-compatible datasets
"""


import plotly.express as px
from langdetect import LangDetectException, detect

from validmind import tags, tasks


@tags("nlp", "text_data", "visualization")
@tasks("text_classification", "text_summarization")
def LanguageDetection(dataset):
    """
    Assesses the diversity of languages in a textual dataset by detecting and visualizing the distribution of languages.

    ### Purpose

    The Language Detection test aims to identify and visualize the distribution of languages present within a textual
    dataset. This test helps in understanding the diversity of languages in the data, which is crucial for developing
    and validating multilingual models.

    ### Test Mechanism

    This test operates by:

    - Checking if the dataset has a specified text column.
    - Using a language detection library to determine the language of each text entry in the dataset.
    - Generating a histogram plot of the language distribution, with language codes on the x-axis and their frequencies
    on the y-axis.

    If the text column is not specified, a ValueError is raised to ensure proper dataset configuration.

    ### Signs of High Risk

    - A high proportion of entries returning "Unknown" language codes.
    - Detection of unexpectedly diverse or incorrect language codes, indicating potential data quality issues.
    - Significant imbalance in language distribution, which might indicate potential biases in the dataset.

    ### Strengths

    - Provides a visual representation of language diversity within the dataset.
    - Helps identify data quality issues related to incorrect or unknown language detection.
    - Useful for ensuring that multilingual models have adequate and appropriate representation from various languages.

    ### Limitations

    - Dependency on the accuracy of the language detection library, which may not be perfect.
    - Languages with similar structures or limited text length may be incorrectly classified.
    - The test returns "Unknown" for entries where language detection fails, which might mask underlying issues with
    certain languages or text formats.
    """
    # check text column
    if not dataset.text_column:
        raise ValueError("Please set text_column name in the Validmind Dataset object")

    # Function to detect language
    def detect_language(text):
        try:
            return detect(text)
        except LangDetectException:
            return "Unknown"  # Return 'Unknown' if language detection fails

    # Applying the language detection function to each text entry
    languages = dataset.df[dataset.text_column].apply(detect_language)
    fig = px.histogram(
        languages,
        x=languages,
        title="Language Distribution",
        labels={"x": "Language Codes"},
    )

    return fig
