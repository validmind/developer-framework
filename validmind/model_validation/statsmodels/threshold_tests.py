from dataclasses import dataclass
from ...vm_models import ThresholdTest, TestResult
from random import random


@dataclass
class RandomTest(ThresholdTest):
    """
    Test that random is greater than 0.5
    """

    category = "model_performance"  # right now we support "model_performance" and "data_quality"
    name = "random_test"
    default_params = {"threshold": 0.5}

    def run(self):
        my_random_value = random()
        passed = my_random_value > self.params["threshold"]

        results = [
            TestResult(
                passed=passed,
                values={
                    "score": my_random_value,
                    "threshold": self.params["threshold"],
                },
            )
        ]

        return self.cache_results(results, passed=all([r.passed for r in results]))

        # y_true = self.test_ds.y
        # class_pred = self.class_predictions(self.y_test_predict)
        # accuracy_score = metrics.accuracy_score(y_true, class_pred)

        # passed = accuracy_score > self.params["min_threshold"]
        # results = [
        #     TestResult(
        #         passed=passed,
        #         values={
        #             "score": accuracy_score,
        #             "threshold": self.params["min_threshold"],
        #         },
        #     )
        # ]

        # return self.cache_results(results, passed=all([r.passed for r in results]))
