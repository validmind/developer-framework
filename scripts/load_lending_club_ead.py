# Load API key and secret from environment variables
from dotenv import load_dotenv

load_dotenv()


import pandas as pd
import xgboost as xgb

import numpy as np
import scipy.stats as stat
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# Custom LinearRegression with p-values
class LinearRegression(linear_model.LinearRegression):
    """
    LinearRegression class after sklearn's, but calculate t-statistics
    and p-values for model coefficients (betas).
    Additional attributes available after .fit()
    are `t` and `p` which are of the shape (y.shape[1], X.shape[1])
    which is (n_features, n_coefs)
    This class sets the intercept to 0 by default, since usually we include it
    in X.
    """

    # nothing changes in __init__
    def __init__(
        self, fit_intercept=True, normalize=False, copy_X=True, n_jobs=1, positive=False
    ):
        self.fit_intercept = fit_intercept
        self.normalize = normalize
        self.copy_X = copy_X
        self.n_jobs = n_jobs
        self.positive = positive

    def fit(self, X, y, n_jobs=1):
        self = super(LinearRegression, self).fit(X, y, n_jobs)

        # Calculate SSE (sum of squared errors)
        # and SE (standard error)
        sse = np.sum((self.predict(X) - y) ** 2, axis=0) / float(
            X.shape[0] - X.shape[1]
        )
        se = np.array([np.sqrt(np.diagonal(sse * np.linalg.inv(np.dot(X.T, X))))])

        # compute the t-statistic for each feature
        self.t = self.coef_ / se
        # find the p-value for each feature
        self.p = np.squeeze(
            2 * (1 - stat.t.cdf(np.abs(self.t), y.shape[0] - X.shape[1]))
        )
        return self


# Initialize ValidMind SDK
import validmind as vm

print("1. Initializing SDK...")

# For test environment use api_host="https://api.test.vm.validmind.ai/api/v1/tracking"
vm.init(
    # project="cl6laq3ys0000tp8hiawa7e4m",
    project="cl6ojsc8c0072ou8hf4p6s1q4",  # xgboost
)

print("2. Logging model metadata...")

with open(f"./scripts/lending_club_metadata/model_overview.md") as f:
    vm.log_metadata("model_overview", f.read())

with open(f"./scripts/lending_club_metadata/dataset_split_regression.md") as f:
    vm.log_metadata("dataset_split", f.read())

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

# Remove reference variables before training
features_reference_cat = [
    "grade:G",
    "home_ownership:RENT",
    "verification_status:Verified",
    "purpose:credit_card",
    "initial_list_status:f",
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

targets = vm.DatasetTargets(
    target_column="ccf",
    description="""Credit Conversion Factor is the proportion of the original
    amount of the loan that is still outstanding when the borrower defaulted.
    Exposure at Default (EAD) is calculated by multiplying CCF
    by the loan amount (EAD = CCF * loan amount).""",
)

vm_dataset = vm.log_dataset(
    dataset=loan_data_defaults,
    dataset_type="training",
    dataset_options=dataset_options,
    targets=targets,
)


print("5. Running data quality tests...")

results = vm.run_dataset_tests(
    loan_data_defaults,
    dataset_type="training",
    vm_dataset=vm_dataset,
    send=True,
)


print("6. Splitting dataset into training and validation sets...")

loan_data_defaults = loan_data_defaults.drop(features_reference_cat, axis=1)

# Generate training and test sets, training set is split into train/validation
#   80%/20% split
(
    ead_inputs_train,
    ead_inputs_test,
    ead_targets_train,
    ead_targets_test,
) = train_test_split(
    loan_data_defaults.drop(["ccf"], axis=1),
    loan_data_defaults["ccf"],
    test_size=0.2,
    random_state=42,
)

# Generate training and validation set for training
#   75%/25% split
#   Training set ends up with 60% of rows
#   Validation set ends up with 20% of rows, same as test set
(x_train, x_val, y_train, y_val) = train_test_split(
    ead_inputs_train,
    ead_targets_train,
    test_size=0.25,
    random_state=42,
)

print("7. Training model...")

# reg_ead = LinearRegression()
# reg_ead.fit(x_train, y_train)

xgb_model = xgb.XGBRegressor()
xgb_model.set_params(
    booster="gblinear",
    eval_metric=mean_squared_error,
)
xgb_model.fit(
    x_train,
    y_train,
    eval_set=[
        (x_train, y_train),
        (x_val, y_val),
    ],
)

print("8. Logging model parameters and training metrics...")

# vm.log_model(reg_ead)
# vm.log_training_metrics(reg_ead, x_train, y_train, x_val, y_val)

vm.log_model(xgb_model)
vm.log_training_metrics(xgb_model, x_train, y_train, x_val, y_val)

print("9. Running model evaluation tests...")

eval_results = vm.run_model_tests(xgb_model, ead_inputs_test, ead_targets_test)
# eval_results = vm.run_model_tests(reg_ead, ead_inputs_test, ead_targets_test)
