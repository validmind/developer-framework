# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from transformers import MarianMTModel, MarianTokenizer

from .StabilityAnalysis import StabilityAnalysis


class StabilityAnalysisTranslation(StabilityAnalysis):
    """
    Evaluate robustness of embeddings models to noise introduced by translating
    the original text to another language and back.

    **Purpose:** The purpose of this test is to assess the robustness of text embeddings models under the influence of
    noise. The noise in this scenario is introduced by translating the original text into another language and then
    translating it back to the original language. Any significant changes in the model's output between the original
    and translated-then-retranslated texts can be indicators of the model's lack of robustness to noise.

    **Test Mechanism:** The test mechanism involves several steps:

    1. Initialize the Marian tokenizer and model for both source and target languages.
    2. Translate the data from the source language to the target language.
    3. Translate the translated data back into the source language.
    4. Compare the original data with the data that has been translated and back-translated to observe any significant
    changes.

    The threshold of this test output would then be determined by the tolerance level of the model to these potentially
    noisy instances.

    **Signs of High Risk:**

    - If there large discrepancies between the original and double-translated text, this could indicate a high level of
    risk, signifying that the model is not robust to noise.
    - If a translation between languages does not closely maintain the meaning and context of the original language, it
    may suggest inadequate robustness against this type of noise.

    **Strengths:**

    - This metric is an effective way to assess the model’s sensitivity and robustness to language translation noise.
    - The use of translation as a means to introduce noise provides a realistic scenario which the model might
    encounter in real-world situations.
    - This metric extends beyond simple lexical changes, testing the model’s capacity to maintain semantic meaning
    under translational perturbations.

    **Limitations:**

    - Relying solely on translation-related noise for robustness testing can overlook other types of noise not
    reflected in language translation, such as typographical errors, grammatical mistakes, or random word substitutions.
    - Potential inaccuracies or discrepancies in the translation process itself might influence the resultant
    robustness score, rather than reflect an inherent failing of the model being tested.
    - The test is predominantly language-dependent, hence it might not fully capture the robustness of the model for
    languages with fewer resources or languages that are highly dissimilar to the source language.
    """

    name = "Text Embeddings Stability Analysis to Translation"
    default_params = {
        "source_lang": "en",
        "target_lang": "fr",
        **StabilityAnalysis.default_params,
    }

    def perturb_data(self, data: str):
        if not isinstance(data, str):
            return data

        source_lang = self.params["source_lang"]
        target_lang = self.params["target_lang"]

        # Initialize the Marian tokenizer and model for the source language
        model_name = f"Helsinki-NLP/opus-mt-{source_lang}-{target_lang}"
        model = MarianMTModel.from_pretrained(model_name)
        tokenizer = MarianTokenizer.from_pretrained(model_name)

        # Initialize the Marian tokenizer and model for the target language
        model_name_reverse = f"Helsinki-NLP/opus-mt-{target_lang}-{source_lang}"
        model_reverse = MarianMTModel.from_pretrained(model_name_reverse)
        tokenizer_reverse = MarianTokenizer.from_pretrained(model_name_reverse)

        # Translate to the target language
        encoded = tokenizer.encode(data, return_tensors="pt", add_special_tokens=True)
        decoded = tokenizer.decode(model.generate(encoded)[0], skip_special_tokens=True)

        # Translate back to the source language
        reverse_encoded = tokenizer_reverse.encode(
            decoded,
            return_tensors="pt",
            add_special_tokens=True,
        )
        reverse_decoded = tokenizer_reverse.decode(
            model_reverse.generate(reverse_encoded)[0],
            skip_special_tokens=True,
        )

        return reverse_decoded
