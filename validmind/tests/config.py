"""
Central configuration for all validation tests.

This configuration will be driven by the API once we
add per-project support on the backend.
"""
from typing import List, Optional

from pydantic import conint, BaseModel, BaseSettings


class TestResult(BaseModel):
    column: Optional[str]  # Optionally track the results for an individual column
    passed: Optional[bool]  # Optionally per-result pass/fail
    values: dict


class TestResults(BaseModel):
    category: str
    test_name: str
    params: dict
    passed: bool
    results: List[TestResult]


class HighCardinalityConfig(BaseModel):
    num_threshold: conint(gt=0) = 100
    percent_threshold: conint(gt=0) = 0.1
    threshold_type: str = "percent"  # or "num"


class DuplicatesConfig(BaseModel):
    # A single duplicate should raise
    min_threshold: int = 1


class PearsonCorrelationConfig(BaseModel):
    max_threshold: int = 0.3


class Settings(BaseSettings):
    class Config:
        env_prefix = "VM_TESTS_"

    high_cardinality: HighCardinalityConfig = HighCardinalityConfig()
    duplicates: DuplicatesConfig = DuplicatesConfig()
    pearson_correlation: PearsonCorrelationConfig = PearsonCorrelationConfig()
