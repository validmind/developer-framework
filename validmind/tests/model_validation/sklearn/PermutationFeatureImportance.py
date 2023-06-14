from dataclasses import dataclass

import matplotlib.pyplot as plt
from sklearn.inspection import permutation_importance

from validmind.logging import get_logger
from validmind.vm_models import Figure, Metric, Model

logger = get_logger(__name__)


@dataclass
class PermutationFeatureImportance(Metric):
    """
    Permutation Feature Importance
    """

    name = "pfi"
    required_context = ["model"]

    def description(self):
        return """
        The Feature Importance plot below calculates a score representing the
        importance of each feature in the model. A higher score indicates
        that the specific input feature will have a larger effect on the
        predictive power of the model.

        The importance score is calculated using Permutation Feature
        Importance. Permutation feature importance measures the decrease of
        model performance after the feature''s values have been permuted, which
        breaks the relationship between the feature and the true outcome. A
        feature is "important" if shuffling its values increases the model
        error, because in this case the model relied on the feature for the
        prediction. A feature is "unimportant" if shuffling its values leaves
        the model error unchanged, because in this case the model ignored the
        feature for the prediction.
        """

    def run(self):
        x = self.model.train_ds.x
        y = self.model.train_ds.y

        model_instance = self.model.model
        model_library = Model.model_library(model_instance)
        if model_library == "statsmodels" or model_library == "pytorch":
            logger.info(f"Skiping PFI for {model_library} models")
            return

        # Check if the model has a fit method. This works for statsmodels
        # if not hasattr(model_instance, "fit"):
        #     model_instance.fit = lambda **kwargs: None

        pfi_values = permutation_importance(
            model_instance,
            x,
            y,
            random_state=0,
            n_jobs=-2,
            # scoring="neg_mean_squared_log_error",
        )
        pfi = {}
        for i, column in enumerate(x.columns):
            pfi[column] = [pfi_values["importances_mean"][i]], [
                pfi_values["importances_std"][i]
            ]

        sorted_idx = pfi_values.importances_mean.argsort()
        fig, ax = plt.subplots()
        ax.barh(
            x.columns[sorted_idx], pfi_values.importances[sorted_idx].mean(axis=1).T
        )
        ax.set_title("Permutation Importances (test set)")

        return self.cache_results(
            metric_value=pfi,
            figures=[
                Figure(
                    for_object=self,
                    key="pfi",
                    figure=fig,
                ),
            ],
        )
