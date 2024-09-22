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
    Assesses the robustness of text embeddings models to random noise introduced via text perturbations.

    ### Purpose

    The purpose of this test is to evaluate the robustness of a text embeddings model to random noise. It introduces
    perturbations such as swapping adjacent words, inserting typos, deleting words, or inserting random words within
    the text to determine how well the model performs under such noisy conditions.

    ### Test Mechanism

    The test applies a series of pre-defined random perturbations to the text data. These perturbations include:

    - Swapping two adjacent words using the `random_swap` function.
    - Introducing a typo in a word using the `introduce_typo` function.
    - Deleting a word using the `random_deletion` function.
    - Inserting a random word at a random position using the `random_insertion` function.

    A probability parameter dictates the likelihood of each perturbation being applied to the words in the text. The
    text is initially tokenized into words, and selected perturbations are applied based on this probability.

    ### Signs of High Risk

    - High error rates in model predictions or classifications after the introduction of random noise.
    - Greater sensitivity to specific types of noise, such as typographical errors or word deletions.
    - Significant change in loss function or accuracy metrics.
    - Inconsistent model outputs for slightly perturbed inputs.

    ### Strengths

    - Measures model robustness against noise, reflecting real-world scenarios where data may contain errors or
    inconsistencies.
    - Easy to implement with adjustable perturbation severity through a probability parameter.
    - Identifies model sensitivity to specific types of noise, offering insights for model improvement.
    - Useful for testing models designed to handle text data.

    ### Limitations

    - May be ineffective for models that are inherently resistant to noise or designed to handle such perturbations.
    - Pseudo-randomness may not accurately represent the real-world distribution of noise or typographical errors.
    - Highly dependent on the probability parameter, requiring fine-tuning to achieve an optimal balance.
    - Only assesses performance against noise in input data, not the ability to capture complex language structures or
    semantics.
    - Does not guarantee model performance on new, unseen, real-world data beyond the generated noisy test data.
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
