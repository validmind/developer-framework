# Core Library Tests

## Data Validation Tests

### Data Validation Metrics

Metrics functions for any Pandas-compatible datasets


### _class_ validmind.data_validation.metrics.DatasetMetadata(test_context: TestContext, params: dict | None = None, result: TestPlanDatasetResult | None = None)
Bases: `TestContextUtils`

Custom class to collect a set of descriptive statistics for a dataset.
This class will log dataset metadata via log_dataset instead of a metric.
Dataset metadata is necessary to initialize dataset object that can be related
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

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

#### run()
Run the metric calculation and cache its results


### _class_ validmind.data_validation.metrics.DatasetDescription(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Collects a set of descriptive statistics for a dataset


#### type(_: ClassVar[str_ _ = 'dataset_ )

#### key(_: ClassVar[str_ _ = 'dataset_description_ )

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

#### run()
Run the metric calculation and cache its results


### _class_ validmind.data_validation.metrics.DescriptiveStatistics(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Collects a set of descriptive statistics for a dataset, both for
numerical and categorical variables


#### type(_: ClassVar[str_ _ = 'dataset_ )

#### key(_: ClassVar[str_ _ = 'descriptive_statistics_ )

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

#### get_summary_statistics_numerical(numerical_fields)

#### get_summary_statistics_categorical(categorical_fields)

#### summary(metric_value)
Build two tables: one for summarizing numerical variables and one for categorical variables


#### run()
Run the metric calculation and cache its results


### _class_ validmind.data_validation.metrics.DatasetSplit(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Attempts to extract information about the dataset split from the
provided training, test and validation datasets.


#### type(_: ClassVar[str_ _ = 'dataset_ )

#### key(_: ClassVar[str_ _ = 'dataset_split_ )

#### required_context(_: ClassVar[List[str]_ _ = ['model'_ )

#### dataset_labels(_ = {'test_ds': 'Test', 'total': 'Total', 'train_ds': 'Training', 'validation_ds': 'Validation'_ )

#### description()
Return the metric description. Should be overridden by subclasses. Defaults
to returning the class’ docstring


#### summary(raw_results)
Returns a summarized representation of the dataset split information


#### run()
Run the metric calculation and cache its results


### _class_ validmind.data_validation.metrics.TimeSeriesLinePlot(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Generates a visual analysis of time series data by plotting the
raw time series. The input dataset can have multiple time series
if necessary. In this case we produce a separate plot for each time series.


#### type(_: ClassVar[str_ _ = 'dataset_ )

#### key(_: ClassVar[str_ _ = 'time_series_line_plot_ )

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

#### run()
Run the metric calculation and cache its results


### _class_ validmind.data_validation.metrics.TimeSeriesHistogram(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Generates a visual analysis of time series data by plotting the
histogram. The input dataset can have multiple time series if
necessary. In this case we produce a separate plot for each time series.


#### type(_: ClassVar[str_ _ = 'dataset_ )

#### key(_: ClassVar[str_ _ = 'time_series_histogram_ )

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

#### run()
Run the metric calculation and cache its results


### _class_ validmind.data_validation.metrics.ScatterPlot(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Generates a visual analysis of data by plotting a scatter plot matrix for all columns
in the dataset. The input dataset can have multiple columns (features) if necessary.


#### type(_: ClassVar[str_ _ = 'dataset_ )

#### key(_: ClassVar[str_ _ = 'scatter_plot_ )

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

#### run()
Run the metric calculation and cache its results


### _class_ validmind.data_validation.metrics.LaggedCorrelationHeatmap(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Generates a heatmap of correlations between the target variable and the lags of independent variables in the dataset.


#### type(_: ClassVar[str_ _ = 'dataset_ )

#### key(_: ClassVar[str_ _ = 'lagged_correlation_heatmap_ )

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

#### run()
Run the metric calculation and cache its results


### _class_ validmind.data_validation.metrics.AutoAR(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Automatically detects the AR order of a time series using both BIC and AIC.


#### type(_: ClassVar[str_ _ = 'dataset_ )

#### key(_: ClassVar[str_ _ = 'auto_ar_ )

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

#### run()
Run the metric calculation and cache its results


### _class_ validmind.data_validation.metrics.AutoMA(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Automatically detects the MA order of a time series using both BIC and AIC.


#### type(_: ClassVar[str_ _ = 'dataset_ )

#### key(_: ClassVar[str_ _ = 'auto_ma_ )

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

#### run()
Run the metric calculation and cache its results


### _class_ validmind.data_validation.metrics.SeasonalDecompose(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Calculates seasonal_decompose metric for each of the dataset features


#### type(_: ClassVar[str_ _ = 'dataset_ )

#### key(_: ClassVar[str_ _ = 'seasonal_decompose_ )

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

#### default_params(_: ClassVar[dict_ _ = {'seasonal_model': 'additive'_ )

#### store_seasonal_decompose(column, sd_one_column)
Stores the seasonal decomposition results in the test context so they
can be re-used by other tests. Note we store one sd at a time for every
column in the dataset.


#### serialize_seasonal_decompose(sd)
Serializes the seasonal decomposition results for one column into a
JSON serializable format that can be sent to the API.


#### run()
Run the metric calculation and cache its results


### _class_ validmind.data_validation.metrics.AutoSeasonality(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Automatically detects the optimal seasonal order for a time series dataset
using the seasonal_decompose method.


#### type(_: ClassVar[str_ _ = 'dataset_ )

#### key(_: ClassVar[str_ _ = 'auto_seasonality_ )

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

#### default_params(_: ClassVar[dict_ _ = {'max_period': 4, 'min_period': 1_ )

#### evaluate_seasonal_periods(series, min_period, max_period)

#### run()
Run the metric calculation and cache its results


### _class_ validmind.data_validation.metrics.ACFandPACFPlot(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Plots ACF and PACF for a given time series dataset.


#### type(_: ClassVar[str_ _ = 'evaluation_ )

#### key(_: ClassVar[str_ _ = 'acf_pacf_plot_ )

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

#### run()
Run the metric calculation and cache its results


### _class_ validmind.data_validation.metrics.AutoStationarity(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Automatically detects stationarity for each time series in a DataFrame
using the Augmented Dickey-Fuller (ADF) test.


#### type(_: ClassVar[str_ _ = 'dataset_ )

#### key(_: ClassVar[str_ _ = 'auto_stationarity_ )

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

#### default_params(_: ClassVar[dict_ _ = {'max_order': 5, 'threshold': 0.05_ )

#### run()
Run the metric calculation and cache its results


### _class_ validmind.data_validation.metrics.RollingStatsPlot(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

This class provides a metric to visualize the stationarity of a given time series dataset by plotting the rolling mean and rolling standard deviation. The rolling mean represents the average of the time series data over a fixed-size sliding window, which helps in identifying trends in the data. The rolling standard deviation measures the variability of the data within the sliding window, showing any changes in volatility over time. By analyzing these plots, users can gain insights into the stationarity of the time series data and determine if any transformations or differencing operations are required before applying time series models.


#### type(_: ClassVar[str_ _ = 'dataset_ )

#### key(_: ClassVar[str_ _ = 'rolling_stats_plot_ )

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

#### default_params(_: ClassVar[dict_ _ = {'window_size': 12_ )

#### _static_ plot_rolling_statistics(series, window_size=12, ax1=None, ax2=None)
Plot rolling mean and rolling standard deviation in different subplots for a given series.


* **Parameters**

    
    * **series** – Pandas Series with time-series data


    * **window_size** – Window size for the rolling calculations


    * **ax1** – Axis object for the rolling mean plot


    * **ax2** – Axis object for the rolling standard deviation plot



#### run()
Run the metric calculation and cache its results


### _class_ validmind.data_validation.metrics.EngleGrangerCoint(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Test for cointegration between pairs of time series variables in a given dataset using the Engle-Granger test.


#### type(_: ClassVar[str_ _ = 'dataset_ )

#### key(_: ClassVar[str_ _ = 'engle_granger_coint_ )

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

#### default_params(_: ClassVar[dict_ _ = {'threshold': 0.05_ )

#### run()
Run the metric calculation and cache its results


### _class_ validmind.data_validation.metrics.SpreadPlot(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

This class provides a metric to visualize the spread between pairs of time series variables in a given dataset. By plotting the spread of each pair of variables in separate figures, users can assess the relationship between the variables and determine if any cointegration or other time series relationships exist between them.


#### type(_: ClassVar[str_ _ = 'dataset_ )

#### key(_: ClassVar[str_ _ = 'spread_plot_ )

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

#### _static_ plot_spread(series1, series2, ax=None)
Plot the spread between two time series variables.


* **Parameters**

    
    * **series1** – Pandas Series with time-series data for the first variable


    * **series2** – Pandas Series with time-series data for the second variable


    * **ax** – Axis object for the spread plot



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

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

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

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

#### default_params(_: ClassVar[dict_ _ = {'min_threshold': 1_ )

#### run()
Run the test and cache its results


### _class_ validmind.data_validation.threshold_tests.HighCardinality(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

The high cardinality test measures the number of unique
values found in categorical columns.


#### category(_: ClassVar[str_ _ = 'data_quality_ )

#### name(_: ClassVar[str_ _ = 'cardinality_ )

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

#### default_params(_: ClassVar[dict_ _ = {'num_threshold': 100, 'percent_threshold': 0.1, 'threshold_type': 'percent'_ )

#### run()
Run the test and cache its results


### _class_ validmind.data_validation.threshold_tests.HighPearsonCorrelation(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

Test that the pairwise Pearson correlation coefficients between the
features in the dataset do not exceed a specified threshold.


#### category(_: ClassVar[str_ _ = 'data_quality_ )

#### name(_: ClassVar[str_ _ = 'pearson_correlation_ )

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

#### default_params(_: ClassVar[dict_ _ = {'max_threshold': 0.3_ )

#### run()
Run the test and cache its results


### _class_ validmind.data_validation.threshold_tests.MissingValues(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

Test that the number of missing values in the dataset across all features
is less than a threshold


#### category(_: ClassVar[str_ _ = 'data_quality_ )

#### name(_: ClassVar[str_ _ = 'missing_ )

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

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

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

#### default_params(_: ClassVar[dict_ _ = {'max_threshold': 1_ )

#### run()
Run the test and cache its results


### _class_ validmind.data_validation.threshold_tests.UniqueRows(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

Test that the number of unique rows is greater than a threshold


#### category(_: ClassVar[str_ _ = 'data_quality_ )

#### name(_: ClassVar[str_ _ = 'unique_ )

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

#### default_params(_: ClassVar[dict_ _ = {'min_percent_threshold': 1_ )

#### run()
Run the test and cache its results


### _class_ validmind.data_validation.threshold_tests.TooManyZeroValues(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

The zeros test finds columns that have too many zero values.


#### category(_: ClassVar[str_ _ = 'data_quality_ )

#### name(_: ClassVar[str_ _ = 'zeros_ )

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

#### default_params(_: ClassVar[dict_ _ = {'max_percent_threshold': 0.03_ )

#### run()
Run the test and cache its results


### _class_ validmind.data_validation.threshold_tests.TimeSeriesOutliers(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

Test that find outliers for time series data using the z-score method


#### category(_: ClassVar[str_ _ = 'data_quality_ )

#### name(_: ClassVar[str_ _ = 'time_series_outliers_ )

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

#### default_params(_: ClassVar[dict_ _ = {'zscore_threshold': 3_ )

#### run()
Run the test and cache its results


### _class_ validmind.data_validation.threshold_tests.TimeSeriesMissingValues(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

Test that the number of missing values is less than a threshold


#### category(_: ClassVar[str_ _ = 'data_quality_ )

#### name(_: ClassVar[str_ _ = 'time_series_missing_values_ )

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

#### default_params(_: ClassVar[dict_ _ = {'min_threshold': 1_ )

#### run()
Run the test and cache its results


### _class_ validmind.data_validation.threshold_tests.TimeSeriesFrequency(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

Test that detect frequencies in the data


#### category(_: ClassVar[str_ _ = 'data_quality_ )

#### name(_: ClassVar[str_ _ = 'time_series_frequency_ )

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

#### run()
Run the test and cache its results
