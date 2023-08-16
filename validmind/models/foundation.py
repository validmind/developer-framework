from dataclasses import dataclass

import numpy as np

from validmind.vm_models.dataset import VMDataset
from validmind.vm_models.model import ModelAttributes, VMModel


@dataclass
class ModelEndpoint:
    url: str
    auth_token: str
    auth_token_type: str  # one of 'Bearer', 'Basic', 'Header'
    auth_token_header: str  # if auth_token_type is 'Header', then this is the header name


class FoundationModel(VMModel):
    """FoundationModel class wraps a Foundation LLM endpoint

    This class wraps an API endpoint for a foundation model (for now) and converts
    it to work with ValidMind's model interface.

    Attributes:
        endpoint (object): The trained model instance. Defaults to None.
        prompt (str): The prompt for the model. Defaults to None.
        train_ds (Dataset, optional): The training dataset. Defaults to None.
        test_ds (Dataset, optional): The test dataset. Defaults to None.
        validation_ds (Dataset, optional): The validation dataset. Defaults to None.
        attributes (ModelAttributes, optional): The attributes of the model. Defaults to None.
    """

    def __init__(
        self,
        endpoint: ModelEndpoint,  # api endpoint
        prompt: str,  # prompt used for model (for now just a string) # TODO: support complex prompts
        train_ds: VMDataset = None,
        test_ds: VMDataset = None,
        validation_ds: VMDataset = None,
        attributes: ModelAttributes = None,
    ):
        super().__init__(
            train_ds=train_ds,
            test_ds=test_ds,
            validation_ds=validation_ds,
            attributes=attributes,
        )

        if self.model and self.train_ds:
            self._y_train_predict = np.array(self.predict(self.train_ds.x))
        if self.model and self.test_ds:
            self._y_test_predict = np.array(self.predict(self.test_ds.x))
        if self.model and self.validation_ds:
            self._y_validation_predict = np.array(self.predict(self.validation_ds.x))

    def predict_proba(self, *args, **kwargs):
        """
        predict_proba (for classification) or predict (for regression) method
        """
        pass  # TODO: implement

    def predict(self, *args, **kwargs):
        """
        Predict method for the model. This is a wrapper around the model's
        """
        pass

    def model_library(self):
        """
        Returns the model library name
        """
        return "Foundation"

    def model_class(self):
        """
        Returns the model class name
        """
        return "FoundationModel"

    def model_name(self):
        """
        Returns model name
        """
        return "FoundationModel"
