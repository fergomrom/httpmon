from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from httpmon.log_process.log_parser import LogParser

expected_parsed_fields = ['remotehost', 'datetime', 'method', 'section', 'subsection', 'status_code', 'bytes']


class TestLogParser:
    @patch('httpmon.log_process.log_parser.open')
    def test_parse_correct_log_lines(self, mock_open):
        log_parser = LogParser('/fake/dir/access.log')

        file_content = (
            """127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /fake_section HTTP/1.0" 200 123\n"""
            """198.255.255.255 - jill [09/May/2018:16:00:41 +0000] "GET /fake_section/user HTTP/1.0" 200 234\n"""
            """1.2.3.4 - frank [09/May/2018:16:00:42 +0000] "POST /fake_section/user HTTP/1.0" 200 34"""
        )

        mock_open.return_value.read.return_value = file_content
        parsed_lines = log_parser.parse_next_lines()

        assert len(parsed_lines) == 3
        for line in parsed_lines:
            assert list(line.keys()) == expected_parsed_fields
            assert isinstance(line['datetime'], datetime)
            assert line['section'] == '/fake_section'

    @patch('httpmon.log_process.log_parser.open')
    @pytest.mark.parametrize('file_content', [
        '999.888.777.666 - james [09/May/2018:16:00:39 +0000] "GET /fake_section HTTP/1.0" 200 123',
        '127.0.0.1 - james [41/XXX/2018:16:00:39 +0000] "GET /fake_section HTTP/1.0" 200 123',
        '127.0.0.1 - james [09/May/2018:16:00:39 +0000] "" 200 123',
        '127.0.0.1 - james "GET /fake_section HTTP/1.0" 200 123',
        '127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /fake_section HTTP/1.0" 123',
        '127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /fake_section HTTP/1.0" twohundred 123',
        '127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /fake_section HTTP/1.0" 200 onetwothree',
        'XXXXX 12345',
        '',
    ])
    def test_parse_wrong_log_lines(self, mock_open, file_content):
        log_parser = LogParser('/fake/dir/access.log')

        mock_open.return_value.read.return_value = file_content
        parsed_lines = log_parser.parse_next_lines()

        assert not parsed_lines

    @patch('httpmon.log_process.log_parser.open')
    def test_end(self, mock_open):
        mock_file = MagicMock()
        mock_open.return_value = mock_file
        log_parser = LogParser('/fake/dir/access.log')

        mock_file.close.assert_not_called()
        log_parser.end()
        mock_file.close.assert_called_once_with()
