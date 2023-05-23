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
from sklearn.metrics import r2_score, mean_squared_error
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
from ...vm_models import (
    Figure,
    Metric,
    Model,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
)
from ...statsutils import adj_r2_score


@dataclass
class ResidualsVisualInspection(Metric):
    """
    Log plots for visual inspection of residuals
    """

    name = "residuals_visual_inspection"

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

            figures.append(
                Figure(
                    for_object=self,
                    key=self.key,
                    figure=fig,
                )
            )
        return self.cache_results(figures=figures)


class ADF(Metric):
    """
    Augmented Dickey-Fuller unit root test for establishing the order of integration of
    time series
    """

    name = "adf"

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

    name = "kolmogorov_smirnov"

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

    name = "shapiro_wilk"

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

    name = "lilliefors_test"

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

    name = "jarque_bera"

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

    name = "ljung_box"

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

    name = "box_pierce"

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

    name = "runs_test"

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

    name = "durbin_watson"

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

    name = "phillips_perron"

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

    name = "zivot_andrews"

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

    name = "dickey_fuller_gls"

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

    name = "kpss"

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


class AutoARIMA(Metric):
    """
    Automatically fits multiple ARIMA models for each variable and ranks them by BIC and AIC.
    """

    name = "auto_arima"

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

    name = "regression_model_summary"

    def run(self):
        if not Model.is_supported_model(self.model.model):
            raise ValueError(
                f"{Model.model_library(self.model.model)}.{Model.model_class(self.model.model)} \
                              is not supported by ValidMind framework yet"
            )

        X_columns = self.model.train_ds.get_features_columns()

        y_true = self.model.train_ds.y
        y_pred = self.model.model.predict(self.model.train_ds.x)

        r2 = r2_score(y_true, y_pred)
        adj_r2 = adj_r2_score(y_true, y_pred, len(y_true), len(X_columns))
        mse = mean_squared_error(y_true=y_true, y_pred=y_pred, squared=True)
        rmse = mean_squared_error(y_true=y_true, y_pred=y_pred, squared=False)

        results = {
            "Independent Variables": X_columns,
            "R-Squared": r2,
            "Adjusted R-Squared": adj_r2,
            "MSE": mse,
            "RMSE": rmse,
        }
        summary_regression = pd.DataFrame(results)

        return self.cache_results(
            {
                "regression_analysis": summary_regression.to_dict(orient="records"),
            }
        )

    def summary(self, metric_value):
        """
        Build one table for summarizing the regression analysis results
        """
        summary_regression = metric_value["regression_analysis"]

        return ResultSummary(
            results=[
                ResultTable(
                    data=summary_regression,
                    metadata=ResultTableMetadata(title="Regression Analysis Results"),
                ),
            ]
        )


@dataclass
class RegressionModelInsampleComparison(Metric):
    """
    Test that output the comparison of stats library regression models.
    """

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

        if self.models is not None:
            all_models.extend(self.models)

        for m in all_models:
            if not Model.is_supported_model(m.model):
                raise ValueError(
                    f"{Model.model_library(m.model)}.{Model.model_class(m.model)} \
                              is not supported by ValidMind framework yet"
                )
        results = self._in_sample_performance_ols(all_models)
        return self.cache_results(
            {
                "in_sample_performance": pd.DataFrame(results).to_dict(
                    orient="records"
                ),
            }
        )

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
            X_columns = model.train_ds.get_features_columns()
            y_true = self.model.train_ds.y
            y_pred = self.model.model.predict(self.model.train_ds.x)

            # Extract R-squared and Adjusted R-squared
            r2 = r2_score(y_true, y_pred)
            adj_r2 = adj_r2_score(y_true, y_pred, len(y_true), len(X_columns))
            mse = mean_squared_error(y_true=y_true, y_pred=y_pred, squared=True)
            rmse = mean_squared_error(y_true=y_true, y_pred=y_pred, squared=False)

            # Append the results to the evaluation_results list
            evaluation_results.append(
                {
                    "Model": f"Model {i + 1}",
                    "Independent Variables": X_columns,
                    "R-Squared": r2,
                    "Adjusted R-Squared": adj_r2,
                    "MSE": mse,
                    "RMSE": rmse,
                }
            )

        return evaluation_results

    def summary(self, metric_value):
        """
        Build one table for summarizing the in-sample performance results
        """
        summary_in_sample_performance = metric_value["in_sample_performance"]

        return ResultSummary(
            results=[
                ResultTable(
                    data=summary_in_sample_performance,
                    metadata=ResultTableMetadata(title="In-Sample Performance Results"),
                ),
            ]
        )


@dataclass
class RegressionModelOutsampleComparison(Metric):
    """
    Test that evaluates the performance of different regression models on a separate test dataset
    that was not used to train the models.
    """

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
            if not Model.is_supported_model(model.model):
                raise ValueError(
                    f"{Model.model_library(model.model)}.{Model.model_class(model.model)} \
                                is not supported by ValidMind framework yet"
                )
            if model.test_ds is None:
                raise ValueError(
                    "Test dataset is missing in the ValidMind Model object"
                )

        results = self._out_sample_performance_ols(
            all_models,
        )
        return self.cache_results(
            {
                "out_sample_performance": results.to_dict(orient="records"),
            }
        )

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
            independent_vars = fitted_model.train_ds.get_features_columns()

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
            results.append(
                {
                    "Model": model_name_with_vars,
                    "MSE": mse,
                    "RMSE": rmse_val,
                }
            )

        # Create a DataFrame to display the results
        results_df = pd.DataFrame(results)

        return results_df

    def summary(self, metric_value):
        """
        Build one table for summarizing the out-of-sample performance results
        """
        summary_out_sample_performance = metric_value["out_sample_performance"]

        return ResultSummary(
            results=[
                ResultTable(
                    data=summary_out_sample_performance,
                    metadata=ResultTableMetadata(
                        title="Out-of-Sample Performance Results"
                    ),
                ),
            ]
        )


@dataclass
class RegressionModelForecastPlot(Metric):
    """
    This metric creates a plot of forecast vs observed for each model in the list.
    """

    name = "regression_forecast_plot"
    default_params = {"start_date": None, "end_date": None}

    def description(self):
        return """
        This section shows plots of training and test datasets vs forecast trainining and forecast test.
        """

    def run(self):
        start_date = self.params["start_date"]
        end_date = self.params["end_date"]

        # Check models list is not empty
        if not self.models:
            raise ValueError("List of models must be provided in the models parameter")
        all_models = []
        for model in self.models:
            if not Model.is_supported_model(model.model):
                raise ValueError(
                    f"{Model.model_library(model.model)}.{Model.model_class(model.model)} \
                                 is not supported by ValidMind framework yet"
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

        for i, fitted_model in enumerate(model_list):
            feature_columns = fitted_model.train_ds.get_features_columns()

            train_ds = fitted_model.train_ds
            test_ds = fitted_model.test_ds

            y_pred = fitted_model.y_train_predict
            y_pred_test = fitted_model.y_test_predict

            # Check that start_date and end_date are within the data range
            all_dates = pd.concat([pd.Series(train_ds.index), pd.Series(test_ds.index)])

            # If start_date or end_date are None, set them to the min/max of all_dates
            if start_date is None:
                start_date = all_dates.min()
            else:
                start_date = pd.Timestamp(start_date)

            if end_date is None:
                end_date = all_dates.max()
            else:
                end_date = pd.Timestamp(end_date)

            # If start_date or end_date are None, set them to the min/max of all_dates
            if start_date is None:
                start_date = all_dates.min()
            else:
                start_date = pd.Timestamp(start_date)

            if end_date is None:
                end_date = all_dates.max()
            else:
                end_date = pd.Timestamp(end_date)

            if start_date < all_dates.min() or end_date > all_dates.max():
                raise ValueError(
                    "start_date and end_date must be within the range of dates in the data"
                )

            fig, ax = plt.subplots()
            ax.plot(train_ds.index, train_ds.y, label="Train Forecast")
            ax.plot(test_ds.index, test_ds.y, label="Test Forecast")
            ax.plot(train_ds.index, y_pred, label="Train Dataset", color="grey")
            ax.plot(test_ds.index, y_pred_test, label="Test Dataset", color="black")

            plt.title(f"Forecast vs Observed for features {feature_columns}")

            # Set the x-axis limits to zoom in/out
            plt.xlim(start_date, end_date)

            plt.legend()
            # TODO: define a proper key for each plot
            print(f"Plotting forecast vs observed for model {fitted_model.model}")

            plt.close("all")

            figures.append(
                Figure(
                    for_object=self,
                    key=f"{self.key}:{i}",
                    figure=fig,
                    metadata={"model": str(feature_columns)},
                )
            )

        return figures


@dataclass
class RegressionModelForecastPlotLevels(Metric):
    """
    This metric creates a plot of forecast vs observed for each model in the list.
    """

    name = "regression_forecast_plot_levels"
    default_params = {
        "transformation": None,
    }

    def description(self):
        return """
        This section shows plots of training and test datasets vs forecast training and test.
        """

    def run(self):
        transformation = self.params["transformation"]

        if not self.models:
            raise ValueError("List of models must be provided in the models parameter")

        all_models = []
        for model in self.models:
            if not Model.is_supported_model(model.model):
                raise ValueError(
                    f"{Model.model_library(model.model)}.{Model.model_class(model.model)} \
                                 is not supported by ValidMind framework yet"
                )
            all_models.append(model)

        figures = self._plot_forecast(all_models, transformation)

        return self.cache_results(figures=figures)

    def integrate_diff(self, series_diff, start_value):
        series_diff = np.array(series_diff)
        series_orig = np.cumsum(series_diff)
        series_orig += start_value
        return series_orig

    def _plot_forecast(
        self,
        model_list,
        transformation=None,
    ):
        figures = []

        for i, fitted_model in enumerate(model_list):
            feature_columns = fitted_model.train_ds.get_features_columns()
            train_ds = fitted_model.train_ds
            test_ds = fitted_model.test_ds

            y_pred = fitted_model.model.predict(fitted_model.train_ds.x)
            y_pred_test = fitted_model.model.predict(fitted_model.test_ds.x)

            all_dates = pd.concat([pd.Series(train_ds.index), pd.Series(test_ds.index)])

            if all_dates.empty:
                raise ValueError(
                    "No dates in the data. Unable to determine start and end dates."
                )

            fig, axs = plt.subplots(2, 2)

            # train vs forecast
            axs[0, 0].plot(
                train_ds.index, train_ds.y, label="Train Dataset", color="grey"
            )
            axs[0, 0].plot(train_ds.index, y_pred, label="Train Forecast")
            axs[0, 0].set_title(f"Forecast vs Observed for features {feature_columns}")
            axs[0, 0].legend()

            # test vs forecast
            axs[0, 1].plot(test_ds.index, test_ds.y, label="Test Dataset", color="grey")
            axs[0, 1].plot(test_ds.index, y_pred_test, label="Test Forecast")
            axs[0, 1].set_title(f"Forecast vs Observed for features {feature_columns}")
            axs[0, 1].legend()

            if transformation == "integrate":
                train_ds_y_transformed = self.integrate_diff(
                    train_ds.y.values, start_value=train_ds.y[0]
                )

                test_ds_y_transformed = self.integrate_diff(
                    test_ds.y.values, start_value=test_ds.y[0]
                )

                # Use the first value of the transformed train dataset as the start_value for predicted datasets

                y_pred_transformed = self.integrate_diff(
                    y_pred, start_value=train_ds_y_transformed[0]
                )
                y_pred_test_transformed = self.integrate_diff(
                    y_pred_test, start_value=test_ds_y_transformed[0]
                )

                # Create copies of the original datasets and update them to reflect transformed data
                train_ds_transformed = train_ds.copy
                train_ds_transformed["y"] = train_ds_y_transformed

                test_ds_transformed = test_ds.copy
                test_ds_transformed["y"] = test_ds_y_transformed

                # transformed train vs forecast
                axs[1, 0].plot(
                    train_ds.index,
                    train_ds_y_transformed,
                    label="Train Dataset",
                    color="grey",
                )

                axs[1, 0].plot(
                    train_ds.index, y_pred_transformed, label="Train Forecast"
                )

                axs[1, 0].set_title(
                    f"Integrated Forecast vs Observed for features {feature_columns}"
                )
                axs[1, 0].legend()

                # transformed test vs forecast
                axs[1, 1].plot(
                    test_ds.index,
                    test_ds_y_transformed,
                    label="Test Dataset",
                    color="grey",
                )

                axs[1, 1].plot(
                    test_ds.index, y_pred_test_transformed, label="Test Forecast"
                )
                axs[1, 1].set_title(
                    f"Integrated Forecast vs Observed for features {feature_columns}"
                )
                axs[1, 1].legend()

            figures.append(
                Figure(for_object=self, key=f"{self.key}:{i}", figure=fig, metadata={})
            )

            # Close the figure to prevent it from displaying
            plt.close(fig)

        return figures


@dataclass
class RegressionModelSensitivityPlot(Metric):
    """
    This metric performs sensitivity analysis applying shocks to one variable at a time.
    """

    name = "regression_sensitivity_plot"
    default_params = {
        "transformation": None,
        "shocks": [0.1],
    }

    def run(self):
        print(self.params)

        transformation = self.params["transformation"]
        shocks = self.params["shocks"]

        if not self.models:
            raise ValueError("List of models must be provided in the models parameter")

        all_models = []
        for model in self.models:
            if not Model.is_supported_model(model.model):
                raise ValueError(
                    f"{Model.model_library(model.model)}.{Model.model_class(model.model)} \
                                 is not supported by ValidMind framework yet"
                )
            all_models.append(model)

        figures = []
        for i, model in enumerate(all_models):
            features_df = model.test_ds.x
            target_df = model.test_ds.y  # series

            shocked_datasets = self.apply_shock(features_df, shocks)

            predictions = self.predict_shocked_datasets(shocked_datasets, model)

            if transformation == "integrate":
                transformed_predictions = []
                start_value = model.train_ds.y[0]
                transformed_target = self.integrate_diff(
                    model.test_ds.y.values, start_value
                )

                predictions = self.predict_shocked_datasets(shocked_datasets, model)
                transformed_predictions = self.transform_predictions(
                    predictions, start_value
                )

            else:
                transformed_target = target_df.values
                transformed_predictions = predictions

            fig = self._plot_predictions(
                target_df.index, transformed_target, transformed_predictions
            )
            figures.append(
                Figure(for_object=self, key=f"{self.key}:{i}", figure=fig, metadata={})
            )
            print(f"{self.key}:{i}")
        return self.cache_results(figures=figures)

    def transform_predictions(self, predictions, start_value):
        transformed_predictions = (
            {}
        )  # Initialize an empty dictionary to store the transformed predictions

        for (
            label,
            pred,
        ) in predictions.items():  # Here, label is the key, pred is the value
            transformed_pred = self.integrate_diff(pred, start_value)
            transformed_predictions[
                label
            ] = transformed_pred  # Store transformed dataframe in the new dictionary

        return transformed_predictions

    def predict_shocked_datasets(self, shocked_datasets, model):
        predictions = {}

        for label, shocked_dataset in shocked_datasets.items():
            y_pred = model.model.predict(shocked_dataset)
            predictions[label] = y_pred

        return predictions

    def _plot_predictions(self, index, target, predictions):
        fig = plt.figure()

        # Plot the target
        plt.plot(index, target, label="Observed")

        # Plot each prediction
        for label, pred in predictions.items():
            plt.plot(index, pred, label=label)

        plt.legend()

        # Close the figure to prevent it from displaying
        plt.close(fig)
        return fig

    def integrate_diff(self, series_diff, start_value):
        series_diff = np.asarray(series_diff, dtype=np.float64)  # Convert to float64
        series = np.cumsum(series_diff)
        series += start_value
        return series

    def apply_shock(self, df, shocks):
        shocked_dfs = {"Baseline": df.copy()}  # Start with the original dataset
        cols_to_shock = df.columns  # All columns

        # Apply shock one variable at a time
        for shock in shocks:
            for col in cols_to_shock:
                temp_df = df.copy()
                temp_df[col] = temp_df[col] * (1 + shock)
                shocked_dfs[
                    f"Shock of {shock} to {col}"
                ] = temp_df  # Include shock value in the key

        return shocked_dfs

    def description(self):
        return """
        The sensitivity analysis metric applies various shocks or adjustments to one variable at a time while keeping all other variables constant. This allows for the examination of how changes in a specific variable affect the overall outcome or response of the system being analyzed.
        """


@dataclass
class RegressionModelsCoeffs(Metric):
    """
    Test that outputs the coefficients of stats library regression models.
    """

    name = "regression_models_coefficients"

    def description(self):
        return """
        This section shows the coefficients of different regression models that were
        trained on the same dataset. This can be useful for comparing how different
        models weigh the importance of various features in the dataset.
        """

    def extract_coef_stats(self, summary, model_name):
        table = summary.tables[1].data
        headers = table.pop(0)
        headers[0] = "Feature"
        df = pd.DataFrame(table, columns=headers)
        df["Model"] = model_name
        return df

    def extract_coefficients_summary(self, summaries):
        coef_stats_df = pd.DataFrame()

        for i, summary in enumerate(summaries):
            model_name = f"Model {i+1}"
            coef_stats_df = pd.concat(
                [coef_stats_df, self.extract_coef_stats(summary, model_name)]
            )

        # Reorder columns to have 'Model' as the first column and reset the index
        coef_stats_df = coef_stats_df.reset_index(drop=True)[
            ["Model"] + [col for col in coef_stats_df.columns if col != "Model"]
        ]

        return coef_stats_df

    def run(self):
        # Check models list is not empty
        if not self.models:
            raise ValueError("List of models must be provided in the models parameter")

        all_models = []

        if self.models is not None:
            all_models.extend(self.models)

        for m in all_models:
            if not Model.is_supported_model(m.model):
                raise ValueError(
                    f"{Model.model_library(m.model)}.{Model.model_class(m.model)} \
                              is not supported by ValidMind framework yet"
                )

        summaries = [m.model.summary() for m in all_models]
        coef_stats_df = self.extract_coefficients_summary(summaries)

        return self.cache_results(
            {
                "coefficients_summary": coef_stats_df.to_dict(orient="records"),
            }
        )

    def summary(self, metric_value):
        """
        Build one table for summarizing the regression models' coefficients
        """
        summary_coefficients = metric_value["coefficients_summary"]

        return ResultSummary(
            results=[
                ResultTable(
                    data=summary_coefficients,
                    metadata=ResultTableMetadata(
                        title="Regression Models' Coefficients"
                    ),
                ),
            ]
        )


@dataclass
class RegressionModelsPerformance(Metric):
    """
    Test that outputs the comparison of stats library regression models.
    """

    name = "regression_models_performance"

    def description(self):
        return """
        This section shows the in-sample and out-of-sample comparison of regression models. In-sample comparison involves comparing the performance of different regression models on the same dataset that was used to train the models. Out-of-sample comparison evaluates the performance of the models on unseen data. This is typically done by calculating goodness-of-fit statistics such as R-squared and mean squared error (MSE) for each model, and then comparing these statistics to determine which model has the best fit to the data.
        """

    def run(self):
        # Check models list is not empty
        if not self.models:
            raise ValueError("List of models must be provided in the models parameter")

        all_models = []

        if self.models is not None:
            all_models.extend(self.models)

        for m in all_models:
            if not Model.is_supported_model(m.model):
                raise ValueError(
                    f"{Model.model_library(m.model)}.{Model.model_class(m.model)} \
                              is not supported by ValidMind framework yet"
                )

        in_sample_results = self._in_sample_performance_ols(all_models)
        out_of_sample_results = self._out_sample_performance_ols(all_models)

        return self.cache_results(
            {
                "in_sample_performance": in_sample_results,
                "out_of_sample_performance": out_of_sample_results,
            }
        )

    def _in_sample_performance_ols(self, models):
        evaluation_results = []

        for i, model in enumerate(models):
            X_columns = model.train_ds.get_features_columns()
            y_true = model.train_ds.y
            y_pred = model.model.predict(model.train_ds.x)

            # Extract R-squared and Adjusted R-squared
            r2 = r2_score(y_true, y_pred)
            mse = mean_squared_error(y_true, y_pred)
            adj_r2 = 1 - ((1 - r2) * (len(y_true) - 1)) / (
                len(y_true) - len(X_columns) - 1
            )

            # Append the results to the evaluation_results list
            evaluation_results.append(
                {
                    "Model": f"Model {i + 1}",
                    "Independent Variables": X_columns,
                    "R-Squared": r2,
                    "Adjusted R-Squared": adj_r2,
                    "MSE": mse,
                }
            )

        return evaluation_results

    def _out_sample_performance_ols(self, models):
        evaluation_results = []

        for i, model in enumerate(models):
            X_columns = model.train_ds.get_features_columns()
            y_true = model.test_ds.y
            y_pred = model.model.predict(model.test_ds.x)

            # Extract R-squared and Adjusted R-squared
            r2 = r2_score(y_true, y_pred)
            mse = mean_squared_error(y_true, y_pred)
            adj_r2 = 1 - ((1 - r2) * (len(y_true) - 1)) / (
                len(y_true) - len(X_columns) - 1
            )

            # Append the results to the evaluation_results list
            evaluation_results.append(
                {
                    "Model": f"Model {i + 1}",
                    "Independent Variables": X_columns,
                    "R-Squared": r2,
                    "Adjusted R-Squared": adj_r2,
                    "MSE": mse,
                }
            )

        return evaluation_results

    def summary(self, metric_value):
        """
        Build a table for summarizing the in-sample and out-of-sample performance results
        """
        summary_in_sample_performance = metric_value["in_sample_performance"]
        summary_out_of_sample_performance = metric_value["out_of_sample_performance"]

        return ResultSummary(
            results=[
                ResultTable(
                    data=summary_in_sample_performance,
                    metadata=ResultTableMetadata(title="In-Sample Performance Results"),
                ),
                ResultTable(
                    data=summary_out_of_sample_performance,
                    metadata=ResultTableMetadata(
                        title="Out-of-Sample Performance Results"
                    ),
                ),
            ]
        )
