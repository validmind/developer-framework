# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import numpy as np
import pandas as pd

from validmind.errors import MissingModelPredictFnError
from validmind.logging import get_logger
from validmind.vm_models.dataset import VMDataset
from validmind.vm_models.model import (
    ModelAttributes,
    VMModel,
    has_method_with_arguments,
)

logger = get_logger(__name__)


@dataclass
class HFModel(VMModel):
    """
    An Hugging Face model class that wraps a trained model instance and its associated data.

    Attributes:
        attributes (ModelAttributes, optional): The attributes of the model. Defaults to None.
        model (object, optional): The trained model instance. Defaults to None.
        train_ds (Dataset, optional): The train dataset. Defaults to None.
        test_ds (Dataset, optional): The test dataset. Defaults to None.
        validation_ds (Dataset, optional): The validation dataset. Defaults to None.
        y_test_predict (object, optional): The predicted outputs for the test dataset. Defaults to None.
        y_validation_predict (object, optional): The predicted outputs for the validation dataset. Defaults to None.
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

        def predict_and_assign(ds, attr_name):
            if self.model and ds:
                if ds.prediction_column:
                    setattr(self, attr_name, ds.y_pred)
                else:
                    logger.info("Running predict()...This may take a while")
                    x_only = ds.x
                    setattr(self, attr_name, np.array(self.predict(x_only)))

        predict_and_assign(self.train_ds, "_y_train_predict")
        predict_and_assign(self.test_ds, "_y_test_predict")
        predict_and_assign(self.validation_ds, "_y_validation_predict")

    def predict_proba(self, *args, **kwargs):
        """
        Invoke predict_proba from underline model
        """
        if not has_method_with_arguments(self.model, "predict_proba", 1):
            raise MissingModelPredictFnError(
                "Model requires a implemention of predict_proba method with 1 argument"
                + " that is tensor features matrix"
            )

        if callable(getattr(self.model, "predict_proba", None)):
            return self.model.predict_proba(*args, **kwargs)[:, 1]

    def predict(self, data):
        """
        Predict method for the model. This is a wrapper around the HF model's pipeline function
        """
        results = self.model([str(datapoint) for datapoint in data])

        tasks = self.model.__class__.__module__.split(".")

        if "text2text_generation" in tasks:
            return pd.DataFrame(results).summary_text.values
        elif "text_classification" in tasks:
            return pd.DataFrame(results).label.values
        elif tasks[-1] == "feature_extraction":
            # extract [CLS] token embedding for each input and wrap in dataframe
            return pd.DataFrame([embedding[0][0] for embedding in results])
        else:
            return results

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

    def is_pytorch_model(self):
        return self.model_library() == "torch"
