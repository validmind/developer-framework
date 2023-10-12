# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass
from typing import ClassVar

from validmind.vm_models import Test
from validmind.vm_models.test_suite.result import TestSuiteDatasetResult


@dataclass
class DatasetMetadata(Test):
    """
    Collects and logs essential metadata of training datasets for transparency in model validation.

    **Purpose**: The `DatasetMetadata` test is primarily aimed at collecting and logging essential descriptive
    statistics related to the training datasets. This test generates essential metadata such as the types of tasks
    (classification, regression, text_classification, text_summarization) and tags (tabular_data, time_series_data,
    text_data) associated with the datasets. This transparency facilitates model validation by linking different
    metrics and test results to the originating dataset.

    **Test Mechanism**: Rather than conducting a test or implementing a grading scale, this class collects and logs
    dataset metadata. During post-initialization, the metadata is linked to the dataset object. The `run` method
    produces a `TestSuiteDatasetResult` object, which is assigned a unique ID and is bound to a dataset. The dataset
    metadata is associated with this ID for use in future, more focused, validation procedures.

    **Signs of High Risk**:
    - The metadata is incomplete or incorrect which can lead to inaccuracies in model risk assessment.
    - Dataset labels or types are missing, leading to issues in further model validation or mispresentations.

    **Strengths**:
    - The class brings transparency to model validation exercises by providing detailed information about the dataset.
    - It assists in error diagnosis and behaviors correlation to the model.
    - Ensures the correctness of tasks and data types associations and allows superior model explanations.
    - Supports dataset versioning by logging each dataset's metadata, maintaining a trackable history of alterations.

    **Limitations**:
    - The `DatasetMetadata` class's completeness and accuracy might be questionable, especially if metadata isn't
    appropriately added or is inaccurate.
    - It doesn't involve the evaluation of the dataset's quality or the direct validation of model predictions, hence
    it should be combined with other tests for a more comprehensive assessment.
    - The class cannot detect potential bias in the dataset. For bias detection, separate tests specifically tailored
    towards fairness and bias detection would be necessary.
    """

    # Class Variables
    test_type: ClassVar[str] = "DatasetMetadata"

    # Instance Variables
    name = "dataset_metadata"
    params: dict = None
    result: TestSuiteDatasetResult = None

    metadata = {
        "task_types": [
            "classification",
            "regression",
            "text_classification",
            "text_summarization",
        ],
        "tags": ["tabular_data", "time_series_data", "text_data"],
    }

    def __post_init__(self):
        """
        Set default params if not provided
        """
        if self.params is None:
            self.params = self.default_params

    def run(self):
        """
        Just set the dataset to the result attribute of the test suite result
        and it will be logged via the `log_dataset` function
        """
        self.result = TestSuiteDatasetResult(
            result_id="dataset_metadata", dataset=self.dataset
        )

        return self.result
