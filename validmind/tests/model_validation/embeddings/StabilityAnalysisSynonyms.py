# Copyright © 2023 ValidMind Inc. All rights reserved.

import random

import nltk
from nltk.corpus import wordnet as wn

from .StabilityAnalysis import StabilityAnalysis


class StabilityAnalysisSynonyms(StabilityAnalysis):
    """
    Evaluate robustness of embeddings models to synonym swaps on the test dataset

    This test uses WordNet to find synonyms for words in the test dataset and
    expects a parameter `probability` that determines the probability of swapping
    a word with a synonym.
    """

    name = "Text Embeddings Stability Analysis to Synonym Swaps"
    default_params = {
        "probability": 0.02,  # probability of swapping a word with a synonym
        **StabilityAnalysis.default_params,
    }

    def perturb_data(self, data):
        # download the nltk wordnet
        nltk.download("wordnet")

        words = nltk.word_tokenize(data)
        modified_words = []

        # For each word, check the probability and swap if needed
        for word in words:
            if random.random() <= self.params["probability"]:
                # get synonyms for the word
                synonyms = [
                    lemma.name() for syn in wn.synsets(word) for lemma in syn.lemmas()
                ]
                # filter out original word
                synonyms = [syn for syn in synonyms if syn != word]

                if synonyms:
                    modified_word = random.choice(synonyms)
                    # WordNet uses underscores for multi-word synonyms
                    modified_words.append(modified_word.replace("_", " "))
                    continue

            modified_words.append(word)

        return " ".join(modified_words)
