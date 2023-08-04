# This software is proprietary and confidential. Unauthorized copying,
# modification, distribution or use of this software is strictly prohibited.
# Please refer to the LICENSE file in the root directory of this repository
# for more information.
#
# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from .ClassifierPerformance import ClassifierPerformance


@dataclass
class ClassifierOutOfSamplePerformance(ClassifierPerformance):
    """
    Test that outputs the performance of the model on the test data.
    """

    name = "classifier_out_of_sample_performance"
    required_context = ["model", "model.test_ds"]

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
