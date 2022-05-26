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
    column: Optional[str]  # Optionally track the results for an individual column
    passed: Optional[bool]  # Optionally per-result pass/fail
    values: dict


class TestResults(BaseResultModel):
    category: str
    test_name: str
    params: dict
    passed: bool
    results: List[TestResult]


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
    max_threshold: int = 0.3


class SkewnessConfig(BaseModel):
    max_threshold: int = 2


class Settings(BaseSettings):
    class Config:
        env_prefix = "VM_TESTS_"

    duplicates: DuplicatesConfig = DuplicatesConfig()
    high_cardinality: HighCardinalityConfig = HighCardinalityConfig()
    missing_values: MissingValuesConfig = MissingValuesConfig()
    pearson_correlation: PearsonCorrelationConfig = PearsonCorrelationConfig()
    skewness: SkewnessConfig = SkewnessConfig()
