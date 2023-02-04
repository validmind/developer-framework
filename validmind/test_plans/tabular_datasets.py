"""
Test plan for tabular datasets

Ideal setup is to have the API client to read a
custom test plan from the project's configuration
"""

from typing import List

from .test_plan import TestPlan
from ..data_validation.threshold_tests import (
    ClassImbalanceTest,
    DuplicatesTest,
    HighCardinalityTest,
    HighPearsonCorrelationTest,
    MissingValuesTest,
    SkewnessTest,
    UniqueRowsTest,
    ZerosTest,
)
from ..vm_models import Dataset, Model


class GenericTabularDatasetTestPlan(TestPlan):
    """
    Test plan for generic tabular datasets
    """

    def __init__(
        self,
        config: dict() = None,
        dataset: Dataset = None,
        model: Model = None,
        tests: List[object] = [],
    ):
        super().__init__(config, dataset, model, tests)

        if dataset is None:
            raise ValueError("Dataset is required for this test plan")

        self.dataset = dataset
        self.name = "generic_tabular_dataset"
        self.tests = [
            ClassImbalanceTest,
            DuplicatesTest,
            HighCardinalityTest,
            HighPearsonCorrelationTest,
            MissingValuesTest,
            SkewnessTest,
            UniqueRowsTest,
            ZerosTest,
        ]
