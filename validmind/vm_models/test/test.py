# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

"""Base Class for Metric, ThresholdTest and any other test type"""

from abc import abstractmethod
from dataclasses import dataclass
from inspect import getdoc
from typing import ClassVar, List
from uuid import uuid4

from ..test_context import TestUtils
from .result_wrapper import ResultWrapper


@dataclass
class Test(TestUtils):
    # Class Variables
    name: ClassVar[str] = ""  # should be overridden by leaf classes
    test_type: ClassVar[str]  # should be overridden by parent classes
    tasks: List[str] = None  # should be overridden by leaf classes
    tags: List[str] = None  # should be overridden by leaf classes

    required_inputs: ClassVar[List[str]] = None  # should be overridden by leaf classes
    default_params: ClassVar[dict] = None  # should be overridden by leaf classes

    # Instance Variables
    _ref_id: str = None  # unique identifier (populated at init)
    _section_id: str = None  # which section of template this test belongs to
    test_id: str = None  # populated when loading tests from suites
    result: ResultWrapper = None  # type should be overridden by parent classes

    params: dict = None  # populated by test suite from user-passed config

    output_template: str = None  # optional output template

    generate_description: bool = (
        True  # whether to generate a description when caching result
    )

    def __post_init__(self):
        """
        Set default params if not provided
        """
        if not self.test_id:
            raise Exception(
                "test_id is missing. It must be passed when initializing the test"
            )

        self._ref_id = str(uuid4())
        self.key = (
            self.test_id
        )  # for backwards compatibility - figures really should get keyed automatically

        # TODO: add validation for required inputs
        if self.default_params is None:
            self.default_params = {}
        if self.required_inputs is None:
            self.required_inputs = []
        if self.tags is None:
            self.tags = []
        if self.tasks is None:
            self.tasks = []

        self.params = {
            **(self.default_params or {}),
            **(self.params if self.params is not None else {}),
        }

    def description(self):
        """
        Return the test description. May be overridden by subclasses. Defaults
        to returning the class' docstring
        """
        return getdoc(self).strip()

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
        return self.result.log()
