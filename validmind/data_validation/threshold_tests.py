"""
Threshold based tests
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from dataclasses import dataclass
from pandas_profiling.config import Settings
from pandas_profiling.model.typeset import ProfilingTypeSet
from scipy import stats


from ..vm_models import Dataset, TestResult, Figure, ThresholdTest


@dataclass
class ClassImbalanceTest(ThresholdTest):
    """
    Test that the minority class does not represent more than a threshold
    of the total number of examples
    """

    category = "data_quality"
    name = "class_imbalance"
    default_params = {"min_percent_threshold": 0.2}

    def run(self):
        # Can only run this test if we have a Dataset object
        if not isinstance(self.dataset, Dataset):
            raise ValueError("ClassImbalanceTest requires a validmind Dataset object")

        if self.dataset.target_column is None:
            print("Skipping class_imbalance test because no target column is defined")
            return

        target_column = self.dataset.target_column
        imbalance_percentages = self.df[target_column].value_counts(normalize=True)

        # Does the minority class represent more than our threshold?
        passed = imbalance_percentages.min() > self.params["min_percent_threshold"]
        results = [
            TestResult(
                column=target_column,
                passed=passed,
                values=imbalance_percentages.to_dict(),
            )
        ]

        return self.cache_results(results, passed=passed)


@dataclass
class DuplicatesTest(ThresholdTest):
    """
    Test that the number of duplicates is less than a threshold
    """

    category = "data_quality"
    name = "duplicates"
    default_params = {"min_threshold": 1}

    def run(self):
        rows = self.df.shape[0]

        n_duplicates = len(self.df[self.df.duplicated(keep=False)])
        p_duplicates = n_duplicates / rows
        passed = n_duplicates < self.params["min_threshold"]

        results = [
            TestResult(
                passed=passed,
                values={"n_duplicates": n_duplicates, "p_duplicates": p_duplicates},
            )
        ]

        # Additionally, run duplicates test on fields that are primary keys
        primary_keys = []
        for field in self.dataset.fields:
            if field.get("type_options", None) and field.get("type_options").get(
                "primary_key", False
            ):
                primary_keys.append(field["id"])

        for col in primary_keys:
            col_n_duplicates = len(self.df[self.df[col].duplicated(keep=False)])
            col_p_duplicates = col_n_duplicates / rows
            col_passed = col_n_duplicates < self.params["min_threshold"]
            results.append(
                TestResult(
                    column=col,
                    passed=col_passed,
                    values={
                        "n_duplicates": col_n_duplicates,
                        "p_duplicates": col_p_duplicates,
                    },
                )
            )

        return self.cache_results(results, passed=all([r.passed for r in results]))


@dataclass
class HighCardinalityTest(ThresholdTest):
    """
    Test that the number of unique values in a column is less than a threshold
    """

    category = "data_quality"
    name = "cardinality"
    default_params = {
        "num_threshold": 100,
        "percent_threshold": 0.1,
        "threshold_type": "percent",  # or "num"
    }

    def run(self):
        typeset = ProfilingTypeSet(Settings())
        dataset_types = typeset.infer_type(self.df)

        results = []
        rows = self.df.shape[0]

        num_threshold = self.params["num_threshold"]
        if self.params["threshold_type"] == "percent":
            num_threshold = int(self.params["percent_threshold"] * rows)

        for col in self.df.columns:
            # Only calculate high cardinality for categorical columns
            if str(dataset_types[col]) != "Categorical":
                continue

            n_distinct = self.df[col].nunique()
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

        return self.cache_results(results, passed=all([r.passed for r in results]))


@dataclass
class HighPearsonCorrelationTest(ThresholdTest):
    """
    Test that the Pearson correlation between two columns is less than a threshold

    Inspired by: https://github.com/ydataai/pandas-profiling/blob/f8bad5dde27e3f87f11ac74fb8966c034bc22db8/src/pandas_profiling/model/correlations.py
    """

    category = "data_quality"
    name = "pearson_correlation"
    default_params = {"max_threshold": 0.3}

    def run(self):
        corr = self.df.corr()
        cols = corr.columns

        # Matrix of True/False where True means the correlation is above the threshold
        # Fill diagonal with False since all diagonal values are 1
        bool_index = abs(corr.values) >= self.params["max_threshold"]
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

        results = [
            TestResult(
                column=col,
                values={"correlations": correlations},
                passed=False,
            )
            for col, correlations in res.items()
        ]

        return self.cache_results(results, passed=passed)


@dataclass
class MissingValuesTest(ThresholdTest):
    """
    Test that the number of missing values is less than a threshold
    """

    category = "data_quality"
    name = "missing"
    default_params = {"min_threshold": 1}

    def run(self):
        rows = self.df.shape[0]

        missing = self.df.isna().sum()
        results = [
            TestResult(
                column=col,
                passed=missing[col] < self.params["min_threshold"],
                values={"n_missing": missing[col], "p_missing": missing[col] / rows},
            )
            for col in missing.index
        ]

        return self.cache_results(results, passed=all([r.passed for r in results]))


@dataclass
class SkewnessTest(ThresholdTest):
    """
    Test that the skewness of a column is less than a threshold
    """

    category = "data_quality"
    name = "skewness"
    default_params = {"max_threshold": 1}

    def run(self):
        typeset = ProfilingTypeSet(Settings())
        dataset_types = typeset.infer_type(self.df)

        skewness = self.df.skew(numeric_only=True)
        passed = all(abs(skewness) < self.params["max_threshold"])
        results = []

        for col in skewness.index:
            # Only calculate skewness for numerical columns
            if str(dataset_types[col]) != "Numeric":
                continue

            col_skewness = skewness[col]
            results.append(
                TestResult(
                    column=col,
                    passed=abs(col_skewness) < self.params["max_threshold"],
                    values={
                        "skewness": col_skewness,
                    },
                )
            )

        return self.cache_results(results, passed=passed)


@dataclass
class UniqueRowsTest(ThresholdTest):
    """
    Test that the number of unique rows is greater than a threshold
    """

    category = "data_quality"
    name = "unique"
    default_params = {"min_percent_threshold": 1}

    def run(self):
        rows = self.df.shape[0]

        unique_rows = self.df.nunique()
        results = [
            TestResult(
                column=col,
                passed=(unique_rows[col] / rows) < self.params["min_percent_threshold"],
                values={
                    "n_unique": unique_rows[col],
                    "p_unique": unique_rows[col] / rows,
                },
            )
            for col in unique_rows.index
        ]

        return self.cache_results(results, passed=all([r.passed for r in results]))


@dataclass
class ZerosTest(ThresholdTest):
    """
    Test that the number of zeros is less than a threshold
    """

    category = "data_quality"
    name = "zeros"
    default_params = {"max_percent_threshold": 0.03}

    def run(self):
        rows = self.df.shape[0]
        typeset = ProfilingTypeSet(Settings())
        dataset_types = typeset.infer_type(self.df)
        results = []

        for col in self.df.columns:
            # Only calculate zeros for numerical columns
            if str(dataset_types[col]) != "Numeric":
                continue

            value_counts = self.df[col].value_counts()

            if 0 not in value_counts.index:
                continue

            n_zeros = value_counts[0]
            p_zeros = n_zeros / rows

            results.append(
                TestResult(
                    column=col,
                    passed=p_zeros < self.params["max_percent_threshold"],
                    values={
                        "n_zeros": n_zeros,
                        "p_zeros": p_zeros,
                    },
                )
            )

        return self.cache_results(results, passed=all([r.passed for r in results]))


@dataclass
class OutliersTest(ThresholdTest):
    """
    Test that find outliers for time series data
    """

    category = "data_quality"
    name = "outliers"
    default_params = {"zscore_threshold": 3}

    def run(self):
        # Validate threshold paremeter
        if "zscore_threshold" not in self.params:
            raise ValueError("zscore_threshold must be provided in params")
        zscore_threshold = self.params["zscore_threshold"]

        typeset = ProfilingTypeSet(Settings())
        dataset_types = typeset.infer_type(self.df)
        test_results = []
        test_figures = []
        num_features_columns = [k for k, v in dataset_types.items() if str(v) == "Numeric"]

        outliers_table = self._identify_outliers(self.df[num_features_columns], zscore_threshold)
        fig = self._plot_outliers(self.df, outliers_table, use_subplots=False)
        passed = outliers_table.empty
        outliers_table["Date"] = outliers_table["Date"].astype(str)

        test_results.append(
            TestResult(
                test_name="outliers",
                passed=passed,
                values=outliers_table.to_dict(orient="list"),
            )
        )
        test_figures.append(Figure(key=self.name, figure=fig, metadata={}))

        return self.cache_results(test_results, passed=passed, figures=test_figures)

    def _identify_outliers(self, df, threshold):
        z_scores = pd.DataFrame(stats.zscore(df), index=df.index, columns=df.columns)
        outliers = z_scores[(z_scores.abs() > threshold).any(axis=1)]
        outlier_table = []
        for idx, row in outliers.iterrows():
            for col in df.columns:
                if abs(row[col]) > threshold:
                    outlier_table.append({"Variable": col, "z-score": row[col], "Threshold": threshold, "Date": idx})
        return pd.DataFrame(outlier_table)

    def _plot_outliers(self, df, outliers_table, use_subplots=True):
        sns.set(style="darkgrid")
        n_variables = len(df.columns)
        fig, axes = plt.subplots(n_variables, 1, figsize=(12, 3 * n_variables), sharex=True)

        for i, col in enumerate(df.columns):
            sns.lineplot(data=df, x=df.index, y=col, ax=axes[i], label=col)

            variable_outliers = outliers_table[outliers_table["Variable"] == col]
            for idx, row in variable_outliers.iterrows():
                date = row["Date"]
                outlier_value = df.loc[date, col]
                axes[i].scatter(date, outlier_value, marker="o", s=100, c="red",
                                label="Outlier" if idx == 0 else "")

            axes[i].legend()
            axes[i].set_ylabel("Value")
            axes[i].set_title(f"Time Series with Outliers for {col}")

        plt.xlabel("Date")
        plt.tight_layout()

        # Do this if you want to prevent the figure from being displayed
        plt.close("all")
        return fig
