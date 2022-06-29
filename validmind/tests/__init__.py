"""
Entrypoint to any validation test exposed by the SDK
"""
from tabulate import tabulate
from tqdm import tqdm

from .config import Settings
from .data_quality_pandas import (
    class_imbalance,
    duplicates,
    high_cardinality,
    missing_values,
    pearson_correlation,
    skewness,
    unique,
    zeros,
)
from ..client import log_test_results, start_run

config = Settings()


def _summarize_results(results):
    """
    Summarize the results of the data quality test suite
    """
    test_results = []
    for result in results:
        num_passed = len([r for r in result.results if r.passed])
        num_failed = len([r for r in result.results if not r.passed])

        percent_passed = (
            1 if len(result.results) == 0 else num_passed / len(result.results)
        )
        test_results.append(
            [
                result.test_name,
                result.passed,
                num_passed,
                num_failed,
                percent_passed * 100,
            ]
        )

    return tabulate(
        test_results,
        headers=["Test", "Passed", "# Passed", "# Errors", "% Passed"],
        numalign="right",
    )


def run_dataset_tests(df, dataset_type, target_column, send=False):
    """
    Run all or a subset of tests on the given dataframe. For now we allow this
    function to automatically start a run for us.

    :param pd.DataFrame df: Dataframe for a dataset. Should contain dependent and independent variables
    :param str dataset_type: The dataset type is necessary for mapping and relating multiple datasets together.
        Can be one of training, validation, test or generic
    :param str target_column: The name of the target column
    :param bool send: Whether to post the test results to the API. send=False is useful for testing
    """
    print(f'Running data quality tests for "{dataset_type}" dataset...\n')
    run_cuid = start_run()

    tests = [
        class_imbalance,
        duplicates,
        high_cardinality,
        missing_values,
        pearson_correlation,
        skewness,
        # unique, # ignore unique for now
        zeros,
    ]
    results = []

    config.target_column = target_column
    for test in tqdm(tests):
        results.append(test(df, config))

    print("\nTest suite has completed.")
    if send:
        print("Sending results to ValidMind...")
        log_test_results(results, run_cuid=run_cuid, dataset_type=dataset_type)

    print("\nSummary of results:\n")
    print(_summarize_results(results))
    print()

    return results


def run_model_tests(model, x_test, y_test, target_column=None, send=False):
    print("test")
