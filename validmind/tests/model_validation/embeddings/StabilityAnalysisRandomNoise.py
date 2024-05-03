# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import random
import string

from .StabilityAnalysis import StabilityAnalysis


def random_swap(word_list):
    """Randomly swap two adjacent words."""
    if len(word_list) < 2:
        return word_list

    index = random.randint(0, len(word_list) - 2)
    word_list[index], word_list[index + 1] = word_list[index + 1], word_list[index]

    return word_list


def introduce_typo(word):
    """Introduce a random typo in a word."""
    if not word:
        return word

    typo_type = random.choice(["insert", "delete", "change"])
    char_pos = random.randint(0, len(word) - 1)

    if typo_type == "insert":
        random_char = random.choice(string.ascii_lowercase)
        return word[:char_pos] + random_char + word[char_pos:]

    if typo_type == "delete":
        return word[:char_pos] + word[char_pos + 1 :]

    random_char = random.choice(string.ascii_lowercase)
    return word[:char_pos] + random_char + word[char_pos + 1 :]


def random_deletion(word_list):
    """Delete a random word."""
    if not word_list:
        return word_list

    index = random.randint(0, len(word_list) - 1)

    return word_list[:index] + word_list[index + 1 :]


def random_insertion(word_list):
    """Insert a random word at a random position."""
    if not word_list:
        return word_list

    random_word = random.choice(word_list)
    index = random.randint(0, len(word_list))

    return word_list[:index] + [random_word] + word_list[index:]


class StabilityAnalysisRandomNoise(StabilityAnalysis):
    """
    Evaluate robustness of embeddings models to random noise introduced by using
    a `probability` parameter to choose random locations in the text to apply
    random perturbations. These perturbations include:

    - Swapping two adjacent words
    - Introducing a random typo in a word
    - Deleting a random word
    - Inserting a random word at a random position

    **Purpose:**
    The purpose of the stability analysis is to evaluate the robustness of a text embeddings model to random noise.
    Random perturbations such as swapping adjacent words, introducing random typos, deleting random words, or inserting
    random words at random positions in the text are introduced, to gauge the model's performance and stability.

    **Test Mechanism:**
    The test mechanism includes a series of function-defined random perturbations like swapping two words
    `random_swap`, introducing a typo in a word `introduce_typo`, deleting a random word `random_deletion`, and
    inserting a random word at a random position `random_insertion`. A probability parameter determines the likelihood
    or frequency of these perturbations within the text data.

    The `perturb_data` function initally tokenizes the string data based on spaces then applies selected random
    perturbations based on the provided probability for each word in the text.

    **Signs of High Risk:**
    - High error rates in model predictions or classifications after the introduction of the random noise
    - Greater sensitivity to certain types and degrees of noise such as typographical errors, insertion or deletion of
    words
    - Significant change in loss function or accuracy metric
    - Inconsistency in model outputs for slightly perturbed inputs

    **Strengths:**
    - Measures model robustness against noise thereby reflecting real-world scenarios where data may contain errors or
    inconsistencies.
    - Easy to implement with adjustable perturbation severity through probability parameter.
    - Enables identification of model sensitivity to certain noise types, providing grounding for model improvement.
    - Useful for testing models designed to handle text data.

    **Limitations:**
    - The test might not be effective for models that have been designed with a high resistance to noise or models that
    are inherently designed to handle such perturbations.
    - Pseudo-randomness may not accurately represent real-world distribution of noise or typographical errors, which
    could be biased towards certain types of errors or malware injections.
    - Highly dependent on the probability parameter to introduce noise, with artificial adjusting required to achieve
    an optimal balance.
    - Only validates the model's performance against noise in input data, not its ability to capture complex language
    structures or semantics.
    - Does not guarantee the model's performance in new, unseen, real-world data beyond what is represented by the
    noise-introduced test data.
    """

    name = "Text Embeddings Stability Analysis to Random Noise"
    default_params = {
        **StabilityAnalysis.default_params,
        "probability": 0.02,
    }

    def perturb_data(self, data):
        if not isinstance(data, str):
            return data

        probability = self.params["probability"]

        # Tokenize the string based on spaces
        words = data.split()

        # Apply random perturbations based on probability
        for _ in range(len(words)):
            if random.random() <= probability:
                action = random.choice(["swap", "typo", "delete", "insert"])
                if action == "swap":
                    words = random_swap(words)
                elif action == "typo":
                    index = random.randint(0, len(words) - 1)
                    words[index] = introduce_typo(words[index])
                elif action == "delete":
                    words = random_deletion(words)
                elif action == "insert":
                    words = random_insertion(words)

        return " ".join(words)
