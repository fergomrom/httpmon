from random import randint

from httpmon.data.metrics import (MetricOccurences, MetricPercentage,
                                  MetricSummary)


class TestMetricOccurences:
    def test_add_element(self):
        metric = MetricOccurences()
        metric_key = 'fake_key'
        metric_data1 = 'fake data 1'
        metric_data2 = 'fake data 2'
        metric.metric_key = metric_key

        assert not metric.metrics_data

        fake_element = {
            metric_key: metric_data1
        }

        random_int1 = randint(1, 10)
        for _ in range(random_int1):
            metric.add_element(fake_element)

        fake_element = {
            metric_key: metric_data2
        }

        random_int2 = randint(1, 10)
        for _ in range(random_int2):
            metric.add_element(fake_element)

        assert metric.metrics_data == {
            metric_data1: random_int1,
            metric_data2: random_int2,
        }

    def test_add_element_error(self):
        metric = MetricOccurences()
        metric_key = 'fake_key'
        metric_data = 'fake data'
        metric.metric_key = metric_key

        fake_element = {
            'another_fake_key': metric_data
        }

        metric.add_element(fake_element)

        assert not metric.metrics_data

    def test_get_sorted_data(self):
        metric = MetricOccurences()
        metric_key = 'fake_key'
        metric_data1 = 'fake data 1'
        metric_data2 = 'fake data 2'
        metric.metric_key = metric_key

        fake_element = {
            metric_key: metric_data1
        }

        for _ in range(5):
            metric.add_element(fake_element)

        fake_element = {
            metric_key: metric_data2
        }

        for _ in range(10):
            metric.add_element(fake_element)

        sorted_data = metric.get_sorted_data()

        assert len(sorted_data) == 2
        assert sorted_data == [(metric_data2, 10), (metric_data1, 5)]

    def test_export(self):
        metric = MetricOccurences()
        metric_key = 'fake_key'
        metric_data1 = 'fake data 1'
        metric_data2 = 'fake data 2'
        metric.metric_key = metric_key

        fake_element = {
            metric_key: metric_data1
        }

        for _ in range(5):
            metric.add_element(fake_element)

        fake_element = {
            metric_key: metric_data2
        }

        for _ in range(10):
            metric.add_element(fake_element)

        exported_data = metric.export()

        assert len(exported_data) == 2
        assert exported_data == {
            'metric_key': metric_key,
            'data': [
                (metric_data2, 10),
                (metric_data1, 5),
            ]
        }


class TestMetricPercentage:
    def test_add_element(self):
        metric = MetricPercentage()
        metric_key = 'fake_key'
        metric_data1 = 'fake data 1'
        metric_data2 = 'fake data 2'
        metric.metric_key = metric_key

        assert not metric.metrics_data

        fake_element = {
            metric_key: metric_data1
        }

        random_int1 = randint(1, 10)
        for _ in range(random_int1):
            metric.add_element(fake_element)

        fake_element = {
            metric_key: metric_data2
        }

        random_int2 = randint(1, 10)
        for _ in range(random_int2):
            metric.add_element(fake_element)

        assert metric.metrics_data == {
            metric_data1: random_int1,
            metric_data2: random_int2,
        }
        assert metric.total == random_int1 + random_int2

    def test_add_element_error(self):
        metric = MetricPercentage()
        metric_key = 'fake_key'
        metric_data = 'fake data'
        metric.metric_key = metric_key

        fake_element = {
            'another_fake_key': metric_data
        }

        metric.add_element(fake_element)

        assert not metric.metrics_data

    def test_get_percentages(self):
        metric = MetricPercentage()
        metric_key = 'fake_key'
        metric_data1 = 'fake data 1'
        metric_data2 = 'fake data 2'
        metric.metric_key = metric_key

        fake_element = {
            metric_key: metric_data1
        }

        random_int1 = randint(1, 10)
        for _ in range(random_int1):
            metric.add_element(fake_element)

        fake_element = {
            metric_key: metric_data2
        }

        random_int2 = randint(1, 10)
        for _ in range(random_int2):
            metric.add_element(fake_element)

        data_percentages = metric.get_percentages()

        assert len(data_percentages) == 2
        assert data_percentages == {
            metric_data1: f'{random_int1 / (random_int1 + random_int2) * 100:.2f}%',
            metric_data2: f'{random_int2 / (random_int1 + random_int2) * 100:.2f}%',
        }

    def test_get_sorted_data(self):
        metric = MetricPercentage()
        metric_key = 'fake_key'
        metric_data1 = 'fake data 1'
        metric_data2 = 'fake data 2'
        metric.metric_key = metric_key

        fake_element = {
            metric_key: metric_data1
        }

        for _ in range(4):
            metric.add_element(fake_element)

        fake_element = {
            metric_key: metric_data2
        }

        for _ in range(6):
            metric.add_element(fake_element)

        sorted_data = metric.get_sorted_data()

        assert len(sorted_data) == 2
        assert sorted_data == [(metric_data2, '60.00%'), (metric_data1, '40.00%')]

    def test_export(self):
        metric = MetricPercentage()
        metric_key = 'fake_key'
        metric_data1 = 'fake data 1'
        metric_data2 = 'fake data 2'
        metric.metric_key = metric_key

        fake_element = {
            metric_key: metric_data1
        }

        for _ in range(4):
            metric.add_element(fake_element)

        fake_element = {
            metric_key: metric_data2
        }

        for _ in range(6):
            metric.add_element(fake_element)

        exported_data = metric.export()

        assert len(exported_data) == 2
        assert exported_data == {
            'metric_key': metric_key,
            'data': [
                (metric_data2, '60.00%'),
                (metric_data1, '40.00%'),
            ]
        }


class TestMetricSummary:
    def test_add_element(self):
        metric = MetricSummary()
        total_bytes = 0
        total_requests = randint(1, 10)

        for _ in range(total_requests):
            element_bytes = randint(1, 1000)
            fake_element = {
                'bytes': element_bytes
            }
            total_bytes += element_bytes
            metric.add_element(fake_element)

        assert metric.metrics_data == {
            'Total bytes': total_bytes,
            'Total requests': total_requests
        }

    def test_add_element_error(self):
        metric = MetricSummary()
        total_requests = randint(1, 10)

        for _ in range(total_requests):
            fake_element = {}
            metric.add_element(fake_element)

        assert metric.metrics_data == {
            'Total bytes': 0,
            'Total requests': total_requests
        }

    def test_export(self):
        metric = MetricSummary()
        total_bytes = 0
        total_requests = randint(1, 10)

        for _ in range(total_requests):
            element_bytes = randint(1, 1000)
            fake_element = {
                'bytes': element_bytes
            }
            total_bytes += element_bytes
            metric.add_element(fake_element)

        exported_data = metric.export()
        assert exported_data == {
            'metric_key': 'summary',
            'data': [
                ('Total bytes', total_bytes),
                ('Total requests', total_requests),
            ]
        }
