# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import plotly.graph_objects as go
from sklearn.inspection import permutation_importance

from validmind.errors import SkipTestError
from validmind.logging import get_logger
from validmind.vm_models import Figure, Metric

logger = get_logger(__name__)


@dataclass
class PermutationFeatureImportance(Metric):
    """
    **Purpose**: The purpose of the "Permutation Feature Importance" (PFI) metric is to quantify the importance of each
    feature used by the ML model. This is measured depending on how much the model's performance decreases when the
    values of each feature are permuted.

    **Test Mechanism**: The PFI metric is calculated using the `permutation_importance` method from the
    `sklearn.inspection` module. This function randomly permutes the columns of the feature dataset fed into the ML
    model and measures how the model's performance changes. If the model's performance worsens significantly after
    permuting a feature's values, that feature is deemed important. If the performance remains relatively constant, the
    feature is considered unimportant. At the end of the execution, PFI metric returns a figure displaying the feature
    importance of each feature.

    **Signs of High Risk**: An indication of risk would be if the model primarily depends on a feature whose values can
    easily be permuted or have high variance, suggesting instability. Another risk could be if there's a feature
    predicted as of no importance but is known to have significant influence on the expected outcome based on domain
    knowledge.

    **Strengths**: The PFI metric has several key advantages. It can provide an understanding of which features are
    crucial for the model's predictions, potentially revealing insights about the data's structure. This can also help
    determine if the model is overfitting on a particular feature or set of features. Moreover, PFI is model-agnostic
    and can be used for any classifier which can provide a measure of prediction accuracy before and after permuting
    features.

    **Limitations**: Although this metric is particularly helpful, there are some limitations too. The primary
    limitation is that feature importance calculated from this method does not imply causality—it only speaks to the
    amount of information the feature provides about the prediction task. Besides, permutation importance does not
    consider the interaction between features. If two features are correlated, the permutation importance might
    allocate importance to only one at the expense of the other. Finally, it cannot handle models from certain
    libraries like statsmodels, pytorch, catboost etc., thus limiting its applicability.
    """

    name = "pfi"
    required_inputs = ["model", "model.train_ds", "model.test_ds"]
    default_params = {
        "fontsize": None,
        "figure_height": 1000,
    }
    metadata = {
        "task_types": ["classification", "text_classification"],
        "tags": [
            "sklearn",
            "binary_classification",
            "multiclass_classification",
            "feature_importance",
            "visualization",
        ],
    }

    def run(self):
        x = self.model.train_ds.x_df()
        y = self.model.train_ds.y_df()

        model_library = self.model.model_library()
        if (
            model_library == "statsmodels"
            or model_library == "pytorch"
            or model_library == "catboost"
            or model_library == "transformers"
            or model_library == "R"
        ):
            raise SkipTestError(f"Skipping PFI for {model_library} models")

        pfi_values = permutation_importance(
            self.model.model,
            x,
            y,
            random_state=0,
            n_jobs=-2,
        )

        pfi = {}
        for i, column in enumerate(x.columns):
            pfi[column] = [pfi_values["importances_mean"][i]], [
                pfi_values["importances_std"][i]
            ]

        sorted_idx = pfi_values.importances_mean.argsort()

        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                y=x.columns[sorted_idx],
                x=pfi_values.importances[sorted_idx].mean(axis=1).T,
                orientation="h",
            )
        )
        fig.update_layout(
            title_text="Permutation Importances (train set)",
            yaxis=dict(
                tickmode="linear",  # set tick mode to linear
                dtick=1,  # set interval between ticks
                tickfont=dict(
                    size=self.params["fontsize"]
                ),  # set the tick label font size
            ),
            height=self.params["figure_height"],  # use figure_height parameter here
        )

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
