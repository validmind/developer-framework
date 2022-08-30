"""
Central configuration for all validation tests.

This configuration will be driven by the API once we
add per-project support on the backend.
"""
from typing import List, Optional

import numpy as np

from pydantic import conint, BaseModel, BaseSettings


class BaseResultModel(BaseModel):
    class Config:
        json_encoders = {
            np.ndarray: lambda obj: obj.tolist(),
            np.integer: lambda obj: int(obj),
            np.floating: lambda obj: float(obj),
        }


class TestResult(BaseResultModel):
    test_name: Optional[str]  # Optionally allow a name for an individual test
    column: Optional[str]  # Optionally track the results for an individual column
    passed: Optional[bool]  # Optionally per-result pass/fail
    values: dict


class TestResults(BaseResultModel):
    category: str
    test_name: str
    params: dict
    passed: bool
    results: List[TestResult]


class ClassImbalanceConfig(BaseModel):
    # A minimum of 20% of minority class must
    # be represented in the dataset
    min_percent_threshold: float = 0.2


class DuplicatesConfig(BaseModel):
    # A single duplicate should fail the test
    min_threshold: int = 1


class HighCardinalityConfig(BaseModel):
    num_threshold: conint(gt=0) = 100
    percent_threshold: conint(gt=0) = 0.1
    threshold_type: str = "percent"  # or "num"


class MissingValuesConfig(BaseModel):
    # A single missing value should fail the test
    min_threshold: int = 1


class PearsonCorrelationConfig(BaseModel):
    max_threshold: float = 0.3


class SkewnessConfig(BaseModel):
    max_threshold: float = 1


class UniqueConfig(BaseModel):
    """
    Determine which columns are full of distinct values.
    Our default threshold is 1: 100% of rows.
    """

    min_percent_threshold: int = 1


class ZerosConfig(BaseModel):
    """
    Determine how many values in a numeric column are zero.
    """

    max_percent_threshold: int = 0.03


class AccuracyScoreConfig(BaseModel):
    """ """

    min_percent_threshold: float = 0.7


class F1ScoreConfig(BaseModel):
    """ """

    min_threshold: float = 0.5


class RocAucScoreConfig(BaseModel):
    """ """

    min_threshold: float = 0.5


class TrainTestDegradationConfig(BaseModel):
    """ """

    max_threshold: float = 0.1


class Settings(BaseSettings):
    class Config:
        env_prefix = "VM_TESTS_"

    target_column: Optional[str]

    class_imbalance: ClassImbalanceConfig = ClassImbalanceConfig()
    duplicates: DuplicatesConfig = DuplicatesConfig()
    high_cardinality: HighCardinalityConfig = HighCardinalityConfig()
    missing_values: MissingValuesConfig = MissingValuesConfig()
    pearson_correlation: PearsonCorrelationConfig = PearsonCorrelationConfig()
    skewness: SkewnessConfig = SkewnessConfig()
    unique: UniqueConfig = UniqueConfig()
    zeros: ZerosConfig = ZerosConfig()

    accuracy_score: AccuracyScoreConfig = AccuracyScoreConfig()
    f1_score: F1ScoreConfig = F1ScoreConfig()
    roc_auc_score: RocAucScoreConfig = RocAucScoreConfig()
    train_test_degradation: TrainTestDegradationConfig = TrainTestDegradationConfig()
