# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

"""Base Class for Metric, ThresholdTest and any other test type"""

from abc import abstractmethod
from dataclasses import dataclass
from typing import ClassVar, List, TypedDict
from uuid import uuid4

from ...utils import run_async
from ..test_context import TestUtils


class TestMetadata(TypedDict):
    """
    TestMetadata is a custom dict type that allows us to add metadata to tests
    """

    task_types: List[str]
    tags: List[str]


@dataclass
class Test(TestUtils):
    # Class Variables
    name: ClassVar[str] = ""  # should be overridden by leaf classes
    test_type: ClassVar[str]  # should be overridden by parent classes
    metadata: ClassVar[TestMetadata]  # should be overridden by leaf classes

    required_inputs: ClassVar[List[str]] = None  # should be overridden by leaf classes
    default_params: ClassVar[dict] = None  # should be overridden by leaf classes

    # Instance Variables
    _ref_id: str = None  # unique identifier (populated at init)
    _section_id: str = None  # which section of template this test belongs to
    test_id: str = None  # populated when loading tests from suites
    result: object = None  # type should be overridden by parent classes

    params: dict = None  # populated by test suite from user-passed config

    output_template: str = None  # optional output template

    def __post_init__(self):
        """
        Set default params if not provided
        """
        if not self.test_id:
            raise Exception(
                "test_id is missing. It must be passed when initializing the test"
            )
        self._ref_id = str(uuid4())

        # TODO: add validation for required inputs
        if self.default_params is None:
            self.default_params = {}

        self.params = {
            **(self.default_params or {}),
            **(self.params if self.params is not None else {}),
        }

    def description(self):
        """
        Return the test description. May be overridden by subclasses. Defaults
        to returning the class' docstring
        """
        return self.__doc__.strip()

    @abstractmethod
    def summary(self, *args, **kwargs):
        """
        Return the summary. Should be overridden by subclasses.
        """
        raise NotImplementedError("base class method should not be called")

    @abstractmethod
    def run(self, *args, **kwargs):
        """
        Run the calculation and cache its results
        """
        raise NotImplementedError("base class method should not be called")

    @abstractmethod
    def cache_results(self, *args, **kwargs):
        """
        Cache the results of the calculation
        """
        raise NotImplementedError("base class method should not be called")

    def log(self):
        """
        Log the test results to ValidMind
        """
        run_async(self.result.log)
