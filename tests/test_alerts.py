from datetime import datetime
from random import randint
from unittest.mock import patch

import pytest

from httpmon.data.alerts import RequestsAlert

alert_message = 'High traffic generated an alert - hits per second = {value:.2f}, triggered at {time}'
recovery_message = 'Traffic recovered at {time} - hits per second = {value:.2f}'


class TestRequestsAlert:
    def test_add_line(self):
        alert = RequestsAlert(10)

        total_requests = randint(1, 20)
        for index in range(1, total_requests + 1):
            request = {
                'datetime': datetime.strptime(f'01/{index}/1970', '%m/%d/%Y')
            }
            alert.add_line(request)

        assert len(alert.requests_queue) == total_requests
        for index in range(total_requests):
            request_time = datetime.strptime(f'01/1/1970', '%m/%d/%Y').timestamp() + 86400 * index
            assert alert.requests_queue[index] == request_time

    @pytest.mark.parametrize('bad_request', [
        {},
        {'fake_field': 'fake data'},
        {'datetime': 9999},
        {'datetime': 'no datetime!'},
    ])
    def test_add_line_error(self, bad_request):
        alert = RequestsAlert(10)

        alert.add_line(bad_request)

        assert not alert.requests_queue

    def test_calculate_average(self):
        alert = RequestsAlert(10)

        total_requests = randint(1, 20)
        for index in range(1, total_requests + 1):
            request = {
                'datetime': datetime.strptime(f'01/{index}/1970', '%m/%d/%Y')
            }
            alert.add_line(request)

        average = alert.calculate_average()

        assert average == total_requests / alert.time_window_seconds

    @patch('httpmon.data.alerts.isinstance', return_value=True)
    @patch('httpmon.data.alerts.datetime')
    def test_check_alert_scenario_1(self, mock_datetime, mock_isinstance):
        alert = RequestsAlert(0.01)

        fake_times = [
            datetime.strptime(f'00:01:31', '%H:%M:%S').timestamp(),
            datetime.strptime(f'00:02:06', '%H:%M:%S').timestamp(),
            datetime.strptime(f'00:02:07', '%H:%M:%S').timestamp(),
            datetime.strptime(f'00:02:16', '%H:%M:%S').timestamp(),
            datetime.strptime(f'00:02:17', '%H:%M:%S').timestamp(),
            datetime.strptime(f'00:02:46', '%H:%M:%S').timestamp(),
        ]

        mock_datetime.now.return_value.timestamp.side_effect = fake_times

        requests = [
            {'datetime': datetime.strptime('00:00:05', '%H:%M:%S')},
            {'datetime': datetime.strptime('00:00:15', '%H:%M:%S')},
            {'datetime': datetime.strptime('00:00:45', '%H:%M:%S')},
        ]
        for request in requests:
            alert.add_line(request)

        # First call, alert is created since 3 requests average in the last 2 minutes
        # is higher than the 0.1 threshold
        returned_alert = alert.check_alert()
        assert returned_alert == (
            alert_message.format(time=mock_datetime.now.return_value, value=len(requests) / 120),
            'ERROR',
        )
        # Second call, alert continues since 2 requests average in the last 2 minutes
        # is higher than the 0.1 threshold
        returned_alert = alert.check_alert()
        assert not returned_alert
        # Third call, alert recovers since 1 requests average in the last 2 minutes
        # is lower than the 0.1 threshold
        returned_alert = alert.check_alert()
        assert returned_alert == (
            recovery_message.format(time=mock_datetime.now.return_value, value=1 / 120),
            'OK',
        )

    @patch('httpmon.data.alerts.isinstance', return_value=True)
    @patch('httpmon.data.alerts.datetime')
    def test_check_alert_scenario_2(self, mock_datetime, mock_isinstance):
        alert = RequestsAlert(0.01)

        fake_times = [
            datetime.strptime(f'00:01:31', '%H:%M:%S').timestamp(),
            datetime.strptime(f'00:01:58', '%H:%M:%S').timestamp(),
            datetime.strptime(f'00:02:06', '%H:%M:%S').timestamp(),
            datetime.strptime(f'00:02:07', '%H:%M:%S').timestamp(),
        ]

        mock_datetime.now.return_value.timestamp.side_effect = fake_times

        requests = [
            {'datetime': datetime.strptime('00:00:05', '%H:%M:%S')},
            {'datetime': datetime.strptime('00:00:05', '%H:%M:%S')},
        ]
        for request in requests:
            alert.add_line(request)

        # First call, alert is created since 2 requests average in the last 2 minutes
        # is higher than the 0.1 threshold
        returned_alert = alert.check_alert()
        assert returned_alert == (
            alert_message.format(time=mock_datetime.now.return_value, value=len(requests) / 120),
            'ERROR',
        )
        # Second call, alert continues since 2 requests average in the last 2 minutes
        # is higher than the 0.1 threshold
        returned_alert = alert.check_alert()
        assert not returned_alert
        # Third call, alert recovers since 0 requests average in the last 2 minutes
        # is lower than the 0.1 threshold
        returned_alert = alert.check_alert()
        assert returned_alert == (
            recovery_message.format(time=mock_datetime.now.return_value, value=0),
            'OK',
        )
