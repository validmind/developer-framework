"""
Metrics functions models trained with statsmodels or that provide
a statsmodels-like API
"""
from dataclasses import dataclass
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import kpss
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.sandbox.stats.runs import runstest_1samp
from statsmodels.stats.diagnostic import kstest_normal
from statsmodels.stats.diagnostic import lilliefors
from statsmodels.stats.stattools import jarque_bera
from statsmodels.graphics.tsaplots import plot_acf
from arch.unitroot import PhillipsPerron
from arch.unitroot import ZivotAndrews
from arch.unitroot import DFGLS
from ...vm_models import Figure, Metric


@dataclass
class ResidualsVisualInspection(Metric):
    """
    Log plots for visual inspection of residuals
    """

    type = "evaluation"
    key = "residuals_visual_inspection"

    def get_residuals(self, column, series):
        """
        Get the seasonal decomposition residuals from the test
        context or re-compute them if not available. This allows
        running the test individually or as part of a test plan.
        """
        sd_all_columns = self.test_context.get_context_data("seasonal_decompose")
        if sd_all_columns is None or column not in sd_all_columns:
            return seasonal_decompose(series, model="additive")

        return sd_all_columns[column]

    @staticmethod
    def residual_analysis(residuals, variable_name, axes):
        residuals = residuals.dropna().reset_index(
            drop=True
        )  # drop NaN values and reset index

        # QQ plot
        stats.probplot(residuals, dist="norm", plot=axes[0, 1])
        axes[0, 1].set_title(f"Residuals Q-Q Plot ({variable_name})")

        # Histogram with KDE
        sns.histplot(residuals, kde=True, ax=axes[0, 0])
        axes[0, 0].set_xlabel("Residuals")
        axes[0, 0].set_title(f"Residuals Histogram ({variable_name})")

        # Residual series dot plot
        sns.lineplot(data=residuals, linewidth=0.5, color="red", ax=axes[1, 0])
        axes[1, 0].set_title(f"Residual Series Dot Plot ({variable_name})")

        # ACF plot
        n_lags = min(100, len(residuals) - 1)  # Adjust the number of lags
        plot_acf(residuals, ax=axes[1, 1], lags=n_lags, zero=False)  # Added zero=False
        axes[1, 1].set_title(f"ACF Plot of Residuals ({variable_name})")

    def run(self):
        x_train = self.train_ds.df
        x_train = self.train_ds.df
        figures = []

        # TODO: specify which columns to plot via params
        for col in x_train.columns:
            sd = self.get_residuals(col, x_train[col])

            # Remove NaN values from the residuals and reset the index
            residuals = pd.Series(sd.resid).dropna().reset_index(drop=True)

            # Create subplots
            fig, axes = plt.subplots(nrows=2, ncols=2)
            fig.suptitle(f"Residuals Inspection for {col}", fontsize=24)

            self.residual_analysis(residuals, col, axes)

            # Adjust the layout
            plt.tight_layout()

            # Do this if you want to prevent the figure from being displayed
            plt.close("all")

            figures.append(Figure(key=self.key, figure=fig, metadata={}))
        return self.cache_results(figures=figures)


class ADF(Metric):
    """
    Augmented Dickey-Fuller unit root test for establishing the order of integration of
    time series
    """

    type = "dataset"  # assume this value
    key = "adf"

    def run(self):
        """
        Calculates ADF metric for each of the dataset features
        """
        dataset = self.dataset.df

        adf_values = {}
        for col in dataset.columns:
            adf, pvalue, usedlag, nobs, critical_values, icbest = adfuller(
                dataset[col].values
            )
            adf_values[col] = {
                "stat": adf,
                "pvalue": pvalue,
                "usedlag": usedlag,
                "nobs": nobs,
                "critical_values": critical_values,
                "icbest": icbest,
            }

        return self.cache_results(adf_values)


@dataclass
class KolmogorovSmirnov(Metric):
    """
    The Kolmogorov-Smirnov metric is a statistical test used to determine
    whether a given set of data follows a normal distribution.
    """

    type = "evaluation"  # assume this value
    scope = "test"  # assume this value (could be "train")
    key = "kolmogorov_smirnov"

    def run(self):
        """
        Calculates KS for each of the dataset features
        """
        x_train = self.train_ds.df
        x_train = self.train_ds.df

        ks_values = {}
        for col in x_train.columns:
            ks_stat, p_value = kstest_normal(x_train[col].values, "norm")
            ks_values[col] = {"stat": ks_stat, "pvalue": p_value}

        return self.cache_results(ks_values)


class ShapiroWilk(Metric):
    """
    The Shapiro-Wilk test is a statistical test used to determine
    whether a given set of data follows a normal distribution.
    """

    type = "evaluation"
    scope = "test"
    key = "shapiro_wilk"

    def run(self):
        """
        Calculates Shapiro-Wilk test for each of the dataset features.
        """
        x_train = self.train_ds.df
        x_train = self.train_ds.df

        sw_values = {}
        for col in x_train.columns:
            sw_stat, sw_pvalue = stats.shapiro(x_train[col].values)

            sw_values[col] = {
                "stat": sw_stat,
                "pvalue": sw_pvalue,
            }

        return self.cache_results(sw_values)


@dataclass
class Lilliefors(Metric):
    """
    The Lilliefors test is a statistical test used to determine
    whether a given set of data follows a normal distribution.
    """

    type = "evaluation"
    scope = "test"
    key = "lilliefors_test"

    def run(self):
        """
        Calculates Lilliefors test for each of the dataset features
        """
        x_train = self.train_ds.df
        x_train = self.train_ds.df

        lilliefors_values = {}
        for col in x_train.columns:
            l_stat, p_value = lilliefors(x_train[col].values)
            lilliefors_values[col] = {
                "stat": l_stat,
                "pvalue": p_value,
            }

        return self.cache_results(lilliefors_values)


class JarqueBera(Metric):
    """
    The Jarque-Bera test is a statistical test used to determine
    whether a given set of data follows a normal distribution.
    """

    type = "evaluation"  # assume this value
    scope = "test"  # assume this value (could be "train")
    key = "jarque_bera"

    def run(self):
        """
        Calculates JB for each of the dataset features
        """
        x_train = self.train_ds.df
        x_train = self.train_ds.df

        jb_values = {}
        for col in x_train.columns:
            jb_stat, jb_pvalue, jb_skew, jb_kurtosis = jarque_bera(x_train[col].values)

            jb_values[col] = {
                "stat": jb_stat,
                "pvalue": jb_pvalue,
                "skew": jb_skew,
                "kurtosis": jb_kurtosis,
            }

        return self.cache_results(jb_values)


class LJungBox(Metric):
    """
    The Ljung-Box test is a statistical test used to determine
    whether a given set of data has autocorrelations
    that are different from zero.
    """

    type = "evaluation"
    scope = "test"
    key = "ljung_box"

    def run(self):
        """
        Calculates Ljung-Box test for each of the dataset features
        """
        x_train = self.train_ds.df
        x_train = self.train_ds.df

        ljung_box_values = {}
        for col in x_train.columns:
            lb_results = acorr_ljungbox(x_train[col].values, return_df=True)

            ljung_box_values[col] = {
                "stat": lb_results["lb_stat"].values[0],
                "pvalue": lb_results["lb_pvalue"].values[0],
            }

        return self.cache_results(ljung_box_values)


class BoxPierce(Metric):
    """
    The Box-Pierce test is a statistical test used to determine
    whether a given set of data has autocorrelations
    that are different from zero.
    """

    type = "evaluation"
    scope = "test"
    key = "box_pierce"

    def run(self):
        """
        Calculates Box-Pierce test for each of the dataset features
        """
        x_train = self.train_ds.df
        x_train = self.train_ds.df

        box_pierce_values = {}
        for col in x_train.columns:
            bp_results = acorr_ljungbox(
                x_train[col].values, boxpierce=True, return_df=True
            )
            box_pierce_values[col] = {
                "stat": bp_results.iloc[0]["lb_stat"],
                "pvalue": bp_results.iloc[0]["lb_pvalue"],
            }

        return self.cache_results(box_pierce_values)


class RunsTest(Metric):
    """
    The runs test is a statistical test used to determine whether a given set
    of data has runs of positive and negative values that are longer than expected
    under the null hypothesis of randomness.
    """

    type = "evaluation"
    scope = "test"
    key = "runs_test"

    def run(self):
        """
        Calculates the run test for each of the dataset features
        """
        x_train = self.train_ds.df
        x_train = self.train_ds.df

        runs_test_values = {}
        for col in x_train.columns:
            runs_stat, runs_p_value = runstest_1samp(x_train[col].values)

            runs_test_values[col] = {
                "stat": runs_stat,
                "pvalue": runs_p_value,
            }

        return self.cache_results(runs_test_values)


@dataclass
class DurbinWatsonTest(Metric):
    """
    The Durbin-Watson Metric is a statistical test that
    can be used to detect autocorrelation in a time series.
    """

    type = "evaluation"  # assume this value
    scope = "test"  # assume this value (could be "train")
    key = "durbin_watson"

    def run(self):
        """
        Calculates DB for each of the dataset features
        """
        x_train = self.train_ds.df
        x_train = self.train_ds.df

        dw_values = {}
        for col in x_train.columns:
            dw_values[col] = durbin_watson(x_train[col].values)

        return self.cache_results(dw_values)


@dataclass
class PhillipsPerronArch(Metric):
    """
    Phillips-Perron (PP) unit root test for
    establishing the order of integration of time series
    """

    type = "evaluation"  # assume this value
    scope = "test"  # assume this value (could be "train")
    key = "phillips_perron"

    def run(self):
        """
        Calculates PP metric for each of the dataset features
        """
        dataset = self.dataset.df

        pp_values = {}
        for col in dataset.columns:
            pp = PhillipsPerron(dataset[col].values)
            pp_values[col] = {
                "stat": pp.stat,
                "pvalue": pp.pvalue,
                "usedlag": pp.lags,
                "nobs": pp.nobs,
            }

        return self.cache_results(pp_values)


@dataclass
class ZivotAndrewsArch(Metric):
    """
    Zivot-Andrews unit root test for
    establishing the order of integration of time series
    """

    type = "evaluation"  # assume this value
    scope = "test"  # assume this value (could be "train")
    key = "zivot_andrews"

    def run(self):
        """
        Calculates Zivot-Andrews metric for each of the dataset features
        """
        dataset = self.dataset.df

        za_values = {}
        for col in dataset.columns:
            za = ZivotAndrews(dataset[col].values)
            za_values[col] = {
                "stat": za.stat,
                "pvalue": za.pvalue,
                "usedlag": za.lags,
                "nobs": za.nobs,
            }

        return self.cache_results(za_values)


@dataclass
class DFGLSArch(Metric):
    """
    Dickey-Fuller GLS unit root test for
    establishing the order of integration of time series
    """

    type = "evaluation"  # assume this value
    scope = "test"  # assume this value (could be "train")
    key = "dickey_fuller_gls"

    def run(self):
        """
        Calculates Dickey-Fuller GLS metric for each of the dataset features
        """
        dataset = self.dataset.df

        dfgls_values = {}
        for col in dataset.columns:
            dfgls_out = DFGLS(dataset[col].values)
            dfgls_values[col] = {
                "stat": dfgls_out.stat,
                "pvalue": dfgls_out.pvalue,
                "usedlag": dfgls_out.lags,
                "nobs": dfgls_out.nobs,
            }

        return self.cache_results(dfgls_values)


@dataclass
class KPSS(Metric):
    """
    Kwiatkowski-Phillips-Schmidt-Shin (KPSS) unit root test for
    establishing the order of integration of time series
    """

    type = "evaluation"  # assume this value
    scope = "test"  # assume this value (could be "train")
    key = "kpss"

    def run(self):
        """
        Calculates KPSS for each of the dataset features
        """
        dataset = self.dataset.df

        kpss_values = {}
        for col in dataset.columns:
            kpss_stat, pvalue, usedlag, critical_values = kpss(dataset[col].values)
            kpss_values[col] = {
                "stat": kpss_stat,
                "pvalue": pvalue,
                "usedlag": usedlag,
                "critical_values": critical_values,
            }

        return self.cache_results(kpss_values)


@dataclass
class DeterminationOfIntegrationOrderADF(Metric):
    """
    This class calculates the order of integration for each feature
    in a dataset using the Augmented Dickey-Fuller (ADF) test.
    The order of integration is the number of times a series
    needs to be differenced to make it stationary.
    """

    type = "evaluation"  # assume this value
    scope = "test"  # assume this value (could be "train")
    key = "integration_order_adf"
    default_params = {"max_order": 3}

    def run(self):
        """
        Calculates the ADF order of integration for each of the dataset features.
        """
        x_train = self.train_ds.df

        adf_orders = {}
        for col in x_train.columns:
            order = 0
            orders_pvalues = []

            while order <= self.params["max_order"]:
                diff_series = x_train[col].diff(order).dropna()
                adf, pvalue, _, _, _, _ = adfuller(diff_series)
                orders_pvalues.append({"order": order, "pvalue": pvalue})
                if pvalue <= 0.05:
                    break
                order += 1

            adf_orders[col] = orders_pvalues

        return self.cache_results(adf_orders)


class AutoARIMA(Metric):
    """
    Automatically fits multiple ARIMA models for each variable and ranks them by BIC and AIC.
    """

    type = "evaluation"  # assume this value
    scope = "test"  # assume this value (could be "train")
    key = "auto_arima"

    max_p = 3
    max_d = 2
    max_q = 3

    def run(self):
        x_train = self.train_ds.df

        results = []

        for col in x_train.columns:
            series = x_train[col].dropna()

            # Check for stationarity using the Augmented Dickey-Fuller test
            adf_test = adfuller(series)
            if adf_test[1] > 0.05:
                print(f"Warning: {col} is not stationary. Results may be inaccurate.")

            arima_orders = []
            bic_values = []
            aic_values = []

            for p in range(self.max_p + 1):
                for d in range(self.max_d + 1):
                    for q in range(self.max_q + 1):
                        try:
                            model = ARIMA(series, order=(p, d, q))
                            model_fit = model.fit()

                            arima_orders.append((p, d, q))
                            bic_values.append(model_fit.bic)
                            aic_values.append(model_fit.aic)
                        except Exception as e:
                            print(
                                f"Error fitting ARIMA({p}, {d}, {q}) model for {col}: {e}"
                            )

            result = {
                "Variable": col,
                "ARIMA Orders": arima_orders,
                "BIC": bic_values,
                "AIC": aic_values,
            }
            results.append(result)

        return self.cache_results(results)


class ModelPredictionOLS(Metric):
    """
    Calculates and plots the model predictions for each of the models
    """

    type = "dataset"
    key = "model_prediction_ols"
    default_params = {"plot_start_date": None, "plot_end_date": None}

    def serialize_time_series_df(self, df):
        # Convert the DateTimeIndex to strings without specifying a date format
        df.index = df.index.astype(str)

        # Reset the index and rename the index column to 'Date'
        df = df.reset_index().rename(columns={"index": "Date"})

        # Convert the DataFrame into a list of dictionaries
        return df.to_dict("records")

    def get_model_prediction(self, model_list, df_test):
        # Extract the training target variable from the first model fit

        first_model_fit = model_list[0].model

        train_data = pd.Series(
            first_model_fit.model.endog, index=first_model_fit.model.data.row_labels
        )
        train_data = train_data.to_frame()
        target_var_name = first_model_fit.model.endog_names
        train_data.columns = [f"{target_var_name}_train"]

        # Initialize an empty DataFrame to store the predictions
        prediction_df = pd.DataFrame(index=df_test.index)
        prediction_df[f"{target_var_name}_test"] = np.nan

        # Concatenate the train_data and prediction_df
        combined_df = pd.concat([train_data, prediction_df], axis=0)

        # Loop through each model fit
        for i, model_fit in enumerate(model_list):
            model_name = f"model_{i+1}"

            # Prepare the test dataset
            exog_names = model_fit.model.model.exog_names
            X_test = df_test.copy()

            # Add the constant if it's missing
            if "const" in exog_names and "const" not in X_test.columns:
                X_test["const"] = 1.0

            # Select the necessary columns
            X_test = X_test[exog_names]

            # Generate the predictions
            predictions = model_fit.model.predict(X_test)

            # Add the predictions to the DataFrame
            combined_df[model_name] = np.nan
            combined_df[model_name].iloc[len(train_data) :] = predictions

        # Add the test data to the '<target_variable>_test' column
        combined_df[f"{target_var_name}_test"].iloc[len(train_data) :] = df_test[
            target_var_name
        ]

        return combined_df

    def plot_predictions(self, prediction_df, start_date=None, end_date=None):
        if start_date and end_date:
            prediction_df = prediction_df.loc[start_date:end_date]

        n_models = prediction_df.shape[1] - 2
        fig, axes = plt.subplots(n_models, 1, sharex=True)

        for i in range(n_models):
            axes[i].plot(
                prediction_df.index,
                prediction_df.iloc[:, 0],
                label=prediction_df.columns[0],
                color="grey",
            )
            axes[i].plot(
                prediction_df.index,
                prediction_df.iloc[:, 1],
                label=prediction_df.columns[1],
                color="lightgrey",
            )
            axes[i].plot(
                prediction_df.index,
                prediction_df.iloc[:, i + 2],
                label=prediction_df.columns[i + 2],
                linestyle="-",
            )
            axes[i].set_ylabel("Target Variable")
            axes[i].set_title(f"Test Data vs. {prediction_df.columns[i + 2]}")
            axes[i].legend()
            axes[i].grid(True)
        plt.xlabel("Date")
        plt.tight_layout()

    def run(self):
        model_list = self.models

        df_test = self.test_ds.df

        plot_start_date = self.params["plot_start_date"]
        plot_end_date = self.params["plot_end_date"]

        print(plot_start_date)

        prediction_df = self.get_model_prediction(model_list, df_test)
        results = self.serialize_time_series_df(prediction_df)

        figures = []
        self.plot_predictions(
            prediction_df, start_date=plot_start_date, end_date=plot_end_date
        )

        # Assuming the plot is the only figure we want to store
        fig = plt.gcf()
        figures.append(Figure(key=self.key, figure=fig, metadata={}))
        plt.close("all")

        # Assuming we do not need to cache any results, just the figure
        return self.cache_results(results, figures=figures)


@dataclass
class RegressionModelSummary(Metric):
    """
    Test that output the summary of regression models of statsmodel library.
    """

    category = "model_performance"
    scope = "test"
    name = "regression_model_summary"

    def run(self):
        # statsmodels library information
        module_name = self.model.model.__class__.__module__
        library_name = module_name.split(".")[0]
        model_name = self.model.model.__class__.__name__

        if library_name != "statsmodels" or model_name != "RegressionResultsWrapper":
            raise ValueError(
                "Only RegressionResultsWrapper models of statsmodels library supported"
            )

        lib_model = self.model.model
        # List of features columns
        X_columns = lib_model.model.exog_names

        # Extract R-squared and Adjusted R-squared
        r2 = lib_model.rsquared
        adj_r2 = lib_model.rsquared_adj

        # Calculate the Mean Squared Error (MSE) and Root Mean Squared Error (RMSE)
        mse = lib_model.mse_resid
        rmse = mse**0.5

        results = {
            "Independent Variables": X_columns,
            "R-Squared": r2,
            "Adjusted R-Squared": adj_r2,
            "MSE": mse,
            "RMSE": rmse,
        }
        return self.cache_results(results)


@dataclass
class RegressionModelInsampleComparison(Metric):
    """
    Test that output the comparison of stats library regression models.
    """

    category = "model_performance"
    scope = "test"
    name = "regression_insample_performance"

    def description(self):
        return """
        This section shows In-sample comparison of regression models involves comparing
        the performance of different regression models on the same dataset that was used
        to train the models. This is typically done by calculating a goodness-of-fit statistic
        such as the R-squared or mean squared error (MSE) for each model, and then comparing
        these statistics to determine which model has the best fit to the data.
        """

    def run(self):
        # Check models list is not empty
        if not self.models:
            raise ValueError("List of models must be provided in the models parameter")
        all_models = []
        for model in self.models:
            if model.model.__class__.__name__ != "RegressionResultsWrapper":
                raise ValueError("Only RegressionResultsWrapper models of statsmodels library supported")
            all_models.append(model.model)

        results = self._in_sample_performance_ols(all_models)
        return self.cache_results(results)

    def _in_sample_performance_ols(self, models):
        """
        Computes the in-sample performance evaluation metrics for a list of OLS models.

        Args:
        models (list): A list of statsmodels OLS models.

        Returns:
        list: A list of dictionaries containing the evaluation results for each model.
        Each dictionary contains the following keys:
        - 'Model': A string identifying the model.
        - 'Independent Variables': A list of strings identifying the independent variables used in the model.
        - 'R-Squared': The R-squared value of the model.
        - 'Adjusted R-Squared': The adjusted R-squared value of the model.
        - 'MSE': The mean squared error of the model.
        - 'RMSE': The root mean squared error of the model.
        """
        evaluation_results = []

        for i, model in enumerate(models):
            # print(model.model)
            X_columns = model.model.exog_names

            # Extract R-squared and Adjusted R-squared
            r2 = model.rsquared
            adj_r2 = model.rsquared_adj

            # Calculate the Mean Squared Error (MSE) and Root Mean Squared Error (RMSE)
            mse = model.mse_resid
            rmse = mse ** 0.5

            # Append the results to the evaluation_results list
            evaluation_results.append({
                'Model': f'Model_{i + 1}',
                'Independent Variables': X_columns,
                'R-Squared': r2,
                'Adjusted R-Squared': adj_r2,
                'MSE': mse,
                'RMSE': rmse
            })

        return evaluation_results
