from pydantic import BaseModel
from typing import List, Any, Dict


class DataTableProps(BaseModel):
    data: List[Dict[str, Any]]


class PlotlyComponentProps(BaseModel):
    data: List[Any]
    layout: Any


class MarkdownEditorProps(BaseModel):
    initialContent: str
