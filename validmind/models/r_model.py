# Copyright © 2023 ValidMind Inc. All rights reserved.
import numpy as np
import pandas as pd

from validmind.errors import MissingModelPredictFnError
from validmind.vm_models.dataset import VMDataset
from validmind.vm_models.model import (
    ModelAttributes,
    VMModel,
    has_method_with_arguments,
)


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
        super().__init__(
            model=model,
            train_ds=train_ds,
            test_ds=test_ds,
            validation_ds=validation_ds,
            attributes=attributes,
        )
        self.r = r
        self.__load_model_predictions()

    def r_predict(self, new_data_r):
        """
        Predict method for the model. This is a wrapper around R's global predict
        """
        # Use the predict method on the loaded model (assuming the model's name in R is 'model')
        predicted_probs = self.r.predict(
            self.model, newdata=new_data_r, type="response"
        )
        return predicted_probs

    def __load_model_predictions(self):
        from rpy2.robjects import pandas2ri

        # Activate the pandas conversion for rpy2
        pandas2ri.activate()

        # An R model doesn't provide separate predict() and predict_proba() methods.
        # Instead, there is a global predict() method that returns the predicted
        # values according to the model type.
        if self.model and self.train_ds:
            train_data_r = pandas2ri.py2rpy(self.train_ds.df)
            self._y_train_predict = self.predict(train_data_r)
        if self.model and self.test_ds:
            test_data_r = pandas2ri.py2rpy(self.test_ds.df)
            self._y_test_predict = self.predict(test_data_r)
        if self.model and self.validation_ds:
            validation_data_r = pandas2ri.py2rpy(self.validation_ds.df)
            self._y_validation_predict = self.predict(validation_data_r)

    def predict_proba(self, new_data):
        """
        Calls the R global predict method with type="response" to get the predicted probabilities
        """
        from rpy2.robjects import pandas2ri

        # Activate the pandas conversion for rpy2
        pandas2ri.activate()

        new_data_class = new_data.__class__.__name__

        if new_data_class == "ndarray":
            # We need to reconstruct the DataFrame from the ndarray using the column names
            new_data = pd.DataFrame(
                new_data, columns=self.test_ds.get_features_columns()
            )
        elif new_data_class != "DataFrame":
            raise ValueError(
                f"new_data must be a DataFrame or ndarray. Got {new_data_class}"
            )

        # Add a new column from self.test_ds to the new_data. This is needed because
        # the R predict method requires the same columns as the training data.
        new_data[self.test_ds.target_column] = 0
        new_data_r = pandas2ri.py2rpy(new_data)

        return self.r_predict(new_data_r)

    def predict(self, new_data_r):
        """
        Converts the predicted probabilities to classes
        """
        predicted_probs = self.r_predict(new_data_r)
        # TODO: do this only for classification models
        predicted_classes = np.where(predicted_probs > 0.5, 1, 0)
        return predicted_classes

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
