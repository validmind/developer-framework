# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import string
from dataclasses import dataclass

import matplotlib.pyplot as plt
import nltk
import pandas as pd
import plotly.express as px
from nltk.corpus import stopwords

from ....vm_models import Figure, Metric, VMDataset


@dataclass
class TextDescription(Metric):
    """
    Performs comprehensive textual analysis on a dataset using NLTK, evaluating various parameters and generating
    visualizations.

    **Purpose**: This test uses the TextDescription metric to conduct a comprehensive textual analysis of a given
    dataset. Various parameters such as total words, total sentences, average sentence length, total paragraphs, total
    unique words, most common words, total punctuations, and lexical diversity are evaluated. This metric aids in
    comprehending the nature of the text and evaluating the potential challenges that machine learning algorithms
    deployed for textual analysis, language processing, or summarization might face.

    **Test Mechanism**: The test works by parsing the given dataset and utilizes the NLTK (Natural Language Toolkit)
    library for tokenizing the text into words, sentences, and paragraphs. Subsequently, it processes the text further
    by eliminating stopwords declared in 'unwanted_tokens' and punctuations. Next, it determines parameters like the
    total count of words, sentences, paragraphs, punctuations alongside the average sentence length and lexical
    diversity. Lastly, the result from these calculations is condensed and scatter plots for certain variable
    combinations (e.g. Total Words vs Total Sentences, Total Words vs Total Unique Words) are produced, providing a
    visual representation of the text's structure.

    **Signs of High Risk**:
    - Anomalies or an increase in complexity within the lexical diversity results.
    - Longer sentences and paragraphs.
    - High uniqueness of words.
    - Presence of a significant amount of unwanted tokens.
    - Missing or erroneous visualizations.
     These signs suggest potential risk in text processing ML models, indicating that the ability of the model to
    absorb and process text could be compromised.

    **Strengths**:
    - An essential pre-processing tool, specifically for textual analysis in machine learning model data.
    - Provides a comprehensive breakdown of a text dataset, which aids in understanding both structural and vocabulary
    complexity.
    - Generates visualizations of correlations between chosen variables to further comprehend the text's structure and
    complexity.

    **Limitations**:
    - Heavy reliance on the NLTK library, restricting its use to only the languages that NLTK supports.
    - Limited customization capacity as the undesirable tokens and stop words are predefined.
    - Lacks the ability to consider semantics or grammatical complexities, which could be crucial aspects in language
    processing.
    - Assumes that the document is well-structured (includes sentences and paragraphs); therefore, unstructured or
    poorly formatted text may distort the results.
    """

    name = "text_description"
    required_inputs = ["dataset"]
    default_params = {
        "unwanted_tokens": {
            "s",
            "s'",
            "mr",
            "ms",
            "mrs",
            "dr",
            "'s",
            " ",
            "''",
            "dollar",
            "us",
            "``",
        },
        "num_top_words": 3,
        "lang": "english",
    }
    tasks = ["text_classification", "text_summarization"]
    tags = ["nlp", "text_data", "visualization"]

    def general_text_metrics(self, df, text_column):
        nltk.download("punkt", quiet=True)
        results = []

        for text in df[text_column]:
            sentences = nltk.sent_tokenize(text)
            words = nltk.word_tokenize(text)
            paragraphs = text.split("\n\n")

            total_words = len(words)
            total_sentences = len(sentences)
            avg_sentence_length = round(
                (
                    sum(len(sentence.split()) for sentence in sentences)
                    / total_sentences
                    if total_sentences
                    else 0
                ),
                1,
            )
            total_paragraphs = len(paragraphs)

            results.append(
                [total_words, total_sentences, avg_sentence_length, total_paragraphs]
            )

        return pd.DataFrame(
            results,
            columns=[
                "Total Words",
                "Total Sentences",
                "Avg Sentence Length",
                "Total Paragraphs",
            ],
        )

    def vocabulary_structure_metrics(
        self, df, text_column, unwanted_tokens, num_top_words, lang
    ):
        stop_words = set(word.lower() for word in stopwords.words(lang))
        unwanted_tokens = set(token.lower() for token in unwanted_tokens)

        results = []

        for text in df[text_column]:
            words = nltk.word_tokenize(text)

            filtered_words = [
                word
                for word in words
                if word.lower() not in stop_words
                and word.lower() not in unwanted_tokens
                and word not in string.punctuation
            ]

            total_unique_words = len(set(filtered_words))
            total_punctuations = sum(1 for word in words if word in string.punctuation)
            lexical_diversity = round(
                total_unique_words / len(filtered_words) if filtered_words else 0, 1
            )

            results.append([total_unique_words, total_punctuations, lexical_diversity])

        return pd.DataFrame(
            results,
            columns=["Total Unique Words", "Total Punctuations", "Lexical Diversity"],
        )

    # Wrapper function that combines the outputs
    def text_description_table(self, df, params):
        text_column = self.inputs.dataset.text_column
        unwanted_tokens = params["unwanted_tokens"]
        num_top_words = params["num_top_words"]
        lang = params["lang"]

        gen_metrics_df = self.general_text_metrics(df, text_column)
        vocab_metrics_df = self.vocabulary_structure_metrics(
            df, text_column, unwanted_tokens, num_top_words, lang
        )
        combined_df = pd.concat([gen_metrics_df, vocab_metrics_df], axis=1)

        return combined_df

    def run(self):
        # Enforce that text_column must be provided as part of the params
        if self.inputs.dataset.text_column is None:
            raise ValueError("A 'text_column' must be provided to run this test.")

        # Can only run this test if we have a Dataset object
        if not isinstance(self.inputs.dataset, VMDataset):
            raise ValueError("TextDescription requires a validmind Dataset object")

        df_text_description = self.text_description_table(
            self.inputs.dataset.df, self.params
        )

        # Define the combinations you want to plot
        combinations_to_plot = [
            ("Total Words", "Total Sentences"),
            ("Total Words", "Total Unique Words"),
            ("Total Sentences", "Avg Sentence Length"),
            ("Total Unique Words", "Lexical Diversity"),
        ]
        params = {"combinations_to_plot": combinations_to_plot}
        figures = self.text_description_plots(df_text_description, params)

        return self.cache_results(
            figures=figures,
        )

    # Function to plot scatter plots for specified combinations using Plotly
    def text_description_plots(self, df, params):
        combinations_to_plot = params["combinations_to_plot"]
        figures = []
        # Create hist plots for each column
        for i, column in enumerate(df.columns):
            fig = px.histogram(df, x=column)
            fig.update_layout(bargap=0.2)
            # Generate a unique key for each histogram using the column name and index
            histogram_key = f"{self.name}_histogram_{column}_{i}"
            figures.append(Figure(for_object=self, key=histogram_key, figure=fig))

        for j, (metric1, metric2) in enumerate(combinations_to_plot):
            fig = px.scatter(
                df, x=metric1, y=metric2, title=f"Scatter Plot: {metric1} vs {metric2}"
            )
            # Generate a unique key for each scatter plot using the metric names and index
            scatter_key = f"{self.name}_scatter_{metric1}_vs_{metric2}_{j}"
            figures.append(Figure(for_object=self, key=scatter_key, figure=fig))
        plt.close("all")

        return figures
