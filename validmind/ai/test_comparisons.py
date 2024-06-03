# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from typing import List

from jinja2 import Template

from ..logging import get_logger
from ..vm_models.test.result_wrapper import MetricResultWrapper
from .utils import get_client_and_model

logger = get_logger(__name__)

SYSTEM_PROMPT = """
You are an expert data scientist and MRM specialist.
You are tasked with analyzing the results of a quantitative test that is run across multiple models or datasets.
Your goal is to compare the different results and generate a new test "result" that summarizes the differences between the models or datasets.
The idea is to provide a clear and concise comparison of the results to know which model or dataset is better.

You will be provided with the test name and the test docstring which will give you an idea of what the test is and what it does.
You will then be provided with the results as a series of messages where each message contains the tables and/or plots produced by the test.
Each result will be identified by a result ID and the name of the model or dataset it corresponds to.

Create a beautiful Markdown comparison of the results (extended Markdown syntax w/ tables, latex math etc).

Your goal is to provide a rich and comprehensive comparison that highlights the differences, helps the user understand which is better and why.
You should start with a brief summary of the test, what it does and why it is important in the context of choosing the best model or dataset.
You should then provide an in-depth comparison of the results, highlighting the key differences and pros/cons of each result.
Finally, you should provide a conclusion that summarizes the comparison, highlights the best choice (if any) and justifies that choice quantitatively and qualitatively.
Your comparison should be objective and based on the data provided in the results.
Your conclusion, however, while based on the data, can be subjective and based on your expert opinion.

Do not include any plots or images in the comparison.

Your response should be in JSON using the following:

<ResponseFormat>
{
    "comparison": "[Markdown Comparison]",
}
</ResponseFormat>
""".strip()


TEST_OVERVIEW_PROMPT = """
Test ID: `{{ test_name }}`

<Test Docstring>
{{ test_description }}
</Test Docstring>
"""

TEST_RESULT_PROMPT = """
Result ID: `{{ result_id }}`
Result Inputs: {{ result_inputs }}

{% if result_tables %}
{% for table in result_tables %}
{{ table }}
{% endfor %}
{% endif %}

{% if num_plots %}
This test produced {{ num_plots }} plots. They are attached to this message.
{% endif %}
"""


def _render_prompt(template, **kwargs):
    return Template(template).render(**kwargs).strip()


def _build_test_result_message(result: MetricResultWrapper):
    tables = result.metric.summary.results if result.metric.summary else []
    content = [
        {
            "type": "text",
            "text": _render_prompt(
                TEST_RESULT_PROMPT,
                result_id=result.result_id,
                result_inputs=",".join(f"`{_input}`" for _input in result.inputs),
                result_tables=[table.serialize() for table in tables],
            ),
        },
    ]

    if result.figures:
        content.extend(
            [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": figure._get_b64_url(),
                    },
                }
                for figure in result.figures
            ]
        )

    return {"role": "user", "content": content}


def generate_comparison(
    test_id: str, test_description: str, test_results: List[MetricResultWrapper]
):
    """Generate an AI comparison of the test results"""
    client, model = get_client_and_model()

    # get last part of test id
    test_name = test_id.split(".")[-1]
    # truncate the test description to save time
    test_description = (
        f"{test_description[:500]}..."
        if len(test_description) > 500
        else test_description
    )

    system_message = {"role": "system", "content": SYSTEM_PROMPT}
    test_overview_message = {
        "role": "user",
        "content": _render_prompt(
            TEST_OVERVIEW_PROMPT, test_name=test_name, test_description=test_description
        ),
    }
    test_result_messages = [
        _build_test_result_message(result) for result in test_results
    ]

    response = client.chat.completions.create(
        model=model,
        messages=[system_message, test_overview_message] + test_result_messages,
        response_format={"type": "json_object"},
        temperature=0.8,
    )

    return response.choices[0].message.content.strip()
