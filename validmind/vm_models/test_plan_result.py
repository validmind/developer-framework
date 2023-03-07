"""
TestPlanResult
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional
import json

from IPython.display import display, display_javascript, HTML
from json2html import json2html

from ..api_client import (
    log_dataset,
    log_figure,
    log_metrics,
    log_model,
    log_test_result,
)
from .dataset import Dataset
from .figure import Figure
from .metric_result import MetricResult
from .test_result import TestResults


@dataclass
class TestPlanResult(ABC):
    """Base Class for test plan results"""

    def __str__(self) -> str:
        """May be overridden by subclasses"""
        return self.__class__.__name__

    @abstractmethod
    def display(self):
        """Display the result... Must be overridden by subclasses"""
        raise NotImplementedError

    @abstractmethod
    def log(self):
        """Log the result... Must be overridden by subclasses"""
        raise NotImplementedError


@dataclass
class TestPlanDatasetResult(TestPlanResult):
    """
    Result wrapper for datasets that run as part of a test plan
    """

    dataset: Dataset = None

    def display(self):
        display(
            HTML(f"<h4>Logged the following dataset to the ValidMind platform:</h4>")
        )
        display(self.dataset.raw_dataset.describe())

    def log(self):
        log_dataset(self.dataset)


@dataclass
class TestPlanMetricResult(TestPlanResult):
    """
    Result wrapper for metrics that run as part of a test plan
    """

    figures: Optional[List[Figure]] = None
    metric: Optional[MetricResult] = None

    def display(self):
        if self.metric:
            display(
                HTML(
                    f"<h4>Logged the following {self.metric.type} metrics to the ValidMind platform:</h4>"
                )
            )
            # convert metric to html and display
            # display(HTML(json2html.convert(json=self.metric.value)))
            # print(dir(self.metric))
            # display(HTML(f'<div id="myjson" style="height: 100%; width:100%;"></div>'))
            # display_javascript(
            #     """
            # require(["https://rawgit.com/caldwell/renderjson/master/renderjson.js"], function() {
            # document.getElementById('myjson').appendChild(renderjson(%s))
            # });
            # """
            #     % (self.metric.value),
            #     raw=True,
            # )
            # print(self.metric.serialize())
            data = self.metric.serialize()
            data["value"] = "value"  # convert value to string so it can be displayed
            display(HTML(json2html.convert(json=data)))
        if self.figures:
            print(f"Logged the following figures to the ValidMind platform:")
            for fig in self.figures:
                display(fig.figure)

    def log(self):
        if self.metric:
            # TODO: need to somehow log the metrics all together i think
            log_metrics([self.metric])
        if self.figures:
            for fig in self.figures:
                log_figure(fig.figure, fig.key, fig.metadata)


@dataclass
class TestPlanModelResult(TestPlanResult):
    """
    Result wrapper for models that run as part of a test plan
    """

    model: object = None

    def display(self):
        display(self.model)

    def log(self):
        log_model(self.model)


@dataclass
class TestPlanTestResult(TestPlanResult):
    """
    Result wrapper for test results produced by the tests that run as part of a test plan
    """

    test_results: TestResults = None

    def display(self):
        # right now the output looks like this:
        # TestResults(category='data_quality', test_name='class_imbalance', params={'min_percent_threshold': 0.2}, passed=True, results=[TestResult(test_name=None, column='Exited', passed=True, values={0: 0.798, 1: 0.202})])
        # make this look clean and nice
        display(
            HTML(
                "<h4>Logged the following test results to the ValidMind platform:</h4>"
            )
        )
        # display(HTML(json2html.convert(json=self.test_results.__dict__)))
        # create an expandable html element that shows the test result with a green checkmark if it passed and a red x if it failed
        # add a button to expand the test result
        html = """
        <div class="test-result">
            <div class="test-result-header">
                <div class="test-result-header-title">
                    <span class="test-result-header-title-text">%s</span>
                    <span class="test-result-header-title-icon">%s</span>
                </div>
                <div class="test-result-header-button">
                    <button id="expand-results-%s">See Results</button>
                </div>
            </div>
            <div class="test-result-body">
                <div class="test-result-body-column">
                    <div class="test-result-body-column-title">Test Name</div>
                    <div class="test-result-body-column-value">%s</div>
                </div>
                <div class="test-result-body-column">
                    <div class="test-result-body-column-title">Category</div>
                    <div class="test-result-body-column-value">%s</div>
                </div>
                <div class="test-result-body-column">
                    <div class="test-result-body-column-title">Passed</div>
                    <div class="test-result-body-column-value">%s</div>
                </div>
                <div class="test-result-body-column">
                    <div class="test-result-body-column-title">Params</div>
                    <div class="test-result-body-column-value">%s</div>
                </div>
            </div>
            <div class="test-result-results">
                <div class="test-result-results-title">Results</div>
                <div class="test-result-results-body">%s</div>
            </div>
        </div>
        <style>
            .test-result {
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-bottom: 10px;
            }
            .test-result-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px;
            }
            .test-result-header-title {
                display: flex;
                align-items: center;
            }
            .test-result-header-title-text {
                font-weight: bold;
            }
            .test-result-header-title-icon {
                margin-left: 10px;
            }
            .test-result-header-button {
                cursor: pointer;
            }
            .test-result-header-button button {
                background: none;
                border: none;
                font-size: 16px;
                font-weight: bold;
                color: #000;
            }
            .test-result-body {
                display: flex;
                padding: 10px;
            }
            .test-result-body-column {
                flex: 1;
            }
            .test-result-body-column-title {
                font-weight: bold;
            }
            .test-result-body-column-value {
                margin-top: 5px;
            }
            .test-result-results {
                display: none;
                padding: 10px;
            }
            .test-result-results-title {
                font-weight: bold;
            }
            .test-result-results-body {
                margin-top: 5px;
            }
        </style>
        <script>
            document.getElementById('expand-results-%s').addEventListener('click', function() {
                var testResult = this.closest('.test-result');
                var testResultBody = testResult.querySelector('.test-result-body');
                var testResultResults = testResult.querySelector('.test-result-results');
                if (testResultResults.style.display === 'none') {
                    testResultResults.style.display = 'block';
                    testResultBody.style.display = 'none';
                    this.innerHTML = 'Hide Results';
                } else {
                    testResultResults.style.display = 'none';
                    testResultBody.style.display = 'flex';
                    this.innerHTML = 'See Results';
                }
            });
        </script>
        """ % (
            " ".join(self.test_results.test_name.split("_")).title(),
            "✅" if self.test_results.passed else "❌",
            self.test_results.test_name,
            self.test_results.test_name,
            self.test_results.category,
            self.test_results.passed,
            self.test_results.params,
            json2html.convert(json=self.test_results.results),
            self.test_results.test_name,
        )
        display(HTML(html))

    def log(self):
        log_test_result(self.test_results)
