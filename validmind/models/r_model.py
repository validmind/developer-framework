# Copyright © 2023 ValidMind Inc. All rights reserved.
import numpy as np
import pandas as pd

from validmind.vm_models.dataset import VMDataset
from validmind.vm_models.model import ModelAttributes, VMModel


def get_full_class_name(obj):
    return f"{obj.__class__.__module__}.{obj.__class__.__name__}"


class RModel(VMModel):
    """
    An R model class that wraps a "fitted" R model instance and its associated data.

    Attributes:
        attributes (ModelAttributes, optional): The attributes of the model. Defaults to None.
        model (object, optional): The trained model instance. Defaults to None.
        train_ds (Dataset, optional): The training dataset. Defaults to None.
        test_ds (Dataset, optional): The test dataset. Defaults to None.
        validation_ds (Dataset, optional): The validation dataset. Defaults to None.
        y_train_predict (object, optional): The predicted outputs for the training dataset. Defaults to None.
        y_test_predict (object, optional): The predicted outputs for the test dataset. Defaults to None.
        y_validation_predict (object, optional): The predicted outputs for the validation dataset. Defaults to None.
        device_type(str, optional) The device where model is trained
    """

    def __init__(
        self,
        r: object = None,  # R instance
        model: object = None,  # Trained model instance
        train_ds: VMDataset = None,
        test_ds: VMDataset = None,
        validation_ds: VMDataset = None,
        attributes: ModelAttributes = None,
    ):
        self.r = r
        self._is_classification_model = False

        super().__init__(
            model=model,
            train_ds=train_ds,
            test_ds=test_ds,
            validation_ds=validation_ds,
            attributes=attributes,
        )

        self._is_classification_model = self.__is_classification_model()
        self.__load_model_predictions()

    def __get_predict_data_as_df(self, new_data):
        """
        Builds the correct data shape and format for the predict method when the
        caller has passed a Pandas dataframe as input. This function makes sure to
        adjust the shape of the input dataset to the predict() signature depending
        if it's a regular R model or an XGBoost model
        """
        if self.__model_class() == "xgb.Booster":
            return new_data.df.drop(new_data.target_column, axis=1)

        return new_data.df

    def __load_model_predictions(self):
        if self.model and self.train_ds:
            self._y_train_predict = self.predict(
                self.__get_predict_data_as_df(self.train_ds)
            )
        if self.model and self.test_ds:
            self._y_test_predict = self.predict(
                self.__get_predict_data_as_df(self.test_ds)
            )
        if self.model and self.validation_ds:
            self._y_validation_predict = self.predict(
                self.__get_predict_data_as_df(self.validation_ds)
            )

    def __model_class(self):
        """
        Returns the model class name
        """
        return self.r["class"](self.model)[0]

    def __is_classification_model(self):
        """
        Only supported classification models are XGBClassifier and GLM with binomial family (logistic regression).

        Since R uses a single global predict() method for any model, we try to figure out
        if the predict() method called by our tests is supposed to return probabilities or classes
        """
        model_class_name = self.__model_class()

        if model_class_name == "xgb.Booster":
            model_params = self.model.rx2("params")
            model_objective = model_params.rx2("objective")[0]
            return model_objective == "binary:logistic"
        elif model_class_name == "glm":
            model_family = self.model.rx2("family").rx2("family")[0]
            return model_family == "binomial"

        return False

    def __glm_model_class(self):
        """
        Returns the model class name for GLM models which include family and link function
        """
        # Access the attributes of the model
        model_family = self.model.rx2("family")
        model_method = self.model.rx2("method")[0]

        # Extract the family name and link function
        family_name = model_family.rx2("family")[0]
        link_function = model_family.rx2("link")[0]

        # Reconstruct the string in Python
        output = (
            f"{model_method} (Family: {family_name}, Link function: {link_function})"
        )

        return output

    def r_predict(self, new_data_r):
        """
        Predict method for the model. This is a wrapper around R's global predict.

        An R model doesn't provide separate predict() and predict_proba() methods.
        Instead, there is a global predict() method that returns the predicted
        values according to the model type.
        """
        # Use the predict method on the loaded model (assuming the model's name in R is 'model')
        predicted_probs = self.r.predict(
            self.model, newdata=new_data_r, type="response"
        )
        return predicted_probs

    def r_xgb_predict(self, new_data_r):
        """
        Predict method for XGBoost models. This is a wrapper around R's global predict
        """
        new_data_matrix = self.r["as.matrix"](new_data_r)
        new_data_r = self.r["xgb.DMatrix"](new_data_matrix)

        predicted_probs = self.r.predict(
            self.model, newdata=new_data_r, type="response"
        )
        return predicted_probs

    def predict_proba(self, new_data):
        """
        Calls the R global predict method with type="response" to get the predicted probabilities
        """
        return self.predict(new_data, return_probs=True)

    def predict(self, new_data, return_probs=False):
        """
        Converts the predicted probabilities to classes
        """
        from rpy2.robjects import pandas2ri

        # Activate the pandas conversion for rpy2
        pandas2ri.activate()

        new_data_class = get_full_class_name(new_data)

        if new_data_class == "numpy.ndarray":
            # We need to reconstruct the DataFrame from the ndarray using the column names
            new_data = pd.DataFrame(
                new_data, columns=self.test_ds.get_features_columns()
            )
        elif new_data_class != "pandas.core.frame.DataFrame":
            raise ValueError(
                f"new_data must be a DataFrame or ndarray. Got {new_data_class}"
            )

        new_data_r = pandas2ri.py2rpy(new_data)

        if self.__model_class() == "xgb.Booster":
            predicted_probs = self.r_xgb_predict(new_data_r)
        else:
            predicted_probs = self.r_predict(new_data_r)

        if self._is_classification_model and return_probs is False:
            predicted_classes = np.where(predicted_probs > 0.5, 1, 0)
            return predicted_classes

        return predicted_probs

    def model_language(self):
        """
        Returns the model library name
        """
        return self.r["version"].rx2("version.string")[0]

    def model_library(self):
        """
        Returns the model library name
        """
        return "R"

    def model_library_version(self, *args, **kwargs):
        """
        Model framework library version
        """
        return "N/A"

    def model_class(self):
        """
        Returns the model class name
        """
        return "R"

    def model_name(self):
        """
        Returns model name
        """
        model_class_name = self.__model_class()

        if model_class_name == "lm":
            return "Linear Regression"
        elif model_class_name == "xgb.Booster":
            return "XGBoost"
        elif model_class_name == "glm":
            return self.__glm_model_class()

        return model_class_name

    def regression_coefficients(self):
        """
        Returns the regression coefficients summary of the model
        """
        # Each list in this list contains the coefficients for one feature, starting with the intercept
        coefficient_values = self.r.summary(self.model).rx2("coefficients")

        # Extract the coefficient names by calling the model terms.
        # [[1]] is the endogenous variable and the rest are the coefficients
        model_terms = self.model.rx2["terms"]
        variables_attr = self.r.attr(model_terms, "variables")

        variables_list = [str(variables_attr[i]) for i in range(1, len(variables_attr))]
        # Remove "Const" from the list of variables for Poisson regression
        variables_list = [v for v in variables_list if v != "Const"]

        # Build a dataframe where each row is a feature (including the intercept) and each column is one
        # of the values in the coefficient_values list, which has: [Estimate, Std. Error, t value, Pr(>|t|)]
        # We use ["coef", "std errr", "z", "P>|z|"] to stay consistent with the statsmodels implementation
        # Remove the first row which is the intercept
        coefficient_values = coefficient_values[1:]
        coefficients_df = pd.DataFrame(
            coefficient_values,
            columns=["coef", "std err", "z", "P>|z|"],
        )

        # Add the feature names as a column and rearrange to have feature name as the first column
        coefficients_df["Feature"] = variables_list[1:]
        coefficients_df = coefficients_df[["Feature"] + list(coefficients_df.columns)]

        return coefficients_df
