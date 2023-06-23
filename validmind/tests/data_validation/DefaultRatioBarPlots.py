import matplotlib.pyplot as plt

from validmind.vm_models import Figure, Metric


class DefaultRatioBarPlots(Metric):
    """
    Generates a visual analysis of loan default ratios by plotting bar plots.
    The input dataset can have multiple categorical variables if necessary.
    In this case, we produce a separate plot for each categorical variable.
    """

    name = "default_ratio_bar_plots"
    required_context = ["dataset"]
    default_params = {"default_column": None, "columns": None}

    def plot_loan_default_ratio(self, default_column, columns=None, rsorted=True):
        df = self.dataset.df

        # Use all categorical features if columns is not specified, else use selected columns
        if columns is None:
            features = self.dataset.get_categorical_features_columns()
        else:
            features = columns
        print(features)
        figures = []
        for feature in features:
            fig, axs = plt.subplots(1, 2)

            # Create sorted unique list of feature values for both plots
            feature_dimension = (
                sorted(df[feature].unique().astype(str))
                if rsorted
                else df[feature].unique().astype(str)
            )

            # First subplot for univariate count
            count_values = [
                df[df[feature] == fd][default_column].count()
                for fd in feature_dimension
            ]
            axs[0].bar(feature_dimension, count_values, color="#6699cc")
            axs[0].set_title(f"{feature}", fontsize=18)
            axs[0].set_ylabel("Count", fontsize=18)

            # Second subplot for univariate ratio
            ratio_values = [
                df[df[feature] == fd][default_column].mean() for fd in feature_dimension
            ]
            axs[1].bar(feature_dimension, ratio_values, color="orange")
            axs[1].set_title(f"{feature}", fontsize=18)
            axs[1].set_ylabel("Loan Defaults Ratio", fontsize=18)

            figures.append(
                Figure(
                    for_object=self,
                    key=f"{self.key}:{feature}",
                    figure=fig,
                )
            )

        plt.tight_layout()
        plt.close("all")

        return self.cache_results(
            figures=figures,
        )

    def check_default_column(self, default_column):
        if default_column is None:
            raise ValueError("The default_column parameter needs to be specified.")

        unique_values = self.dataset.df[default_column].unique()
        binary_values = [0, 1]

        if sorted(unique_values) != binary_values:
            raise ValueError(
                f"The column {default_column} is not binary. It contains: {unique_values}"
            )

        print(f"The column {default_column} is correct and contains only 1 and 0.")

    def run(self):
        default_column = self.params["default_column"]
        columns = self.params["columns"]

        # Check loan status variable has only 1 and 0
        self.check_default_column(default_column)

        return self.plot_loan_default_ratio(
            default_column=default_column, columns=columns
        )
