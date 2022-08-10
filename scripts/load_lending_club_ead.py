# Load API key and secret from environment variables
from dotenv import load_dotenv

load_dotenv()


import pandas as pd
import xgboost as xgb

from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import SMOTE

from sklearn import linear_model
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# Initialize ValidMind SDK
import validmind as vm

print("1. Initializing SDK...")

# For test environment use api_host="https://api.test.vm.validmind.ai/api/v1/tracking"
vm.init(
    project="cl6laq3ys0000tp8hiawa7e4m",
)

# Load model_overview.md markdown file and call log_metadata with its text
print("2. Logging model metadata...")

# content_ids = [
#     "model_overview",
#     "model_selection",
#     "dataset_split",
#     "feature_selection",
# ]

# for content_id in content_ids:
#     with open(f"./scripts/lending_club_metadata/{content_id}.md") as f:
#         vm.log_metadata(content_id, f.read())

print("3. Loading dataset...")

# Do some preprocessing on the dataset before we log it:
#
# 1) We want to load only loans that have defaulted
# 2) Generate our target column (CCF)
# 3) Select the actual columns we need for training

# TODO - support dummy variables for data description

df = pd.read_csv("./notebooks/datasets/_temp/loan_data_2007_2014_preprocessed.csv")

loan_data_defaults = df[
    df["loan_status"].isin(
        ["Charged Off", "Does not meet the credit policy. Status:Charged Off"]
    )
]
loan_data_defaults["mths_since_last_delinq"].fillna(0, inplace=True)
loan_data_defaults["mths_since_last_record"].fillna(0, inplace=True)

# - CCF is the proportion of the original amount of the loan that is still
# outstanding when the borrower defaulted
# - EAD is the oustanding amount so, EAD = CCF * loan amount
ccf = (
    loan_data_defaults["funded_amnt"] - loan_data_defaults["total_rec_prncp"]
) / loan_data_defaults["funded_amnt"]

# Independent variables needed for model training
features_all = [
    "grade:A",
    "grade:B",
    "grade:C",
    "grade:D",
    "grade:E",
    "grade:F",
    "grade:G",
    "home_ownership:MORTGAGE",
    "home_ownership:NONE",
    "home_ownership:OTHER",
    "home_ownership:OWN",
    "home_ownership:RENT",
    "verification_status:Not Verified",
    "verification_status:Source Verified",
    "verification_status:Verified",
    "purpose:car",
    "purpose:credit_card",
    "purpose:debt_consolidation",
    "purpose:educational",
    "purpose:home_improvement",
    "purpose:house",
    "purpose:major_purchase",
    "purpose:medical",
    "purpose:moving",
    "purpose:other",
    "purpose:renewable_energy",
    "purpose:small_business",
    "purpose:vacation",
    "purpose:wedding",
    "initial_list_status:f",
    "initial_list_status:w",
    "term_int",
    "emp_length_int",
    "mths_since_issue_d",
    "mths_since_earliest_cr_line",
    "funded_amnt",
    "int_rate",
    "installment",
    "annual_inc",
    "dti",
    "delinq_2yrs",
    "inq_last_6mths",
    "mths_since_last_delinq",
    "mths_since_last_record",
    "open_acc",
    "pub_rec",
    "total_acc",
    "acc_now_delinq",
    "total_rev_hi_lim",
]

loan_data_defaults = loan_data_defaults[features_all]
loan_data_defaults["ccf"] = ccf

print("4. Logging dataset metadata and statistics...")

dataset_options = {
    "dummy_variables": [
        "grade",
        "home_ownership",
        "verification_status",
        "purpose",
        "initial_list_status",
    ],
}

vm_dataset = vm.log_dataset(
    dataset=loan_data_defaults,
    dataset_type="training",
    dataset_options=dataset_options,
)


print("5. Running data quality tests...")

results = vm.run_dataset_tests(
    loan_data_defaults,
    dataset_type="training",
    vm_dataset=vm_dataset,
    send=True,
)


print("6. Loading and preparing dataset for training...")

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
