"""
Threshold based tests
"""

from dataclasses import dataclass
from sklearn import metrics
import pandas as pd

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


@dataclass
class WeakSpotsDiagnosisTest(ThresholdTest):
    """
    Test that identify weak regions with high residuals by slicing techniques.
    """

    category = "model_diagnosis"
    name = "weak_spots"
    
    default_params = {"weak_spots_thresholds": {"Age": 0.02}}
    default_metrics = {
        "accuracy": metrics.accuracy_score,
        }

    def run(self):
        if "weak_spots_thresholds" not in self.params:
           raise ValueError("weak_spot_thresholds must be provided in params")

        features_thresholds_dict = self.params["weak_spots_thresholds"]
        if not isinstance(features_thresholds_dict, dict):
            raise ValueError("weak_spot_thresholds must be a dictionary with feature and threshold value")
        
        target_column = self.train_ds.target_column
        prediction_column = f"{target_column}_pred"

        train_df = self.train_ds.df
        train_class_pred = self.class_predictions(self.y_train_predict)
        train_df[prediction_column] = train_class_pred

        test_df = self.test_ds.df
        test_class_pred = self.class_predictions(self.y_test_predict)
        test_df[prediction_column] = test_class_pred

        test_results = []
        results_headers = ["slice", "shape", "accuracy"]
        for feature in features_thresholds_dict.keys():
            train_df['bin'] = pd.cut(train_df[feature], bins=10)
            results_train =  {k: [] for k in results_headers}
            results_test = {k: [] for k in results_headers}

            for region, df_region in train_df.groupby('bin'):
                self.compute_metrics(results_train, region, df_region, target_column, prediction_column)
                df_test_region = test_df[(test_df[feature] > region.left) & (test_df[feature] <= region.right)]
                self.compute_metrics(results_test, region, df_test_region, target_column, prediction_column)

            results = self.prepare_results(results_train, results_test, features_thresholds_dict[feature])
            passed = results.empty
            results = results.to_dict(orient="list")
            test_results.append(
                TestResult(
                    test_name=f"{self.name}_{feature}",
                    passed=passed,
                    values={
                        "results": results,
                    },
                )
            )

        return self.cache_results(test_results, passed=all([r.passed for r in test_results]))

    def prepare_results(self, results_train, results_test, threshold):

        results_train = pd.DataFrame(results_train)
        results_test = pd.DataFrame(results_test)
        results = results_train.copy()
        results['test records'] = results_test['shape']
        results['test accuracy'] = results_test['accuracy']
        results["gap"] = results_train["accuracy"] - results_test["accuracy"]
        results = results[results["gap"] > threshold]
        results.rename(columns={"shape": "training records", "accuracy": "training accuracy"}, inplace=True)

        return results

    def compute_metrics(self, results, region, df_region, target_column, prediction_column): 
        results["slice"].append(str(region))
        results["shape"].append(df_region.shape[0])
        y_true = df_region[target_column].values
        y_prediction = df_region[prediction_column].astype(df_region[target_column].dtypes).values

        for metric, metric_fn in self.default_metrics.items():
            results[metric].append(metric_fn(y_true, y_prediction))
