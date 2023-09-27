# Copyright © 2023 ValidMind Inc. All rights reserved.

import itertools
from dataclasses import dataclass

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest

from validmind.vm_models import Figure, Metric


@dataclass
class IsolationForestOutliers(Metric):
    """
    **Purpose**: The purpose of the `IsolationForestOutliers` test is to identify anomalies or outliers in the model's
    dataset. It assumes anomalous data points, due to their distinctive properties, can be detected more quickly by the
    isolation forest algorithm. This algorithm evaluates anomalies through the creation of isolation trees and
    identifying instances with shorter average path lengths in these trees, as these instances are expected to be
    different from the majority of the data points.

    **Test Mechanism**: This test uses the isolation forest algorithm, which isolates anomalies rather than identifying
    normal data points. It runs by building an ensemble of isolation trees, utilizing binary trees created by randomly
    selecting features and splitting the data based on random thresholds. For each pair of variables, it generates a
    scatter plot distinguishing the identified outliers from the inliers. The test results are visualized in these
    scatter plots showing the distinction of outliers from inliers.

    **Signs of High Risk**: Signs of high risk or failure in the model's performance might be the presence of high
    contamination which indicates a lot of anomalies, an inability to detect clusters of anomalies that are
    geographically close in the feature space, detecting normal instances as anomalies or overlooking actual anomalies.

    **Strengths**: The strengths of the isolation forest algorithm include its ability to handle large high-dimensional
    datasets, its efficiency in isolating anomalies rather than normal instances tradition, and its insensitivity to
    the underlying distribution of data. It is able to recognize anomalies even when they are not separated from the
    data cloud by identifying distinctive properties of the anomalies. Additionally, it visualizes the test results,
    aiding understanding and interpretability.

    **Limitations**: Among its limitations, the isolation forest test might find it hard to detect anomalies that are
    close to each other, or in datasets where anomalies are more prevalent. The results strongly rely on the
    contamination parameter, which might need fine-tuning to be effective. It may also not be effective in detecting
    collective anomalies if they behave similarly to normal data. Furthermore, it potentially lacks precision in
    identifying which features contribute most to the anomalous behavior.
    """

    name = "isolation_forest"
    default_params = {
        "random_state": 0,
        "contamination": 0.1,
        "features_columns": None,
    }
    metadata = {
        "task_types": ["classification"],
        "tags": ["tabular_data", "anomaly_detection"],
    }

    required_inputs = ["dataset"]

    def run(self):

        if self.params["features_columns"] is None:
            features_list = self.dataset.get_features_columns()
        else:
            features_list = self.params["features_columns"]

        # Check if all elements from features_list are present in the feature columns
        all_present = all(
            elem in self.dataset.get_features_columns() for elem in features_list
        )
        if not all_present:
            raise ValueError(
                "The list of feature columns provided do not match with "
                + "training dataset feature columns"
            )

        dataset = self.dataset.df

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
