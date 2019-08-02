import curses
import sys
from typing import Dict, List, Tuple

from httpmon.exceptions import UserEndedSession
from httpmon.utils import truncate_text


class TerminalUI:
    """Terminal interface that displays different metrics and alerts dynamically.
    """
    def __init__(self, metrics: Dict[str, str]):
        self.screen = curses.initscr()
        self.windows = {}
        self.remaining_time = 0

        self.window_width = (curses.COLS - 1) // len(metrics)
        self.window_height = (curses.LINES // 3) * 2
        if not self.screen:
            sys.exit(1)

        self._initialize_curses()
        self._create_windows(metrics)
        self.alerts_window = self._create_alert_window()
        self.counter_window = self._create_counter_window()
        self.legend_window = self._create_legend_window()

    def _initialize_curses(self):
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_YELLOW)

    def _create_windows(self, metrics: Dict[str, str]):
        current_x = 0

        for metric_key, metric_title in metrics.items():
            header_box = curses.newwin(3, self.window_width, 0, current_x)
            header_box.box()
            header_box.refresh()

            header = header_box.derwin(2, self.window_width - 2, 1, 1)
            header.addstr(truncate_text(metric_title, self.window_width - 5), curses.color_pair(3))
            header.refresh()

            current_window_box = curses.newwin(
                self.window_height,
                self.window_width,
                3,
                current_x
            )
            current_window_box.box()
            current_window_box.refresh()

            current_window = current_window_box.derwin(
                self.window_height - 2,
                self.window_width - 2,
                1,
                1
            )

            self.windows[metric_key] = current_window
            current_x += self.window_width
            current_window.noutrefresh()

    def _create_alert_window(self):
        header = curses.newwin(3, self.window_width, self.window_height + 4, 0)
        header.addstr('Alerts', curses.color_pair(6))
        header.refresh()

        alert_window = curses.newwin(
            self.window_height,
            curses.COLS - 1,
            self.window_height + 7,
            1
        )

        return alert_window

    def _create_counter_window(self):
        window_y = curses.LINES - 2
        counter_window = curses.newwin(3, curses.COLS - 20, window_y, 0)
        return counter_window

    def _create_legend_window(self):
        window_y = curses.LINES - 2
        window_x = curses.COLS - 20
        legend_window = curses.newwin(3, 20, window_y, window_x)
        legend_window.nodelay(1)
        legend_window.addstr('Press q to end', curses.color_pair(4))
        return legend_window

    def end(self):
        curses.nocbreak()
        curses.echo()
        curses.curs_set(1)
        curses.endwin()

    def display_metrics(self, metrics: List[Dict]):
        for metric in metrics:
            current_window = self.windows.get(metric['metric_key'])
            current_window.erase()
            if not metric['data']:
                current_window.addstr('No data', curses.color_pair(1))
            for index, line in enumerate(metric['data'][:self.window_height - 3]):
                text = truncate_text(f'{index + 1}. {line[0]}', self.window_width - 5)
                current_window.addstr(text)
                current_window.addstr(
                    f'{line[1]}\n'.rjust(self.window_width - len(text) - 5)
                )
            if len(metric['data']) > self.window_height:
                current_window.addstr('...')
            current_window.noutrefresh()
        curses.doupdate()

    def update_alert(self, alert_tuple: Tuple):
        self.alerts_window.erase()
        if alert_tuple[1] == 'OK':
            self.alerts_window.addstr(alert_tuple[0], curses.color_pair(2))
        if alert_tuple[1] == 'ERROR':
            self.alerts_window.addstr(alert_tuple[0], curses.color_pair(5))
        self.alerts_window.refresh()

    def update_counter(self, counter_seconds: int):
        if counter_seconds == self.remaining_time:
            return
        self.remaining_time = counter_seconds
        self.counter_window.erase()
        if counter_seconds == 0:
            self.counter_window.addstr(f'Refreshing...', curses.color_pair(2))
        else:
            self.counter_window.addstr(f'Next refresh in {counter_seconds}...'.ljust(40), curses.color_pair(2))
        self.counter_window.refresh()

    def check_pressed_keys(self):
        key = self.legend_window.getch()
        if key == ord('q'):
            raise UserEndedSession()
