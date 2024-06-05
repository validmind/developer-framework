"""
Utility functions for running integration tests for run_test().
"""

import os

import validmind as vm
import xgboost as xgb

from openai import OpenAI
from sklearn.ensemble import RandomForestClassifier

from validmind.datasets.classification import customer_churn
from validmind.datasets.nlp import cnn_dailymail
from validmind.datasets.regression import fred
from validmind.models import FoundationModel, Prompt

os.environ["OPENAI_API_KEY"] = "123"


def assign_features_pairs_config(test_config, raw_df, train_df=None, test_df=None):
    """
    Generates pairs of features for tests such as BivariateFeaturesBarPlots test
    """
    test_config["features_pairs_raw"] = {"features_pairs": {}}

    for i in range(0, len(raw_df.columns)):
        for j in range(i + 1, len(raw_df.columns)):
            test_config["features_pairs_raw"]["features_pairs"][raw_df.columns[i]] = (
                raw_df.columns[j]
            )


def setup_tabular_test_inputs(test_inputs={}, test_config={}):
    """
    Setup test inputs for tabular datasets

    Args:
        test_inputs (dict): Glogal test inputs to be updated
        test_config (dict): Global test config to be updated
    """
    df = customer_churn.load_data()
    df = df.sample(1000, random_state=42)

    train_df, validation_df, test_df = customer_churn.preprocess(df)
    x_train = train_df.drop(customer_churn.target_column, axis=1)
    y_train = train_df[customer_churn.target_column]
    x_val = validation_df.drop(customer_churn.target_column, axis=1)
    y_val = validation_df[customer_churn.target_column]

    classifier = xgb.XGBClassifier(early_stopping_rounds=10)
    classifier.set_params(eval_metric=["error", "logloss", "auc"])
    classifier.fit(x_train, y_train, eval_set=[(x_val, y_val)], verbose=False)

    classifier_rf = RandomForestClassifier()
    classifier_rf.fit(x_train, y_train)

    # Models
    vm_classifier_model = vm.init_model(
        classifier,
        input_id="xgb_classifier",
        __log=False,
    )
    vm_classifier_rf_model = vm.init_model(
        classifier_rf,
        input_id="rf_classifier",
        __log=False,
    )

    # Datasets
    vm_raw_dataset = vm.init_dataset(
        dataset=df,
        input_id="raw_dataset",
        target_column=customer_churn.target_column,
        class_labels=customer_churn.class_labels,
        __log=False,
    )
    vm_train_ds = vm.init_dataset(
        dataset=train_df,
        input_id="train_dataset",
        target_column=customer_churn.target_column,
        __log=False,
    )
    vm_test_ds = vm.init_dataset(
        dataset=test_df,
        input_id="test_dataset",
        target_column=customer_churn.target_column,
        __log=False,
    )

    # Assign predictions for each model
    vm_train_ds.assign_predictions(vm_classifier_model)
    vm_train_ds.assign_predictions(vm_classifier_rf_model)

    vm_test_ds.assign_predictions(vm_classifier_model)
    vm_test_ds.assign_predictions(vm_classifier_rf_model)

    assign_features_pairs_config(test_config, df)

    # Usage:
    #
    # For 1 dataset tests use the raw dataset (i.e. data quality tests)
    # For 2 dataset/model tests, use model and test dataset
    # For 3 two dataset tests, use both the training and test datasets (comparison tests)
    test_inputs["classification"] = {
        "single_dataset": {
            "dataset": vm_raw_dataset,
        },
        "two_datasets": {
            "datasets": [vm_train_ds, vm_test_ds],
        },
        "single_model": {
            "model": vm_classifier_model,
        },
        "dataset_and_two_models": {
            "dataset": vm_test_ds,
            "models": [vm_classifier_model, vm_classifier_rf_model],
        },
        "model_and_dataset": {
            "dataset": vm_test_ds,
            "model": vm_classifier_model,
        },
        "model_and_two_datasets": {
            "model": vm_classifier_model,
            "datasets": [vm_train_ds, vm_test_ds],
        },
        "two_models": {
            "models": [vm_classifier_model, vm_classifier_rf_model],
        },
    }


def setup_time_series_test_inputs(test_inputs={}, test_config={}):
    """
    Setup test inputs for time series datasets

    Args:
        test_inputs (dict): Glogal test inputs to be updated
        test_config (dict): Global test config to be updated
    """
    df = fred.load_data()
    df = df.sample(1000, random_state=42)

    # Models

    # Datasets
    vm_raw_dataset = vm.init_dataset(
        input_id="raw_dataset",
        dataset=df,
        target_column=fred.target_column,
        __log=False,
    )

    # Assign predictions for each model
    # vm_train_ds.assign_predictions(vm_classifier_model)

    # Usage:
    #
    # For 1 dataset tests use the raw dataset (i.e. data quality tests)
    # For 2 dataset/model tests, use model and test dataset
    # For 3 two dataset tests, use both the training and test datasets (comparison tests)
    test_inputs["time_series"] = {
        "single_dataset": {
            "dataset": vm_raw_dataset,
        },
    }


def setup_summarization_test_inputs(test_inputs={}, test_config={}):
    """
    Setup test inputs for summarization tests

    Args:
        test_inputs (dict): Glogal test inputs to be updated
        test_config (dict): Global test config to be updated
    """
    _, test_df = cnn_dailymail.load_data(source="offline", dataset_size="100")

    # Dataset
    vm_test_ds = vm.init_dataset(
        dataset=test_df,
        input_id="test_dataset",
        text_column="article",
        target_column="highlights",
        __log=False,
    )

    # Prompt and model
    prompt_template = """
    You are an AI with expertise in summarizing financial news.
    Your task is to provide a concise summary of the specific news article provided below.
    Before proceeding, take a moment to understand the context and nuances of the financial terminology used in the article.

    Article to Summarize:

    ```
    {article}
    ```

    Please respond with a concise summary of the article's main points.
    Ensure that your summary is based on the content of the article and not on external information or assumptions.
    """.strip()

    prompt_variables = ["article"]

    model = OpenAI()

    # This should not call the model since we're using precomputed predictions
    def call_model(prompt):
        return (
            model.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt},
                ],
            )
            .choices[0]
            .message.content
        )

    vm_model = vm.init_model(
        model=FoundationModel(
            predict_fn=call_model,
            prompt=Prompt(
                template=prompt_template,
                variables=prompt_variables,
            ),
        ),
        input_id="gpt_35",
        __log=False,
    )

    # Assign precomputed predictions
    vm_test_ds.assign_predictions(vm_model, prediction_column="gpt_35_prediction")

    test_inputs["text_summarization"] = {
        "single_dataset": {
            "dataset": vm_test_ds,
        },
        "model_and_dataset": {
            "dataset": vm_test_ds,
            "model": vm_model,
        },
    }
