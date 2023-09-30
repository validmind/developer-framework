# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass
from typing import ClassVar

from validmind.vm_models import Test
from validmind.vm_models.test_suite.result import TestSuiteDatasetResult


@dataclass
class DatasetMetadata(Test):
    """
    **Purpose**: The main objective of the `DatasetMetadata` test is to gather and log crucial descriptive statistics
    about the datasets used during model training. It serves as an important tool for monitoring relevant
    characteristics of the dataset, such as task types (classification, regression, text_classification,
    text_summarization) and tags (tabular_data, time_series_data, text_data). This helps ensure that model validation
    exercises are conducted with full transparency and context by connecting different metrics and test results to the
    underlying dataset.

    **Test Mechanism**: This class does not include a specific test or grading scale. Instead, it collects metadata
    associated with the dataset and logs it for future reference. The metadata is attached to the dataset object during
    the post-initialization phase. The `run` method initializes a `TestSuiteDatasetResult` object with a unique result
    ID and dataset. The dataset metadata then gets associated with this ID for future use in more targeted validation
    efforts.

    **Signs of High Risk**: The risks associated with this process are not connected with model performance or biases.
    However, incomplete metadata, incorrect dataset labels, or missing dataset types could lead to inaccuracies in
    model risk assessment and may constitute signs of risk within the metadata gathering process itself.

    **Strengths**: A key strength of this class is the transparency it brings to model validation exercises by
    providing detailed information about the dataset. This can help in diagnosing errors, identifying correlations to
    the model's behavior, ensuring correct task and data-type associations, and enabling superior model explanations.
    Also, it can support dataset versioning by logging each dataset's metadata, offering a trackable history of changes.

    **Limitations**: The `DatasetMetadata` class could lack completeness or accuracy, particularly if metadata is not
    adequately added or is incorrect. The process does not inherently evaluate the quality of the dataset or directly
    validate the model's predictions, so it must be combined with other tests for a comprehensive evaluation. Lastly,
    any potential bias in the dataset won't be recognized using this class. Bias detection would require separate tests
    tailored specifically towards fairness and bias detection.
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
