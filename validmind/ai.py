# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import concurrent.futures
import os

from openai import AzureOpenAI, OpenAI

SYSTEM_PROMPT = """
You are an expert data scientist and MRM specialist tasked with providing concise and'
objective insights based on the results of quantitative model or dataset analysis.

Examine the provided statistical test results and compose a brief summary. Highlight crucial
insights, focusing on the distribution characteristics, central tendencies (such as mean or median),
and the variability (including standard deviation and range) of the metrics. Evaluate how
these statistics might influence the development and performance of a predictive model. Identify
and explain any discernible trends or anomalies in the test results.

Your analysis will act as the description of the result in the model documentation.

Avoid long sentences and complex vocabulary.
Structure the response clearly and logically.
Use valid Markdown syntax to format the response (tables are supported).
Use the Test ID that is provided to form the Test Name e.g. "ClassImbalance" -> "Class Imbalance".
Use the following format for the response (feel free to modify slightly if necessary):
```
**<Test Name>** <continue to explain what it does in detail>...

The results of this test <detailed explanation of the results>...

In summary the following key insights can be gained:

- **<key insight 1 - title>**: <explanation of key insight 1>
- ...<continue with any other key insights using the same format>
```
It is very important that the text is nicely formatted and contains enough information to be useful to the user as documentation.
""".strip()
USER_PROMPT = """
Test ID: {test_name}
Test Description: {test_description}
Test Results (the raw results of the test):
{test_results}
Test Summary (what the user sees in the documentation):
{test_summary}
""".strip()
USER_PROMPT_FIGURES = """
Test ID: {test_name}
Test Description: {test_description}
The attached plots show the results of the test.
""".strip()

__client = None
__model = None

__executor = concurrent.futures.ThreadPoolExecutor()


def __get_client_and_model():
    """
    Get the model to use for generating interpretations
    """
    global __client, __model

    if __client and __model:
        return __client, __model

    if "OPENAI_API_KEY" in os.environ:
        __client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        __model = os.environ.get("VM_OPENAI_MODEL", "gpt-4o")

    elif "AZURE_OPENAI_KEY" in os.environ:
        if "AZURE_OPENAI_ENDPOINT" not in os.environ:
            raise ValueError(
                "AZURE_OPENAI_ENDPOINT must be set to run LLM tests with Azure"
            )

        if "AZURE_OPENAI_MODEL" not in os.environ:
            raise ValueError(
                "AZURE_OPENAI_MODEL must be set to run LLM tests with Azure"
            )

        __client = AzureOpenAI(
            azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
            api_key=os.environ.get("AZURE_OPENAI_KEY"),
            api_version=os.environ.get("AZURE_OPENAI_VERSION", "2023-05-15"),
        )
        __model = os.environ.get("AZURE_OPENAI_MODEL")

    else:
        raise ValueError("OPENAI_API_KEY or AZURE_OPENAI_KEY must be set")

    return __client, __model


class DescriptionFuture:
    """This will be immediately returned from generate_description so that
    the tests can continue to be run in parallel while the description is
    retrieved asynchronously.

    The value will be retrieved later and if its not ready yet, it should
    block until it is.
    """

    def __init__(self, future):
        self._future = future

    def get_description(self):
        # This will block until the future is completed
        return self._future.result()


def generate_description_async(
    test_name: str,
    test_description: str,
    test_results: str,
    test_summary: str,
    figures: list = None,
):
    """Generate the description for the test results"""
    client, _ = __get_client_and_model()

    # get last part of test id
    test_name = test_name.split(".")[-1]

    if not test_results and not test_summary:
        if not figures:
            raise ValueError("No results, summary or figures provided")

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": USER_PROMPT_FIGURES.format(
                                test_name=test_name,
                                test_description=test_description,
                            ),
                        },
                        *[
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": figure._get_b64_url(),
                                },
                            }
                            for figure in figures
                        ],
                    ],
                },
            ],
        )
    else:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": USER_PROMPT.format(
                        test_name=test_name,
                        test_description=test_description,
                        test_results=test_results,
                        test_summary=test_summary,
                    ),
                },
            ],
        )

    return response.choices[0].message.content.strip("```").strip()


def generate_description(
    test_name: str,
    test_description: str,
    test_results: str,
    test_summary: str,
    figures: list = None,
):
    future = __executor.submit(
        generate_description_async,
        test_name,
        test_description,
        test_results,
        test_summary,
        figures,
    )

    return DescriptionFuture(future)
