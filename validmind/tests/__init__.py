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
    skewness,
    zeros,
)
from ..client import log_test_results, start_run
from ..dataset_utils import get_transformed_dataset

config = Settings()


def _summarize_data_quality_results(results):
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


def run_dataset_tests(dataset, dataset_type, vm_dataset, send=True, run_cuid=None):
    """
    Run all or a subset of tests on the given dataframe. For now we allow this
    function to automatically start a run for us.

    :param pd.DataFrame df: Dataframe for a dataset. Should contain dependent and independent variables
    :param str dataset_type: The dataset type is necessary for mapping and relating multiple datasets together.
        Can be one of training, validation, test or generic
    :param vm_dataset: VM Dataset metadata
    :param bool send: Whether to post the test results to the API. send=False is useful for testing
    """
    print(f'Running data quality tests for "{dataset_type}" dataset...\n')
    if run_cuid is None:
        run_cuid = start_run()

    # TODO: standardize the way we pass in the dataset object
    df = dataset

    tests = [
        class_imbalance,
        duplicates,
        high_cardinality,
        missing_values,
        # pearson_correlation, # Skipping this test for now
        skewness,
        # unique, # ignore unique for now
        zeros,
    ]
    results = []

    print("Preparing dataset for tests...")
    transformed_df = get_transformed_dataset(df, vm_dataset)

    for test in tqdm(tests):
        test_results = test(transformed_df, vm_dataset, config)
        if test_results is not None:
            results.append(test_results)

    print("\nTest suite has completed.")
    if send:
        print("Sending results to ValidMind...")
        log_test_results(results, run_cuid=run_cuid, dataset_type=dataset_type)

    print("\nSummary of results:\n")
    print(_summarize_data_quality_results(results))
    print()

    return results
