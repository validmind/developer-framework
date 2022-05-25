"""
Generates data quality metrics for a given dataset.
"""
import numpy as np

from .config import TestResult, TestResults


def high_cardinality(df, config):
    results = []
    rows = df.shape[0]

    test_params = {
        "num_threshold": config.high_cardinality.num_threshold,
        "percent_threshold": config.high_cardinality.percent_threshold,
        "threshold_type": config.high_cardinality.threshold_type,
    }

    num_threshold = config.high_cardinality.num_threshold
    if config.high_cardinality.threshold_type == "percent":
        num_threshold = int(config.high_cardinality.percent_threshold * rows)

    for col in df.columns:
        if df[col].dtype == np.object:
            passed = True
            n_distinct = df[col].nunique()
            p_distinct = n_distinct / rows

            passed = n_distinct < num_threshold

            results.append(
                TestResult(
                    column=col,
                    passed=passed,
                    values={
                        "n_distinct": n_distinct,
                        "p_distinct": p_distinct,
                    },
                )
            )

    return TestResults(
        category="data_quality",
        test_name="cardinality",
        params=test_params,
        passed=all([r.passed for r in results]),
        results=results,
    )


def duplicates(df, config):
    rows = df.shape[0]

    test_params = {
        "min_threshold": config.duplicates.min_threshold,
    }

    n_duplicates = len(df[df.duplicated(keep=False)])
    p_duplicates = n_duplicates / rows
    passed = n_duplicates < config.duplicates.min_threshold

    return TestResults(
        category="data_quality",
        test_name="duplicates",
        params=test_params,
        passed=passed,
        results=[
            TestResult(
                values={"n_duplicates": n_duplicates, "p_duplicates": p_duplicates},
            )
        ],
    )
