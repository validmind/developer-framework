# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

"""
Result Wrappers for test and metric results
"""
import asyncio
import json
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

import ipywidgets as widgets
import markdown
import pandas as pd
from IPython.display import display

from ... import api_client
from ...utils import NumpyEncoder, run_async, test_id_to_name
from ..figure import Figure
from .metric_result import MetricResult
from .output_template import OutputTemplate
from .result_summary import ResultSummary
from .threshold_test_result import ThresholdTestResults


async def update_metadata(content_id: str, text: str) -> None:
    """
    Update the metadata of a content item. By default we don't
    override the existing metadata, but we can override it by
    setting the VM_OVERRIDE_METADATA environment variable to True
    """
    VM_OVERRIDE_METADATA = os.environ.get("VM_OVERRIDE_METADATA", False)
    try:
        existing_metadata = await api_client.get_metadata(content_id)
    except Exception:
        existing_metadata = None  # TODO: handle this better

    if (
        existing_metadata is None
        or VM_OVERRIDE_METADATA == "True"
        or VM_OVERRIDE_METADATA is True
    ):
        await api_client.log_metadata(content_id, text)


def plot_figures(figures: List[Figure]) -> None:
    """
    Plot figures to a ipywidgets GridBox
    """

    plots = [figure.to_widget() for figure in figures]

    num_columns = 2 if len(figures) > 1 else 1
    return widgets.GridBox(
        plots,
        layout=widgets.Layout(grid_template_columns=f"repeat({num_columns}, 1fr)"),
    )


@dataclass
class ResultWrapper(ABC):
    """Base Class for test suite results"""

    name: str = "ResultWrapper"
    # id of the result, can be set by the subclass. This helps
    # looking up results later on
    result_id: str = None
    # Text metadata about the result, can include description, etc.
    result_metadata: List[dict] = None
    # Output template to use for rendering the result
    output_template: Optional[str] = None

    def __str__(self) -> str:
        """May be overridden by subclasses"""
        return self.__class__.__name__

    @abstractmethod
    def to_widget(self):
        """Create an ipywdiget representation of the result... Must be overridden by subclasses"""
        raise NotImplementedError

    def render(self, output_template=None):
        """Helper method thats lets the user try out output templates"""
        if output_template:
            self.output_template = output_template

        return self.to_widget()

    def _markdown_description_to_html(self, description: str):
        """
        Convert a markdown string to html
        """

        return markdown.markdown(description, extensions=["markdown.extensions.tables"])

    def _summary_tables_to_widget(self, summary: ResultSummary):
        """
        Create an ipywdiget representation of the summary tables
        """
        tables = []
        for table in summary.results:
            # Explore advanced styling
            summary_table = (
                pd.DataFrame(table.data)
                .style.format(precision=4)
                .hide(axis="index")
                .set_table_styles(
                    [
                        {
                            "selector": "",
                            "props": [
                                ("width", "100%"),
                            ],
                        },
                        {
                            "selector": "tbody tr:nth-child(even)",
                            "props": [
                                ("background-color", "#FFFFFF"),
                            ],
                        },
                        {
                            "selector": "tbody tr:nth-child(odd)",
                            "props": [
                                ("background-color", "#F5F5F5"),
                            ],
                        },
                        {
                            "selector": "td, th",
                            "props": [
                                ("padding-left", "5px"),
                                ("padding-right", "5px"),
                            ],
                        },
                    ]
                )  # add borders
                .to_html(escape=False)
            )  # table.data is an orient=records dump

            if table.metadata and table.metadata.title:
                tables.append(widgets.HTML(value=f"<h3>{table.metadata.title}</h3>"))
            tables.append(widgets.HTML(value=summary_table))
        return tables

    def show(self):
        """Display the result... May be overridden by subclasses"""
        display(self.to_widget())

    @abstractmethod
    async def log_async(self):
        """Log the result... Must be overridden by subclasses"""
        raise NotImplementedError

    def log(self):
        """Log the result... May be overridden by subclasses"""
        return run_async(self.log_async)


@dataclass
class FailedResultWrapper(ResultWrapper):
    """
    Result wrapper for test suites that fail to load or run properly
    """

    name: str = "Failed"
    error: Exception = None
    message: str = None

    def __repr__(self) -> str:
        return f'FailedResult(result_id="{self.result_id}")'

    def to_widget(self):
        return widgets.HTML(
            value=f"<h3 style='color: red;'>{self.message}</h3><p>{self.error}</p>"
        )

    async def log_async(self):
        pass


@dataclass
class MetricResultWrapper(ResultWrapper):
    """
    Result wrapper for metrics that run as part of a test suite
    """

    name: str = "Metric"
    figures: Optional[List[Figure]] = None
    metric: Optional[MetricResult] = None
    inputs: List[str] = None

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

    def to_widget(self):
        if self.metric and self.metric.key == "dataset_description":
            return ""

        vbox_children = []

        if self.result_metadata:
            metric_description = self.result_metadata[0]
            vbox_children.append(
                widgets.HTML(
                    value=self._markdown_description_to_html(
                        metric_description.get("text", "")
                    )
                )
            )

        if self.metric:
            if self.output_template:
                rendered_output = OutputTemplate(self.output_template).render(
                    value=self.metric.value
                )
                vbox_children.append(widgets.HTML(rendered_output))
            elif self.metric.summary:
                tables = self._summary_tables_to_widget(self.metric.summary)
                vbox_children.extend(tables)

        if self.figures:
            vbox_children.append(widgets.HTML(value="<h3>Plots</h3>"))
            plot_widgets = plot_figures(self.figures)
            vbox_children.append(plot_widgets)

        vbox_children.append(
            widgets.HTML(
                value="""
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
        </style>
        """
            )
        )

        return widgets.VBox(vbox_children)

    async def log_async(self):
        tasks = []  # collect tasks to run in parallel (async)

        if self.metric:
            tasks.append(
                api_client.log_metrics(
                    metrics=[self.metric],
                    inputs=self.inputs,
                    output_template=self.output_template,
                )
            )
        if self.figures:
            tasks.append(api_client.log_figures(self.figures))
        if hasattr(self, "result_metadata") and self.result_metadata:
            for metadata in self.result_metadata:
                tasks.append(update_metadata(metadata["content_id"], metadata["text"]))

        await asyncio.gather(*tasks)


@dataclass
class ThresholdTestResultWrapper(ResultWrapper):
    """
    Result wrapper for test results produced by the tests that run as part of a test suite
    """

    name: str = "Threshold Test"
    figures: Optional[List[Figure]] = None
    test_results: ThresholdTestResults = None
    inputs: List[str] = None

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

    def to_widget(self):
        vbox_children = []
        description_html = []

        test_params = json.dumps(self.test_results.params, cls=NumpyEncoder, indent=2)

        test_title = test_id_to_name(self.test_results.test_name)
        description_html.append(
            f"""
            <h2>{test_title} {"✅" if self.test_results.passed else "❌"}</h2>
            """
        )

        if self.result_metadata:
            metric_description = self.result_metadata[0]
            description_html.append(
                self._markdown_description_to_html(metric_description.get("text", ""))
            )

        description_html.append(
            f"""
                <h4>Test Parameters</h4>
                <pre>{test_params}</pre>
            """
        )

        vbox_children.append(widgets.HTML(value="".join(description_html)))

        if self.test_results.summary:
            tables = self._summary_tables_to_widget(self.test_results.summary)
            vbox_children.extend(tables)

        if self.figures:
            vbox_children.append(widgets.HTML(value="<h3>Plots</h3>"))
            plot_widgets = plot_figures(self.figures)
            vbox_children.append(plot_widgets)

        return widgets.VBox(vbox_children)

    async def log_async(self):
        tasks = [api_client.log_test_result(self.test_results, self.inputs)]

        if self.figures:
            tasks.append(api_client.log_figures(self.figures))
        if hasattr(self, "result_metadata") and self.result_metadata:
            for metadata in self.result_metadata:
                tasks.append(update_metadata(metadata["content_id"], metadata["text"]))

        await asyncio.gather(*tasks)
