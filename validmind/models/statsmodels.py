# Copyright © 2023 ValidMind Inc. All rights reserved.
import pandas as pd

from validmind.vm_models.dataset import VMDataset
from validmind.vm_models.model import ModelAttributes

from .sklearn import SKlearnModel


class StatsModelsModel(SKlearnModel):
    """
    An Statsmodels model class that wraps a trained model instance and its associated data.

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

    def model_class(self):
        """
        Returns the model class name
        """
        return "statsmodels"

    def regression_coefficients(self):
        """
        Returns the regression coefficients summary of the model
        """
        raw_summary = self.model.summary()

        table = raw_summary.tables[1].data
        headers = table.pop(0)
        headers[0] = "Feature"

        return pd.DataFrame(table, columns=headers)
