from typing import Dict, List

from httpmon.data import available_metrics


class LogAggregator:
    def __init__(self, included_metrics: List[str]):
        """Keep track of all the metrics data and aggregates them together.

        Params:
            - included_metrics: list. Example: ['section', 'ip_address', 'summary']
        """
        self.included_metrics = included_metrics
        self.metrics = self._initialize_metrics()

    def _initialize_metrics(self):
        return [
            metric_value['class']() for metric_key, metric_value in available_metrics.items()
            if metric_key in self.included_metrics
        ]

    def add_line(self, log_line: Dict[str, str]):
        for metric in self.metrics:
            metric.add_element(log_line)

    def export_all_metrics(self):
        return [metric.export() for metric in self.metrics]

    def reset_aggregations(self):
        self.metrics = self._initialize_metrics()
