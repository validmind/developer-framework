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


### _class_ validmind.data_validation.metrics.DatasetDescription(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Collects a set of descriptive statistics for a dataset


#### type(_: ClassVar[str_ _ = 'dataset_ )

#### key(_: ClassVar[str_ _ = 'dataset_description_ )

#### run()
Run the metric calculation and cache its results


### _class_ validmind.data_validation.metrics.TimeSeriesLinePlot(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Generates a visual analysis of time series data by plotting the
raw time series. The input dataset can have multiple time series
if necessary. In this case we produce a separate plot for each time series.


#### type(_: ClassVar[str_ _ = 'dataset_ )

#### key(_: ClassVar[str_ _ = 'time_series_line_plot_ )

#### run()
Run the metric calculation and cache its results


### _class_ validmind.data_validation.metrics.TimeSeriesHistogram(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Generates a visual analysis of time series data by plotting the
histogram. The input dataset can have multiple time series if
necessary. In this case we produce a separate plot for each time series.


#### type(_: ClassVar[str_ _ = 'dataset_ )

#### key(_: ClassVar[str_ _ = 'time_series_histogram_ )

#### run()
Run the metric calculation and cache its results


### _class_ validmind.data_validation.metrics.ScatterPlot(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Generates a visual analysis of data by plotting a scatter plot matrix for all columns
in the dataset. The input dataset can have multiple columns (features) if necessary.


#### type(_: ClassVar[str_ _ = 'dataset_ )

#### key(_: ClassVar[str_ _ = 'scatter_plot_ )

#### run()
Run the metric calculation and cache its results


### _class_ validmind.data_validation.metrics.LaggedCorrelationHeatmap(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Generates a heatmap of correlations between the target variable and the lags of independent variables in the dataset.


#### type(_: ClassVar[str_ _ = 'dataset_ )

#### key(_: ClassVar[str_ _ = 'lagged_correlation_heatmap_ )

#### run()
Run the metric calculation and cache its results


### _class_ validmind.data_validation.metrics.AutoAR(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Automatically detects the AR order of a time series using both BIC and AIC.


#### type(_: ClassVar[str_ _ = 'dataset_ )

#### key(_: ClassVar[str_ _ = 'auto_ar_ )

#### run()
Run the metric calculation and cache its results


### _class_ validmind.data_validation.metrics.AutoMA(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Automatically detects the MA order of a time series using both BIC and AIC.


#### type(_: ClassVar[str_ _ = 'dataset_ )

#### key(_: ClassVar[str_ _ = 'auto_ma_ )

#### run()
Run the metric calculation and cache its results

### Data Validation Threshold Tests

Threshold based tests


### _class_ validmind.data_validation.threshold_tests.ClassImbalance(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

The class imbalance test measures the disparity between the majority
class and the minority class in the target column.


#### category(_: ClassVar[str_ _ = 'data_quality_ )

#### name(_: ClassVar[str_ _ = 'class_imbalance_ )

#### default_params(_: ClassVar[dict_ _ = {'min_percent_threshold': 0.2_ )

#### run()
Run the test and cache its results


### _class_ validmind.data_validation.threshold_tests.Duplicates(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

The duplicates test measures the number of duplicate rows found in
the dataset. If a primary key column is specified, the dataset is
checked for duplicate primary keys as well.


#### category(_: ClassVar[str_ _ = 'data_quality_ )

#### name(_: ClassVar[str_ _ = 'duplicates_ )

#### default_params(_: ClassVar[dict_ _ = {'min_threshold': 1_ )

#### run()
Run the test and cache its results


### _class_ validmind.data_validation.threshold_tests.HighCardinality(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

The high cardinality test measures the number of unique
values found in categorical columns.


#### category(_: ClassVar[str_ _ = 'data_quality_ )

#### name(_: ClassVar[str_ _ = 'cardinality_ )

#### default_params(_: ClassVar[dict_ _ = {'num_threshold': 100, 'percent_threshold': 0.1, 'threshold_type': 'percent'_ )

#### run()
Run the test and cache its results


### _class_ validmind.data_validation.threshold_tests.HighPearsonCorrelation(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

Test that the pairwise Pearson correlation coefficients between the
features in the dataset do not exceed a specified threshold.


#### category(_: ClassVar[str_ _ = 'data_quality_ )

#### name(_: ClassVar[str_ _ = 'pearson_correlation_ )

#### default_params(_: ClassVar[dict_ _ = {'max_threshold': 0.3_ )

#### run()
Run the test and cache its results


### _class_ validmind.data_validation.threshold_tests.MissingValues(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

Test that the number of missing values in the dataset across all features
is less than a threshold


#### category(_: ClassVar[str_ _ = 'data_quality_ )

#### name(_: ClassVar[str_ _ = 'missing_ )

#### default_params(_: ClassVar[dict_ _ = {'min_threshold': 1_ )

#### run()
Run the test and cache its results


### _class_ validmind.data_validation.threshold_tests.Skewness(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

The skewness test measures the extent to which a distribution of
values differs from a normal distribution. A positive skew describes
a longer tail of values in the right and a negative skew describes a
longer tail of values in the left.


#### category(_: ClassVar[str_ _ = 'data_quality_ )

#### name(_: ClassVar[str_ _ = 'skewness_ )

#### default_params(_: ClassVar[dict_ _ = {'max_threshold': 1_ )

#### run()
Run the test and cache its results


### _class_ validmind.data_validation.threshold_tests.UniqueRows(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

Test that the number of unique rows is greater than a threshold


#### category(_: ClassVar[str_ _ = 'data_quality_ )

#### name(_: ClassVar[str_ _ = 'unique_ )

#### default_params(_: ClassVar[dict_ _ = {'min_percent_threshold': 1_ )

#### run()
Run the test and cache its results


### _class_ validmind.data_validation.threshold_tests.TooManyZeroValues(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

The zeros test finds columns that have too many zero values.


#### category(_: ClassVar[str_ _ = 'data_quality_ )

#### name(_: ClassVar[str_ _ = 'zeros_ )

#### default_params(_: ClassVar[dict_ _ = {'max_percent_threshold': 0.03_ )

#### run()
Run the test and cache its results


### _class_ validmind.data_validation.threshold_tests.OutliersTest(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

Test that find outliers for time series data using the z-score method


#### category(_: ClassVar[str_ _ = 'data_quality_ )

#### name(_: ClassVar[str_ _ = 'time_series_outliers_ )

#### default_params(_: ClassVar[dict_ _ = {'zscore_threshold': 3_ )

#### run()
Run the test and cache its results


### _class_ validmind.data_validation.threshold_tests.TimeSeriesMissingValuesTest(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

Test that the number of missing values is less than a threshold


#### category(_: ClassVar[str_ _ = 'data_quality_ )

#### name(_: ClassVar[str_ _ = 'time_series_missing_values_ )

#### default_params(_: ClassVar[dict_ _ = {'min_threshold': 1_ )

#### run()
Run the test and cache its results
