# Core Library Tests

## Data Validation Tests

### Data Validation Metrics

Metrics functions for any Pandas-compatible datasets


### _class_ validmind.data_validation.metrics.DatasetMetadata(test_context: TestContext, params: dict | None = None, result: TestPlanDatasetResult | None = None)
Bases: `TestContextUtils`

Custom class to collect a set of descriptive statistics for a dataset.
This class will log dataset metadata via log_dataset instead of a metric.
Dataset metadat is necessary to initialize dataset object that can be related
to different metrics and test results


#### test_context(_: TestContex_ )

#### test_type(_: ClassVar[str_ _ = 'DatasetMetadata_ )

#### default_params(_: ClassVar[dict_ _ = {_ )

#### name(_ = 'dataset_metadata_ )

#### params(_: dic_ _ = Non_ )

#### result(_: TestPlanDatasetResul_ _ = Non_ )

#### run()
Just set the dataset to the result attribute of the test plan result
and it will be logged via the log_dataset function


### _class_ validmind.data_validation.metrics.DatasetCorrelations(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Extracts the correlation matrix for a dataset. The following coefficients
are calculated:
- Pearson’s R for numerical variables
- Cramer’s V for categorical variables
- Correlation ratios for categorical-numerical variables


#### type(_: ClassVar[str_ _ = 'dataset_ )

#### key(_: ClassVar[str_ _ = 'dataset_correlations_ )

#### run()
Run the metric calculation and cache its results


#### test_context(_: TestContex_ )

### _class_ validmind.data_validation.metrics.DatasetDescription(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Collects a set of descriptive statistics for a dataset


#### type(_: ClassVar[str_ _ = 'dataset_ )

#### key(_: ClassVar[str_ _ = 'dataset_description_ )

#### run()
Run the metric calculation and cache its results


#### test_context(_: TestContex_ )

### _class_ validmind.data_validation.metrics.TimeSeriesUnivariateInspectionRaw(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Generates a visual analysis of time series data by plotting the
raw time series. The input dataset can have multiple time series
if necessary. In this case we produce a separate plot for each time series.


#### type(_: ClassVar[str_ _ = 'dataset_ )

#### key(_: ClassVar[str_ _ = 'time_series_univariate_inspection_raw_ )

#### run()
Run the metric calculation and cache its results


#### test_context(_: TestContex_ )

### _class_ validmind.data_validation.metrics.TimeSeriesUnivariateInspectionHistogram(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Generates a visual analysis of time series data by plotting the
histogram. The input dataset can have multiple time series if
necessary. In this case we produce a separate plot for each time series.


#### type(_: ClassVar[str_ _ = 'dataset_ )

#### key(_: ClassVar[str_ _ = 'time_series_univariate_inspection_histogram_ )

#### run()
Run the metric calculation and cache its results


#### test_context(_: TestContex_ )
### Data Validation Threshold Tests

Threshold based tests


### _class_ validmind.data_validation.threshold_tests.ClassImbalanceTest(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

Test that the minority class does not represent more than a threshold
of the total number of examples


#### category(_: ClassVar[str_ _ = 'data_quality_ )

#### name(_: ClassVar[str_ _ = 'class_imbalance_ )

#### default_params(_: ClassVar[dict_ _ = {'min_percent_threshold': 0.2_ )

#### run()
Run the test and cache its results


#### test_context(_: TestContex_ )

### _class_ validmind.data_validation.threshold_tests.DuplicatesTest(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

Test that the number of duplicates is less than a threshold


#### category(_: ClassVar[str_ _ = 'data_quality_ )

#### name(_: ClassVar[str_ _ = 'duplicates_ )

#### default_params(_: ClassVar[dict_ _ = {'min_threshold': 1_ )

#### run()
Run the test and cache its results


#### test_context(_: TestContex_ )

### _class_ validmind.data_validation.threshold_tests.HighCardinalityTest(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

Test that the number of unique values in a column is less than a threshold


#### category(_: ClassVar[str_ _ = 'data_quality_ )

#### name(_: ClassVar[str_ _ = 'cardinality_ )

#### default_params(_: ClassVar[dict_ _ = {'num_threshold': 100, 'percent_threshold': 0.1, 'threshold_type': 'percent'_ )

#### run()
Run the test and cache its results


#### test_context(_: TestContex_ )

### _class_ validmind.data_validation.threshold_tests.HighPearsonCorrelationTest(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

Test that the Pearson correlation between two columns is less than a threshold

Inspired by: [https://github.com/ydataai/pandas-profiling/blob/f8bad5dde27e3f87f11ac74fb8966c034bc22db8/src/pandas_profiling/model/correlations.py](https://github.com/ydataai/pandas-profiling/blob/f8bad5dde27e3f87f11ac74fb8966c034bc22db8/src/pandas_profiling/model/correlations.py)


#### category(_: ClassVar[str_ _ = 'data_quality_ )

#### name(_: ClassVar[str_ _ = 'pearson_correlation_ )

#### default_params(_: ClassVar[dict_ _ = {'max_threshold': 0.3_ )

#### run()
Run the test and cache its results


#### test_context(_: TestContex_ )

### _class_ validmind.data_validation.threshold_tests.MissingValuesTest(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

Test that the number of missing values is less than a threshold


#### category(_: ClassVar[str_ _ = 'data_quality_ )

#### name(_: ClassVar[str_ _ = 'missing_ )

#### default_params(_: ClassVar[dict_ _ = {'min_threshold': 1_ )

#### run()
Run the test and cache its results


#### test_context(_: TestContex_ )

### _class_ validmind.data_validation.threshold_tests.SkewnessTest(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

Test that the skewness of a column is less than a threshold


#### category(_: ClassVar[str_ _ = 'data_quality_ )

#### name(_: ClassVar[str_ _ = 'skewness_ )

#### default_params(_: ClassVar[dict_ _ = {'max_threshold': 1_ )

#### run()
Run the test and cache its results


#### test_context(_: TestContex_ )

### _class_ validmind.data_validation.threshold_tests.UniqueRowsTest(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

Test that the number of unique rows is greater than a threshold


#### category(_: ClassVar[str_ _ = 'data_quality_ )

#### name(_: ClassVar[str_ _ = 'unique_ )

#### default_params(_: ClassVar[dict_ _ = {'min_percent_threshold': 1_ )

#### run()
Run the test and cache its results


#### test_context(_: TestContex_ )

### _class_ validmind.data_validation.threshold_tests.ZerosTest(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

Test that the number of zeros is less than a threshold


#### category(_: ClassVar[str_ _ = 'data_quality_ )

#### name(_: ClassVar[str_ _ = 'zeros_ )

#### default_params(_: ClassVar[dict_ _ = {'max_percent_threshold': 0.03_ )

#### run()
Run the test and cache its results


#### test_context(_: TestContex_ )
