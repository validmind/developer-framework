"""
Class for storing ValidMind metric objects and associated
data for display and reporting purposes
"""


class MetricResult:
    def __init__(self, api_metric, api_figures=None, plots=None, metadata=None):
        self.api_metric = api_metric
        self.api_figures = api_figures
        self.plots = plots
        self.metadata = metadata
