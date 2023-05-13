# Test Plans

Test Plans entry point


### validmind.test_plans.list_plans(pretty: bool = True)
Returns a list of all available test plans


### validmind.test_plans.list_tests(test_type: str = 'all', pretty: bool = True)
Returns a list of all available tests.


### validmind.test_plans.get_by_name(name: str)
Returns the test plan by name


### validmind.test_plans.describe_plan(plan_id: str)
Returns a description of the test plan


### validmind.test_plans.register_test_plan(plan_id: str, plan: TestPlan)
Registers a custom test plan

## Test Plans for SKLearn-Compatible Classifiers

## Test Plans for Tabular Datasets

Test plan for tabular datasets

Ideal setup is to have the API client to read a
custom test plan from the project’s configuration


### _class_ validmind.test_plans.tabular_datasets.TabularDatasetDescription(config: {} = None, test_context: TestContext = None, _test_plan_instances: List[object] = None, dataset: Dataset = None, model: Model = None, models: List[Model] = None, pbar: IntProgress = None, pbar_description: Label = None, pbar_box: HBox = None, summary: str = None)
Bases: `TestPlan`

Test plan to extract metadata and descriptive
statistics from a tabular dataset


#### name(_: ClassVar[str_ _ = 'tabular_dataset_description_ )

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

#### tests(_: ClassVar[List[object]_ _ = [<class 'validmind.data_validation.metrics.DatasetMetadata'>, <class 'validmind.data_validation.metrics.DatasetDescription'>, <class 'validmind.data_validation.metrics.DescriptiveStatistics'>, <class 'validmind.data_validation.metrics.DatasetCorrelations'>_ )

### _class_ validmind.test_plans.tabular_datasets.TabularDataQuality(config: {} = None, test_context: TestContext = None, _test_plan_instances: List[object] = None, dataset: Dataset = None, model: Model = None, models: List[Model] = None, pbar: IntProgress = None, pbar_description: Label = None, pbar_box: HBox = None, summary: str = None)
Bases: `TestPlan`

Test plan for data quality on tabular datasets


#### name(_: ClassVar[str_ _ = 'tabular_data_quality_ )

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

#### tests(_: ClassVar[List[object]_ _ = [<class 'validmind.data_validation.threshold_tests.ClassImbalance'>, <class 'validmind.data_validation.threshold_tests.Duplicates'>, <class 'validmind.data_validation.threshold_tests.HighCardinality'>, <class 'validmind.data_validation.threshold_tests.HighPearsonCorrelation'>, <class 'validmind.data_validation.threshold_tests.MissingValues'>, <class 'validmind.data_validation.threshold_tests.Skewness'>, <class 'validmind.data_validation.threshold_tests.UniqueRows'>, <class 'validmind.data_validation.threshold_tests.TooManyZeroValues'>_ )

### _class_ validmind.test_plans.tabular_datasets.TimeSeriesDataQuality(config: {} = None, test_context: TestContext = None, _test_plan_instances: List[object] = None, dataset: Dataset = None, model: Model = None, models: List[Model] = None, pbar: IntProgress = None, pbar_description: Label = None, pbar_box: HBox = None, summary: str = None)
Bases: `TestPlan`

Test plan for data quality on time series datasets


#### name(_: ClassVar[str_ _ = 'time_series_data_quality_ )

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

#### tests(_: ClassVar[List[object]_ _ = [<class 'validmind.data_validation.threshold_tests.TimeSeriesOutliers'>, <class 'validmind.data_validation.threshold_tests.TimeSeriesMissingValues'>, <class 'validmind.data_validation.threshold_tests.TimeSeriesFrequency'>_ )
