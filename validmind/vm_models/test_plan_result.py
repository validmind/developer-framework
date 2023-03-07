"""
TestPlanResult
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from io import BytesIO
from typing import List, Optional
import base64

from IPython.display import display, HTML
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
from .model import Model
from .test_result import TestResults


@dataclass
class TestPlanResult(ABC):
    """Base Class for test plan results"""

    def __str__(self) -> str:
        """May be overridden by subclasses"""
        return self.__class__.__name__

    @abstractmethod
    def _to_html(self):
        """Create an html representation of the result... Must be overridden by subclasses"""
        raise NotImplementedError

    def show(self):
        """Display the result... May be overridden by subclasses"""
        display(HTML(self._to_html()))

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

    def _to_html(self):
        html = "<h4>Logged the following dataset to the ValidMind platform:</h4>"
        return html + self.dataset.raw_dataset.describe().to_html()

    def log(self):
        log_dataset(self.dataset)


@dataclass
class TestPlanMetricResult(TestPlanResult):
    """
    Result wrapper for metrics that run as part of a test plan
    """

    figures: Optional[List[Figure]] = None
    metric: Optional[MetricResult] = None

    def _to_html(self):
        html = ""

        if self.metric:
            html += f"""
            <h4>Logged the following {self.metric.type} metric to the ValidMind platform:</h4>
            """
        else:
            html += f"""
            <h4>Logged the following figure{"s" if len(self.figures) > 1 else ""} 
            to the ValidMind platform:</h4>
            """

        if self.metric:
            html += f"""
            <div class="metric-result">
                <div class="metric-result-body">
                    <div class="metric-body-column">
                        <div class="metric-body-column-title">Metric Name</div>
                        <div class="metric-body-column-value">
                            {" ".join(self.metric.key.split("_")).title()}
                        </div>
                    </div>
                    <div class="metric-body-column">
                        <div class="metric-body-column-title">Metric Type</div>
                        <div class="metric-body-column-value">{self.metric.type}</div>
                    </div>
                    <div class="metric-body-column">
                        <div class="metric-body-column-title">Metric Scope</div>
                        <div class="metric-body-column-value">{self.metric.scope}</div>
                    </div>
                </div>
                <div class="metric-value">
                    <div class="metric-value-title">Metric Value</div>
                    <div class="metric-value-value">
            """

        if self.figures:
            for fig in self.figures:
                tmpfile = BytesIO()
                fig.figure.savefig(tmpfile, format="png")
                encoded = base64.b64encode(tmpfile.getvalue()).decode("utf-8")
                html += f'<img src="data:image/png;base64,{encoded}"/>'
        else:
            html += f"<pre>{self.metric.value}</pre>"

        html += """
        </div></div>
        <style>
            .metric-result {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 10px;
                margin: 10px 0;
            }
            .metric-result-body {
                display: flex;
                flex-direction: row;
                justify-content: space-between;
            }
            .metric-body-column {
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                width: 33%;
            }
            .metric-body-column-title {
                font-size: 14px;
                font-weight: 500;
            }
            .metric-value {
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                margin-top: 15px;
            }
            .metric-value-title {
                font-size: 14px;
                font-weight: 500;
            }
            .metric-value-value {
                font-size: 14px;
                font-weight: 500;
                margin-top: 10px;
            }
        </style>
        """

        return html

    def log(self):
        if self.metric:
            log_metrics([self.metric])
        if self.figures:
            for fig in self.figures:
                log_figure(fig.figure, fig.key, fig.metadata)


@dataclass
class TestPlanModelResult(TestPlanResult):
    """
    Result wrapper for models that run as part of a test plan
    """

    model: Model = None

    def _to_html(self):
        html = "<h4>Logged the following model to the ValidMind platform:</h4>"
        html += f"""
        <div class="model-result">
            <div class="model-result-header">
                <div class="model-result-header-title">
                    <span class="model-result-header-title-text">
                        {self.model.model.__class__.__name__} ({self.model.model_id})
                    </span>
                    <span class="model-result-header-title-icon">📦</span>
                </div>
            </div>
            <div class="model-result-body">
                <div class="model-body-column">
                    <div class="model-body-column-title">Framework</div>
                    <div class="model-body-column-value">
                        {self.model.attributes.framework} (v{self.model.attributes.framework_version})
                    </div>
                </div>
                <div class="model-body-column">
                    <div class="model-body-column-title">Architecture</div>
                    <div class="model-body-column-value">{self.model.attributes.architecture}</div>
                </div>
                <div class="model-body-column">
                    <div class="model-body-column-title">Task</div>
                    <div class="model-body-column-value">{self.model.task}</div>
                </div>
                <div class="model-body-column">
                    <div class="model-body-column-title">Subtask</div>
                    <div class="model-body-column-value">{self.model.subtask}</div>
                </div>
            </div>
        </div>
        <style>
            .model-result {{
                border: 1px solid #ccc;
                border-radius: 5px;
                margin: 10px 0;
            }}
            .model-result-header {{
                padding: 10px;
                background-color: #eee;
                border-radius: 5px 5px 0 0;
            }}
            .model-result-header-title {{
                display: flex;
                align-items: center;
            }}
            .model-result-header-title-text {{
                font-weight: bold;
                font-size: 1.2em;
            }}
            .model-result-header-title-icon {{
                margin-left: 10px;
            }}
            .model-result-body {{
                padding: 10px;
                display: flex;
                flex-wrap: wrap;
            }}
            .model-body-column {{
                flex: 1 1 50%;
                padding: 5px;
            }}
            .model-body-column-title {{
                font-weight: bold;
            }}
        </style>
        """
        return html

    def log(self):
        log_model(self.model)


@dataclass
class TestPlanTestResult(TestPlanResult):
    """
    Result wrapper for test results produced by the tests that run as part of a test plan
    """

    test_results: TestResults = None

    def _to_html(self):
        html = "<h4>Logged the following test results to the ValidMind platform:</h4>"
        # TODO: probably want to move this into an html template file
        html += f"""
        <div class="test-result">
            <div class="test-result-header">
                <div class="test-result-header-title">
                    <span class="test-result-header-title-text">
                        {" ".join(self.test_results.test_name.split("_")).title()}
                    </span>
                    <span class="test-result-header-title-icon">
                        {"✅" if self.test_results.passed else "❌"}
                    </span>
                </div>
                <div class="test-result-header-button">
                    <a id="expand-results-{self.test_results.test_name}">See Results</a>
                    <span>(double click)</span>
                </div>
            </div>
            <div class="test-result-body">
                <div class="test-result-body-column">
                    <div class="test-result-body-column-title">Test Name</div>
                    <div class="test-result-body-column-value">{self.test_results.test_name}</div>
                </div>
                <div class="test-result-body-column">
                    <div class="test-result-body-column-title">Category</div>
                    <div class="test-result-body-column-value">{self.test_results.category}</div>
                </div>
                <div class="test-result-body-column">
                    <div class="test-result-body-column-title">Passed</div>
                    <div class="test-result-body-column-value">{self.test_results.passed}</div>
                </div>
                <div class="test-result-body-column">
                    <div class="test-result-body-column-title">Params</div>
                    <div class="test-result-body-column-value">{self.test_results.params}</div>
                </div>
            </div>
            <div class="test-result-results">
                <div class="test-result-results-title">Results</div>
                <div class="test-result-results-body">{json2html.convert(json=self.test_results.results)}</div>
            </div>
        </div>
        <style>
            .test-result {{
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-bottom: 10px;
            }}
            .test-result-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px;
            }}
            .test-result-header-title {{
                display: flex;
                align-items: center;
            }}
            .test-result-header-title-text {{
                font-weight: bold;
            }}
            .test-result-header-title-icon {{
                margin-left: 10px;
            }}
            .test-result-header-button {{
                cursor: pointer;
            }}
            .test-result-header-button button {{
                background: none;
                border: none;
                font-size: 16px;
                font-weight: bold;
                color: #000;
            }}
            .test-result-body {{
                display: flex;
                padding: 10px;
            }}
            .test-result-body-column {{
                flex: 1;
            }}
            .test-result-body-column-title {{
                font-weight: bold;
            }}
            .test-result-body-column-value {{
                margin-top: 5px;
            }}
            .test-result-results {{
                display: none;
                padding: 10px;
            }}
            .test-result-results-title {{
                font-weight: bold;
            }}
            .test-result-results-body {{
                margin-top: 5px;
            }}
        </style>
        <script>
            document.getElementById('expand-results-{self.test_results.test_name}').addEventListener('click', function() {{
                var testResult = this.closest('.test-result');
                var testResultBody = testResult.querySelector('.test-result-body');
                var testResultResults = testResult.querySelector('.test-result-results');
                if (testResultResults.style.display === 'none') {{
                    testResultResults.style.display = 'block';
                    testResultBody.style.display = 'none';
                    this.innerHTML = 'Hide Results';
                }} else {{
                    testResultResults.style.display = 'none';
                    testResultBody.style.display = 'flex';
                    this.innerHTML = 'See Results';
                }}
            }});
        </script>
        """

        return html

    def log(self):
        log_test_result(self.test_results)
