from unittest.mock import MagicMock, patch

from httpmon.log_process.log_aggregator import LogAggregator

metric1_mock = MagicMock
metric2_mock = MagicMock

fake_available_metrics = {
    'metric1': {
        'class': metric1_mock,
        'description': 'Fake description metric 1'
    },
    'metric2': {
        'class': metric2_mock,
        'description': 'Fake description metric 2'
    }
}


class TestLogAggregator:
    @patch('httpmon.log_process.log_aggregator.available_metrics', fake_available_metrics)
    def test_included_metrics(self):
        log_aggregator = LogAggregator([list(fake_available_metrics.keys())[0]])
        assert len(log_aggregator.metrics) == 1

        log_aggregator = LogAggregator(list(fake_available_metrics.keys()))
        assert len(log_aggregator.metrics) == len(fake_available_metrics)

    @patch('httpmon.log_process.log_aggregator.available_metrics', fake_available_metrics)
    def test_unexisting_metric(self):
        log_aggregator = LogAggregator(['unexisting_metric', *fake_available_metrics])
        assert len(log_aggregator.metrics) == len(fake_available_metrics)

    @patch('httpmon.log_process.log_aggregator.available_metrics', fake_available_metrics)
    def test_add_line(self):
        log_aggregator = LogAggregator(list(fake_available_metrics.keys()))

        fake_line = {
            'field1': 'fake data 1',
            'field2': 'fake data 2',
        }

        log_aggregator.add_line(fake_line)

        for fake_metric in log_aggregator.metrics:
            fake_metric.add_element.assert_called_once_with(fake_line)

    @patch('httpmon.log_process.log_aggregator.available_metrics', fake_available_metrics)
    def test_export_all_metrics(self):
        log_aggregator = LogAggregator(list(fake_available_metrics.keys()))

        fake_export = {
            'field_name': 'fake field',
            'data': ['fake', 'data'],
        }

        for fake_metric in log_aggregator.metrics:
            fake_metric.export.return_value = fake_export

        exported_data = log_aggregator.export_all_metrics()

        assert len(exported_data) == len(fake_available_metrics)
        assert exported_data == [fake_export for _ in fake_available_metrics]

    @patch('httpmon.log_process.log_aggregator.available_metrics', fake_available_metrics)
    def test_reset_aggregations(self):
        log_aggregator = LogAggregator(list(fake_available_metrics.keys()))

        metric_objects = log_aggregator.metrics

        log_aggregator.reset_aggregations()

        assert metric_objects != log_aggregator.metrics
