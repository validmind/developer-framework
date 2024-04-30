# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import pandas as pd

from validmind.logging import get_logger
from validmind.models.foundation import Prompt
from validmind.vm_models.model import VMModel

logger = get_logger(__name__)


@dataclass
class RAGPrompt(Prompt):
    def __post_init__(self):
        if "context" not in self.variables:
            raise ValueError("Prompt must contain 'context' variable")

    template: str
    variables: list


DEFAULT_PROMPT_TEMPLATE = """
Please generate a response to the following query:
```
{x}
```

Using the information provided in the following context:
```
{context}
```
""".strip()

DEFAULT_PROMPT = RAGPrompt(
    template=DEFAULT_PROMPT_TEMPLATE,
    variables=["x", "context"],
)


class RAGModel(VMModel):
    """RAGModel class wraps a RAG Model and its components

    This class wraps a set of component models that make up a RAG model.

    The following required components must be supplied:
    - retriever: A retriever model that can be used to retrieve relevant documents
    - generator: A generator model that can be used to generate text based on a prompt
        and context from the retriever

    The following optional components may also be included:
    - embedder: An embedder model that can be used to embed text
    - prompt: A prompt object that defines the prompt template and the variables

    When the `predict` method is called, the model will first use the embedder (if provided)
    to embed the input text. It will then "pipe" the embedding into the retriever to
    retrieve a list of relevant context strings. Finally, it will use the generator to
    generate text based on the
    Attributes:
        embedder (VMModel): The embedder model
        retriever (VMModel): The retriever model
        generator (VMModel): The generator model
        prompt (RAGPrompt): The prompt object that defines the prompt template and the
            variables
        attributes (ModelAttributes, optional): The attributes of the model. Defaults to None.
        input_id (str, optional): The input ID of the model. Defaults to None.
        name (str, optional): The name of the model. Defaults to RAG Model
    """

    retriever: VMModel
    generator: VMModel
    embedder: VMModel = None

    def __post_init__(self):
        if not self.retriever:
            raise ValueError("Retriever model is a required argument for RAGModel")

        if not self.generator:
            raise ValueError("Generator model is a required argument for RAGModel")

        self.name = self.name or "RAG Model"

    def predict(self, X):
        Y = []

        for x in X:
            if self.embedder:
                x_embed = self.embedder.predict(x)
            else:
                x_embed = x

            x.append(self.retriever.predict([x_embed])[0])
            Y.append(self.generator.predict([x]))

        return Y
