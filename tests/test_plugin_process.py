# Copyright 2017, Major Hayden <major@mhtx.net>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for the process plugin."""

import json

from click.testing import CliRunner

from monitorstack.cli import cli
from monitorstack.plugins import process


class TestUptime(object):
    """Tests for the uptime monitor class."""

    def test_run_failure(self):
        """Ensure the run() method works."""
        runner = CliRunner()
        process_name = 'dont-go-chasing-waterfalls'
        result = runner.invoke(cli, [
            '-f', 'json',
            'process', process_name])
        result_json = json.loads(result.output)
        assert result_json['variables'] == {process_name: 0}
        assert result.exit_code == 1

    def test_run_success(self):
        """Ensure the run() method works."""
        runner = CliRunner()
        process_name = '/'
        result = runner.invoke(cli, [
            '-f', 'json',
            'process', process_name])
        result_json = json.loads(result.output)
        assert result_json['variables'] == {process_name: 1}
        assert result.exit_code == 0

    def test_check_process_success(self, monkeypatch):
        """Ensure the check_process() method works."""
        def mock_get_cmdlines():
            return ['process1', 'process2']

        monkeypatch.setattr(process, 'get_cmdlines', mock_get_cmdlines)
        result = process.check_process('process2')
        assert result

    def test_get_cmdlines(self):
        """Ensure the get_cmdlines() method works."""
        cmdlines = process.get_cmdlines()
        assert isinstance(cmdlines, list)
