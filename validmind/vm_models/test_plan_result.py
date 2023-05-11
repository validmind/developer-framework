"""
TestPlanResult
"""
# TODO: we are probably going to want to move all this html generation into an html template file
# and use something like jinja to render it. This is fine for now, but the html is a bit messy
import os

from abc import ABC, abstractmethod
from dataclasses import dataclass
from io import BytesIO, StringIO
from typing import List, Optional
import base64

from IPython.display import display, HTML

from ..api_client import (
    get_metadata,
    log_dataset,
    log_figure,
    log_metadata,
    log_metrics,
    log_model,
    log_test_result,
)
from .dataset import Dataset
from .figure import Figure
from .metric_result import MetricResult
from .model import Model
from .test_result import TestResults


def update_metadata(content_id: str, text: str) -> None:
    """
    Update the metadata of a content item. By default we don't
    override the existing metadata, but we can override it by
    setting the VM_OVERRIDE_METADATA environment variable to True
    """
    VM_OVERRIDE_METADATA = os.environ.get("VM_OVERRIDE_METADATA", False)
    existing_metadata = get_metadata(content_id)

    if (
        existing_metadata is None
        or VM_OVERRIDE_METADATA == "True"
        or VM_OVERRIDE_METADATA is True
    ):
        log_metadata(content_id, text)


def plot_figures(html: StringIO, figures: List[Figure]) -> None:
    """
    Plot figures to html
    """

    plot_htmls = []

    for fig in figures:
        tmpfile = BytesIO()
        fig.figure.savefig(tmpfile, format="png")
        encoded = base64.b64encode(tmpfile.getvalue()).decode("utf-8")
        plot_htmls.append(
            f"""
        <div class="metric-plot">
            <img src="data:image/png;base64,{encoded}"/>
        </div>
        """
        )

    if len(plot_htmls) > 2:
        # if theres a lot of plots, we want to only show the first
        # one and then have an expand button to show the rest
        html.write(
            f"""
        <div class="metric-value">
            <div class="metric-value-title">
                Metric Plots
            </div>
            <div class="metric-value-value">
                <a onclick="showMetricPlots(this)" style="cursor: pointer; color: blue;">
                Show All Plots
                </a>
            </div>
            <div class="metric-value-value">
                {plot_htmls[0]}
                <div class="allplots" style="display: none;">
                    {"".join(plot_htmls[1:])}
                </div>
            </div>
        </div>
        <script>
            function showMetricPlots(btn) {{
                const plots = btn.parentElement.parentElement.querySelector(".allplots");
                if (plots.style.display === "none") {{
                    plots.style.display = "block";
                    btn.innerHTML = "Collapse";
                }} else {{
                    plots.style.display = "none";
                    btn.innerHTML = "Show All Plots";
                }}
            }}
        </script>
        """
        )
    else:
        html.write(
            f"""
        <div class="metric-value">
            <div class="metric-value-title">Metric Plots</div>
            <div class="metric-value-value">
                {"".join(plot_htmls)}
            </div>
        </div>
        """
        )


@dataclass
class TestPlanResult(ABC):
    """Base Class for test plan results"""

    # id of the result, can be set by the subclass. This helps
    # looking up results later on
    result_id: str = None
    # Text metadata about the result, can include description, etc.
    result_metadata: List[dict] = None

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

    def __repr__(self) -> str:
        return f'TestPlanDatasetResult(result_id="{self.result_id}")'

    def _to_html(self):
        html = "<h4>Logged the following dataset to the ValidMind platform:</h4>"
        return html + self.dataset.df.describe().to_html()

    def log(self):
        log_dataset(self.dataset)


@dataclass
class TestPlanMetricResult(TestPlanResult):
    """
    Result wrapper for metrics that run as part of a test plan
    """

    figures: Optional[List[Figure]] = None
    metric: Optional[MetricResult] = None

    def __repr__(self) -> str:
        if self.metric:
            return f'{self.__class__.__name__}(result_id="{self.result_id}", metric, figures)'
        else:
            return f'{self.__class__.__name__}(result_id="{self.result_id}", figures)'

    def __str__(self) -> str:
        if self.metric:
            return f'{self.__class__.__name__}(result_id="{self.result_id}", metric, figures)'
        else:
            return f"{self.__class__.__name__}(result_id={self.result_id}, figures)"

    def _to_html(self):
        if self.metric and self.metric.key == "dataset_description":
            return ""

        html = StringIO()

        if self.metric:
            html.write(
                f"""
            <h4>Logged the following {self.metric.type} metric to the ValidMind platform:</h4>
            """
            )
        else:
            html.write(
                f"""
            <h4>Logged the following plot{"s" if len(self.figures) > 1 else ""}
            to the ValidMind platform:</h4>
            """
            )

        if self.metric:
            metric_value = self.metric.value
            # Don't log the entire metric if it has more than 1000 characters
            if len(metric_value.__str__()) > 1024:
                metric_value = metric_value.__str__()[:1024] + "..."

            html.write(
                f"""
            <div class="metric-result">
                <div class="metric-result-body">
                    <div class="metric-body-column">
                        <div class="metric-body-column-title">Metric Name</div>
                        <div class="metric-body-column-value">{self.metric.key}</div>
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
                        <pre>{metric_value}</pre>
                    </div>
                </div>
            """
            )

        if self.figures:
            plot_figures(html, self.figures)

        html.write(
            """
        </div>
        <style>
            .metric-result {
                background-color: #F5F5F5;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 10px;
                margin: 10px 0;
            }
            .metric-result-body {
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                gap: 10px;
            }
            .metric-body-column {
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                width: 33%;
            }
            .metric-body-column-title {
                font-size: 16px;
                font-weight: 600;
            }
            .metric-value {
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                margin-top: 15px;
            }
            .metric-value-title {
                font-size: 16px;
                font-weight: 600;
            }
            .metric-value-value {
                font-size: 14px;
                font-weight: 500;
                margin-top: 10px;
            }
            .metric-plot img {
                margin-left: auto !important;
                margin-right: auto !important;
                max-height: 500px !important;
                height: 100%;
                width: auto;
                max-width: 800px;
            }
        </style>
        """
        )

        return html.getvalue()

    def log(self):
        if self.metric:
            log_metrics([self.metric])
        if self.figures:
            for fig in self.figures:
                log_figure(fig.figure, fig.key, fig.metadata)
        if hasattr(self, "result_metadata") and self.result_metadata:
            for metadata in self.result_metadata:
                update_metadata(metadata["content_id"], metadata["text"])


@dataclass
class TestPlanModelResult(TestPlanResult):
    """
    Result wrapper for models that run as part of a test plan
    """

    model: Model = None

    def _to_html(self):
        return f"""
        <h4>Logged the following model to the ValidMind platform:</h4>
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
                        {self.model.attributes.framework}
                        <span>(v{self.model.attributes.framework_version})</span>
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

    def log(self):
        log_model(self.model)


@dataclass
class TestPlanTestResult(TestPlanResult):
    """
    Result wrapper for test results produced by the tests that run as part of a test plan
    """

    figures: Optional[List[Figure]] = None
    test_results: TestResults = None

    def __repr__(self) -> str:
        if self.test_results:
            return (
                f'{self.__class__.__name__}(result_id="{self.result_id}", test_results)'
            )
        else:
            return f'{self.__class__.__name__}(result_id="{self.result_id}", figures)'

    def __str__(self) -> str:
        if self.test_results:
            return (
                f'{self.__class__.__name__}(result_id="{self.result_id}", test_results)'
            )
        else:
            return f'{self.__class__.__name__}(result_id="{self.result_id}", figures)'

    def _to_html(self):
        html = StringIO()
        html.write(
            f"""
        <h4>Logged the following test result to the ValidMind platform:</h4>
        <div class="metric-result">
            <div class="metric-result-body">
                <div class="test-result-header-title">
                    <span class="test-result-header-title-text">
                        {" ".join(self.test_results.test_name.split("_")).title()}
                    </span>
                    <span class="test-result-header-title-icon">
                        {"✅" if self.test_results.passed else "❌"}
                    </span>
                </div>
            </div>
            <div class="metric-result-body">
                <div class="metric-body-column">
                    <div class="metric-body-column-title">Test Name</div>
                    <div class="metric-body-column-value">{self.test_results.test_name}</div>
                </div>
                <div class="metric-body-column">
                    <div class="metric-body-column-title">Category</div>
                    <div class="metric-body-column-value">{self.test_results.category}</div>
                </div>
                <div class="metric-body-column">
                    <div class="metric-body-column-title">Passed</div>
                    <div class="metric-body-column-value">{self.test_results.passed}</div>
                </div>
                <div class="metric-body-column">
                    <div class="metric-body-column-title">Params</div>
                    <div class="metric-body-column-value">{self.test_results.params}</div>
                </div>
            </div>
            <div class="results-objs" style="display: none;">
                <div class="results-objs-title">Results</div>
                <div class="results-objs-body">{self.test_results.results}</div>
            </div>
            <div class="metric-result-body">
                <a onclick="toggleTestResults(this)" style="margin-top: 10px; cursor: pointer; color: blue;">
                    See Result Details
                </a>
            </div>
            <div class="metric-result-body">
        """
        )

        if self.figures:
            plot_figures(html, self.figures)

        html.write(
            """
            </div>
        </div>
        <style>
            .metric-result {
                background-color: #F5F5F5;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 10px;
                margin: 10px 0;
            }
            .metric-result-body {
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                gap: 10px;
            }
            .metric-body-column {
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                width: 33%;
            }
            .metric-body-column-title {
                font-size: 16px;
                font-weight: 600;
            }
            .metric-value {
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                margin-top: 15px;
            }
            .metric-value-title {
                font-size: 16px;
                font-weight: 600;
            }
            .metric-value-value {
                font-size: 14px;
                font-weight: 500;
                margin-top: 10px;
            }
            .metric-plot img {
                margin-left: auto !important;
                margin-right: auto !important;
                max-height: 500px !important;
                height: 100%;
                width: auto;
                max-width: 800px;
            }
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
                text-decoration: underline;
                font-size: 18px;
                font-weight: 600;
            }
            .test-result-header-title-icon {
                margin-left: 10px;
            }
            .results-objs {
                padding: 10px;
            }
            .results-objs-title {
                font-weight: bold;
            }
            .results-objs-body {
                margin-top: 5px;
            }
        </style>
        <script>
            function toggleTestResults(btn) {{
                const rslts = btn.parentElement.parentElement.querySelector('.results-objs');
                if (rslts.style.display === 'none') {{
                    rslts.style.display = 'block';
                    btn.innerHTML = 'Hide Result Details';
                }} else {{
                    rslts.style.display = 'none';
                    btn.innerHTML = 'See Result Details';
                }}
            }}
        </script>
        """
        )

        return html.getvalue()

    def log(self):
        log_test_result(self.test_results)
        if self.figures:
            for fig in self.figures:
                log_figure(fig.figure, fig.key, fig.metadata)
        if hasattr(self, "result_metadata") and self.result_metadata:
            for metadata in self.result_metadata:
                update_metadata(metadata["content_id"], metadata["text"])
