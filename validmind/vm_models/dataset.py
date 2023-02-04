"""
Dataset class wrapper
"""
from dataclasses import dataclass, field, fields

from .dataset_utils import (
    describe_dataset_field,
    generate_correlation_plots,
    parse_dataset_variables,
    validate_pd_dataset_targets,
)


@dataclass()
class DatasetTargets:
    """
    Dataset targets definition
    """

    target_column: str
    description: str = None
    class_labels: dict = None


@dataclass()
class Dataset:
    """
    Model class wrapper
    """

    raw_dataset: object
    fields: list
    variables: list
    sample: list
    shape: dict
    correlation_matrix: object = None
    correlations: dict = None
    type: str = None
    options: dict = None
    statistics: dict = None
    targets: dict = None
    __feature_lookup: dict = field(default_factory=dict)
    __transformed_df: object = None

    def get_feature_by_id(self, feature_id):
        """
        Returns the feature with the given id. We also build a lazy
        lookup cache in case the same feature is requested multiple times.
        """
        if feature_id not in self.__feature_lookup:
            for feature in self.fields:
                if feature["id"] == feature_id:
                    self.__feature_lookup[feature_id] = feature
                    return feature
            raise ValueError(f"Feature with id {feature_id} does not exist")

        return self.__feature_lookup[feature_id]

    def get_feature_type(self, feature_id):
        """
        Returns the type of the feature with the given id
        """
        feature = self.get_feature_by_id(feature_id)
        return feature["type"]

    def serialize(self):
        """
        Serializes the model to a dictionary so it can be sent to the API
        """
        dataset_dict = {
            "correlations": {
                # TODO: generalize this
                "pearson": self.correlations,
            },
            "fields": self.fields,
            "sample": self.sample,
            "shape": self.shape,
            "statistics": self.statistics,
            "type": self.type,
        }

        # Dataset with no targets can be logged
        if self.targets:
            dataset_dict["targets"] = self.targets.__dict__

        return dataset_dict

    def describe(self):
        """
        Extracts descriptive statistics for each field in the dataset
        """
        transformed_df = self.transformed_dataset

        for ds_field in self.fields:
            describe_dataset_field(transformed_df, ds_field)

    # def get_correlations(self):
    #     """
    #     Extracts correlations for each field in the dataset
    #     """
    #     # Ignore fields that have very high cardinality
    #     fields_for_correlation = []
    #     for ds_field in self.fields:
    #         if "statistics" in ds_field and "distinct" in ds_field["statistics"]:
    #             if ds_field["statistics"]["distinct"] < 0.1:
    #                 fields_for_correlation.append(ds_field["id"])

    #     self.correlation_matrix = associations(
    #         self.transformed_dataset[fields_for_correlation],
    #         compute_only=True,
    #         plot=False,
    #     )["corr"]

    #     # Transform to the current format expected by the UI
    #     n = len(self.raw_dataset)
    #     self.correlations = [
    #         [
    #             {
    #                 "field": key,
    #                 "value": value,
    #                 # For simplicity we calculate it for every pair but
    #                 # it only applies to Pearson correlation
    #                 "p_value": correlation_significance(value, n),
    #             }
    #             for key, value in correlation_row.items()
    #         ]
    #         for correlation_row in self.correlation_matrix.to_dict(orient="records")
    #     ]

    def get_correlation_plots(self, n_top=15):
        """
        Extracts correlation plots for the n_top correlations in the dataset
        """
        correlation_plots = generate_correlation_plots(self, n_top)
        return correlation_plots

    @property
    def transformed_dataset(self, force_refresh=False):
        """
        Returns a transformed dataset that uses the features from vm_dataset.
        Some of the features in vm_dataset are of type Dummy so we need to
        reverse the one hot encoding and drop the individual dummy columns
        """
        if self.__transformed_df is not None and force_refresh is False:
            return self.__transformed_df

        print("Preparing in-memory dataset copy...")

        # Get the list of features that are of type Dummy
        dataset_options = self.options
        dummy_variables = (
            dataset_options.get("dummy_variables", []) if dataset_options else []
        )
        # Exclude columns that have prefixes that are in the dummy feature list
        dummy_column_names = [
            column_name
            for column_name in self.raw_dataset.columns
            if any(
                column_name.startswith(dummy_variable)
                for dummy_variable in dummy_variables
            )
        ]
        transformed_df = self.raw_dataset.drop(dummy_column_names, axis=1)

        # Add reversed dummy features to the transformed dataset
        for dummy_variable in dummy_variables:
            columns_with_dummy_prefix = [
                col
                for col in self.raw_dataset.columns
                if col.startswith(dummy_variable)
            ]
            transformed_df[dummy_variable] = (
                self.raw_dataset[columns_with_dummy_prefix]
                .idxmax(axis=1)
                .replace(f"{dummy_variable}[-_:]", "", regex=True)
            )

        return transformed_df

    @classmethod
    def create_from_dict(cls, dict_):
        class_fields = {f.name for f in fields(cls)}
        return Dataset(**{k: v for k, v in dict_.items() if k in class_fields})

    # TODO: Accept variable descriptions from framework
    # TODO: Accept type overrides from framework
    @classmethod
    def init_from_pd_dataset(cls, df, options=None, targets=None):
        print("Inferring dataset types...")
        vm_dataset_variables = parse_dataset_variables(df, options)

        shape = {
            "rows": df.shape[0],
            "columns": df.shape[1],
        }
        df_head = df.head().to_dict(orient="records")
        df_tail = df.tail().to_dict(orient="records")

        if targets:
            validate_pd_dataset_targets(df, targets)

        return Dataset(
            raw_dataset=df,
            fields=vm_dataset_variables,  # TODO - deprecate naming in favor of variables
            variables=vm_dataset_variables,
            sample=[
                {
                    "id": "head",
                    "data": df_head,
                },
                {
                    "id": "tail",
                    "data": df_tail,
                },
            ],
            shape=shape,
            targets=targets,
            options=options,
        )
