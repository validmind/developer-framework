# Load API key and secret from environment variables
from dotenv import load_dotenv

load_dotenv()

import validmind as vm

import click

import pandas as pd
import xgboost as xgb

from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import SMOTE
from numpy import argmax
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, precision_recall_curve
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split

from jeffreys_test import (
    calculate_and_return,
    get_calibrated_pds,
    process_observations,
)


def log_metadata(vm):
    print("* Logging model metadata...")

    content_ids = [
        "model_overview",
        "model_selection",
        "dataset_split",
        "feature_selection",
    ]

    for content_id in content_ids:
        with open(f"./scripts/lending_club_metadata/{content_id}.md") as f:
            vm.log_metadata(content_id, f.read())


def load_dataset(vm, fast=False):
    print("* Loading dataset...")

    # df = pd.read_pickle("./notebooks/datasets/_temp/df_loans_cleaned.pickle")
    # This dataset has been cleaned up much more after df_loans_cleaned
    train_df = pd.read_pickle("./notebooks/datasets/_temp/df_loans_fe.pickle")
    if fast:
        print("Fast flag was passed, using only 100k rows of data")
        train_df = train_df.sample(100000)

    targets = vm.DatasetTargets(
        target_column="loan_status",
        class_labels={
            "0": "Fully Paid",
            "1": "Charged Off",
        },
    )

    # vm.analyze_dataset(
    #     dataset=train_df,
    #     dataset_type="training",
    #     targets=targets,
    # )

    COLS_CORRELATED = [
        "num_actv_rev_tl",
        "open_il_12m",
        "open_rv_12m",
        "avg_cur_bal",
        "num_bc_tl",
        "mo_sin_old_rev_tl_op",
    ]

    train_df.drop(COLS_CORRELATED, axis=1, inplace=True)
    print("The following features  were removed.", COLS_CORRELATED)

    df_categories = train_df.select_dtypes("object")
    train_df = pd.get_dummies(
        train_df, columns=list(df_categories.columns), drop_first=False
    )

    return train_df


def prepare_datasets(vm, df):
    print("* Splitting dataset into training and validation sets...")

    train_inputs, x_test, train_targets, y_test = train_test_split(
        df.drop(["loan_status"], axis=1),
        df["loan_status"],
        test_size=0.2,
        stratify=df["loan_status"],
        random_state=10,
    )

    (x_train, x_val, y_train, y_val) = train_test_split(
        train_inputs, train_targets, test_size=0.25, random_state=10
    )

    x_train.to_csv("./notebooks/datasets/_temp/x_train_lc.csv", index=False)
    x_test.to_csv("./notebooks/datasets/_temp/x_test_lc.csv", index=False)

    return (
        (x_train, y_train),
        (x_val, y_val),
        (x_test, y_test),
    )


# print("7. Balancing training dataset...")

# x_train_subset = x_train[:1000]
# y_train_subset = y_train[:1000]
# pca = PCA(n_components=2)
# x_train_subset = pca.fit_transform(x_train_subset)

# over = SMOTE(sampling_strategy=0.5, k_neighbors=10)
# under = RandomUnderSampler(sampling_strategy=1.0)
# x_train_subset_o, y_train_subset_o = over.fit_resample(x_train_subset, y_train_subset)
# x_train_subset_o_u, y_train_subset_o_u = under.fit_resample(
#     x_train_subset_o, y_train_subset_o
# )

# x_train, y_train = over.fit_resample(x_train, y_train)
# x_train, y_train = under.fit_resample(x_train, y_train)


def grid_search(model_type, train_set):
    """
    Only train a model to find an optimal set of parameters

    https://machinelearningmastery.com/tune-number-size-decision-trees-xgboost-python/
    """
    print("Grid search was passed, running grid search to find best model...")

    (x_train, y_train) = train_set

    # TODO: allow grid search according to model type
    model = xgb.XGBClassifier()
    model.set_params(
        eval_metric=["error", "logloss", "auc"],
    )

    # n_estimators = range(50, 250, 50)
    # param_grid = dict(n_estimators=n_estimators)
    # max_delta_step = range(1, 10, 2)
    # param_grid = dict(max_delta_step=max_delta_step)
    # weights = [1, 5, 10, 20, 25]
    # param_grid = dict(scale_pos_weight=weights)
    # colsample_bytree = [0.1, 0.2, 0.5, 0.75, 1]
    # param_grid = dict(colsample_bytree=colsample_bytree)
    subsample = [0.1, 0.2, 0.5, 0.75, 1]
    param_grid = dict(subsample=subsample)
    kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=7)
    grid_search = GridSearchCV(
        model, param_grid, scoring="f1", n_jobs=-1, cv=kfold, verbose=2
    )
    grid_result = grid_search.fit(x_train, y_train)

    print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
    means = grid_result.cv_results_["mean_test_score"]
    stds = grid_result.cv_results_["std_test_score"]
    params = grid_result.cv_results_["params"]
    for mean, stdev, param in zip(means, stds, params):
        print("%f (%f) with: %r" % (mean, stdev, param))


def train_model(vm, model_type, train_set, val_set, test_set):
    print("* Training model...")

    (x_train, y_train) = train_set
    (x_val, y_val) = val_set
    (x_test, y_test) = test_set

    model = xgb.XGBClassifier()
    # Values obtained from grid search above
    model.set_params(
        n_estimators=200,
        max_delta_step=3,
        scale_pos_weight=5,
        colsample_bytree=0.75,
        subsample=0.5,
        eval_metric=["error", "logloss", "auc"],
    )

    model.fit(
        x_train,
        y_train,
        eval_set=[(x_train, y_train), (x_val, y_val)],
        verbose=False,
    )

    y_pred = model.predict_proba(x_test)[:, -1]
    predictions = [round(value) for value in y_pred]
    accuracy = accuracy_score(y_test, predictions)

    print(f"Accuracy on test data: {accuracy}")

    return model


def evaluate_model(vm, model, train_set, val_set, test_set):
    vm.evaluate_model(
        model,
        train_set=train_set,
        val_set=val_set,
        test_set=test_set,
    )


# # Find an optimal threshold for the model before we evaluate it
# # We want to focus on a threshold that maximizes the F1 score since
# # we are interested in optimizing performance for the minority class
# y_pred_val = xgb_model.predict_proba(x_val)[:, -1]

# precision, recall, thresholds = precision_recall_curve(y_val, y_pred_val)
# fscore = (2 * precision * recall) / (precision + recall)
# # Get the index of the largest F1 Score
# ix = argmax(fscore)
# threshold = thresholds[ix]
# print("Optimal threshold=%f, F1 Score=%.3f" % (threshold, fscore[ix]))

# threshold_metric = vm.Metric(
#     type="evaluation", scope="test", key="decision_threshold", value=[threshold]
# )

# vm.log_metrics([threshold_metric])


def run_jeffreys_test(vm, model, train_set, val_set, test_set):
    segments = [
        {
            "name": "Grade",
            "segments": [
                {"name": "Grade A", "query": "grade_A == 1"},
                {"name": "Grade B", "query": "grade_B == 1"},
                {"name": "Grade C", "query": "grade_C == 1"},
                {"name": "Grade D", "query": "grade_D == 1"},
                {"name": "Grade E", "query": "grade_E == 1"},
                {"name": "Grade F", "query": "grade_F == 1"},
                {"name": "Grade G", "query": "grade_G == 1"},
            ],
        },
        {
            "name": "Delinquency",
            "segments": [
                {"name": "Delinquency: None", "query": "acc_now_delinq == 0"},
                {"name": "Delinquency: 1 Account", "query": "acc_now_delinq == 1"},
                {"name": "Delinquency: 2 Accounts", "query": "acc_now_delinq == 2"},
            ],
        },
    ]

    segment_names = [segment["name"] for segment in segments]
    print(f"* Running Jeffrey's test on the following segments: {segment_names}")

    # Get calibrated PDs from training dataset
    calibrated_pds = get_calibrated_pds(train_set[0], model, segments)

    # Create observations DataFrame to match the format expected by the provided functions
    observations = process_observations(test_set[0], model, segments)

    # Define parameters for the test, for now only threshold
    jeffreys_params = {"threshold": 0.85}

    results = calculate_and_return(
        observations,
        cal_pd=calibrated_pds,
        pool="Segment",
        obs="Observed",
        threshold=jeffreys_params["threshold"],
    )

    # Test passed only if all values for 'Outcome' are 'Satisfactory'
    test_passed = results["Outcome"].all() == "Satisfactory"

    # Build a vm.TestResult object for each row in the results dataframe
    test_results = []
    for _, row in results.iterrows():
        test_results.append(
            vm.TestResult(
                passed=row["Outcome"] == "Satisfactory",
                values={
                    "segment": row["Segment"],
                    "defaults": row["Defaults"],
                    "observations": row["Observations"],
                    "default_rate": row["Default Rate"],
                    "calibrated_pd": row["Calibrated PD"],
                    "p_value": row["P-value"],
                },
            )
        )

    jeffreys_test_result = vm.TestResults(
        category="model_performance",
        test_name="jeffreys_test",
        params=jeffreys_params,
        passed=test_passed,
        results=test_results,
    )

    vm.log_test_results([jeffreys_test_result])


@click.command()
@click.option(
    "--model",
    type=click.Choice(["xgb", "lr"], case_sensitive=False),
    default="xgb",
)
@click.option(
    "--env",
    type=click.Choice(["local", "dev", "staging"], case_sensitive=False),
    default="local",
)
@click.option("--fast", is_flag=True, default=False)
@click.option("--grid", is_flag=True, default=False)
def run(model, env, fast, grid):
    project_id = "cl1jyvh2c000909lg1rk0a0zb"
    vm_init_opts = {
        "project": project_id,
    }
    if env != "local":
        vm_init_opts["api_host"] = f"https://api.{env}.vm.validmind.ai/api/v1/tracking"
    vm.init(**vm_init_opts)

    log_metadata(vm)
    df = load_dataset(vm, fast)

    train_set, val_set, test_set = prepare_datasets(vm, df)

    if grid:
        grid_search(model, train_set)
        return

    model = train_model(vm, model, train_set, val_set, test_set)
    evaluate_model(vm, model, train_set=train_set, val_set=val_set, test_set=test_set)
    run_jeffreys_test(vm, model, train_set, val_set, test_set)


if __name__ == "__main__":
    run()
