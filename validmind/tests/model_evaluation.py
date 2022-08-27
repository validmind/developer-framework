"""
Model Evaluation Tests. Currently we only support
models that have a sklearn compatible metrics interface
"""
from sklearn import metrics

from .config import TestResult, TestResults


def base_accuracy_test(model, test_set, test_preds, config=None):
    """
    Compute accuracy score metric from sklearn.
    """
    _, y_true = test_set
    _, class_pred = test_preds

    score = metrics.accuracy_score(y_true, class_pred)

    test_params = {
        "min_percent_threshold": config.accuracy_score.min_percent_threshold,
    }

    passed = score > test_params["min_percent_threshold"]

    test_result = TestResults(
        category="model_performance",
        test_name="accuracy_score",
        params=test_params,
        passed=passed,
        results=[
            TestResult(
                passed=passed,
                values={
                    "score": score,
                    "threshold": test_params["min_percent_threshold"],
                },
            )
        ],
    )

    return test_result


def base_f1_score_test(model, test_set, test_preds, config=None):
    """
    Compute f1 score metric from sklearn.
    """
    _, y_true = test_set
    _, class_pred = test_preds

    score = metrics.f1_score(y_true, class_pred)

    test_params = {
        "min_threshold": config.f1_score.min_threshold,
    }

    passed = score > test_params["min_threshold"]

    test_result = TestResults(
        category="model_performance",
        test_name="f1_score",
        params=test_params,
        passed=passed,
        results=[
            TestResult(
                passed=passed,
                values={"score": score, "threshold": test_params["min_threshold"]},
            )
        ],
    )

    return test_result


def base_roc_auc_score_test(model, test_set, test_preds, config=None):
    """
    Compute ROC AUC score metric from sklearn.
    """
    _, y_true = test_set
    _, class_pred = test_preds

    score = metrics.roc_auc_score(y_true, class_pred)

    test_params = {
        "min_threshold": config.roc_auc_score.min_threshold,
    }

    passed = score > test_params["min_threshold"]

    test_result = TestResults(
        category="model_performance",
        test_name="roc_auc_score",
        params=test_params,
        passed=passed,
        results=[
            TestResult(
                passed=passed,
                values={"score": score, "threshold": test_params["min_threshold"]},
            )
        ],
    )

    return test_result
