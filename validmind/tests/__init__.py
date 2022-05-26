"""
Entrypoint to any validation test exposed by the SDK
"""
from tabulate import tabulate
from tqdm import tqdm

from .config import Settings
from .data_quality_pandas import (
    duplicates,
    high_cardinality,
    missing_values,
    pearson_correlation,
    skewness,
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


def run_tests(df, dataset_type, send=False):
    """
    Run all or a subset of tests on the given dataframe. For now we allow this
    function to automatically start a run for us.
    """
    print(f'Running data quality tests for "{dataset_type}" dataset...\n')
    test_run_cuid = start_run()

    tests = [
        duplicates,
        high_cardinality,
        missing_values,
        pearson_correlation,
        skewness,
    ]
    results = []

    for test in tqdm(tests):
        results.append(test(df, config))

    print("\nTest suite has completed.")
    if send:
        print("Sending results to ValidMind...")
        log_test_results(
            results, test_run_cuid=test_run_cuid, dataset_type=dataset_type
        )

    print("\nSummary of results:\n")
    print(_summarize_results(results))
    print()

    return results
