# Copyright © 2023 ValidMind Inc. All rights reserved.

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
    random perturbations.

    These perturbations include:
    - Swapping two adjacent words
    - Introducing a random typo in a word
    - Deleting a random word
    - Inserting a random word at a random position

    The `probability` parameter determines the probability of applying a
    perturbation at each `word` in the text.
    """

    name = "Text Embeddings Stability Analysis to Random Noise"
    default_params = {
        "keyword_dict": None,  # set to none by default... this must be overridden
        **StabilityAnalysis.default_params,
    }

    def perturb_data(self, data, probability=0.02):
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
