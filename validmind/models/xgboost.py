# Copyright © 2023 ValidMind Inc. All rights reserved.
from validmind.vm_models.dataset import VMDataset
from validmind.vm_models.model import ModelAttributes

from .sklearn import SKlearnModel


class XGBoostModel(SKlearnModel):
    """
    An XGBoost model class that wraps a trained model instance and its associated data.

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
        model: object = None,
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
