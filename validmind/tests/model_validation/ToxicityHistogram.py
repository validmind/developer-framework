# Copyright © 2023 ValidMind Inc. All rights reserved.

import itertools
from dataclasses import dataclass

import evaluate

from validmind.vm_models import Metric


@dataclass
class ToxicityHistogram(Metric):
    """
    toxicity Histogram
    """

    name = "toxicity_histogram"
    required_inputs = ["model", "model.test_ds"]
    default_params = {"toxicity_obj": None}

    def description(self):
        return """
        Toxicity detailed description coming soon...!
        """

    def run(self):
        toxicity_obj = self.params["toxicity_obj"]
        if toxicity_obj is None:
            toxicity_obj = evaluate.load("toxicity")

        y_true = list(itertools.chain.from_iterable(self.model.y_test_true))
        y_pred = self.model.y_test_predict

        print(y_true)
        print(y_pred)
