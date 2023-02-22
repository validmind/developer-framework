"""
Threshold based tests
"""

from dataclasses import dataclass
from sklearn import metrics

from ...vm_models import TestResult, ThresholdTest


@dataclass
class AccuracyTest(ThresholdTest):
    """
    Test that the accuracy score is above a threshold.
    """

    category = "model_performance"
    name = "accuracy_score"
    default_params = {"min_threshold": 0.7}

    def run(self):
        y_true = self.test_ds.y
        class_pred = self.class_predictions(self.y_test_predict)
        accuracy_score = metrics.accuracy_score(y_true, class_pred)

        passed = accuracy_score > self.params["min_threshold"]
        results = [
            TestResult(
                passed=passed,
                values={
                    "score": accuracy_score,
                    "threshold": self.params["min_threshold"],
                },
            )
        ]

        return self.cache_results(results, passed=all([r.passed for r in results]))


@dataclass
class F1ScoreTest(ThresholdTest):
    """
    Test that the F1 score is above a threshold.
    """

    category = "model_performance"
    name = "f1_score"
    default_params = {"min_threshold": 0.5}

    def run(self):
        y_true = self.test_ds.y
        class_pred = self.class_predictions(self.y_test_predict)
        f1_score = metrics.f1_score(y_true, class_pred)

        passed = f1_score > self.params["min_threshold"]
        results = [
            TestResult(
                passed=passed,
                values={
                    "score": f1_score,
                    "threshold": self.params["min_threshold"],
                },
            )
        ]

        return self.cache_results(results, passed=all([r.passed for r in results]))


@dataclass
class ROCAUCScoreTest(ThresholdTest):
    """
    Test that the ROC AUC score is above a threshold.
    """

    category = "model_performance"
    name = "roc_auc_score"
    default_params = {"min_threshold": 0.5}

    def run(self):
        y_true = self.test_ds.y
        class_pred = self.class_predictions(self.y_test_predict)
        roc_auc = metrics.roc_auc_score(y_true, class_pred)

        passed = roc_auc > self.params["min_threshold"]
        results = [
            TestResult(
                passed=passed,
                values={
                    "score": roc_auc,
                    "threshold": self.params["min_threshold"],
                },
            )
        ]

        return self.cache_results(results, passed=all([r.passed for r in results]))


@dataclass
class TrainingTestDegradationTest(ThresholdTest):
    """
    Test that the training set metrics are better than the test set metrics.
    """

    category = "model_performance"
    name = "training_test_degradation"
    default_params = {"metrics": ["accuracy", "precision", "recall", "f1"]}
    default_metrics = {
        "accuracy": metrics.accuracy_score,
        "precision": metrics.precision_score,
        "recall": metrics.recall_score,
        "f1": metrics.f1_score,
    }

    def run(self):
        y_true = self.test_ds.y

        train_class_pred = self.class_predictions(self.y_train_predict)
        test_class_pred = self.class_predictions(self.y_test_predict)

        metrics_to_compare = self.params["metrics"]
        test_results = []
        for metric in metrics_to_compare:
            metric_fn = self.default_metrics[metric]

            train_score = metric_fn(self.train_ds.y, train_class_pred)
            test_score = metric_fn(y_true, test_class_pred)
            degradation = (train_score - test_score) / train_score

            passed = train_score > test_score
            test_results.append(
                TestResult(
                    test_name=metric,
                    passed=passed,
                    values={
                        "test_score": test_score,
                        "train_score": train_score,
                        "degradation": degradation,
                    },
                )
            )

        return self.cache_results(
            test_results, passed=all([r.passed for r in test_results])
        )
