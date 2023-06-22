import matplotlib.pyplot as plt

from validmind.vm_models import Figure, Metric


class LoanDefaultRatio(Metric):
    """
    Generates a visual analysis of loan default ratios by plotting bar plots.
    The input dataset can have multiple categorical variables if necessary.
    In this case, we produce a separate plot for each categorical variable.
    """

    name = "loan_default_ratio"
    required_context = ["dataset"]
    default_params = {"loan_status_col": None, "columns": None}

    def plot_loan_default_ratio(self, loan_status_col, columns=None, rsorted=True):
        df = self.dataset.df

        # Use all features if columns is not specified, else use selected columns
        features = df.columns if columns is None else columns

        figures = []
        for feature in features:
            fig, axs = plt.subplots(1, 2)

            # Create sorted unique list of feature values for both plots
            feature_dimension = (
                sorted(df[feature].unique()) if rsorted else df[feature].unique()
            )

            # First subplot for univariate count
            count_values = [
                df[df[feature] == fd][loan_status_col].count()
                for fd in feature_dimension
            ]
            axs[0].bar(feature_dimension, count_values, color="#6699cc")
            axs[0].set_title(f"{feature}", fontsize=18)
            axs[0].set_ylabel("Count", fontsize=18)

            # Second subplot for univariate ratio
            ratio_values = [
                df[df[feature] == fd][loan_status_col].mean()
                for fd in feature_dimension
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

        return self.cache_results(figures=figures)

    def check_loan_status(self, loan_status_col):
        if loan_status_col is None:
            raise ValueError("The loan_status_col parameter needs to be specified.")

        unique_values = self.dataset.df[loan_status_col].unique()
        binary_values = [0, 1]

        if sorted(unique_values) != binary_values:
            raise ValueError(
                f"The column {loan_status_col} is not binary. It contains: {unique_values}"
            )

        print(f"The column {loan_status_col} is correct and contains only 1 and 0.")

    def run(self):
        loan_status = self.params["loan_status_col"]
        columns = self.params["columns"]

        # Check loan status variable has only 1 and 0
        self.check_loan_status(loan_status)

        return self.plot_loan_default_ratio(
            loan_status_col=loan_status, columns=columns
        )
