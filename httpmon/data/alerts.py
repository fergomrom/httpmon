import abc
from collections import deque
from datetime import datetime
from typing import Dict

TIME_WINDOW_SECONDS = 120


class AlertInterface(abc.ABC):
    @abc.abstractmethod
    def add_line(self, line):
        pass

    @abc.abstractmethod
    def check_alert(self):
        pass


class RequestsAlert(AlertInterface):
    """Keep track of the traffic in real time adding elements to a queue.

    Through the check_alert method, return an alert if the total average in a window of time
    is greater than the given threshold. If the average goes below the threshold, return a recovery.
    """
    alert_message = 'High traffic generated an alert - hits per second = {value:.2f}, triggered at {time}'
    recovery_message = 'Traffic recovered at {time} - hits per second = {value:.2f}'

    def __init__(self, threshold: int):
        self.threshold = threshold
        self.time_window_seconds = TIME_WINDOW_SECONDS
        self.requests_queue = deque()
        self.alert_active = False

    def add_line(self, request: Dict):
        if 'datetime' in request and isinstance(request['datetime'], datetime):
            self.requests_queue.append(request['datetime'].timestamp())

    def calculate_average(self):
        return len(self.requests_queue) / self.time_window_seconds

    def check_alert(self):
        """Check if an error or recovery alert must be sent.

        For all the available requests, check if the first element in the queue is inside the time window.
        If it is not, pop it. If it is, check if the average is above the threshold.
        """
        while self.requests_queue:
            if self.requests_queue[0] < (datetime.now().timestamp() - self.time_window_seconds):
                self.requests_queue.popleft()
            else:
                request_average = self.calculate_average()
                if request_average >= self.threshold:
                    if not self.alert_active:
                        self.alert_active = True
                        return (
                            self.alert_message.format(
                                value=request_average, time=datetime.now()
                            ), 'ERROR'
                        )
                elif self.alert_active:
                    self.alert_active = False
                    return (
                        self.recovery_message.format(
                            value=request_average, time=datetime.now()
                        ), 'OK'
                    )
                break

        if not self.requests_queue and self.alert_active:
            self.alert_active = False
            return (
                self.recovery_message.format(
                    value=0, time=datetime.now()
                ), 'OK'
            )
