"""
Dataset class wrapper
"""
from dataclasses import dataclass, fields

from dython.nominal import associations

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
    # This is list of metadata objects for each field in the dataset. It does
    # not contain the actual data for each field, just metadata about it
    fields: list
    sample: list
    shape: dict
    correlation_matrix: object = None
    correlations: dict = None
    type: str = None
    options: dict = None
    statistics: dict = None

    # Specify targets via DatasetTargets or via target_column and class_labels
    targets: dict = None
    target_column: str = ""
    class_labels: dict = None

    _feature_lookup: dict = None
    _transformed_df: object = None

    def __post_init__(self):
        """
        Set target_column and class_labels from DatasetTargets
        """
        self._feature_lookup = {}

        if self.targets:
            self.target_column = self.targets.target_column
            self.class_labels = self.targets.class_labels

    @property
    def df(self):
        """
        Returns the raw Pandas DataFrame
        """
        return self.raw_dataset

    @property
    def x(self):
        """
        Returns the dataset's features
        """
        return self.raw_dataset.drop(self.target_column, axis=1)

    @property
    def y(self):
        """
        Returns the dataset's target column
        """
        return self.raw_dataset[self.target_column]

    @property
    def index(self):
        """
        Returns the dataset's index.
        """
        return self.raw_dataset.index

    @property
    def isnull(self):
        """
        Returns True if there are any null values in the dataset or the index, False otherwise.
        """
        return (
            self.raw_dataset.isnull().values.any()
            or self.raw_dataset.index.isnull().any()
        )

    @property
    def copy(self):
        """
        Returns a copy of the raw_dataset.
        """
        return self.raw_dataset.copy()

    def drop_columns(self, columns_to_drop):
        """
        Drop specified columns of the raw_dataset.
        """
        modified_dataset = self.raw_dataset.copy()
        modified_dataset = modified_dataset.drop(columns=columns_to_drop)
        return modified_dataset

    def get_feature_by_id(self, feature_id):
        """
        Returns the feature with the given id. We also build a lazy
        lookup cache in case the same feature is requested multiple times.

        Args:
            feature_id (str): The id of the feature to return

        Raises:
            ValueError: If the feature with the given id does not exist

        Returns:
            dict: The feature with the given id
        """
        if feature_id not in self._feature_lookup:
            for feature in self.fields:
                if feature["id"] == feature_id:
                    self._feature_lookup[feature_id] = feature
                    return feature
            raise ValueError(f"Feature with id {feature_id} does not exist")

        return self._feature_lookup[feature_id]

    def get_feature_type(self, feature_id):
        """
        Returns the type of the feature with the given id

        Args:
            feature_id (str): The id of the feature to return

        Returns:
            str: The type of the feature with the given id
        """
        feature = self.get_feature_by_id(feature_id)
        return feature["type"]

    def get_features_columns(self):
        """
        Returns list of features columns

        Returns:
            list: The list of features columns
        """
        return [
            field_dic["id"]
            for field_dic in self.fields
            if (field_dic["id"] != self.target_column)
        ]

    def get_numeric_features_columns(self):
        """
        Returns list of numeric features columns

        Returns:
            list: The list of numberic features columns
        """
        return [
            field_dic["id"]
            for field_dic in self.fields
            if (
                field_dic["type"] == "Numeric" and field_dic["id"] != self.target_column
            )
        ]

    def get_categorical_features_columns(self):
        """
        Returns list of categorical features columns

        Returns:
            list: The list of categorical features columns
        """
        return [
            field_dic["id"]
            for field_dic in self.fields
            if (
                field_dic["type"] == "Categorical"
                and field_dic["id"] != self.target_column
            )
        ]

    def serialize(self):
        """
        Serializes the model to a dictionary so it can be sent to the API
        """
        dataset_dict = {
            "shape": self.shape,
            "type": self.type,
        }

        # Dataset with no targets can be logged
        if self.targets:
            dataset_dict["targets"] = self.targets.__dict__
        else:
            dataset_dict["targets"] = {
                "target_column": self.target_column,
                "class_labels": self.class_labels,
            }

        return dataset_dict

    def describe(self):
        """
        Extracts descriptive statistics for each field in the dataset
        """
        transformed_df = self.transformed_dataset

        for ds_field in self.fields:
            describe_dataset_field(transformed_df, ds_field)

    def get_correlations(self):
        """
        Extracts correlations for each field in the dataset
        """
        # Ignore fields that have very high cardinality
        fields_for_correlation = []
        for ds_field in self.fields:
            if "statistics" in ds_field and "distinct" in ds_field["statistics"]:
                if ds_field["statistics"]["distinct"] < 0.1:
                    fields_for_correlation.append(ds_field["id"])

        self.correlation_matrix = associations(
            self.transformed_dataset[fields_for_correlation],
            compute_only=True,
            plot=False,
        )["corr"]

        # Transform to the current format expected by the UI
        self.correlations = [
            [
                {
                    "field": key,
                    "value": value,
                }
                for key, value in correlation_row.items()
            ]
            for correlation_row in self.correlation_matrix.to_dict(orient="records")
        ]

    def get_correlation_plots(self, n_top=15):
        """
        Extracts correlation plots for the n_top correlations in the dataset

        Args:
            n_top (int, optional): The number of top correlations to extract. Defaults to 15.

        Returns:
            list: A list of correlation plots
        """
        correlation_plots = generate_correlation_plots(self, n_top)
        return correlation_plots

    @property
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
        if self._transformed_df is not None and force_refresh is False:
            return self._transformed_df

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
        """
        Creates a Dataset object from a dictionary

        Args:
            dict_ (dict): The dictionary to create the Dataset object from

        Returns:
            Dataset: The Dataset object
        """
        class_fields = {f.name for f in fields(cls)}
        return Dataset(**{k: v for k, v in dict_.items() if k in class_fields})

    # TODO: Accept variable descriptions from framework
    # TODO: Accept type overrides from framework
    @classmethod
    def init_from_pd_dataset(
        cls, df, options=None, targets=None, target_column=None, class_labels=None
    ):
        """
        Initializes a Dataset object from a pandas DataFrame

        Args:
            df (pd.DataFrame): The pandas DataFrame to initialize the Dataset object from
            options (dict, optional): The options to use when initializing the Dataset object. Defaults to None.
            targets (list, optional): The targets to use when initializing the Dataset object. Defaults to None.
            target_column (str, optional): The target column to use when initializing the Dataset object. Defaults to None.
            class_labels (list, optional): The class labels to use when initializing the Dataset object. Defaults to None.

        Returns:
            Dataset: The Dataset object
        """
        print("Inferring dataset types...")
        vm_dataset_variables = parse_dataset_variables(df, options)

        shape = {
            "rows": df.shape[0],
            "columns": df.shape[1],
        }
        df_head = df.head().to_dict(orient="records")
        df_tail = df.tail().to_dict(orient="records")

        # TODO: validate with target_column and class_labels
        if targets:
            validate_pd_dataset_targets(df, targets)

        return Dataset(
            raw_dataset=df,
            fields=vm_dataset_variables,
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
            target_column=target_column,
            class_labels=class_labels,
            options=options,
        )
