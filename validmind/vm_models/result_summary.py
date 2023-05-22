from dataclasses import dataclass
from typing import Any, List, Union

import pandas as pd


@dataclass
class ResultTableMetadata:
    """
    A dataclass that holds the metadata of a table summary
    """

    title: str


@dataclass
class ResultTable:
    """
    A dataclass that holds the table summary of result
    """

    data: Union[List[Any], pd.DataFrame]
    type: str = "table"
    metadata: ResultTableMetadata = None

    def serialize(self):
        """
        Serializes the Figure to a dictionary so it can be sent to the API
        """
        table_result = {
            "type": self.type,
        }

        # Convert to a DataFrame so that we can round the values in a standard way
        table_df = pd.DataFrame(self.data) if isinstance(self.data, list) else self.data
        table_result["data"] = table_df.round(4).to_dict(orient="records")

        if self.metadata is not None:
            table_result["metadata"] = vars(self.metadata)

        return table_result


@dataclass()
class ResultSummary:
    """
    A dataclass that holds the summary of a metric or threshold test results
    """

    results: List[ResultTable]  # TBD other types of results

    def add_result(self, result: ResultTable):
        """
        Adds a result to the list of results
        """
        if self.results is None:
            self.results = []
        self.results.append(result)

    def serialize(self):
        """
        Serializes the ResultSummary to a list of results
        """
        return [result.serialize() for result in self.results]
