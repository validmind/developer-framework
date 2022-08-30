"""
Model Evaluation Tests. Currently we only support
models that have a sklearn compatible metrics interface

TODO: How to cache the results of the metrics that are computed on diferent
tests so we can reuse them and don't recompute them every time, while keeping
each test as functional and independent as possible?
"""
from sklearn import metrics

from .config import TestResult, TestResults


def base_accuracy_test(
    model, test_set, test_preds, train_set, train_preds, config=None
):
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


def base_f1_score_test(
    model, test_set, test_preds, train_set, train_preds, config=None
):
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


def base_roc_auc_score_test(
    model, test_set, test_preds, train_set, train_preds, config=None
):
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


def training_better_than_test(
    model, test_set, test_preds, train_set, train_preds, config=None
):
    """
    Compare training and test set performance
    """
    if train_preds[0] is None:
        print("Skipping training_better_than_test because train_preds was not passed")

    # TBD: drive this via config
    metrics_to_compare = [
        {
            "name": "accuracy_train_vs_test",
            "metric": metrics.accuracy_score,
        },
    ]

    test_results = []

    # Compute the same metric for both training and test set and check if train is better than test
    _, y_train_true = train_set
    _, train_class_pred = train_preds
    _, y_test_true = test_set
    _, test_class_pred = test_preds

    for metric in metrics_to_compare:
        metric_fn = metric["metric"]
        score_train = metric_fn(y_train_true, train_class_pred)
        score_test = metric_fn(y_test_true, test_class_pred)

        passed = score_train > score_test

        test_results.append(
            TestResult(
                test_name=metric["name"],
                passed=passed,
                values={
                    "score_train": score_train,
                    "score_test": score_test,
                },
            )
        )

    return TestResults(
        category="model_performance",
        test_name="training_better_than_test",
        params=dict(),
        passed=all([r.passed for r in test_results]),
        results=test_results,
    )


def training_test_degradation_test(
    model, test_set, test_preds, train_set, train_preds, config=None
):
    """
    Compare training and test set performance degradation according
    to a predermined threshold
    """
    if train_preds[0] is None:
        print(
            "Skipping training_test_degradation_test because train_preds was not passed"
        )

    # TBD: drive this via config
    metrics_to_compare = [
        {
            "name": "accuracy_degradation",
            "metric": metrics.accuracy_score,
        },
        {
            "name": "precision_degradation",
            "metric": metrics.precision_score,
        },
        {
            "name": "recall_degradation",
            "metric": metrics.recall_score,
        },
    ]

    test_params = {
        "max_threshold": config.train_test_degradation.max_threshold,
    }

    test_results = []

    # Compute the same metric for both training and test set and check if train is better than test
    _, y_train_true = train_set
    _, train_class_pred = train_preds
    _, y_test_true = test_set
    _, test_class_pred = test_preds

    for metric in metrics_to_compare:
        metric_fn = metric["metric"]
        score_train = metric_fn(y_train_true, train_class_pred)
        score_test = metric_fn(y_test_true, test_class_pred)

        degradation = (score_train - score_test) / score_train
        passed = degradation < test_params["max_threshold"]

        test_results.append(
            TestResult(
                test_name=metric["name"],
                passed=passed,
                values={
                    "score_train": score_train,
                    "score_test": score_test,
                    "degradation": degradation,
                },
            )
        )

    return TestResults(
        category="model_performance",
        test_name="training_test_degradation",
        params=test_params,
        passed=all([r.passed for r in test_results]),
        results=test_results,
    )
