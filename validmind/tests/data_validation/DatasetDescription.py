# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass
import numpy as np
from validmind.logging import get_logger


from validmind.vm_models import Metric

DEFAULT_HISTOGRAM_BINS = 10
DEFAULT_HISTOGRAM_BIN_SIZES = [5, 10, 20, 50]
logger = get_logger(__name__)


@dataclass
class DatasetDescription(Metric):
    """
    Collects a set of descriptive statistics for a dataset
    """

    name = "dataset_description"
    required_context = ["dataset"]

    def run(self):
        self.describe()
        # This will populate the "fields" attribute in the dataset object
        return self.cache_results(self.dataset.fields)

    def transformed_dataset(self, force_refresh=False):
        """
        Returns a transformed dataset that uses the features from vm_dataset.
        Some of the features in vm_dataset are of type Dummy so we need to
        reverse the one hot encoding and drop the individual dummy columns

        Args:
            force_refresh (bool, optional): Whether to force a refresh of the transformed dataset. Defaults to False.

        Returns:
            pd.DataFrame: The transformed dataset
        """

        # Get the list of features that are of type Dummy
        dataset_options = self.dataset.options
        dummy_variables = (
            dataset_options.get("dummy_variables", []) if dataset_options else []
        )
        # Exclude columns that have prefixes that are in the dummy feature list
        dummy_column_names = [
            column_name
            for column_name in self.dataset.df.columns
            if any(
                column_name.startswith(dummy_variable)
                for dummy_variable in dummy_variables
            )
        ]
        transformed_df = self.dataset.df.drop(dummy_column_names, axis=1)

        # Add reversed dummy features to the transformed dataset
        for dummy_variable in dummy_variables:
            columns_with_dummy_prefix = [
                col
                for col in self.raw_dataset.columns
                if col.startswith(dummy_variable)
            ]
            transformed_df[dummy_variable] = (
                self.dataset.df[columns_with_dummy_prefix]
                .idxmax(axis=1)
                .replace(f"{dummy_variable}[-_:]", "", regex=True)
            )

        return transformed_df

    def describe(self):
        """
        Extracts descriptive statistics for each field in the dataset
        """
        transformed_df = self.transformed_dataset()

        for ds_field in self.dataset.fields:
            self.describe_dataset_field(transformed_df, ds_field)

    def describe_dataset_field(self, df, field):
        """
        Gets descriptive statistics for a single field in a Pandas DataFrame.
        """
        field_type = field["type"]
        field_type_options = field.get("type_options", dict())

        # Force a categorical field when it's declared as a primary key
        if field_type_options.get("primary_key", False):
            field_type = "Categorical"
            field["type"] = "Categorical"

        # - When we call describe on one field at a time, Pandas will
        #   know better if it needs to report on numerical or categorical statistics
        # - Boolean (binary) fields should be reported as categorical
        #       (force to categorical when nunique == 2)
        if field_type == ["Boolean"] or df[field["id"]].nunique() == 2:
            top_value = df[field["id"]].value_counts().nlargest(1)

            field["statistics"] = {
                "count": df[field["id"]].count(),
                "unique": df[field["id"]].nunique(),
                "top": top_value.index[0],
                "freq": top_value.values[0],
            }
        elif field_type == "Numeric":
            field["statistics"] = (
                df[field["id"]]
                .describe(percentiles=[0.25, 0.5, 0.75, 0.9, 0.95])
                .to_dict()
            )
        elif field_type == "Categorical" or field_type == "Dummy":
            field["statistics"] = (
                df[field["id"]].astype("category").describe().to_dict()
            )

        # Initialize statistics object for non-numeric or categorical fields
        if "statistics" not in field:
            field["statistics"] = {}

        field["statistics"]["n_missing"] = df[field["id"]].isna().sum()
        field["statistics"]["missing"] = field["statistics"]["n_missing"] / len(
            df[field["id"]]
        )
        field["statistics"]["n_distinct"] = df[field["id"]].nunique()
        field["statistics"]["distinct"] = field["statistics"]["n_distinct"] / len(
            df[field["id"]]
        )

        field["histograms"] = self.get_field_histograms(df, field["id"], field_type)

    def get_field_histograms(self, df, field, type_):
        """
        Returns a collection of histograms for a numerical or categorical field.
        We store different combinations of bin sizes to allow analyzing the data better

        Will be used in favor of _get_histogram in the future
        """
        # Set the minimum number of bins to nunique if it's less than the default
        if type_ == "Numeric":
            return self.get_numerical_histograms(df, field)
        elif type_ == "Categorical" or type_ == "Boolean" or type_ == "Dummy":
            value_counts = df[field].value_counts()
            return {
                "default": {
                    "bin_size": len(value_counts),
                    "histogram": value_counts.to_dict(),
                }
            }
        elif type_ == "Null":
            logger.info(f"Ignoring histogram generation for null column {field}")
        else:
            raise ValueError(
                f"Unsupported field type found when computing its histogram: {type_}"
            )

    def get_numerical_histograms(self, df, field):
        """
        Returns a collection of histograms for a numerical field, each one
        with a different bin size
        """
        values = df[field].to_numpy()
        values_cleaned = values[~np.isnan(values)]

        # bins='sturges'. Cannot use 'auto' until we review and fix its performance
        #  on datasets with too many unique values
        #
        # 'sturges': R’s default method, only accounts for data size. Only optimal
        # for gaussian data and underestimates number of bins for large non-gaussian datasets.
        default_hist = np.histogram(values_cleaned, bins="sturges")

        histograms = {
            "default": {
                "bin_size": len(default_hist[0]),
                "histogram": {
                    "bin_edges": default_hist[1].tolist(),
                    "counts": default_hist[0].tolist(),
                },
            }
        }

        for bin_size in DEFAULT_HISTOGRAM_BIN_SIZES:
            hist = np.histogram(values_cleaned, bins=bin_size)
            histograms[f"bins_{bin_size}"] = {
                "bin_size": bin_size,
                "histogram": {
                    "bin_edges": hist[1].tolist(),
                    "counts": hist[0].tolist(),
                },
            }

        return histograms
