import dotenv

import validmind as vm
import xgboost as xgb
from validmind.datasets.classification import customer_churn as demo_dataset


if __name__ == "__main__":
    dotenv.load_dotenv()

    vm.init(
        api_host = "http://localhost:3000/api/v1/tracking",
        project = "clhqxa93500vh0i8hxz2gfzzo"
    )

    df = demo_dataset.load_data()

    vm_dataset = vm.init_dataset(
        dataset=df,
        target_column=demo_dataset.target_column,
        class_labels=demo_dataset.class_labels
    )

    train_df, validation_df, test_df = demo_dataset.preprocess(df)

    x_train = train_df.drop(demo_dataset.target_column, axis=1)
    y_train = train_df[demo_dataset.target_column]
    x_val = validation_df.drop(demo_dataset.target_column, axis=1)
    y_val = validation_df[demo_dataset.target_column]

    model = xgb.XGBClassifier(early_stopping_rounds=10)
    model.set_params(
        eval_metric=["error", "logloss", "auc"],
    )
    model.fit(
        x_train,
        y_train,
        eval_set=[(x_val, y_val)],
        verbose=False,
    )

    vm_train_ds = vm.init_dataset(
        dataset=train_df,
        type="generic",
        target_column=demo_dataset.target_column
    )

    vm_test_ds = vm.init_dataset(
        dataset=test_df,
        type="generic",
        target_column=demo_dataset.target_column
    )

    vm_model = vm.init_model(
        model,
        train_ds=vm_train_ds,
        test_ds=vm_test_ds,
    )

    vm.run_test_suite("binary_classifier_full_suite", dataset=vm_dataset, model=vm_model)
