# Load API key and secret from environment variables
from dotenv import load_dotenv

load_dotenv()


import pandas as pd
import xgboost as xgb

from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import SMOTE
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# Initialize ValidMind SDK
import validmind as vm

print("1. Initializing SDK...")

# For test environment use api_host="https://api.test.vm.validmind.ai/api/v1/tracking"
vm.init(
    # api_host="https://api.test.vm.validmind.ai/api/v1/tracking",
    project="cl1jyvh2c000909lg1rk0a0zb",
)

run_cuid = vm.start_run()

# Load model_overview.md markdown file and call log_metadata with its text
print("2. Logging model metadata...")

content_ids = [
    "model_overview",
    "model_selection",
    "dataset_split",
]

for content_id in content_ids:
    with open(f"./scripts/lending_club_metadata/{content_id}.md") as f:
        vm.log_metadata(content_id, f.read())

print("3. Loading dataset...")

# df = pd.read_pickle("./notebooks/datasets/_temp/df_loans_cleaned.pickle")
# This dataset has been cleaned up much more after df_loans_cleaned
train_df = pd.read_pickle("./notebooks/datasets/_temp/df_loans_fe.pickle")

targets = vm.DatasetTargets(
    target_column="loan_status",
    class_labels={
        "0": "Fully Paid",
        "1": "Charged Off",
    },
)

print("4. Logging dataset metadata and statistics...")

vm_dataset = vm.log_dataset(train_df, "training", analyze=True, targets=targets)


print("5. Running data quality tests...")

results = vm.run_dataset_tests(
    train_df,
    dataset_type="training",
    vm_dataset=vm_dataset,
    send=True,
    run_cuid=run_cuid,
)


# print("6. Loading and preparing dataset for training...")

# COLS_CORRELATED = [
#     "num_actv_rev_tl",
#     "open_il_12m",
#     "open_rv_12m",
#     "avg_cur_bal",
#     "num_bc_tl",
#     "mo_sin_old_rev_tl_op",
# ]

# train_df.drop(COLS_CORRELATED, axis=1, inplace=True)
# print("The following features  were removed.", COLS_CORRELATED)

# df_categories = train_df.select_dtypes("object")
# train_df = pd.get_dummies(
#     train_df, columns=list(df_categories.columns), drop_first=False
# )

# print("7. Splitting dataset into training and validation sets...")

# X, Y = train_df[train_df.columns.difference(["loan_status"])], train_df["loan_status"]

# X_train, X_test, y_train, y_test = train_test_split(
#     X, Y, test_size=0.3, stratify=Y, random_state=10
# )

# train_ds, val_ds = train_test_split(train_df, test_size=0.3)

# # For training
# X_train = train_ds.drop("loan_status", axis=1)
# y_train = train_ds.loc[:, "loan_status"].astype(int)
# X_test = val_ds.drop("loan_status", axis=1)
# y_test = val_ds.loc[:, "loan_status"].astype(int)

# print("8. Balancing training dataset...")

# X_train_subset = X_train[:1000]
# y_train_subset = y_train[:1000]
# pca = PCA(n_components=2)
# X_train_subset = pca.fit_transform(X_train_subset)

# over = SMOTE(sampling_strategy=0.5, k_neighbors=10)
# under = RandomUnderSampler(sampling_strategy=1.0)
# X_train_subset_o, y_train_subset_o = over.fit_resample(X_train_subset, y_train_subset)
# X_train_subset_o_u, y_train_subset_o_u = under.fit_resample(
#     X_train_subset_o, y_train_subset_o
# )

# X_train, y_train = over.fit_resample(X_train, y_train)
# X_train, y_train = under.fit_resample(X_train, y_train)

# print("9. Training model...")

# xgb_model = xgb.XGBClassifier(
#     early_stopping_rounds=10,
#     # n_estimators=5,
# )
# xgb_model.set_params(
#     eval_metric=["error", "logloss", "auc"],
# )
# xgb_model.fit(
#     X_train,
#     y_train,
#     eval_set=[(X_train, y_train), (X_test, y_test)],
# )

# print("10. Logging model parameters and training metrics...")

# vm.log_model(xgb_model)
# vm.log_training_metrics(xgb_model, X_train, y_train, run_cuid=run_cuid)

# y_pred = xgb_model.predict_proba(X_test)[:, -1]
# predictions = [round(value) for value in y_pred]
# accuracy = accuracy_score(y_test, predictions)

# print(f"Accuracy: {accuracy}")

# print("11. Running model evaluation tests...")

# eval_results = vm.run_model_tests(
#     xgb_model, X_test, y_test, send=True, run_cuid=run_cuid
# )
