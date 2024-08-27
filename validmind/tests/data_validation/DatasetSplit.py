# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from validmind.vm_models import Metric, ResultSummary, ResultTable


class DatasetSplit(Metric):
    """
    Evaluates and visualizes the distribution proportions among training, testing, and validation datasets of an ML
    model.

    ### Purpose

    The DatasetSplit test is designed to evaluate and visualize the distribution of data among training, testing, and
    validation datasets, if available, within a given machine learning model. The main purpose is to assess whether the
    model's datasets are split appropriately, as an imbalanced split might affect the model's ability to learn from the
    data and generalize to unseen data.

    ### Test Mechanism

    The DatasetSplit test first calculates the total size of all available datasets in the model. Then, for each
    individual dataset, the methodology involves determining the size of the dataset and its proportion relative to the
    total size. The results are then conveniently summarized in a table that shows dataset names, sizes, and
    proportions. Absolute size and proportion of the total dataset size are displayed for each individual dataset.

    ### Signs of High Risk

    - A very small training dataset, which may result in the model not learning enough from the data.
    - A very large training dataset and a small test dataset, which may lead to model overfitting and poor
    generalization to unseen data.
    - A small or non-existent validation dataset, which might complicate the model's performance assessment.

    ### Strengths

    - The DatasetSplit test provides a clear, understandable visualization of dataset split proportions, which can
    highlight any potential imbalance in dataset splits quickly.
    - It covers a wide range of task types including classification, regression, and text-related tasks.
    - The metric is not tied to any specific data type and is applicable to tabular data, time series data, or text
    data.

    ### Limitations

    - The DatasetSplit test does not provide any insight into the quality or diversity of the data within each split,
    just the size and proportion.
    - The test does not give any recommendations or adjustments for imbalanced datasets.
    - Potential lack of compatibility with more complex modes of data splitting (for example, stratified or time-based
    splits) could limit the applicability of this test.
    """

    name = "dataset_split"
    required_inputs = ["datasets"]
    tasks = [
        "classification",
        "regression",
        "text_classification",
        "text_summarization",
    ]

    tags = ["tabular_data", "time_series_data", "text_data"]

    dataset_labels = {
        "train_ds": "Training",
        "test_ds": "Test",
        "validation_ds": "Validation",
        "total": "Total",
    }

    def summary(self, raw_results):
        """
        Returns a summarized representation of the dataset split information
        """
        table_records = []
        for key, value in raw_results.items():
            if key.endswith("_size"):
                dataset_name = key.replace("_size", "")
                if dataset_name == "total":
                    table_records.append(
                        {
                            "Dataset": "Total",
                            "Size": value,
                            "Proportion": "100%",
                        }
                    )
                    continue

                proportion = raw_results[f"{dataset_name}_proportion"] * 100
                table_records.append(
                    {
                        "Dataset": dataset_name,  # DatasetSplit.dataset_labels[dataset_name],
                        "Size": value,
                        "Proportion": f"{proportion:.2f}%",
                    }
                )

        return ResultSummary(results=[ResultTable(data=table_records)])

    def run(self):
        # Try to extract metrics from each available dataset
        available_datasets = self.inputs.datasets
        results = {}
        total_size = 0

        # First calculate the total size of the dataset
        for dataset in available_datasets:
            if dataset is not None:
                total_size += len(dataset.df)

        # Then calculate the proportion of each dataset
        for dataset in available_datasets:
            if dataset is not None:
                results[f"{dataset.input_id}_size"] = len(dataset.df)
                results[f"{dataset.input_id}_proportion"] = len(dataset.df) / total_size

        results["total_size"] = total_size

        return self.cache_results(results)

    def test(self):
        """Unit Test for DatasetSplit Metric"""
        assert self.result is not None

        assert self.result.metric is not None
        assert isinstance(self.result.metric.value, dict)

        assert self.result.figures is None
