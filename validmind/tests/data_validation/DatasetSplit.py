# Copyright © 2023 ValidMind Inc. All rights reserved.

from validmind.vm_models import Metric, ResultSummary, ResultTable


class DatasetSplit(Metric):
    """
    Attempts to extract information about the dataset split from the
    provided training, test and validation datasets.
    """

    name = "dataset_split"
    required_context = ["model"]

    dataset_labels = {
        "train_ds": "Training",
        "test_ds": "Test",
        "validation_ds": "Validation",
        "total": "Total",
    }

    def description(self):
        return """
        This section shows the size of the dataset split into training, test (and validation) sets
        where applicable. The size of each dataset is shown in absolute terms and as a proportion
        of the total dataset size.

        The dataset split is important to understand because it can affect the performance of
        the model. For example, if the training set is too small, the model may not be able to
        learn the patterns in the data and will perform poorly on the test set. On the other hand,
        if the test set is too small, the model may not be able to generalize well to unseen data
        and will perform poorly on the validation set.
        """

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
                        "Dataset": DatasetSplit.dataset_labels[dataset_name],
                        "Size": value,
                        "Proportion": f"{proportion:.2f}%",
                    }
                )

        return ResultSummary(results=[ResultTable(data=table_records)])

    def run(self):
        # Try to extract metrics from each available dataset
        available_datasets = ["train_ds", "test_ds", "validation_ds"]
        results = {}
        total_size = 0

        # First calculate the total size of the dataset
        for dataset_name in available_datasets:
            dataset = getattr(self.model, dataset_name, None)
            if dataset is not None:
                total_size += len(dataset.df)

        # Then calculate the proportion of each dataset
        for dataset_name in available_datasets:
            dataset = getattr(self.model, dataset_name, None)
            if dataset is not None:
                results[f"{dataset_name}_size"] = len(dataset.df)
                results[f"{dataset_name}_proportion"] = len(dataset.df) / total_size

        results["total_size"] = total_size

        return self.cache_results(results)
