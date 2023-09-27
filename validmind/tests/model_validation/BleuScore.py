# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import evaluate
from nltk.tokenize import word_tokenize

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class BleuScore(Metric):
    """
    **Purpose**: The Bilingual Evaluation Understudy (BLEU) metric measures the quality of machine-translated text by
    comparing it to human-translated text. This comparison is done at the sentence level and is designed to bring
    machine translations closer to the quality of a professional human translation. It is commonly used in the field of
    translation evaluation, and its purpose is to assess the accuracy of a model's output against that of a benchmark.

    **Test Mechanism**: The implementation of the BLEU score involves using the NLTK's word_tokenize function to split
    the text into individual words, upon which the BLEU score can be calculated. The method employs the evaluate
    library's BLEU metric to compute the BLEU score for each translated sentence, comparing the model's translations
    (predictions) against the actual, correct translations (references). The results are returned as a single score
    which indicates the average 'distance' between the generated translations and the human translations across the
    entire test set.

    **Signs of High Risk**: Low BLEU scores indicate high model risk. This occurs when there is a significant
    discrepancy between the machine translation and its human equivalent. This may be due to the model not learning
    effectively, overfitting the training data, or not handling the nuances of the language effectively. Machine bias
    toward a certain language style or mode of translation can also result in lower scores.

    **Strengths**: The main strength of the BLEU score is its simplicity and interpretability. It provides an intuitive
    way to assess the quality of translated texts that can correlate well with human judgements. Additionally, it
    operates at a granular level (sentence level), enabling more precise assessment of errors. Lastly, it encapsulates
    the performance of the model with a single, comprehensive score that is easy to compare and monitor.

    **Limitations**: The BLEU score places emphasis on exact matches, which can lead to bias in favor of literal
    translations. As a result, it may not fully capture the quality of more complex or flexible translations that don't
    adhere strictly to a word-for-word structure. Another limitation is that it doesn't directly evaluate the
    intelligibility or grammatical correctness of the translations. Moreover, it may not identify errors that arise
    from subtle nuances in language, cultural contexts, or ambiguities.
    """

    name = "bleu_score"
    required_inputs = ["model", "model.test_ds"]

    def run(self):
        # Load the BLEU evaluation metric
        bleu = evaluate.load("bleu")

        # Compute the BLEU score
        bleu = bleu.compute(
            predictions=self.model.y_test_predict,
            references=self.model.y_test_true,
            tokenizer=word_tokenize,
        )
        return self.cache_results(metric_value={"blue_score_metric": bleu})

    def summary(self, metric_value):
        """
        Build one table for summarizing the bleu score results
        """
        summary_bleu_score = metric_value["blue_score_metric"]

        table = []
        table.append(summary_bleu_score)
        return ResultSummary(
            results=[
                ResultTable(
                    data=table,
                    metadata=ResultTableMetadata(title="Bleu score Results"),
                ),
            ]
        )
