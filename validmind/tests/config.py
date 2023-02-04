"""
Central configuration for all validation tests.

This configuration will be driven by the API once we
add per-project support on the backend.
"""
from typing import Optional

from pydantic import BaseModel, BaseSettings


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

    accuracy_score: AccuracyScoreConfig = AccuracyScoreConfig()
    f1_score: F1ScoreConfig = F1ScoreConfig()
    roc_auc_score: RocAucScoreConfig = RocAucScoreConfig()
    train_test_degradation: TrainTestDegradationConfig = TrainTestDegradationConfig()
