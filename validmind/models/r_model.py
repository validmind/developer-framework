# Copyright © 2023 ValidMind Inc. All rights reserved.
import numpy as np

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
        # TODO: do this only for classification models
        predicted_classes = np.where(predicted_probs > 0.5, 1, 0)
        return predicted_classes

    def __load_model_predictions(self):
        from rpy2.robjects import pandas2ri

        # Activate the pandas conversion for rpy2
        pandas2ri.activate()

        # An R model doesn't provide separate predict() and predict_proba() methods.
        # Instead, there is a global predict() method that returns the predicted
        # values according to the model type.
        if self.model and self.train_ds:
            train_data_r = pandas2ri.py2rpy(self.train_ds.df)
            self._y_train_predict = self.r_predict(train_data_r)
        if self.model and self.test_ds:
            test_data_r = pandas2ri.py2rpy(self.test_ds.df)
            self._y_test_predict = self.r_predict(test_data_r)
        if self.model and self.validation_ds:
            validation_data_r = pandas2ri.py2rpy(self.validation_ds.df)
            self._y_validation_predict = self.r_predict(validation_data_r)

    def predict_proba(self, *args, **kwargs):
        """
        predict_proba (for classification) or predict (for regression) method
        """
        if not has_method_with_arguments(self.model, "predict_proba", 1):
            raise MissingModelPredictFnError(
                "Model requires a implemention of predict_proba method with 1 argument"
                + " that is features matrix"
            )
        if callable(getattr(self.model, "predict_proba", None)):
            return self.model.predict_proba(*args, **kwargs)[:, 1]
        return None

    def predict(self, *args, **kwargs):
        """
        Predict method for the model. This is a wrapper around the model's
        """
        return self.model.predict(*args, **kwargs)

    def model_library(self):
        """
        Returns the model library name
        """
        return self.model.__class__.__module__.split(".")[0]

    def model_class(self):
        """
        Returns the model class name
        """
        return self.model.__class__.__name__

    def model_name(self):
        """
        Returns model name
        """
        return type(self.model).__name__
