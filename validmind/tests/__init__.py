"""
Entrypoint to any validation test exposed by the SDK
"""
from .config import Settings
from .data_quality_pandas import (
    high_cardinality,
    duplicates,
)

config = Settings()


def run_tests(df, send=False):
    """
    Run all or a subset of tests on the given dataframe
    """
    results = []
    results.append(high_cardinality(df, config))
    results.append(duplicates(df, config))

    return results
