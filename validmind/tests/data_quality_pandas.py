"""
Generates data quality metrics for a given dataset.
"""
import numpy as np

from pandas_profiling.config import Settings
from pandas_profiling.model.typeset import ProfilingTypeSet

from .config import TestResult, TestResults


def class_imbalance(df, config):
    test_params = {
        "min_percent_threshold": config.class_imbalance.min_percent_threshold,
    }

    target_column = config.target_column
    imbalance_percentages = df[target_column].value_counts(normalize=True)

    # Is the smallest number less than our threshold?
    passed = imbalance_percentages.min() < test_params["min_percent_threshold"]

    return TestResults(
        category="data_quality",
        test_name="class_imbalance",
        params=test_params,
        passed=passed,
        results=[
            TestResult(
                column=target_column,
                passed=passed,
                values=imbalance_percentages.to_dict(),
            )
        ],
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
                passed=passed,
                values={"n_duplicates": n_duplicates, "p_duplicates": p_duplicates},
            )
        ],
    )


def missing_values(df, config):
    rows = df.shape[0]

    test_params = {
        "min_threshold": config.missing_values.min_threshold,
    }

    missing = df.isna().sum()
    results = [
        TestResult(
            column=col,
            passed=missing[col] < config.missing_values.min_threshold,
            values={"n_missing": missing[col], "p_missing": missing[col] / rows},
        )
        for col in missing.index
    ]

    return TestResults(
        category="data_quality",
        test_name="missing",
        params=test_params,
        passed=all([r.passed for r in results]),
        results=results,
    )


def high_cardinality(df, config):
    typeset = ProfilingTypeSet(Settings())
    dataset_types = typeset.infer_type(df)

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
        # Only calculate high cardinality for categorical columns
        if str(dataset_types[col]) != "Categorical":
            continue

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
                passed=False,
            )
            for col, correlations in res.items()
        ],
    )


def skewness(df, config):
    typeset = ProfilingTypeSet(Settings())
    dataset_types = typeset.infer_type(df)

    test_params = {
        "max_threshold": config.skewness.max_threshold,
    }

    skewness = df.skew(numeric_only=True)
    passed = all(abs(skewness) < test_params["max_threshold"])
    results = []

    for col in skewness.index:
        # Only calculate skewness for numerical columns
        if str(dataset_types[col]) != "Numeric":
            continue

        col_skewness = skewness[col]
        results.append(
            TestResult(
                column=col,
                passed=abs(col_skewness) < test_params["max_threshold"],
                values={
                    "skewness": col_skewness,
                },
            )
        )

    return TestResults(
        category="data_quality",
        test_name="skewness",
        params=test_params,
        passed=passed,
        results=results,
    )


def unique(df, config):
    rows = df.shape[0]

    test_params = {
        "min_percent_threshold": config.unique.min_percent_threshold,
    }

    unique_rows = df.nunique()
    results = [
        TestResult(
            column=col,
            passed=(unique_rows[col] / rows) < test_params["min_percent_threshold"],
            values={
                "n_unique": unique_rows[col],
                "p_unique": unique_rows[col] / rows,
            },
        )
        for col in unique_rows.index
    ]

    return TestResults(
        category="data_quality",
        test_name="unique",
        params=test_params,
        passed=all([r.passed for r in results]),
        results=results,
    )


def zeros(df, config):
    rows = df.shape[0]
    typeset = ProfilingTypeSet(Settings())
    dataset_types = typeset.infer_type(df)
    results = []

    test_params = {
        "max_percent_threshold": config.zeros.max_percent_threshold,
    }

    for col in df.columns:
        # Only calculate zeros for numerical columns
        if str(dataset_types[col]) != "Numeric":
            continue

        value_counts = df[col].value_counts()

        if 0 not in value_counts.index:
            continue

        n_zeros = value_counts[0]
        p_zeros = n_zeros / rows

        results.append(
            TestResult(
                column=col,
                passed=p_zeros < test_params["max_percent_threshold"],
                values={
                    "n_zeros": n_zeros,
                    "p_zeros": p_zeros,
                },
            )
        )

    return TestResults(
        category="data_quality",
        test_name="zeros",
        params=test_params,
        passed=all([r.passed for r in results]),
        results=results,
    )
