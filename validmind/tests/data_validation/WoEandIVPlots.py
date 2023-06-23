import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from dataclasses import dataclass
from validmind.vm_models import Figure, Metric


@dataclass
class WoEandIVPlots(Metric):
    """
    Generates a visual analysis of the WoE and IV values distribution for categorical variables.
    The input dataset is required.
    """

    name = "woe_and_iv_plots"
    required_context = ["dataset"]
    default_params = {"label_rotation": 0, "features": None}

    def run(self):
        df = self.dataset.df
        target_column = self.dataset.target_column
        features = self.params["features"]

        woe_iv_df = self.calculate_woe_iv(df, target_column, features)
        figures = self.plot_woe_iv_distribution(
            woe_iv_df, self.params["label_rotation"]
        )

        return self.cache_results(figures=figures)

    @staticmethod
    def calculate_woe_iv(df, target_column, features=None):
        # If no specific features specified, use all columns in the DataFrame
        if features is None:
            features = df.drop(target_column, axis=1).columns.tolist()

        # Create a dataframe to store WoE and IV values
        master = []

        for feature in features:
            lst = []

            # For each unique category in the feature
            for val in df[feature].unique():
                lst.append(
                    {
                        "Variable": feature,
                        "Value": val,
                        "All": df[df[feature] == val].count()[feature],
                        "Good": df[
                            (df[feature] == val) & (df[target_column] == 0)
                        ].count()[feature],
                        "Bad": df[
                            (df[feature] == val) & (df[target_column] == 1)
                        ].count()[feature],
                    }
                )

            dset = pd.DataFrame(lst)

            # Calculate WoE and IV
            dset["Distr_Good"] = dset["Good"] / dset["Good"].sum()
            dset["Distr_Bad"] = dset["Bad"] / dset["Bad"].sum()
            dset["WoE"] = np.log(dset["Distr_Good"] / dset["Distr_Bad"])
            dset["IV"] = (dset["Distr_Good"] - dset["Distr_Bad"]) * dset["WoE"]

            master.append(dset)

        master_dset = pd.concat(master, ignore_index=True)

        return master_dset.sort_values(by=["Variable", "WoE"])

    def plot_woe_iv_distribution(self, woe_iv_df, label_rotation):
        variables = woe_iv_df["Variable"].unique()
        figures = []

        for variable in variables:
            variable_df = woe_iv_df[woe_iv_df["Variable"] == variable]
            fig, axs = plt.subplots(2, 2)

            # WoE bar plot
            sns.barplot(
                x="Value", y="WoE", data=variable_df, ax=axs[0, 0], color="skyblue"
            )
            axs[0, 0].set_title(f"WoE for {variable}")
            axs[0, 0].set_ylabel("Weight of Evidence (WoE)")
            axs[0, 0].set_xticklabels(
                axs[0, 0].get_xticklabels(), rotation=label_rotation
            )

            # IV bar plot
            sns.barplot(
                x="Value", y="IV", data=variable_df, ax=axs[0, 1], color="skyblue"
            )
            axs[0, 1].set_title(f"IV for {variable}")
            axs[0, 1].set_ylabel("Information Value (IV)")
            axs[0, 1].set_xticklabels(
                axs[0, 1].get_xticklabels(), rotation=label_rotation
            )

            # Distribution plot
            distribution_df = variable_df.melt(
                id_vars="Value", value_vars=["Distr_Good", "Distr_Bad"]
            )
            sns.barplot(
                x="Value", y="value", hue="variable", data=distribution_df, ax=axs[1, 0]
            )
            axs[1, 0].set_title(f"Distribution of Good and Bad for {variable}")
            axs[1, 0].set_ylabel("Distribution")
            axs[1, 0].set_xticklabels(
                axs[1, 0].get_xticklabels(), rotation=label_rotation
            )

            # WoE trend plot
            sns.lineplot(x="Value", y="WoE", data=variable_df, marker="o", ax=axs[1, 1])
            axs[1, 1].set_title(f"WoE Trend for {variable}")
            axs[1, 1].set_ylabel("Weight of Evidence (WoE)")
            axs[1, 1].set_xticklabels(
                axs[1, 1].get_xticklabels(), rotation=label_rotation
            )

            plt.tight_layout()
            plt.show()

            figures.append(
                Figure(
                    for_object=self, key=f"{self.key}:{variable}", figure=plt.figure()
                )
            )

        plt.close("all")

        return figures
