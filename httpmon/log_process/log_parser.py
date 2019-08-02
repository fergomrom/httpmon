import os
import re
from datetime import datetime


class LogParser:
    """Parse a HTTP access log with the format defined in https://www.w3.org/Daemon/User/Config/Logging.html.

    Example lines:
        127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 200 123
        127.0.0.1 - jill [09/May/2018:16:00:41 +0000] "GET /api/user HTTP/1.0" 200 234
    """
    regex_expression = (
        r"(?P<remotehost>(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}"
        r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?).*\w*) "
        r"\[(?P<datetime>.*)] "
        r"\"(?P<method>[A-Z]*) (?P<section>/\w*)(?P<subsection>/\w*)?.*\" "
        r"(?P<status_code>\d{3}) "
        r"(?P<bytes>\d+)"
    )
    date_format = '%d/%b/%Y:%H:%M:%S %z'

    def __init__(self, file_dir: str):
        self.file_handler = open(file_dir, 'r')
        self.file_handler.seek(0, os.SEEK_END)
        self.regex = re.compile(self.regex_expression)

    def end(self):
        self.file_handler.close()

    def parse_next_lines(self):
        next_lines = self.file_handler.read()
        matches = self.regex.finditer(next_lines)

        parsed_lines = []
        for line in matches:
            parsed_line = line.groupdict()
            try:
                parsed_line['datetime'] = datetime.strptime(parsed_line['datetime'], self.date_format)
            except ValueError:
                continue

            parsed_lines.append(parsed_line)

        return parsed_lines
