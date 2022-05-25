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
        # Run it for all data types for now
        # if df[col].dtype == np.object:
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


# Inspired by: https://github.com/ydataai/pandas-profiling/blob/f8bad5dde27e3f87f11ac74fb8966c034bc22db8/src/pandas_profiling/model/correlations.py
def pearson_correlation(df, config):
    test_params = {
        "max_threshold": config.pearson_correlation.max_threshold,
    }

    corr = df.corr(method="spearman")
    cols = corr.columns

    # Matrix of True/False where True means the correlation is above the threshold
    # Fill diagonal with False since all diagonal values are 1
    bool_index = abs(corr.values) >= test_params["max_threshold"]
    np.fill_diagonal(bool_index, False)

    # Simple cache to avoid a->b and b->a correlation entries
    correlation_mapping_cache = {}

    def cache_hit(from_field, to_field):
        correlation_keys = [from_field, to_field]
        correlation_keys.sort()
        cache_key = "-".join(correlation_keys)

        if cache_key in correlation_mapping_cache:
            return True

        correlation_mapping_cache[cache_key] = True
        return False

    def corr_items(from_field, to_fields):
        return [
            {
                "column": to_field,
                "correlation": corr.loc[from_field, to_field],
            }
            for to_field in to_fields
            if cache_hit(from_field, to_field) is False
        ]

    res = {
        col: corr_items(col, cols[bool_index[i]].values.tolist())
        for i, col in enumerate(cols)
        if any(bool_index[i])
    }

    # Cleanup keys with no values
    res = {k: v for k, v in res.items() if len(v) > 0}
    passed = len(res) == 0

    return TestResults(
        category="data_quality",
        test_name="pearson_correlation",
        params=test_params,
        passed=passed,
        results=[
            TestResult(
                column=col,
                values={"correlations": correlations},
            )
            for col, correlations in res.items()
        ],
    )
