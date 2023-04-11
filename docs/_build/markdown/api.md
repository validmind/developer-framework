# Python Library API

Main entrypoint to the ValidMind Python Library


### validmind.init(project, api_key=None, api_secret=None, api_host=None)
Initializes the API client instances and calls the /ping endpoint to ensure
the provided credentials are valid and we can connect to the ValidMind API.

If the API key and secret are not provided, the client will attempt to
retrieve them from the environment variables VM_API_KEY and VM_API_SECRET.


* **Parameters**

    
    * **project** (*str*) – The project CUID


    * **api_key** (*str**, **optional*) – The API key. Defaults to None.


    * **api_secret** (*str**, **optional*) – The API secret. Defaults to None.


    * **api_host** (*str**, **optional*) – The API host. Defaults to None.



* **Raises**

    **ValueError** – If the API key and secret are not provided



* **Returns**

    True if the ping was successful



* **Return type**

    bool



### validmind.init_dataset(dataset, type='training', options=None, targets=None, target_column=None, class_labels=None)
Initializes a VM Dataset, which can then be passed to other functions
that can perform additional analysis and tests on the data. This function
also ensures we are reading a valid dataset type. We only support Pandas
DataFrames at the moment.


* **Parameters**

    
    * **dataset** (*pd.DataFrame*) – We only support Pandas DataFrames at the moment


    * **type** (*str*) – The dataset split type is necessary for mapping and relating multiple
    datasets together. Can be one of training, validation, test or generic


    * **options** (*dict*) – A dictionary of options for the dataset


    * **targets** (*vm.vm.DatasetTargets*) – A list of target variables


    * **target_column** (*str*) – The name of the target column in the dataset


    * **class_labels** (*dict*) – A list of class labels for classification problems



* **Raises**

    **ValueError** – If the dataset type is not supported



* **Returns**

    A VM Dataset instance



* **Return type**

    vm.vm.Dataset



### validmind.init_model(model)
Initializes a VM Model, which can then be passed to other functions
that can perform additional analysis and tests on the data. This function
also ensures we are reading a supported model type.


* **Parameters**

    **model** – A trained sklearn model



* **Raises**

    **ValueError** – If the model type is not supported



* **Returns**

    A VM Model instance



* **Return type**

    vm.vm.Model



### validmind.run_test_plan(test_plan_name, send=True, \*\*kwargs)
High Level function for running a test plan

This function provides a high level interface for running a test plan. It removes the need
to manually initialize a TestPlan instance and run it. This function will automatically
find the correct test plan class based on the test_plan_name, initialize the test plan, and
run it.


* **Parameters**

    
    * **test_plan_name** (*str*) – The test plan name (e.g. ‘sklearn_classifier’)


    * **send** (*bool**, **optional*) – Whether to post the test results to the API. send=False is useful for testing. Defaults to True.


    * **\*\*kwargs** – Additional keyword arguments to pass to the test plan. These will provide
    the TestPlan instance with the necessary context to run the tests. e.g. dataset, model etc.
    See the documentation for the specific test plan for more details.



* **Raises**

    **ValueError** – If the test plan name is not found or if there is an error initializing the test plan



* **Returns**

    A dictionary of test results



* **Return type**

    dict



### validmind.log_dataset(vm_dataset)
Logs metadata and statistics about a dataset to ValidMind API.


* **Parameters**

    
    * **vm_dataset** (*validmind.VMDataset*) – A VM dataset object


    * **dataset_type** (*str**, **optional*) – The type of dataset. Can be one of “training”, “test”, or “validation”. Defaults to “training”.


    * **dataset_options** (*dict**, **optional*) – Additional dataset options for analysis. Defaults to None.


    * **dataset_targets** (*validmind.DatasetTargets**, **optional*) – A list of targets for the dataset. Defaults to None.


    * **features** (*list**, **optional*) – Optional. A list of features metadata. Defaults to None.



* **Raises**

    **Exception** – If the API call fails



* **Returns**

    The VMDataset object



* **Return type**

    validmind.VMDataset



### validmind.log_figure(data_or_path, key, metadata, run_cuid=None)
Logs a figure


* **Parameters**

    
    * **data_or_path** (*str** or **matplotlib.figure.Figure*) – The path of the image or the data of the plot


    * **key** (*str*) – Identifier of the figure


    * **metadata** (*dict*) – Python data structure


    * **run_cuid** (*str**, **optional*) – The run CUID. If not provided, a new run will be created. Defaults to None.



* **Raises**

    **Exception** – If the API call fails



* **Returns**

    True if the API call was successful



* **Return type**

    bool



### validmind.log_metadata(content_id, text=None, extra_json=None)
Logs free-form metadata to ValidMind API.


* **Parameters**

    
    * **content_id** (*str*) – Unique content identifier for the metadata


    * **text** (*str**, **optional*) – Free-form text to assign to the metadata. Defaults to None.


    * **extra_json** (*dict**, **optional*) – Free-form key-value pairs to assign to the metadata. Defaults to None.



* **Raises**

    **Exception** – If the API call fails



* **Returns**

    True if the API call was successful



* **Return type**

    bool



### validmind.log_metrics(metrics, run_cuid=None)
Logs metrics to ValidMind API.


* **Parameters**

    
    * **metrics** (*list*) – A list of Metric objects


    * **run_cuid** (*str**, **optional*) – The run CUID. If not provided, a new run will be created. Defaults to None.



* **Raises**

    **Exception** – If the API call fails



* **Returns**

    True if the API call was successful



* **Return type**

    bool



### validmind.log_model(vm_model)
Logs model metadata and hyperparameters to ValidMind API.


* **Parameters**

    **vm_model** (*validmind.VMModel*) – A VM model object



* **Raises**

    **Exception** – If the API call fails



* **Returns**

    True if the API call was successful



* **Return type**

    bool



### validmind.log_test_results(results, run_cuid=None, dataset_type='training')
Logs test results information. This method will be called automatically be any function
running tests but can also be called directly if the user wants to run tests on their own.


* **Parameters**

    
    * **results** (*list*) – A list of TestResults objects


    * **run_cuid** (*str**, **optional*) – The run CUID. If not provided, a new run will be created. Defaults to None.


    * **dataset_type** (*str**, **optional*) – The type of dataset. Can be one of “training”, “test”, or “validation”. Defaults to “training”.



* **Raises**

    **Exception** – If the API call fails



* **Returns**

    True if the API call was successful



* **Return type**

    bool



### _class_ validmind.Dataset(raw_dataset: object, fields: list, variables: list, sample: list, shape: dict, correlation_matrix: object | None = None, correlations: dict | None = None, type: str | None = None, options: dict | None = None, statistics: dict | None = None, targets: dict | None = None, target_column: str = '', class_labels: dict | None = None, _Dataset__feature_lookup: dict = <factory>, _Dataset__transformed_df: object | None = None)
Bases: `object`

Model class wrapper


#### raw_dataset(_: objec_ )

#### fields(_: lis_ )

#### variables(_: lis_ )

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

#### _property_ x()
Returns the dataset’s features


#### _property_ y()
Returns the dataset’s target column


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



### _class_ validmind.DatasetTargets(target_column: str, description: str | None = None, class_labels: dict | None = None)
Bases: `object`

Dataset targets definition


#### target_column(_: st_ )

#### description(_: st_ _ = Non_ )

#### class_labels(_: dic_ _ = Non_ )

### _class_ validmind.Figure(key: str, metadata: dict, figure: object, extras: dict | None = None)
Bases: `object`

Figure objects track the schema supported by the ValidMind API


#### key(_: st_ )

#### metadata(_: dic_ )

#### figure(_: objec_ )

#### extras(_: dict | Non_ _ = Non_ )

#### serialize()
Serializes the Figure to a dictionary so it can be sent to the API


### _class_ validmind.Metric(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `TestContextUtils`

Metric objects track the schema supported by the ValidMind API


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

#### run(\*args, \*\*kwargs)
Run the metric calculation and cache its results


#### cache_results(metric_value: dict | list | DataFrame, figures: List[Figure] | None = None)
Cache the results of the metric calculation and do any post-processing if needed


* **Parameters**

    
    * **metric_value** (*Union**[**dict**, **list**, **pd.DataFrame**]*) – The value of the metric


    * **figures** (*Optional**[**object**]*) – Any figures to attach to the test plan result



* **Returns**

    The test plan result object



* **Return type**

    TestPlanResult



### _class_ validmind.Model(attributes: ModelAttributes | None = None, task: str | None = None, subtask: str | None = None, params: dict | None = None, model_id: str = 'main', model: object | None = None)
Bases: `object`

Model class wrapper


#### attributes(_: ModelAttribute_ _ = Non_ )

#### task(_: st_ _ = Non_ )

#### subtask(_: st_ _ = Non_ )

#### params(_: dic_ _ = Non_ )

#### model_id(_: st_ _ = 'main_ )

#### model(_: objec_ _ = Non_ )

#### serialize()
Serializes the model to a dictionary so it can be sent to the API


#### predict(\*args, \*\*kwargs)
Predict method for the model. This is a wrapper around the model’s
predict_proba (for classification) or predict (for regression) method

NOTE: This only works for sklearn or xgboost models at the moment


#### _classmethod_ is_supported_model(model)
Checks if the model is supported by the API


* **Parameters**

    **model** (*object*) – The trained model instance to check



* **Returns**

    True if the model is supported, False otherwise



* **Return type**

    bool



#### _classmethod_ create_from_dict(dict_)
Creates a Model instance from a dictionary


* **Parameters**

    **dict** (*dict*) – The dictionary to create the Model instance from



* **Returns**

    The Model instance created from the dictionary



* **Return type**

    Model



### _class_ validmind.ModelAttributes(architecture: str | None = None, framework: str | None = None, framework_version: str | None = None)
Bases: `object`

Model attributes definition


#### architecture(_: st_ _ = Non_ )

#### framework(_: st_ _ = Non_ )

#### framework_version(_: st_ _ = Non_ )

### _class_ validmind.TestResult(\*, test_name: str | None = None, column: str | None = None, passed: bool | None = None, values: dict)
Bases: `BaseResultModel`

TestResult model


#### test_name(_: str | Non_ )

#### column(_: str | Non_ )

#### passed(_: bool | Non_ )

#### values(_: dic_ )

### _class_ validmind.TestResults(\*, category: str, test_name: str, params: dict, passed: bool, results: List[TestResult])
Bases: `BaseResultModel`

TestResults model


#### category(_: st_ )

#### test_name(_: st_ )

#### params(_: dic_ )

#### passed(_: boo_ )

#### results(_: List[TestResult_ )

### _class_ validmind.ThresholdTest(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `TestContextUtils`

A threshold test is a combination of a metric/plot we track and a
corresponding set of parameters and thresholds values that allow
us to determine whether the metric/plot passes or fails.


#### test_context(_: TestContex_ )

#### test_type(_: ClassVar[str_ _ = 'ThresholdTest_ )

#### category(_: ClassVar[str_ _ = '_ )

#### name(_: ClassVar[str_ _ = '_ )

#### default_params(_: ClassVar[dict_ _ = {_ )

#### params(_: dic_ _ = Non_ )

#### test_results(_: TestResult_ _ = Non_ )

#### run(\*args, \*\*kwargs)
Run the test and cache its results


#### cache_results(results: List[TestResult], passed: bool)
Cache the individual results of the threshold test as a list of TestResult objects


* **Parameters**

    
    * **results** (*List**[**TestResult**]*) – The results of the threshold test


    * **passed** (*bool*) – Whether the threshold test passed or failed



* **Returns**

    The test plan result object



* **Return type**

    TestPlanResult
