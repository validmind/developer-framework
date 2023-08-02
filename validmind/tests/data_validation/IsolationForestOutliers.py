# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from sklearn.ensemble import IsolationForest
import itertools
import matplotlib.pyplot as plt
import seaborn as sns


from validmind.vm_models import (
    Figure,
    Metric,
)


@dataclass
class IsolationForestOutliers(Metric):
    """
    Isolation Forest.
    This class implements the Isolation Forest algorithm for anomaly detection.
    Attributes:
        name (str): The name of the Isolation Forest.
        default_params (dict): The default parameters for the Isolation Forest.
        required_context (list): The required context for running the Isolation Forest.

    Methods:
        description(): Returns the description of the Isolation Forest.
        run(): Runs the Isolation Forest algorithm.
    """

    name = "isolation_forest"
    default_params = {
        "random_state": 0,
        "contamination": 0.1,
        "features_columns": None,
    }
    required_context = ["dataset"]

    def description(self):
        return """
        The Isolation Forest test is an algorithm used for anomaly detection in datasets. It is based
        on the concept of isolating anomalies rather than identifying normal data points. The test builds an ensemble
        of isolation trees, which are binary trees created by randomly selecting features and splitting the data based
        on random thresholds.

        The main idea behind the Isolation Forest test is that anomalies are likely to be isolated quickly in these trees
        compared to normal instances. Anomalies are expected to have shorter average path lengths in the trees,
        as they are different from the majority of the data points.

        It's important to note that the Isolation Forest test assumes anomalies are less frequent and have different properties
        compared to normal instances. However, it may not be as effective in detecting anomalies that are close to each other
        or in datasets where anomalies are more prevalent."""

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
