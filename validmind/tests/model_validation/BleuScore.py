# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import evaluate

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class BleuScore(Metric):
    """
    Assesses translation quality by comparing machine-translated sentences with human-translated ones using BLEU score.

    **Purpose**: The Bilingual Evaluation Understudy (BLEU) metric measures the quality of machine-translated text by
    comparing it to human-translated text. This comparison is done at the sentence level and is designed to bring
    machine translations closer to the quality of a professional human translation. It is commonly used in the field of
    translation evaluation, and its purpose is to assess the accuracy of a model's output against that of a benchmark.

    **Test Mechanism**: The BLEU score is implemented using the NLTK's word_tokenize function to split the text into
    individual words. After tokenization, the evaluate library's BLEU metric calculates the BLEU score for each
    translated sentence by comparing the model's translations (predictions) against the actual, correct translations
    (references). The test algorithm then combines these individual scores into a single score that represents the
    average 'distance' between the generated translations and the human translations across the entire test set.

    **Signs of High Risk**:
    - Low BLEU scores suggest high model risk. This could indicate significant discrepancies between the machine
    translation and its human equivalent.
    - This could be due to ineffective model learning, overfitting of training data, or inadequate handling of the
    language's nuances.
    - Machine biases toward a certain language style or translation mode can result in lower scores.

    **Strengths**:
    - The BLEU score's primary strength lies in its simplicity and interpretability. It offers a straightforward way to
    assess translated text quality, and its calculations often align with human judgments.
    - The BLEU score breaks down its evaluations at the sentence level, offering granular insights into any errors.
    - The score consolidates the model’s performance into a single, comprehensive score, making it easy to compare and
    monitor.

    **Limitations**:
    - The BLEU score heavily favours exact matches, which can create a bias towards literal translations. Thus, it may
    fail to fully evaluate more complex or flexible translations that shy away from a word-for-word structure.
    - The score does not directly measure the intelligibility or grammatical correctness of the translations.
    - It may miss errors originating from subtle nuances in language, cultural contexts, or ambiguities.
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
