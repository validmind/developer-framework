"""
A TestSuite is a collection of TestPlans. It is a helpful way to organize
TestPlans that are related to each other. For example, a TestSuite could be
created for a specific use case or model methodology, to run a colllection
of plans for data validation and model validation with a single function call.
"""

from dataclasses import dataclass
from typing import ClassVar, List

from .test_context import TestContext
from .test_plan import TestPlan


@dataclass
class TestSuite(TestPlan):
    """
    Base class for test suites. Test suites are used to define any
    arbitrary grouping of test plans that will be run on a dataset and/or model.
    """

    test_plans: ClassVar[List[str]] = []
    # Stores a reference to the child test plan instances
    # so we can access their results after running the test suite
    _test_plan_instances: List[object] = None

    def run(self, send=True):
        """
        Runs the test suite.
        """
        # Avoid circular import
        from ..test_plans import get_by_name

        self._test_plan_instances = []

        if self.test_context is None:
            self.test_context = TestContext(
                dataset=self.dataset,
                model=self.model,
                models=self.models,
            )

        for test_plan_id in self.test_plans:
            test_plan = get_by_name(test_plan_id)
            test_plan_instance = test_plan(
                config=self.config,
                test_context=self.test_context,
            )
            test_plan_instance.run(send=send)
            self._test_plan_instances.append(test_plan_instance)

    @property
    def results(self):
        """
        Returns the results of the test suite.
        """
        return [test_plan.results for test_plan in self._test_plan_instances]
