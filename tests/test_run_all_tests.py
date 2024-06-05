"""This is a test harness to run unit tests against the ValidMind tests"""

import time
import unittest

import matplotlib.pyplot as plt
import xgboost as xgb

from sklearn.ensemble import RandomForestClassifier
from tabulate import tabulate
from tqdm import tqdm

import validmind as vm
from validmind.datasets.classification import customer_churn as demo_dataset
from validmind.logging import get_logger
from validmind.vm_models.test.result_wrapper import (
    MetricResultWrapper,
    ThresholdTestResultWrapper,
)
from validmind.tests import list_tests, load_test, run_test


logger = get_logger(__name__)
# Override plt.show to do nothing
plt.show = lambda: None

# These tests are expected to fail and need to be fixed
KNOWN_FAILING_TESTS = [
    "validmind.data_validation.BivariateScatterPlots",
    "validmind.data_validation.DefaultRatesbyRiskBandPlot",
    "validmind.data_validation.PiTCreditScoresHistogram",
    "validmind.data_validation.PiTPDHistogram",
    # Fix X_train["probability"] to use probability_column
    "validmind.model_validation.statsmodels.PDRatingClassPlot",
    # The tests below only work for statsmodels
    "validmind.model_validation.statsmodels.FeatureImportanceAndSignificance",
    "validmind.model_validation.statsmodels.RegressionCoeffsPlot",
    "validmind.model_validation.statsmodels.RegressionFeatureSignificance",
    "validmind.model_validation.statsmodels.RegressionModelsCoeffs",
    # Remove in_sample_datasetsm, out_of_sample_datasets inputs
    "validmind.model_validation.statsmodels.RegressionModelsPerformance",
    "validmind.model_validation.statsmodels.ScorecardHistogram",
]
SKIPPED_TESTS = []
SUCCESSFUL_TESTS = []
TABULAR_DATASET_TASKS = [
    "classification",
    "regression",
]

# Some tests require specific configurations. This is either expected and required
# or we need to fix these tests so they can run with sane defaults
#
# Here we assign config param keys to each test and then let the test runner know
# how to load the config for that test
TEST_TO_PARAMS_CONFIG = {
    # TODO: features_pairs should default to all input dataset pairs
    "validmind.data_validation.BivariateFeaturesBarPlots": "features_pairs_raw",
    "validmind.data_validation.BivariateHistograms": "features_pairs_raw",
    "validmind.data_validation.BivariateScatterPlots": "features_pairs_raw",
}
TEST_CONFIG = {}


class TestRunTest(unittest.TestCase):
    pass


test_inputs = {}


def _assign_features_pairs_config(raw_df, train_df=None, test_df=None):
    """
    Generates pairs of features for tests such as BivariateFeaturesBarPlots test
    """
    TEST_CONFIG["features_pairs_raw"] = {"features_pairs": {}}

    for i in range(0, len(raw_df.columns)):
        for j in range(i + 1, len(raw_df.columns)):
            TEST_CONFIG["features_pairs_raw"]["features_pairs"][raw_df.columns[i]] = (
                raw_df.columns[j]
            )


def _setup_tabular_test_inputs():
    df = demo_dataset.load_data()
    df = df.sample(1000)

    train_df, validation_df, test_df = demo_dataset.preprocess(df)
    x_train = train_df.drop(demo_dataset.target_column, axis=1)
    y_train = train_df[demo_dataset.target_column]
    x_val = validation_df.drop(demo_dataset.target_column, axis=1)
    y_val = validation_df[demo_dataset.target_column]

    classifier = xgb.XGBClassifier(early_stopping_rounds=10)
    classifier.set_params(eval_metric=["error", "logloss", "auc"])
    classifier.fit(x_train, y_train, eval_set=[(x_val, y_val)], verbose=False)

    classifier_rf = RandomForestClassifier()
    classifier_rf.fit(x_train, y_train)

    # Models
    vm_classifier_model = vm.init_model(
        classifier,
        input_id="xgb_classifier",
        __log=False,
    )
    vm_classifier_rf_model = vm.init_model(
        classifier_rf,
        input_id="rf_classifier",
        __log=False,
    )

    # Datasets
    vm_raw_dataset = vm.init_dataset(
        dataset=df,
        input_id="raw_dataset",
        target_column=demo_dataset.target_column,
        class_labels=demo_dataset.class_labels,
        __log=False,
    )
    vm_train_ds = vm.init_dataset(
        dataset=train_df,
        input_id="train_dataset",
        target_column=demo_dataset.target_column,
        __log=False,
    )
    vm_test_ds = vm.init_dataset(
        dataset=test_df,
        input_id="test_dataset",
        target_column=demo_dataset.target_column,
        __log=False,
    )

    # Assign predictions for each model
    vm_train_ds.assign_predictions(vm_classifier_model)
    vm_train_ds.assign_predictions(vm_classifier_rf_model)

    vm_test_ds.assign_predictions(vm_classifier_model)
    vm_test_ds.assign_predictions(vm_classifier_rf_model)

    _assign_features_pairs_config(df)

    # Usage:
    #
    # For 1 dataset tests use the raw dataset (i.e. data quality tests)
    # For 2 dataset/model tests, use model and test dataset
    # For 3 two dataset tests, use both the training and test datasets (comparison tests)
    test_inputs["classification"] = {
        "single_dataset": {
            "dataset": vm_raw_dataset,
        },
        "two_datasets": {
            "datasets": [vm_train_ds, vm_test_ds],
        },
        "single_model": {
            "model": vm_classifier_model,
        },
        "dataset_and_two_models": {
            "dataset": vm_test_ds,
            "models": [vm_classifier_model, vm_classifier_rf_model],
        },
        "model_and_dataset": {
            "dataset": vm_test_ds,
            "model": vm_classifier_model,
        },
        "model_and_two_datasets": {
            "model": vm_classifier_model,
            "datasets": [vm_train_ds, vm_test_ds],
        },
        "two_models": {
            "models": [vm_classifier_model, vm_classifier_rf_model],
        },
    }


def create_unit_test_func(vm_test_id, vm_test_class):
    def unit_test_func(self):
        self.assertTrue(
            hasattr(vm_test_class, "required_inputs"),
            f"{vm_test_id} missing required_inputs",
        )
        self.assertTrue(
            hasattr(vm_test_class, "metadata"),
            f"{vm_test_id} missing metadata",
        )
        self.assertTrue(
            "task_types" in vm_test_class.metadata
            and len(vm_test_class.metadata["task_types"]) > 0,
            f"{vm_test_id} missing task_types in metadata",
        )
        self.assertTrue(
            "tags" in vm_test_class.metadata
            and len(vm_test_class.metadata["tags"]) > 0,
            f"{vm_test_id} missing tags in metadata",
        )

        required_inputs = sorted(vm_test_class.required_inputs)
        if required_inputs == ["datasets", "models"]:
            logger.debug(
                "Skipping test - multi-(dataset,model) tests are not supported at the moment %s",
                vm_test_id,
            )
            SKIPPED_TESTS.append(vm_test_id)
            return

        # Skip all of these tests until we fix them
        if "clustering" in vm_test_class.metadata["task_types"]:
            logger.debug(
                "--- Skipping test - clustering tests not supported yet %s",
                vm_test_id,
            )
            SKIPPED_TESTS.append(vm_test_id)
            return

        if (
            "time_series_data" in vm_test_class.metadata["tags"]
            and "tabular_data" not in vm_test_class.metadata["tags"]
        ):
            logger.debug(
                "--- Skipping test - time series data tests not supported yet %s",
                vm_test_id,
            )
            SKIPPED_TESTS.append(vm_test_id)
            return

        if (
            "llm" in vm_test_class.metadata["tags"]
            or "nlp" in vm_test_class.metadata["tags"]
            or "embeddings" in vm_test_class.metadata["tags"]
        ):
            logger.debug(
                "--- Skipping test - NLP/LLM tests not supported yet %s",
                vm_test_id,
            )
            SKIPPED_TESTS.append(vm_test_id)
            return

        logger.debug(">>> Running test %s", vm_test_id)
        inputs = test_inputs["classification"]

        # Build the single test inputs according to the required inputs
        single_test_inputs = {}
        if required_inputs == ["dataset"]:
            single_test_inputs = inputs["single_dataset"]
        elif required_inputs == ["dataset", "model"]:
            single_test_inputs = inputs["model_and_dataset"]
        elif required_inputs == ["datasets"]:
            single_test_inputs = inputs["two_datasets"]
        elif required_inputs == ["datasets", "model"]:
            single_test_inputs = inputs["model_and_two_datasets"]
        elif required_inputs == ["models"]:
            single_test_inputs = inputs["two_models"]
        elif required_inputs == ["dataset", "models"]:
            single_test_inputs = inputs["dataset_and_two_models"]
        elif required_inputs == ["model"]:
            single_test_inputs = inputs["single_model"]

        test_kwargs = {
            "test_id": vm_test_id,
            "inputs": single_test_inputs,
            "__log": False,
            "show": False,
        }

        # Check if the test requires a specific configuration
        if vm_test_id in TEST_TO_PARAMS_CONFIG:
            key = TEST_TO_PARAMS_CONFIG.get(vm_test_id)
            if key in TEST_CONFIG:
                test_config = TEST_CONFIG.get(key)
                # Only set the config if it's not None
                if test_config:
                    test_kwargs["params"] = test_config
            else:
                logger.error(
                    "Skipping test %s - missing expected configuration for %s",
                    vm_test_id,
                    key,
                )
                SKIPPED_TESTS.append(vm_test_id)
                return

        start_time = time.time()
        results = run_test(**test_kwargs)
        end_time = time.time()
        execution_time = round(end_time - start_time, 2)

        self.assertTrue(
            isinstance(results, (MetricResultWrapper, ThresholdTestResultWrapper)),
            f"Expected MetricResultWrapper or ThresholdTestResultWrapper, got {type(results)}",
        )
        self.assertEqual(
            results.result_id,
            vm_test_id,
            f"Expected result_id to be {vm_test_id}, got {results.result_id}",
        )
        if isinstance(results, MetricResultWrapper):
            self.assertTrue(
                results.metric is not None or results.figures is not None,
                f"A metric result needs to produce a metric result or a figure",
            )

        if isinstance(results, ThresholdTestResultWrapper):
            self.assertTrue(
                results.test_results is not None or results.figures is not None,
                f"A threshold test needs to produce a test result or a figure",
            )

        # Finally, the test worked so we can add it to the list of successful tests
        # and note the time it took to run
        SUCCESSFUL_TESTS.append(
            {"test_id": vm_test_id, "execution_time": execution_time}
        )

    return unit_test_func


def create_test_summary_func():
    """
    Create a function that prints a summary of the test results.
    We do this dynamically so it runs after all the tests have run.
    """

    def test_summary(self):
        self.assertTrue(
            True,
            "Test results not found. Did any tests run?",
        )
        logger.info(">>> Test Summary")
        logger.info(
            ">>> NOTE: Please review failing test cases directly in the output below."
        )

        test_summary = []
        for test in SUCCESSFUL_TESTS:
            test_summary.append([test["test_id"], "SUCCESS", test["execution_time"]])

        for test in KNOWN_FAILING_TESTS:
            test_summary.append([test, "KNOWN FAILURE", None])

        for test in SKIPPED_TESTS:
            test_summary.append([test, "SKIPPED", None])

        print(
            tabulate(
                test_summary,
                headers=["Test ID", "Status", "Execution Time"],
                tablefmt="pretty",
            )
        )

    return test_summary


def create_unit_test_funcs_from_vm_tests():
    _setup_tabular_test_inputs()

    for vm_test_id in tqdm(sorted(list_tests(pretty=False))):
        if vm_test_id in KNOWN_FAILING_TESTS:
            logger.debug("Skipping known failing test %s", vm_test_id)
            continue

        # load the test class
        vm_test_class = load_test(vm_test_id)

        # create a unit test function for the test class
        unit_test_func = create_unit_test_func(vm_test_id, vm_test_class)
        unit_test_func_name = f'test_{vm_test_id.replace(".", "_")}'

        # add the unit test function to the unit test class
        setattr(TestRunTest, f"test_{unit_test_func_name}", unit_test_func)

    # create a test summary function. the zzz is to ensure it runs last
    test_summary_func = create_test_summary_func()
    setattr(TestRunTest, "test_zzz_summary", test_summary_func)


create_unit_test_funcs_from_vm_tests()


if __name__ == "__main__":
    unittest.main()
