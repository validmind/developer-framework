# Load API key and secret from environment variables
from dotenv import load_dotenv

load_dotenv()

import validmind as vm

import click
import pandas as pd
import xgboost as xgb

import numpy as np
import scipy.stats as stat
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

project_ids = {
    "xgb": "cl7zf0v4j00lhum8h34oeg23m",
    "ols": "cl80k7sph0096ui8hxia5ra62",
}

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
        self.se = se

        # compute the t-statistic for each feature
        self.t = self.coef_ / se
        # find the p-value for each feature
        self.p = np.squeeze(
            2 * (1 - stat.t.cdf(np.abs(self.t), y.shape[0] - X.shape[1]))
        )

        return self


def log_metadata(vm):
    print("* Logging model metadata...")

    with open(f"./scripts/lending_club_metadata/model_overview.md") as f:
        vm.log_metadata("model_overview", f.read())

    with open(f"./scripts/lending_club_metadata/dataset_split_regression.md") as f:
        vm.log_metadata("dataset_split", f.read())


def load_dataset(vm):
    """
    Do some preprocessing on the dataset before we log it:

    1) We want to load only loans that have defaulted
    2) Generate our target column (CCF)
    3) Select the actual columns we need for training
    """
    print("* Loading dataset...")
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

    vm.analyze_dataset(
        dataset=loan_data_defaults,
        dataset_type="training",
        dataset_options=dataset_options,
        targets=targets,
    )

    loan_data_defaults = loan_data_defaults.drop(features_reference_cat, axis=1)

    return loan_data_defaults


def prepare_datasets(vm, df):
    print("* Splitting dataset into training and validation sets...")

    # Generate training and test sets, training set is split into train/validation
    #   80%/20% split
    (
        ead_inputs_train,
        ead_inputs_test,
        ead_targets_train,
        ead_targets_test,
    ) = train_test_split(
        df.drop(["ccf"], axis=1),
        df["ccf"],
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

    return (
        (x_train, y_train),
        (x_val, y_val),
        (ead_inputs_test, ead_targets_test),
    )


def train_model(vm, model_type, train_set, val_set):
    print("* Training model...")

    (x_train, y_train) = train_set
    (x_val, y_val) = val_set

    if model_type == "ols":
        model = LinearRegression()
        model.fit(x_train, y_train)
    elif model_type == "xgb":
        model = xgb.XGBRegressor()
        model.set_params(
            booster="gblinear",
            eval_metric=mean_squared_error,
        )
        model.fit(
            x_train,
            y_train,
            eval_set=[
                (x_train, y_train),
                (x_val, y_val),
            ],
        )

    return model


def evaluate_model(vm, model, train_set, val_set, test_set):
    vm.evaluate_model(
        model,
        test_set=test_set,
        train_set=train_set,
        val_set=val_set,
    )


@click.command()
@click.option(
    "--model", type=click.Choice(["xgb", "ols"], case_sensitive=False), required=True
)
@click.option(
    "--env",
    type=click.Choice(["local", "dev", "staging"], case_sensitive=False),
    default="local",
)
def run(model, env):
    project_id = project_ids[model]
    vm_init_opts = {
        "project": project_id,
    }
    if env != "local":
        vm_init_opts["api_host"] = f"https://api.{env}.vm.validmind.ai/api/v1/tracking"
    vm.init(**vm_init_opts)

    log_metadata(vm)
    df = load_dataset(vm)

    train_set, val_set, test_set = prepare_datasets(vm, df)
    model = train_model(vm, model, train_set, val_set)
    evaluate_model(vm, model, train_set=train_set, val_set=val_set, test_set=test_set)


if __name__ == "__main__":
    run()
