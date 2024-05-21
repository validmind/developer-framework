# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import concurrent.futures
import os

from openai import AzureOpenAI, OpenAI

SYSTEM_PROMPT = """
You are an expert data scientist and MRM specialist.
You are tasked with analyzing the results of a quantitative test run on some model or dataset.
Your goal is to create a test description that will act as part of the model documentation.
You will provide both the developer and other consumers of the documentation with a clear and concise "interpretation" of the results they will see.
The overarching theme to maintain is MRM documentation.

Examine the provided statistical test results and compose a description of the results.
This will act as the description and interpretation of the result in the model documentation.
It will be displayed alongside the test results table and figures.

Avoid long sentences and complex vocabulary.
Structure the response clearly and logically.
Use valid Markdown syntax to format the response.
Respond only with your analysis and insights, not the verbatim test results.
Respond only with the markdown content, no explanation or context for your response is necessary.
Use the Test ID that is provided to form the Test Name e.g. "ClassImbalance" -> "Class Imbalance".

Explain the test, its purpose, its mechanism/formula etc and why it is useful.
If relevant, provide a very brief description of the way this test is used in model/dataset evaluation and how it is interpreted.
Highlight the key insights from the test results. The key insights should be concise and easily understood.
End the response with any closing remarks, summary or additional useful information.

Use the following format for the response (feel free to modify slightly if necessary):
```
**<Test Name>** calculates the xyz <continue to explain what it does in detail>...

This test is useful for <explain why and for what this test is useful>...

**Key Insights:**

The following key insights can be identified in the test results:

- **<key insight 1 - title>**: <concise explanation of key insight 1>
- ...<continue with any other key insights using the same format>
```
It is very important that the text is nicely formatted and contains enough information to be useful to the user as documentation.
""".strip()


USER_PROMPT = """
Test ID: `{test_name}`

<Test Docstring>
{test_description}
</Test Docstring>

<Test Results Summary>
{test_summary}
</Test Results Summary>
""".strip()


USER_PROMPT_FIGURES = """
Test ID: `{test_name}`

<Test Docstring>
{test_description}
</Test Docstring>

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
    test_summary: str,
    figures: list = None,
):
    """Generate the description for the test results"""
    if not test_summary and not figures:
        raise ValueError("No summary or figures provided - cannot generate description")

    client, _ = __get_client_and_model()
    # get last part of test id
    test_name = test_name.split(".")[-1]

    if test_summary:
        return (
            client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": USER_PROMPT.format(
                            test_name=test_name,
                            test_description=test_description,
                            test_summary=test_summary,
                        ),
                    },
                ],
            )
            .choices[0]
            .message.content.strip("```")
            .strip()
        )

    return (
        client.chat.completions.create(
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
        .choices[0]
        .message.content.strip("```")
        .strip()
    )


def generate_description(
    test_name: str,
    test_description: str,
    test_summary: str,
    figures: list = None,
):
    future = __executor.submit(
        generate_description_async,
        test_name,
        test_description,
        test_summary,
        figures,
    )

    return DescriptionFuture(future)
