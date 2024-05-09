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
