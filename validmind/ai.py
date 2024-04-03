# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import os

from openai import AzureOpenAI, OpenAI

SYSTEM_PROMPT = """
You are an expert data scientist and MRM specialist tasked with providing concise and'
objective insights based on the results of quantitative model or dataset analysis.

Examine the provided statistical test results and compose a brief summary paragraph.
Highlight crucial insights, focusing on the distribution characteristics, central
tendencies (such as mean or median), and the variability (including standard deviation
and range) of the metrics. Evaluate how these statistics might influence the
development and performance of a predictive model. Identify and explain any discernible
trends or anomalies in the test results. Your summary should be concise, coherent, and
tailored for inclusion in machine learning model documentation, providing a clear
understanding of the test results implications for predictive analytics.

Your analysis will act as the description of the result in the model documentation.

Provide an unbiased and straightforward analysis of the data without any advisory
content. Focus solely on presenting the data analysis in a factual and objective
manner. Avoid any form of recommendations, suggestions, or advice. Keep the tone
purely analytical and neutral.

Ensure that the response does not exceed 150 words.
Avoid long sentences and complex vocabulary.
Structure the response clearly and logically.
Use Markdown syntax to format the response.
"""
USER_PROMPT = """
Test Name: {test_name}
Test Type: {test_type}
Test Description: {test_description}
Test Results (the raw results of the test):
{test_results}
Test Summary (what the user sees in the documentation):
{test_summary}
"""

__client = None
__model = None


def __get_client_and_model():
    """
    Get the model to use for generating interpretations
    """
    global __client, __model

    if __client and __model:
        return __client, __model

    if "OPENAI_API_KEY" in os.environ:
        __client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        __model = os.environ.get("VM_OPENAI_MODEL", "gpt-4-turbo-preview")

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


def generate_description(
    test_name: str,
    test_type: str,
    test_description: str,
    test_results: str,
    test_summary: str,
):
    """Generate the description for the test results"""
    client, model = __get_client_and_model()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": USER_PROMPT.format(
                    test_name=test_name,
                    test_type=test_type,
                    test_description=test_description,
                    test_results=test_results,
                    test_summary=test_summary,
                ),
            },
        ],
    )

    return response.choices[0].message.content
