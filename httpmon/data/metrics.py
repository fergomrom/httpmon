import abc
from collections import defaultdict


class MetricInterface(abc.ABC):
    @abc.abstractmethod
    def add_element(self, element):
        pass

    @abc.abstractmethod
    def export(self):
        pass


class MetricOccurences(MetricInterface):
    def __init__(self):
        self.metric_key = ''
        self.metrics_data = defaultdict(int)

    def add_element(self, log_line):
        if self.metric_key in log_line:
            self.metrics_data[log_line[self.metric_key]] += 1

    def get_sorted_data(self):
        return sorted(self.metrics_data.items(), key=lambda x: x[1], reverse=True)

    def export(self):
        return {
            'metric_key': self.metric_key,
            'data': self.get_sorted_data()
        }


class MetricPercentage(MetricInterface):
    def __init__(self):
        self.metric_key = ''
        self.metrics_data = defaultdict(int)
        self.total = 0

    def add_element(self, log_line):
        if self.metric_key in log_line:
            self.metrics_data[log_line[self.metric_key]] += 1
            self.total += 1

    def get_percentages(self):
        return {key: f'{(value / self.total) * 100:.2f}%' for key, value in self.metrics_data.items()}

    def get_sorted_data(self):
        return sorted(self.get_percentages().items(), key=lambda x: x[1], reverse=True)

    def export(self):
        return {
            'metric_key': self.metric_key,
            'data': self.get_sorted_data()
        }


class SectionMetric(MetricOccurences):
    def __init__(self):
        super(SectionMetric, self).__init__()
        self.metric_key = 'section'


class HostMetric(MetricOccurences):
    def __init__(self):
        super(HostMetric, self).__init__()
        self.metric_key = 'remotehost'


class StatusCodeMetric(MetricPercentage):
    def __init__(self):
        super(StatusCodeMetric, self).__init__()
        self.metric_key = 'status_code'


class MethodMetric(MetricPercentage):
    def __init__(self):
        super(MethodMetric, self).__init__()
        self.metric_key = 'method'


class MetricSummary(MetricInterface):
    def __init__(self):
        self.metric_key = 'summary'
        self.metrics_data = {
            'Total bytes': 0,
            'Total requests': 0,
        }

    def add_element(self, log_line):
        if 'bytes' in log_line:
            self.metrics_data['Total bytes'] += int(log_line['bytes'])
        self.metrics_data['Total requests'] += 1

    def export(self):
        return {
            'metric_key': self.metric_key,
            'data': [(key, value) for key, value in self.metrics_data.items()]
        }
