# Copyright © 2023 ValidMind Inc. All rights reserved.

from transformers import MarianMTModel, MarianTokenizer

from .StabilityAnalysis import StabilityAnalysis


class StabilityAnalysisTranslation(StabilityAnalysis):
    """
    Evaluate robustness of embeddings models to noise introduced by translating
    the original text to another language and back.
    """

    name = "Text Embeddings Stability Analysis to Translation"
    default_params = {
        "source_lang": "en",
        "target_lang": "fr",
        **StabilityAnalysis.default_params,
    }

    def perturb_data(self, data: str):
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
