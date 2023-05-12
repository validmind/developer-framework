# ValidMind Models

Models entrypoint


### _class_ validmind.vm_models.Dataset(raw_dataset: object, fields: list, sample: list, shape: dict, correlation_matrix: object | None = None, correlations: dict | None = None, type: str | None = None, options: dict | None = None, statistics: dict | None = None, targets: dict | None = None, target_column: str = '', class_labels: dict | None = None, _Dataset__feature_lookup: dict = <factory>, _Dataset__transformed_df: object | None = None)
Bases: `object`

Model class wrapper


#### raw_dataset(_: objec_ )

#### fields(_: lis_ )

#### sample(_: lis_ )

#### shape(_: dic_ )

#### correlation_matrix(_: objec_ _ = Non_ )

#### correlations(_: dic_ _ = Non_ )

#### type(_: st_ _ = Non_ )

#### options(_: dic_ _ = Non_ )

#### statistics(_: dic_ _ = Non_ )

#### targets(_: dic_ _ = Non_ )

#### target_column(_: st_ _ = '_ )

#### class_labels(_: dic_ _ = Non_ )

#### _property_ df()
Returns the raw Pandas DataFrame


#### _property_ x()
Returns the dataset’s features


#### _property_ y()
Returns the dataset’s target column


#### _property_ index()
Returns the dataset’s index.


#### get_feature_by_id(feature_id)
Returns the feature with the given id. We also build a lazy
lookup cache in case the same feature is requested multiple times.


* **Parameters**

    **feature_id** (*str*) – The id of the feature to return



* **Raises**

    **ValueError** – If the feature with the given id does not exist



* **Returns**

    The feature with the given id



* **Return type**

    dict



#### get_feature_type(feature_id)
Returns the type of the feature with the given id


* **Parameters**

    **feature_id** (*str*) – The id of the feature to return



* **Returns**

    The type of the feature with the given id



* **Return type**

    str



#### get_numeric_features_columns()
Returns list of numeric features columns


* **Returns**

    The list of numberic features columns



* **Return type**

    list



#### get_categorical_features_columns()
Returns list of categorical features columns


* **Returns**

    The list of categorical features columns



* **Return type**

    list



#### serialize()
Serializes the model to a dictionary so it can be sent to the API


#### describe()
Extracts descriptive statistics for each field in the dataset


#### get_correlations()
Extracts correlations for each field in the dataset


#### get_correlation_plots(n_top=15)
Extracts correlation plots for the n_top correlations in the dataset


* **Parameters**

    **n_top** (*int**, **optional*) – The number of top correlations to extract. Defaults to 15.



* **Returns**

    A list of correlation plots



* **Return type**

    list



#### _property_ transformed_dataset()
Returns a transformed dataset that uses the features from vm_dataset.
Some of the features in vm_dataset are of type Dummy so we need to
reverse the one hot encoding and drop the individual dummy columns


* **Parameters**

    **force_refresh** (*bool**, **optional*) – Whether to force a refresh of the transformed dataset. Defaults to False.



* **Returns**

    The transformed dataset



* **Return type**

    pd.DataFrame



#### _classmethod_ create_from_dict(dict_)
Creates a Dataset object from a dictionary


* **Parameters**

    **dict** (*dict*) – The dictionary to create the Dataset object from



* **Returns**

    The Dataset object



* **Return type**

    Dataset



#### _classmethod_ init_from_pd_dataset(df, options=None, targets=None, target_column=None, class_labels=None)
Initializes a Dataset object from a pandas DataFrame


* **Parameters**

    
    * **df** (*pd.DataFrame*) – The pandas DataFrame to initialize the Dataset object from


    * **options** (*dict**, **optional*) – The options to use when initializing the Dataset object. Defaults to None.


    * **targets** (*list**, **optional*) – The targets to use when initializing the Dataset object. Defaults to None.


    * **target_column** (*str**, **optional*) – The target column to use when initializing the Dataset object. Defaults to None.


    * **class_labels** (*list**, **optional*) – The class labels to use when initializing the Dataset object. Defaults to None.



* **Returns**

    The Dataset object



* **Return type**

    Dataset



### _class_ validmind.vm_models.DatasetTargets(target_column: str, description: str | None = None, class_labels: dict | None = None)
Bases: `object`

Dataset targets definition


#### target_column(_: st_ )

#### description(_: st_ _ = Non_ )

#### class_labels(_: dic_ _ = Non_ )

### _class_ validmind.vm_models.Figure(key: str, metadata: dict, figure: object, extras: dict | None = None)
Bases: `object`

Figure objects track the schema supported by the ValidMind API


#### key(_: st_ )

#### metadata(_: dic_ )

#### figure(_: objec_ )

#### extras(_: dict | Non_ _ = Non_ )

#### serialize()
Serializes the Figure to a dictionary so it can be sent to the API


### _class_ validmind.vm_models.Metric(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `TestContextUtils`

Metric objects track the schema supported by the ValidMind API

TODO: Metric should validate required context too


#### test_context(_: TestContex_ )

#### test_type(_: ClassVar[str_ _ = 'Metric_ )

#### type(_: ClassVar[str_ _ = '_ )

#### scope(_: ClassVar[str_ _ = '_ )

#### key(_: ClassVar[str_ _ = '_ )

#### value_formatter(_: ClassVar[str | None_ _ = Non_ )

#### default_params(_: ClassVar[dict_ _ = {_ )

#### params(_: dic_ _ = Non_ )

#### result(_: TestPlanMetricResul_ _ = Non_ )

#### _property_ name()

#### description()
Return the metric description. Should be overridden by subclasses. Defaults
to returning the class’ docstring


#### summary(metric_value: dict | list | DataFrame | None = None)
Return the metric summary. Should be overridden by subclasses. Defaults to None.
The metric summary allows renderers (e.g. Word and ValidMind UI) to display a
short summary of the metric results.

We return None here because the metric summary is optional.


#### run(\*args, \*\*kwargs)
Run the metric calculation and cache its results


#### cache_results(metric_value: dict | list | DataFrame | None = None, figures: List[Figure] | None = None)
Cache the results of the metric calculation and do any post-processing if needed


* **Parameters**

    
    * **metric_value** (*Union**[**dict**, **list**, **pd.DataFrame**]*) – The value of the metric


    * **figures** (*Optional**[**object**]*) – Any figures to attach to the test plan result



* **Returns**

    The test plan result object



* **Return type**

    TestPlanResult



#### required_context(_: ClassVar[List[str]_ )

### _class_ validmind.vm_models.MetricResult(type: str, scope: str, key: dict, value: dict | list | DataFrame, summary: ResultSummary | None = None, value_formatter: str | None = None)
Bases: `object`

MetricResult class definition. A MetricResult is returned by any internal method
that extracts metrics from a dataset or model, and returns 1) Metric and Figure
objects that can be sent to the API and 2) and plots and metadata for display purposes


#### type(_: st_ )

#### scope(_: st_ )

#### key(_: dic_ )

#### value(_: dict | list | DataFram_ )

#### summary(_: ResultSummary | Non_ _ = Non_ )

#### value_formatter(_: str | Non_ _ = Non_ )

#### serialize()
Serializes the Metric to a dictionary so it can be sent to the API


### _class_ validmind.vm_models.Model(attributes: ModelAttributes | None = None, task: str | None = None, subtask: str | None = None, params: dict | None = None, model_id: str = 'main', model: object | None = None, train_ds: Dataset | None = None, test_ds: Dataset | None = None, validation_ds: Dataset | None = None, y_train_predict: object | None = None, y_test_predict: object | None = None, y_validation_predict: object | None = None)
Bases: `object`

A class that wraps a trained model instance and its associated data.


#### attributes()
The attributes of the model. Defaults to None.


* **Type**

    ModelAttributes, optional



#### task()
The task that the model is intended to solve. Defaults to None.


* **Type**

    str, optional



#### subtask()
The subtask that the model is intended to solve. Defaults to None.


* **Type**

    str, optional



#### params()
The parameters of the model. Defaults to None.


* **Type**

    dict, optional



#### model_id()
The identifier of the model. Defaults to “main”.


* **Type**

    str



#### model()
The trained model instance. Defaults to None.


* **Type**

    object, optional



#### train_ds()
The training dataset. Defaults to None.


* **Type**

    Dataset, optional



#### test_ds()
The test dataset. Defaults to None.


* **Type**

    Dataset, optional



#### validation_ds()
The validation dataset. Defaults to None.


* **Type**

    Dataset, optional



#### y_train_predict()
The predicted outputs for the training dataset. Defaults to None.


* **Type**

    object, optional



#### y_test_predict()
The predicted outputs for the test dataset. Defaults to None.


* **Type**

    object, optional



#### y_validation_predict()
The predicted outputs for the validation dataset. Defaults to None.


* **Type**

    object, optional



#### attributes(_: ModelAttribute_ _ = Non_ )

#### task(_: st_ _ = Non_ )

#### subtask(_: st_ _ = Non_ )

#### params(_: dic_ _ = Non_ )

#### model_id(_: st_ _ = 'main_ )

#### model(_: objec_ _ = Non_ )

#### train_ds(_: Datase_ _ = Non_ )

#### test_ds(_: Datase_ _ = Non_ )

#### validation_ds(_: Datase_ _ = Non_ )

#### y_train_predict(_: objec_ _ = Non_ )

#### y_test_predict(_: objec_ _ = Non_ )

#### y_validation_predict(_: objec_ _ = Non_ )

#### serialize()
Serializes the model to a dictionary so it can be sent to the API


#### class_predictions(y_predict)
Converts a set of probability predictions to class predictions


* **Parameters**

    **y_predict** (*np.array**, **pd.DataFrame*) – Predictions to convert



* **Returns**

    Class predictions



* **Return type**

    (np.array, pd.DataFrame)



#### predict(\*args, \*\*kwargs)
Predict method for the model. This is a wrapper around the model’s
predict_proba (for classification) or predict (for regression) method

NOTE: This only works for sklearn or xgboost models at the moment


#### _static_ model_library(model)
Returns the model library name


#### _static_ model_class(model)
Returns the model class name


#### _static_ is_supported_model(model)
Checks if the model is supported by the API


* **Parameters**

    **model** (*object*) – The trained model instance to check



* **Returns**

    True if the model is supported, False otherwise



* **Return type**

    bool



#### _classmethod_ init_vm_model(model, train_ds, test_ds, validation_ds, attributes)
Initializes a model instance from the provided data.


#### _classmethod_ create_from_dict(dict_)
Creates a Model instance from a dictionary


* **Parameters**

    **dict** (*dict*) – The dictionary to create the Model instance from



* **Returns**

    The Model instance created from the dictionary



* **Return type**

    Model



### _class_ validmind.vm_models.ModelAttributes(architecture: str | None = None, framework: str | None = None, framework_version: str | None = None)
Bases: `object`

Model attributes definition


#### architecture(_: st_ _ = Non_ )

#### framework(_: st_ _ = Non_ )

#### framework_version(_: st_ _ = Non_ )

### _class_ validmind.vm_models.ResultSummary(results: List[ResultTable])
Bases: `object`

A dataclass that holds the summary of a metric or threshold test results


#### results(_: List[ResultTable_ )

#### add_result(result: ResultTable)
Adds a result to the list of results


#### serialize()
Serializes the ResultSummary to a list of results


### _class_ validmind.vm_models.ResultTable(data: Dict[str, Any] | DataFrame, type: str = 'table', metadata: ResultTableMetadata | None = None)
Bases: `object`

A dataclass that holds the table summary of result


#### data(_: Dict[str, Any] | DataFram_ )

#### type(_: st_ _ = 'table_ )

#### metadata(_: ResultTableMetadat_ _ = Non_ )

#### serialize()
Serializes the Figure to a dictionary so it can be sent to the API


### _class_ validmind.vm_models.ResultTableMetadata(title: str)
Bases: `object`

A dataclass that holds the metadata of a table summary


#### title(_: st_ )

### _class_ validmind.vm_models.TestContext(dataset: Dataset | None = None, model: Model | None = None, models: List[Model] | None = None, context_data: dict | None = None)
Bases: `object`

Holds context that can be used by tests to run.
Allows us to store data that needs to be reused
across different tests/metrics such as shared dataset metrics, etc.


#### dataset(_: Datase_ _ = Non_ )

#### model(_: Mode_ _ = Non_ )

#### models(_: List[Model_ _ = Non_ )

#### context_data(_: dic_ _ = Non_ )

#### set_context_data(key, value)

#### get_context_data(key)

### _class_ validmind.vm_models.TestContextUtils()
Bases: `object`

Utility methods for classes that receive a TestContext

TODO: more validation


#### test_context(_: TestContex_ )

#### required_context(_: ClassVar[List[str]_ )

#### _property_ dataset()

#### _property_ model()

#### _property_ models()

#### _property_ df()
Returns a Pandas DataFrame for the dataset, first checking if
we passed in a Dataset or a DataFrame


#### validate_context()
Validates that the context elements are present
in the instance so that the test plan can be run


### _class_ validmind.vm_models.TestPlan(config: {} = None, test_context: TestContext = None, _test_plan_instances: List[object] = None, dataset: Dataset = None, model: Model = None, models: List[Model] = None, pbar: tqdm = None)
Bases: `object`

Base class for test plans. Test plans are used to define any
arbitrary grouping of tests that will be run on a dataset or model.


#### name(_: ClassVar[str_ )

#### required_context(_: ClassVar[List[str]_ )

#### tests(_: ClassVar[List[object]_ _ = [_ )

#### test_plans(_: ClassVar[List[object]_ _ = [_ )

#### results(_: ClassVar[List[TestPlanResult]_ _ = [_ )

#### config(_: {_ _ = Non_ )

#### test_context(_: TestContex_ _ = Non_ )

#### dataset(_: Datase_ _ = Non_ )

#### model(_: Mode_ _ = Non_ )

#### models(_: List[Model_ _ = Non_ )

#### pbar(_: tqd_ _ = Non_ )

#### title()
Returns the title of the test plan. Defaults to the title
version of the test plan name


#### description()
Returns the description of the test plan. Defaults to the
docstring of the test plan


#### validate_context()
Validates that the context elements are present
in the instance so that the test plan can be run


#### get_config_params_for_test(test_name)
Returns the config for a given test, if it exists. The config
attribute is a dictionary where the keys are the test names and
the values are dictionaries of config values for that test.

The key in the config must match the name of the test, i.e. for
a test called “time_series_univariate_inspection_raw” we could
pass a config like this:

{

    “time_series_univariate_inspection_raw”: {

        “columns”: [“col1”, “col2”]

    }

}


#### run(send=True)
Runs the test plan


#### log_results()
Logs the results of the test plan to ValidMind

This method will be called after the test plan has been run and all results have been
collected. This method will log the results to ValidMind.


#### summarize()
Summarizes the results of the test plan

This method will be called after the test plan has been run and all results have been
logged to ValidMind. It will summarize the results of the test plan by creating an
html table with the results of each test. This html table will be displayed in an
VS Code, Jupyter or other notebook environment.


#### get_results(result_id: str | None = None)
Returns one or more results of the test plan. Includes results from
sub test plans.


### _class_ validmind.vm_models.TestPlanDatasetResult(result_id: str | None = None, result_metadata: List[dict] | None = None, dataset: Dataset | None = None)
Bases: `TestPlanResult`

Result wrapper for datasets that run as part of a test plan


#### dataset(_: Datase_ _ = Non_ )

#### log()
Log the result… Must be overridden by subclasses


### _class_ validmind.vm_models.TestPlanMetricResult(result_id: str | None = None, result_metadata: List[dict] | None = None, figures: List[Figure] | None = None, metric: MetricResult | None = None)
Bases: `TestPlanResult`

Result wrapper for metrics that run as part of a test plan


#### figures(_: List[Figure] | Non_ _ = Non_ )

#### metric(_: MetricResult | Non_ _ = Non_ )

#### log()
Log the result… Must be overridden by subclasses


### _class_ validmind.vm_models.TestPlanModelResult(result_id: str | None = None, result_metadata: List[dict] | None = None, model: Model | None = None)
Bases: `TestPlanResult`

Result wrapper for models that run as part of a test plan


#### model(_: Mode_ _ = Non_ )

#### log()
Log the result… Must be overridden by subclasses


### _class_ validmind.vm_models.TestPlanTestResult(result_id: str | None = None, result_metadata: List[dict] | None = None, figures: List[Figure] | None = None, test_results: TestResults | None = None)
Bases: `TestPlanResult`

Result wrapper for test results produced by the tests that run as part of a test plan


#### figures(_: List[Figure] | Non_ _ = Non_ )

#### test_results(_: TestResult_ _ = Non_ )

#### log()
Log the result… Must be overridden by subclasses


### _class_ validmind.vm_models.TestResult(values: dict, test_name: str | None = None, column: str | None = None, passed: bool | None = None)
Bases: `object`

TestResult model


#### values(_: dic_ )

#### test_name(_: str | Non_ _ = Non_ )

#### column(_: str | Non_ _ = Non_ )

#### passed(_: bool | Non_ _ = Non_ )

#### serialize()
Serializes the TestResult to a dictionary so it can be sent to the API


### _class_ validmind.vm_models.TestResults(category: str, test_name: str, params: dict, passed: bool, results: List[TestResult], summary: ResultSummary | None)
Bases: `object`

TestResults model


#### category(_: st_ )

#### test_name(_: st_ )

#### params(_: dic_ )

#### passed(_: boo_ )

#### results(_: List[TestResult_ )

#### summary(_: ResultSummary | Non_ )

#### serialize()
Serializes the TestResults to a dictionary so it can be sent to the API


### _class_ validmind.vm_models.ThresholdTest(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `TestContextUtils`

A threshold test is a combination of a metric/plot we track and a
corresponding set of parameters and thresholds values that allow
us to determine whether the metric/plot passes or fails.

TODO: ThresholdTest should validate required context too


#### test_context(_: TestContex_ )

#### test_type(_: ClassVar[str_ _ = 'ThresholdTest_ )

#### category(_: ClassVar[str_ _ = '_ )

#### name(_: ClassVar[str_ _ = '_ )

#### default_params(_: ClassVar[dict_ _ = {_ )

#### params(_: dic_ _ = Non_ )

#### test_results(_: TestResult_ _ = Non_ )

#### description()
Return the test description. Should be overridden by subclasses. Defaults
to returning the class’ docstring


#### summary(test_results: TestResults | None = None)
Return the threshold test summary. Should be overridden by subclasses. Defaults to None.
The test summary allows renderers (e.g. Word and ValidMind UI) to display a
short summary of the test results.

We return None here because the test summary is optional.


#### run(\*args, \*\*kwargs)
Run the test and cache its results


#### cache_results(results: List[TestResult], passed: bool, figures: List[Figure] | None = None)
Cache the individual results of the threshold test as a list of TestResult objects


* **Parameters**

    
    * **results** (*List**[**TestResult**]*) – The results of the threshold test


    * **passed** (*bool*) – Whether the threshold test passed or failed



* **Returns**

    The test plan result object



* **Return type**

    TestPlanResult



#### required_context(_: ClassVar[List[str]_ )
