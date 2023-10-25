# Copyright © 2023 ValidMind Inc. All rights reserved.

import re

from .StabilityAnalysis import StabilityAnalysis


class StabilityAnalysisKeyword(StabilityAnalysis):
    """
    Evaluate robustness of embeddings models to keyword swaps on the test dataset

    This tests expects a parameter `keyword_dict` that maps words to other words
    so that any instances of the key words in the test dataset will be replaced
    with the corresponding value.
    """

    name = "Text Embeddings Stability Analysis to Keyword Swaps"
    default_params = {
        "keyword_dict": None,  # set to none by default... this must be overridden
        **StabilityAnalysis.default_params,
    }

    def perturb_data(self, data: str):
        # Tokenize the string
        tokens = re.findall(r"[\w']+[.,!?;]?|[\w']+", data)
        modified_tokens = []

        # lowercase all keys in the keword_dict
        self.params["keyword_dict"] = {
            k.lower(): v for k, v in self.params["keyword_dict"].items()
        }

        for token in tokens:
            # Separate word and punctuation
            word_part = re.match(r"([\w']+)", token).group()
            punctuation_part = token[len(word_part) :]

            # Check if the token is a word and if it's in the dictionary
            if token.lower() in self.params["keyword_dict"]:
                modified_tokens.append(
                    self.params["keyword_dict"][word_part.lower()] + punctuation_part
                )
            else:
                modified_tokens.append(token)

        return " ".join(modified_tokens)
