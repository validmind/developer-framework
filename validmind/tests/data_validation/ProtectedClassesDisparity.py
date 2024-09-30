# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from aequitas.group import Group
from aequitas.bias import Bias
from aequitas.plotting import Plot
import io
import pandas as pd
import matplotlib.pyplot as plt


def ProtectedClassesDisparity(
    dataset,
    model,
    protected_classes,
    disparity_tolerance,
    metrics=["fnr", "fpr", "tpr"],
):
    """
    Investigates disparities in model outcomes across protected classes using various fairness metrics.

    ### Purpose

    This test aims to identify and quantify potential biases in model outcomes across different demographic groups
    or protected classes. It helps ensure that the model's predictions are fair and do not disproportionately
    disadvantage any particular group.

    ### Test Mechanism

    The test calculates and compares various fairness metrics across different segments of protected classes:

    1. Computes metrics such as False Negative Rate (FNR), False Positive Rate (FPR), and True Positive Rate (TPR)
       for each group within the protected classes.
    2. Calculates disparity ratios between groups for each metric.
    3. Compares these ratios against a specified disparity tolerance threshold.
    4. Generates visualizations to highlight disparities.

    The test also provides additional metrics in the output table:

    - True Positive Rate (TPR): Fraction of true positives within label positive entities of a group.
    - True Negative Rate (TNR): Fraction of true negatives within label negative entities of a group.
    - False Negative Rate (FNR): Fraction of false negatives within label positive entities of a group.
    - False Positive Rate (FPR): Fraction of false positives within label negative entities of a group.
    - Precision: Fraction of true positives within predicted positive entities of a group.
    - Negative Predictive Value (NPV): Fraction of true negatives within predicted negative entities of a group.
    - False Discovery Rate (FDR): Fraction of false positives within predicted positive entities of a group.
    - False Omission Rate (FOR): Fraction of false negatives within predicted negative entities of a group.
    - Predicted Positive (PPR): Number of entities within a group where the decision is positive.
    - Predicted Prevalence (PPREV): Fraction of entities within a group predicted as positive.

    ### Signs of High Risk

    - Disparity ratios exceeding the specified tolerance threshold for any metric.
    - Consistent patterns of disparity across multiple metrics for a particular group.
    - Large variations in false positive or false negative rates between groups.

    ### Strengths

    - Provides a comprehensive view of fairness across multiple metrics.
    - Allows for customizable disparity tolerance thresholds.
    - Generates visual representations to easily identify areas of concern.

    ### Limitations

    - Relies on pre-defined protected classes, which may not capture all relevant demographic factors.
    - Does not account for intersectionality or compounding effects of multiple protected attributes.
    - The choice of reference group can influence the interpretation of results.

    """

    df = dataset._df

    for protected_class in protected_classes:
        # make the dataset compatible for the python package of interest
        df[protected_class] = pd.Categorical(df[protected_class]).astype("object")

    df["score"] = dataset.y_pred(model).astype(int)
    df["label_value"] = df[dataset.target_column].astype(int)

    # let map the attributes for each protected class
    # default use reference that is most observable for dictionary
    attributes_and_reference_groups = {}
    for protected_class in protected_classes:
        attributes_and_reference_groups[protected_class] = (
            df[protected_class].value_counts().idxmax()
        )

    attributes_to_audit = list(attributes_and_reference_groups.keys())

    # Initialize Aequitas
    g = Group()
    b = Bias()
    aqp = Plot()

    columns_to_include = (
        protected_classes + [dataset.target_column] + ["score", "label_value"]
    )

    # get_crosstabs returns a dataframe of the group counts and group value bias metrics.
    xtab, _ = g.get_crosstabs(df[columns_to_include], attr_cols=attributes_to_audit)
    bdf = b.get_disparity_predefined_groups(
        xtab,
        original_df=df[columns_to_include],
        ref_groups_dict=attributes_and_reference_groups,
        alpha=0.05,
        mask_significance=True,
    )

    plots = []
    for protected_class in protected_classes:
        plot = aqp.plot_disparity(
            bdf, metrics, protected_class, fairness_threshold=disparity_tolerance
        )

        buf = io.BytesIO()  # create a bytes array to save the image into in memory
        plot.save(
            buf, format="png"
        )  # as long as the above library is installed, this will work
        plots.append(buf.getvalue())

    string = "_disparity"
    metrics_adj = [x + string for x in metrics]

    table = bdf[["attribute_name", "attribute_value"] + b.list_disparities(bdf)]

    # Convert the disparity_all plot to bytes
    all_disparity_plot = aqp.plot_disparity_all(bdf, metrics=metrics_adj)
    buf = io.BytesIO()
    all_disparity_plot.savefig(buf, format="png")
    buf.seek(0)  # Move the cursor to the beginning of the buffer
    plots.append(buf.getvalue())

    plt.close(all_disparity_plot)  # Close the figure to free up memory

    plots_return = tuple(plots)

    return (table, *plots_return)
