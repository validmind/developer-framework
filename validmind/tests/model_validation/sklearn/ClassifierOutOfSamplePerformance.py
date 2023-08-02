# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import numpy as np

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
        if self.model.device_type and self.model._is_pytorch_model:
            if not self.model.device_type == "gpu":
                y_true = np.array(self.model.test_ds.y.cpu())
            else:
                y_true = np.array(self.model.test_ds.y)
        else:
            y_true = np.array(self.model.test_ds.y)

        return y_true

    def y_pred(self):
        return self.model.model.predict(self.model.test_ds.x)
