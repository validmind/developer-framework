# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import itertools
from dataclasses import dataclass

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest

from validmind.vm_models import Figure, Metric


@dataclass
class IsolationForestOutliers(Metric):
    """
    Detects outliers in a dataset using the Isolation Forest algorithm and visualizes results through scatter plots.

    ### Purpose

    The IsolationForestOutliers test is designed to identify anomalies or outliers in the model's dataset using the
    isolation forest algorithm. This algorithm assumes that anomalous data points can be isolated more quickly due to
    their distinctive properties. By creating isolation trees and identifying instances with shorter average path
    lengths, the test is able to pick out data points that differ from the majority.

    ### Test Mechanism

    The test uses the isolation forest algorithm, which builds an ensemble of isolation trees by randomly selecting
    features and splitting the data based on random thresholds. It isolates anomalies rather than focusing on normal
    data points. For each pair of variables, a scatter plot is generated which distinguishes the identified outliers
    from the inliers. The results of the test can be visualized using these scatter plots, illustrating the distinction
    between outliers and inliers.

    ### Signs of High Risk

    - The presence of high contamination, indicating a large number of anomalies
    - Inability to detect clusters of anomalies that are close in the feature space
    - Misclassifying normal instances as anomalies
    - Failure to detect actual anomalies

    ### Strengths

    - Ability to handle large, high-dimensional datasets
    - Efficiency in isolating anomalies instead of normal instances
    - Insensitivity to the underlying distribution of data
    - Ability to recognize anomalies even when they are not separated from the main data cloud through identifying
    distinctive properties
    - Visually presents the test results for better understanding and interpretability

    ### Limitations

    - Difficult to detect anomalies that are close to each other or prevalent in datasets
    - Dependency on the contamination parameter which may need fine-tuning to be effective
    - Potential failure in detecting collective anomalies if they behave similarly to normal data
    - Potential lack of precision in identifying which features contribute most to the anomalous behavior
    """

    name = "isolation_forest"
    default_params = {
        "random_state": 0,
        "contamination": 0.1,
        "features_columns": None,
    }
    tasks = ["classification"]
    tags = ["tabular_data", "anomaly_detection"]

    required_inputs = ["dataset"]

    def run(self):
        if self.params["features_columns"] is None:
            features_list = self.inputs.dataset.feature_columns_numeric
        else:
            features_list = self.params["features_columns"]

        # Check if all elements from features_list are present in the feature columns
        all_present = all(
            elem in self.inputs.dataset.feature_columns for elem in features_list
        )
        if not all_present:
            raise ValueError(
                "The list of feature columns provided do not match with "
                + "training dataset feature columns"
            )

        dataset = self.inputs.dataset.df[features_list]

        # Training with isolation forest algorithm
        clf = IsolationForest(
            random_state=self.params["random_state"],
            contamination=self.params["contamination"],
        )
        clf.fit(dataset)
        y_pred = clf.predict(dataset)

        test_figures = []
        combination_pairs = list(itertools.combinations(features_list, 2))
        for feature1, feature2 in combination_pairs:
            fig = plt.figure()
            ax = sns.scatterplot(
                data=dataset, x=feature1, y=feature2, hue=y_pred, palette="bright"
            )
            handles, labels = ax.get_legend_handles_labels()
            labels = list(map(lambda x: x.replace("-1", "Outliers"), labels))
            labels = list(map(lambda x: x.replace("1", "Inliers"), labels))
            ax.legend(handles, labels)
            # Do this if you want to prevent the figure from being displayed
            plt.close("all")

            test_figures.append(
                Figure(
                    for_object=self,
                    key=f"{self.name}:{feature1}_{feature2}",
                    figure=fig,
                )
            )

        return self.cache_results(figures=test_figures)
