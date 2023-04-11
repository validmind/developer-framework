"""
TestResult models
"""

from typing import List, Optional

import numpy as np
from pydantic import BaseModel


class BaseResultModel(BaseModel):
    """
    Base class for all result models
    """

    class Config:
        json_encoders = {
            np.ndarray: lambda obj: obj.tolist(),
            np.integer: lambda obj: int(obj),
            np.floating: lambda obj: float(obj),
        }


class TestResult(BaseResultModel):
    """
    TestResult model
    """

    test_name: Optional[str]  # Optionally allow a name for an individual test
    column: Optional[str]  # Optionally track the results for an individual column
    passed: Optional[bool]  # Optionally per-result pass/fail
    values: dict


class TestResults(BaseResultModel):
    """
    TestResults model
    """

    category: str
    test_name: str
    params: dict
    passed: bool
    results: List[TestResult]
