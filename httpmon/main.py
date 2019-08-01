import sys
import time
from typing import List

from httpmon.data import available_metrics
from httpmon.data.alerts import RequestsAlert
from httpmon.exceptions import UserEndedSession
from httpmon.log_process.log_aggregator import LogAggregator
from httpmon.log_process.log_parser import LogParser
from httpmon.outputs.terminal_ui import TerminalUI
from httpmon.utils import Counter


class HTTPMonCLI:
    def __init__(self, log_dir: str, max_requests: int, refresh_frequency: int, included_metrics: List[str]):
        metrics_with_desc = {
            metric: metric_value['description'] for metric, metric_value in available_metrics.items()
            if metric in included_metrics
        }

        self.counter = Counter(refresh_frequency)
        self.ui = TerminalUI(metrics_with_desc)
        self.log_file = LogParser(log_dir)
        self.log_aggregator = LogAggregator(included_metrics)
        self.requests_alert = RequestsAlert(max_requests)

    def start(self):
        continue_running = True
        try:
            self.counter.start()

            while continue_running:
                if self.counter.has_finished:
                    self.ui.display_metrics(self.log_aggregator.export_all_metrics())
                    self.log_aggregator.reset_aggregations()
                    self.counter.start()

                self.ui.update_counter(int(self.counter.remaining_time))
                self.ui.check_pressed_keys()

                self._process_log()
                self._process_alerts()

                time.sleep(0.1)

        except (UserEndedSession, KeyboardInterrupt):
            sys.exit()
        finally:
            self.log_file.end()
            self.ui.end()

    def _process_log(self):
        parsed_lines = self.log_file.parse_next_lines()
        for parsed_line in parsed_lines:
            self.log_aggregator.add_line(parsed_line)
            self.requests_alert.add_line(parsed_line)

    def _process_alerts(self):
        alert_tuple = self.requests_alert.check_alert()
        if alert_tuple:
            self.ui.update_alert(alert_tuple)
