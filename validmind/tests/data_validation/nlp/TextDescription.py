# Copyright © 2023 ValidMind Inc. All rights reserved.


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
    **Purpose**: This is an in-depth textual analysis test used to assess the lexical complexity, structure, and
    vocabulary of a given dataset. The TextDescription metric measures various parameters such as:

    - **Total Words**: Assess the length and complexity of the input text. Longer documents might require more
    sophisticated summarization techniques, while shorter ones may need more concise summaries.
    - **Total Sentences**: Understand the structural makeup of the content. Longer texts with numerous sentences might
    require the model to generate longer summaries to capture essential information.
    - **Avg Sentence Length**: Determine the average length of sentences in the text. This can help the model decide on
    the appropriate length for generated summaries, ensuring they are coherent and readable.
    - **Total Paragraphs**: Analyze how the content is organized into paragraphs. The model should be able to maintain
    the logical structure of the content when producing summaries.
    - **Total Unique Words**: Measure the diversity of vocabulary in the text. A higher count of unique words could
    indicate more complex content, which the model needs to capture accurately.
    - **Most Common Words**: Identify frequently occurring words that likely represent key themes. The model should pay
    special attention to including these words and concepts in its summaries.
    - **Total Punctuations**: Evaluate the usage of punctuation marks, which contribute to the tone and structure of
    the content. The model should be able to maintain appropriate punctuation in summaries.
    - **Lexical Diversity**: Calculate the richness of vocabulary in relation to the overall text length. A higher
    lexical diversity suggests a broader range of ideas and concepts that the model needs to capture in its summaries.

    It is also responsible for paring down unwanted tokens, measuring the average sentence length, and calculating the
    lexical diversity in the available text. This metric's measures help in understanding the nature of the text and
    assessing the potential challenges of machine learning algorithms deployed for textual analysis, language
    processing, or summarization.

    **Test Mechanism**: The test operates by parsing the dataset and using the NLTK library to tokenize the text into
    words, sentences, and paragraphs. It dissects the processed text further, removing stopwords declared in
    'unwanted_tokens' and punctuations. It then calculates parameters such as the total number of words, sentences,
    paragraphs, punctuations; average sentence length; and lexical diversity. The metric also condenses these results
    and plots scatter plots for certain combinations of variables (Total Words vs Total Sentences, Total Words vs Total
    Unique Words, etc.) to provide a visual depiction of the text structure.

    **Signs of High Risk**: Anomaly in results or increased complexity in lexical diversity, long sentences and
    paragraphs, high uniqueness of words, or an excess of unwanted tokens can signify risk in text processing ML
    models. It suggests that the model's text absorption and processing capability can be compromised. Additionally,
    missing or erroneous visualizations may also indicate issues with the text description analysis.

    **Strengths**: This metric is an essential tool for ML model data pre-processing, focusing on textual analysis. It
    provides a detailed dissection of a text dataset to understand structural and vocabulary complexity, which is
    helpful to strategize a ML model's textual processing capability. Besides, it visualizes correlations between
    chosen variables, helping further in grasping the text's structure and complexity.

    **Limitations**: This metric relies heavily on the NLTK library, rendering it unsuitable for languages unsupported
    by NLTK. The unwanted tokens and stop words are predefined, limiting customization by context or application. This
    metric does not consider semantics or grammatical complexities, which can be crucial in language processing.
    Finally, it assumes that the document is well-structured (with sentences and paragraphs); unstructured or poorly
    formatted text may skew the results.
    """

    name = "text_description"
    required_inputs = ["dataset", "dataset.text_column"]
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
                sum(len(sentence.split()) for sentence in sentences) / total_sentences
                if total_sentences
                else 0,
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
        text_column = self.dataset.text_column
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
        # Can only run this test if we have a Dataset object
        if not isinstance(self.dataset, VMDataset):
            raise ValueError("TextDescretion requires a validmind Dataset object")

        df_text_description = self.text_description_table(self.dataset.df, self.params)

        # Define the combinations you want to plot
        combinations_to_plot = [
            ("Total Words", "Total Sentences"),
            ("Total Words", "Total Unique Words"),
            ("Total Sentences", "Avg Sentence Length"),
            ("Total Unique Words", "Lexical Diversity"),
        ]
        params = {"combinations_to_plot": combinations_to_plot}
        figures = self.text_description_scatter_plot(df_text_description, params)

        return self.cache_results(
            figures=figures,
        )

    # Function to plot scatter plots for specified combinations using Plotly
    def text_description_scatter_plot(self, df, params):

        combinations_to_plot = params["combinations_to_plot"]
        figures = []
        # Create hist plots for each column
        for i, column in enumerate(df.columns):
            fig = px.histogram(df, x=column)
            fig.update_layout(bargap=0.2)
            figures.append(Figure(for_object=self, key=self.key, figure=fig))

        for metric1, metric2 in combinations_to_plot:
            fig = px.scatter(
                df, x=metric1, y=metric2, title=f"Scatter Plot: {metric1} vs {metric2}"
            )
            figures.append(Figure(for_object=self, key=self.key, figure=fig))
        plt.close("all")

        return figures
