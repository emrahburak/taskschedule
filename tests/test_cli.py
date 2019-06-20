# pylint: disable=missing-docstring,no-self-use

import subprocess
import unittest

from .context import taskschedule


class CLITest(unittest.TestCase):
    def test_cli_valid_date_does_not_error(self):
        # Ensure it times out, because that means it atleast
        # entered the main loop
        try:
            subprocess.run(
                ['python3 __main__.py --from today --until tomorrow'],
                shell=True,
                timeout=1,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, check=True)
        except subprocess.TimeoutExpired:
            pass

    def test_cli_invalid_date_prints_error(self):
        try:
            process = subprocess.run(
                ['python3 __main__.py --from asdfafk --until tomorrow'],
                shell=True,
                timeout=10,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, check=True)
            output = process.stdout.split(b'\n')
            self.assertEqual(output[0], b"Error: time data 'asdfafk' does not match format '%Y-%m-%dT%H:%M:%S'")
        except subprocess.CalledProcessError:
            pass

    def test_cli_help_returns_help_message(self):
        process = subprocess.run(['python3 __main__.py -h'],
                                 shell=True,
                                 timeout=10,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, check=True)
        output = process.stdout.split(b'\n')
        assert output[0].startswith(b'usage:')
