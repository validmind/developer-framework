"""
Classification Metrics
"""
from sklearn import metrics
from sklearn.metrics import (
    confusion_matrix as cfm_sklearn,
    roc_curve as roc_curve_sklearn,
    precision_recall_curve as prc_sklearn,
)


def accuracy_score(model, test_set, test_preds):
    """
    Compute recall score metric from sklearn.
    """
    _, y_true = test_set
    _, class_pred = test_preds

    return {
        "metric": {
            "type": "evaluation",
            "scope": "test",
            "key": "accuracy",
            "value": [metrics.accuracy_score(y_true, class_pred)],
        }
    }


def confusion_matrix(model, test_set, test_preds):
    """
    Compute confusion matrix values from sklearn.
    """
    _, y_true = test_set
    _, class_pred = test_preds

    y_labels = list(map(lambda x: x.item(), y_true.unique()))
    y_labels.sort()

    tn, fp, fn, tp = cfm_sklearn(y_true, class_pred, labels=y_labels).ravel()
    return {
        "type": "evaluation",
        "scope": "test",
        "key": "confusion_matrix",
        "value": {
            "tn": tn,
            "fp": fp,
            "fn": fn,
            "tp": tp,
        },
    }


def f1_score(model, test_set, test_preds):
    """
    Compute recall score metric from sklearn.
    """
    _, y_true = test_set
    _, class_pred = test_preds

    return {
        "metric": {
            "type": "evaluation",
            "scope": "test",
            "key": "f1_score",
            "value": [metrics.f1_score(y_true, class_pred)],
        }
    }


def precision_recall_curve(model, test_set, test_preds):
    """
    Compute precision recall curve values from sklearn.
    """
    _, y_true = test_set
    y_pred, _ = test_preds

    precision, recall, pr_thresholds = prc_sklearn(y_true, y_pred)
    return {
        "metric": {
            "type": "evaluation",
            "scope": "test",
            "key": "pr_curve",
            "value": {
                "precision": precision,
                "recall": recall,
                "thresholds": pr_thresholds,
            },
        }
    }


def recall_score(model, test_set, test_preds):
    """
    Compute recall score metric from sklearn.
    """
    _, y_true = test_set
    _, class_pred = test_preds

    return {
        "metric": {
            "type": "evaluation",
            "scope": "test",
            "key": "recall",
            "value": [metrics.recall_score(y_true, class_pred)],
        }
    }


def roc_auc_score(model, test_set, test_preds):
    """
    Compute precision score metric from sklearn.
    """
    _, y_true = test_set
    _, class_pred = test_preds

    return {
        "metric": {
            "type": "evaluation",
            "scope": "test",
            "key": "roc_auc",
            "value": [metrics.roc_auc_score(y_true, class_pred)],
        }
    }


def precision_score(model, test_set, test_preds):
    """
    Compute precision score metric from sklearn.
    """
    _, y_true = test_set
    _, class_pred = test_preds

    return {
        "metric": {
            "type": "evaluation",
            "scope": "test",
            "key": "precision",
            "value": [metrics.precision_score(y_true, class_pred)],
        }
    }


def roc_curve(model, test_set, test_preds):
    """
    Compute ROC curve values from sklearn.
    """
    _, y_true = test_set
    y_pred, _ = test_preds

    fpr, tpr, roc_thresholds = roc_curve_sklearn(y_true, y_pred, drop_intermediate=True)
    return {
        "metric": {
            "type": "evaluation",
            "scope": "test",
            "key": "roc_curve",
            "value": {
                "fpr": fpr,
                "tpr": tpr,
                "thresholds": roc_thresholds,
            },
        }
    }
