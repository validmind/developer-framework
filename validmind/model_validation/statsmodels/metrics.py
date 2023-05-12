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
        if self.model is not None:
            all_models.append(self.model)

        if self.models is not None:
            all_models.extend(self.models)

        for model in all_models:
            if model.model.__class__.__name__ != "RegressionResultsWrapper":
                raise ValueError(
                    "Only RegressionResultsWrapper models of statsmodels library supported"
                )

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
            X_columns = model.model.model.exog_names
            # Extract R-squared and Adjusted R-squared
            r2 = model.model.rsquared
            adj_r2 = model.model.rsquared_adj

            # Calculate the Mean Squared Error (MSE) and Root Mean Squared Error (RMSE)
            mse = model.model.mse_resid
            rmse = mse**0.5

            # Append the results to the evaluation_results list
            evaluation_results.append(
                {
                    "Model": f"Model_{i + 1}",
                    "Independent Variables": X_columns,
                    "R-Squared": r2,
                    "Adjusted R-Squared": adj_r2,
                    "MSE": mse,
                    "RMSE": rmse,
                }
            )

        return evaluation_results


@dataclass
class RegressionModelOutsampleComparison(Metric):
    """
    Test that evaluates the performance of different regression models on a separate test dataset
    that was not used to train the models.
    """

    category = "model_performance"
    scope = "test"
    name = "regression_outsample_performance"

    def description(self):
        return """
        This section shows Out-of-sample comparison of regression models involves evaluating
        the performance of different regression models on a separate test dataset that was not
        used to train the models. This is typically done by calculating a goodness-of-fit statistic
        such as the R-squared or mean squared error (MSE) for each model, and then comparing these
        statistics to determine which model has the best fit to the test data.
        """

    def run(self):
        # Check models list is not empty
        if not self.models:
            raise ValueError("List of models must be provided in the models parameter")
        all_models = []
        if self.model is not None:
            all_models.append(self.model)

        if self.models is not None:
            all_models.extend(self.models)

        for model in all_models:
            if model.model.__class__.__name__ != "RegressionResultsWrapper":
                raise ValueError(
                    "Only RegressionResultsWrapper models of statsmodels library supported"
                )
            if model.test_ds is None:
                raise ValueError(
                    "Test dataset is missing in the ValidMind Model object"
                )

        results = self._out_sample_performance_ols(
            all_models,
        )
        return self.cache_results(results.to_dict("records"))

    def _out_sample_performance_ols(self, model_list):
        """
        Returns the out-of-sample performance evaluation metrics of a list of OLS regression models.

        Args:
        model_list (list): A list of OLS models to evaluate.
        test_data (pandas.DataFrame): The test dataset containing the independent and dependent variables.
        target_col (str): The name of the target variable column in the test dataset.

        Returns:
        pandas.DataFrame: A DataFrame containing the evaluation results of the OLS models. The columns are 'Model',
        'MSE' (Mean Squared Error), and 'RMSE' (Root Mean Squared Error).
        """

        # Initialize a list to store results
        results = []

        for fitted_model in model_list:
            # Extract the column names of the independent variables from the model
            independent_vars = fitted_model.model.model.exog_names

            # Separate the target variable and features in the test dataset
            X_test = fitted_model.test_ds.x
            y_test = fitted_model.test_ds.y

            # Predict the test data
            y_pred = fitted_model.model.predict(X_test)

            # Calculate the residuals
            residuals = y_test - y_pred

            # Calculate the mean squared error and root mean squared error
            mse = np.mean(residuals**2)
            rmse_val = np.sqrt(mse)

            # Store the results
            model_name_with_vars = f"({', '.join(independent_vars)})"
            results.append([model_name_with_vars, mse, rmse_val])

        # Create a DataFrame to display the results
        results_df = pd.DataFrame(results, columns=["Model", "MSE", "RMSE"])

        return results_df


@dataclass
class RegressionModelForecastPlot(Metric):
    """
    This metric creates a plot of forecast vs observed for each model in the list.
    """

    category = "model_forecast"
    scope = "test"
    key = "regression_forecast_plot"
    default_params = {"start_date": None, "end_date": None}

    def description(self):
        return """
        This section shows plots of training and test datasets vs forecast trainining and forecast test.
        """

    def run(self):
        print(self.params)

        start_date = self.params["start_date"]
        end_date = self.params["end_date"]

        print(self.params)

        # Check models list is not empty
        if not self.models:
            raise ValueError("List of models must be provided in the models parameter")
        all_models = []
        for model in self.models:
            if model.model.__class__.__name__ != "RegressionResultsWrapper":
                raise ValueError(
                    "Only RegressionResultsWrapper models of statsmodels library supported"
                )
            all_models.append(model)

        figures = self._plot_forecast(all_models, start_date, end_date)

        return self.cache_results(figures=figures)

    def _plot_forecast(self, model_list, start_date=None, end_date=None):
        # Convert start_date and end_date to pandas Timestamp for comparison
        start_date = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date)

        # Initialize a list to store figures
        figures = []

        for fitted_model in model_list:
            train_ds = fitted_model.train_ds
            test_ds = fitted_model.test_ds

            # Check that start_date and end_date are within the data range
            all_dates = pd.concat([pd.Series(train_ds.index), pd.Series(test_ds.index)])
            print(all_dates)
            if start_date < all_dates.min() or end_date > all_dates.max():
                raise ValueError(
                    "start_date and end_date must be within the range of dates in the data"
                )

            fig, ax = plt.subplots()
            sns.lineplot(
                x=train_ds.index,
                y=train_ds.y,
                ax=ax,
                label="Train Forecast",
            )
            sns.lineplot(
                x=test_ds.index,
                y=test_ds.y,
                ax=ax,
                label="Test Forecast",
            )
            sns.lineplot(
                x=train_ds.index,
                y=fitted_model.y_train_predict.loc[train_ds.index],
                ax=ax,
                label="Train Dataset",
                color="grey",
            )
            sns.lineplot(
                x=test_ds.index,
                y=fitted_model.y_test_predict.loc[test_ds.index],
                ax=ax,
                label="Test Dataset",
                color="black",
            )
            plt.title(
                f"Forecast vs Observed for {fitted_model.model.__class__.__name__}"
            )

            # Set the x-axis limits to zoom in/out
            plt.xlim(start_date, end_date)

            plt.legend()
            figures.append(Figure(key=self.key, figure=fig, metadata={}))
            plt.close("all")

        return figures
