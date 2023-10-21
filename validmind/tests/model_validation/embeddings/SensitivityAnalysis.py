# Copyright © 2023 ValidMind Inc. All rights reserved.

import plotly.express as px
from sklearn.cluster import KMeans

from validmind.vm_models import Figure, Metric


def perturb_data(dataset, prob=0.02):
    """
    Evaluates machine learning text model robustness to minor perturbations in text input via cluster distribution
    analysis.

    Perturbs the dataset based on the specified perturbation type.

    Parameters:
    - dataset: List or dataframe of text articles.
    - perturbation_type: One of 'random_deletion', 'random_swap', or 'random_insertion'.
    - prob: Probability with which a word in an article is perturbed.

    Returns:
    - perturbed_dataset: List of perturbed articles.
    """

    perturbed_dataset = []

    for article in dataset:
        words = article.split()
        num_words = len(words)

        if perturbation_type == "random_deletion":
            selected_indices = np.random.choice(
                num_words, int(prob * num_words), replace=False
            )
            for idx in selected_indices:
                words[idx] = ""

        elif perturbation_type == "random_swap":
            num_swaps = int(prob * num_words)
            for _ in range(num_swaps):
                idx = np.random.randint(
                    0, num_words - 1
                )  # Ensure it's not the last index
                words[idx], words[idx + 1] = words[idx + 1], words[idx]

        elif perturbation_type == "random_insertion":
            num_inserts = int(prob * num_words)
            for _ in range(num_inserts):
                idx = np.random.randint(0, num_words)
                random_word = np.random.choice(
                    words
                )  # Insert a random word from the article
                words.insert(idx, random_word)

        perturbed_dataset.append(" ".join(words))

    return perturbed_dataset


class SensitivityAnalysis(Metric):
    """
    **Purpose**: This test uses the method of Sensitivity Analysis to assess the robustness and stability of a
    text-based Machine Learning model. It investigates how small changes in the model's input, manifested as minor
    perturbations in textual data, impact the model's output embeddings. This is important to ensure the model's
    performance is not drastically impacted by small variations in the input data, corroborating its generalization
    ability.

    **Test Mechanism**: This test incorporates three types of perturbations – random deletion, random swap, and random
    insertion – each made in the articles with a certain probability. The perturbed data is then passed through the
    model, and KMeans clustering is applied to the resulting embeddings. A histogram plot visualizes the distribution
    of the output embeddings across the clusters. The number of clusters in the KMeans algorithm is a parameter that
    can be adjusted.

    **Signs of High Risk**:
    - Significant shifts in the cluster distribution from minor perturbations, indicating the model is overly sensitive
    to slight input changes.
    - Consistently altered output when introduced to minor input changes.
    - Noticeable imbalance in the cluster distribution which shows inconsistent model responses.

    **Strengths**:
    - Efficient in testing the model's stability against minor changes in the input. This is particularly necessary for
    text-based models due to the inherent noise and variability in languages.
    - Provides a visual representation of the model's sensitivity making it easy to interpret.
    - It's a non-parametric test, and it doesn't assume any underlying statistical distribution of the model.


    **Limitations**:
    - Assumes that changes in input should result in proportionate changes in output, which might not always be the
    case.
    - It only tests the model's robustness against specific types of perturbations (deletion, swap, insertion) and may
    not capture all potential sources of instability.
    - The output is significantly influenced by the parameter settings like the number of clusters which brings
    subjectivity.
    - The test might not be effective for very large datasets due to the high computational cost of KMeans on large
    data.
    - It doesn't directly provide a quantitative measure of the model's sensitivity which would be useful for
    establishing cut-off benchmarks.
    """

    name = "Text Embeddings Cluster Distribution"
    required_inputs = ["model", "model.test_ds"]
    default_params = {
        "num_clusters": 5,
    }
    metadata = {
        "task_types": ["feature_extraction"],
        "tags": ["llm", "text_data", "text_embeddings", "visualization"],
    }

    def run(self):
        # run kmeans clustering on embeddings
        kmeans = KMeans(n_clusters=self.params["num_clusters"]).fit(
            self.model.y_test_predict.values
        )

        # plot the distribution
        fig = px.histogram(
            kmeans.labels_,
            nbins=self.params["num_clusters"],
            title="Embeddings Cluster Distribution",
        )

        return self.cache_results(
            figures=[
                Figure(
                    for_object=self,
                    key=self.key,
                    figure=fig,
                )
            ],
        )
