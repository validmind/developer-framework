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
from typing import Dict, List, Optional, Union

import pandas as pd
from ipywidgets import HTML, GridBox, Layout, VBox

from ... import api_client
from ...ai import DescriptionFuture
from ...input_registry import input_registry
from ...logging import get_logger
from ...utils import NumpyEncoder, display, md_to_html, run_async, test_id_to_name
from ..dataset import VMDataset
from ..figure import Figure
from .metric_result import MetricResult
from .output_template import OutputTemplate
from .result_summary import ResultSummary
from .threshold_test_result import ThresholdTestResults

logger = get_logger(__name__)


async def update_metadata(content_id: str, text: str, _json: Union[Dict, List] = None):
    """
    Update the metadata of a content item. By default we don't
    override the existing metadata, but we can override it by
    setting the VM_OVERRIDE_METADATA environment variable to True
    """
    should_update = False

    # check if the env variable is set to force overwriting metadata
    if os.environ.get("VM_OVERRIDE_METADATA", "false").lower() == "true":
        should_update = True

    # if not set, check if the content_id is a composite metric def
    if not should_update and content_id.startswith("composite_metric_def:"):
        # we always want composite metric definitions to be updated
        should_update = True

    # if not set, lets check if the metadata already exists
    if not should_update:
        try:
            await api_client.get_metadata(content_id)
        except Exception:  # TODO: this shouldn't be a catch-all
            # if the metadata doesn't exist, we should create (update) it
            should_update = True

    if should_update:
        await api_client.log_metadata(content_id, text, _json)


def plot_figures(figures: List[Figure]) -> None:
    """
    Plot figures to a ipywidgets GridBox
    """

    plots = [figure.to_widget() for figure in figures]

    num_columns = 2 if len(figures) > 1 else 1
    return GridBox(
        plots,
        layout=Layout(grid_template_columns=f"repeat({num_columns}, 1fr)"),
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
        return md_to_html(description)

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
                            "props": [("width", "100%")],
                        },
                        {
                            "selector": "th",
                            "props": [("text-align", "left")],
                        },
                        {
                            "selector": "tbody tr:nth-child(even)",
                            "props": [("background-color", "#FFFFFF")],
                        },
                        {
                            "selector": "tbody tr:nth-child(odd)",
                            "props": [("background-color", "#F5F5F5")],
                        },
                        {
                            "selector": "td, th",
                            "props": [
                                ("padding-left", "5px"),
                                ("padding-right", "5px"),
                            ],
                        },
                    ]
                )
                .set_properties(**{"text-align": "left"})
                .to_html(escape=False)
            )  # table.data is an orient=records dump

            if table.metadata and table.metadata.title:
                tables.append(HTML(value=f"<h3>{table.metadata.title}</h3>"))
            tables.append(HTML(value=summary_table))
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
        run_async(self.log_async)


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
        return HTML(f"<h3 style='color: red;'>{self.message}</h3><p>{self.error}</p>")

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

        vbox_children = [
            HTML(value=f"<h1>{test_id_to_name(self.result_id)}</h1>"),
        ]

        if self.result_metadata:
            metric_description = self.result_metadata[0].get("text", "")
            if isinstance(metric_description, DescriptionFuture):
                metric_description = metric_description.get_description()
                self.result_metadata[0]["text"] = metric_description

            vbox_children.append(
                HTML(value=self._markdown_description_to_html(metric_description))
            )

        if self.metric:
            if self.output_template:
                rendered_output = OutputTemplate(self.output_template).render(
                    value=self.metric.value
                )
                vbox_children.append(HTML(rendered_output))
            elif self.metric.summary:
                tables = self._summary_tables_to_widget(self.metric.summary)
                vbox_children.extend(tables)

        if self.figures:
            vbox_children.append(HTML(value="<h3>Plots</h3>"))
            plot_widgets = plot_figures(self.figures)
            vbox_children.append(plot_widgets)

        vbox_children.append(
            HTML(
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

        return VBox(vbox_children)

    def _get_filtered_summary(self):
        """Check if the metric summary has columns from input datasets"""
        dataset_columns = set()

        for input_id in self.inputs:
            input_obj = input_registry.get(input_id)
            if isinstance(input_obj, VMDataset):
                dataset_columns.update(input_obj.columns)

        for table in [*self.metric.summary.results]:
            columns = set()

            if isinstance(table.data, pd.DataFrame):
                columns.update(table.data.columns)
            elif isinstance(table.data, list):
                columns.update(table.data[0].keys())
            else:
                raise ValueError("Invalid data type in summary table")

            if bool(columns.intersection(dataset_columns)):
                logger.warning(
                    "Sensitive data in metric summary table. Not logging to API automatically."
                    " Pass `unsafe=True` to result.log() method to override manually."
                )
                logger.warning(
                    f"The following columns are present in the table: {columns}"
                    f" and also present in the dataset: {dataset_columns}"
                )

                self.metric.summary.results.remove(table)

        return self.metric.summary

    async def log_async(self, unsafe=False):
        tasks = []  # collect tasks to run in parallel (async)

        if self.metric:
            if self.metric.summary and not unsafe:
                self.metric.summary = self._get_filtered_summary()

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
            description = self.result_metadata[0].get("text", "")
            if isinstance(description, DescriptionFuture):
                description = description.get_description()
                self.result_metadata[0]["text"] = description

            for metadata in self.result_metadata:
                tasks.append(
                    update_metadata(
                        content_id=metadata["content_id"],
                        text=metadata.get("text", ""),
                        _json=metadata.get("json"),
                    )
                )

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
            <h1>{test_title} {"✅" if self.test_results.passed else "❌"}</h1>
            """
        )

        if self.result_metadata:
            metric_description = self.result_metadata[0].get("text", "")
            if isinstance(metric_description, DescriptionFuture):
                metric_description = metric_description.get_description()
                self.result_metadata[0]["text"] = metric_description

            description_html.append(
                self._markdown_description_to_html(metric_description)
            )

        description_html.append(
            f"""
                <h4>Test Parameters</h4>
                <pre>{test_params}</pre>
            """
        )

        vbox_children.append(HTML(value="".join(description_html)))

        if self.test_results.summary:
            tables = self._summary_tables_to_widget(self.test_results.summary)
            vbox_children.extend(tables)

        if self.figures:
            vbox_children.append(HTML(value="<h3>Plots</h3>"))
            plot_widgets = plot_figures(self.figures)
            vbox_children.append(plot_widgets)

        return VBox(vbox_children)

    async def log_async(self):
        tasks = [api_client.log_test_result(self.test_results, self.inputs)]

        if self.figures:
            tasks.append(api_client.log_figures(self.figures))
        if hasattr(self, "result_metadata") and self.result_metadata:
            description = self.result_metadata[0].get("text", "")
            if isinstance(description, DescriptionFuture):
                description = description.get_description()
                self.result_metadata[0]["text"] = description

            for metadata in self.result_metadata:
                tasks.append(update_metadata(metadata["content_id"], metadata["text"]))

        await asyncio.gather(*tasks)
