# Load API key and secret from environment variables
from random import random
from dotenv import load_dotenv

load_dotenv()


import pandas as pd
import xgboost as xgb

from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import SMOTE
from numpy import argmax
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, precision_recall_curve
from sklearn.model_selection import train_test_split

# Initialize ValidMind SDK
import validmind as vm

print("1. Initializing SDK...")

# For test environment use api_host="https://api.test.vm.validmind.ai/api/v1/tracking"
# Staging project ID=cl5qyzlup00001mmf5xox0ptp
vm.init(
    api_host="https://api.test.vm.validmind.ai/api/v1/tracking",
    project="cl1jyvh2c000909lg1rk0a0zb",
    # project="cl5qyzlup00001mmf5xox0ptp",
    # api_key="ddeff6b7b68b6c6346dcfad49d62a2e2",
    # api_secret="dc7fb85e3aefd1675f68cfee091339a9c62a2f05097b89393a8d044228214188",
)

# Load model_overview.md markdown file and call log_metadata with its text
print("2. Logging model metadata...")

content_ids = [
    "model_overview",
    "model_selection",
    "dataset_split",
    "feature_selection",
]

for content_id in content_ids:
    with open(f"./scripts/lending_club_metadata/{content_id}.md") as f:
        vm.log_metadata(content_id, f.read())

print("3. Loading dataset...")

df = pd.read_pickle("./notebooks/datasets/_temp/df_loans_cleaned.pickle")
# This dataset has been cleaned up much more after df_loans_cleaned
train_df = pd.read_pickle("./notebooks/datasets/_temp/df_loans_fe.pickle")

targets = vm.DatasetTargets(
    target_column="loan_status",
    class_labels={
        "0": "Fully Paid",
        "1": "Charged Off",
    },
)

print("4. Analyzing dataset...")

analyze_results = vm.analyze_dataset(
    dataset=train_df,
    dataset_type="training",
    targets=targets,
)

print("5. Loading and preparing dataset for training...")

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

print("6. Splitting dataset into training and validation sets...")

train_inputs, x_test, train_targets, y_test = train_test_split(
    train_df.drop(["loan_status"], axis=1),
    train_df["loan_status"],
    test_size=0.2,
    stratify=train_df["loan_status"],
    random_state=10,
)

(x_train, x_val, y_train, y_val) = train_test_split(
    train_inputs, train_targets, test_size=0.25, random_state=10
)

print("7. Balancing training dataset...")

x_train_subset = x_train[:1000]
y_train_subset = y_train[:1000]
pca = PCA(n_components=2)
x_train_subset = pca.fit_transform(x_train_subset)

over = SMOTE(sampling_strategy=0.5, k_neighbors=10)
under = RandomUnderSampler(sampling_strategy=1.0)
x_train_subset_o, y_train_subset_o = over.fit_resample(x_train_subset, y_train_subset)
x_train_subset_o_u, y_train_subset_o_u = under.fit_resample(
    x_train_subset_o, y_train_subset_o
)

x_train, y_train = over.fit_resample(x_train, y_train)
x_train, y_train = under.fit_resample(x_train, y_train)

print("8. Training model...")

xgb_model = xgb.XGBClassifier(
    early_stopping_rounds=10,
    # n_estimators=5,
)
xgb_model.set_params(
    eval_metric=["error", "logloss", "auc"],
)
xgb_model.fit(
    x_train,
    y_train,
    eval_set=[(x_train, y_train), (x_test, y_test)],
)

print("10. Evaluating model performance...")

y_pred = xgb_model.predict_proba(x_test)[:, -1]
predictions = [round(value) for value in y_pred]
accuracy = accuracy_score(y_test, predictions)

print(f"Accuracy: {accuracy}")

eval_results = vm.evaluate_model(
    xgb_model,
    train_set=(x_train, y_train),
    val_set=(x_val, y_val),
    test_set=(x_test, y_test),
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
