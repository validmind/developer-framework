# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from .ClassifierPerformance import ClassifierPerformance


@dataclass
class ClassifierOutOfSamplePerformance(ClassifierPerformance):
    """
    Test that outputs the performance of the model on the test data.
    """

    name = "classifier_out_of_sample_performance"
    required_inputs = ["model", "model.test_ds"]

    def description(self):
        return """
        This section shows the performance of the model on the test data. Popular
        metrics such as the accuracy, precision, recall, F1 score, etc. are
        used to evaluate the model.
        """

    def y_true(self):
        return self.model.y_test_true

    def y_pred(self):
        return self.model.y_test_predict
