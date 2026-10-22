import json
import unittest
from types import SimpleNamespace

import matplotlib.pyplot as plt

from validmind.tests.comparison import _combine_figures
from validmind.vm_models.figure import Figure
from validmind.vm_models.result import TestResult


class TestComparisonFigureVariants(unittest.TestCase):
    def test_each_figure_sends_the_combination_that_made_it(self):
        """Reordered combinations must not reuse another combination's figure"""
        results = []
        for dataset in ("train_ds", "test_ds"):
            fig, _ = plt.subplots()
            results.append(
                TestResult(
                    result_id="roc",
                    inputs={"dataset": SimpleNamespace(input_id=dataset)},
                    params={"threshold": 0.5},
                    figures=[Figure(key=f"roc:{dataset}", figure=fig, ref_id="r")],
                )
            )

        figures = _combine_figures(results, show_params=False)
        variants = [
            json.loads(json.loads(f.serialize()["metadata"])["_variant"])
            for f in figures
        ]

        self.assertEqual(
            variants,
            [
                {"inputs": {"dataset": "train_ds"}, "params": {"threshold": 0.5}},
                {"inputs": {"dataset": "test_ds"}, "params": {"threshold": 0.5}},
            ],
        )
        for figure in figures:
            plt.close(figure.figure)


if __name__ == "__main__":
    unittest.main()
