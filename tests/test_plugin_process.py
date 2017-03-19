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

import mock

from monitorstack.plugins import process

import tests  # Import the test base module


class TestUptime(object):
    """Tests for the uptime monitor class."""

    def test_run_failure(self):
        """Ensure the run() method works."""
        process_name = 'dont-go-chasing-waterfalls'
        result = tests.runner('process', extra_args=[process_name])
        assert result['variables'] == {process_name: 0}
        assert result['exit_code'] == 1

    def test_run_success(self):
        """Ensure the run() method works."""
        process_name = '/'
        result = tests.runner('process', extra_args=[process_name])
        assert result['variables'] == {process_name: 1}
        assert result['exit_code'] == 0

    def test_check_process_success(self, monkeypatch):
        """Ensure the check_process() method works."""
        def mock_get_cmdlines():
            return ['process1', 'process2']

        monkeypatch.setattr(process, 'get_cmdlines', mock_get_cmdlines)
        result = process.check_process('process2')
        assert result

    def test_get_cmdlines(self):
        """Ensure the get_cmdlines() method works."""
        assert isinstance(process.get_cmdlines(), list)

    def test_get_cmdlines_exception(self, monkeypatch):
        """Ensure the get_cmdlines() method works."""
        class _RaisePid(object):
            pid = 'not-a-pid'

            @staticmethod
            def cmdline():
                raise process.psutil.NoSuchProcess('not-a-pid')

        def _mock_process_iter():
            return [_RaisePid, _RaisePid, _RaisePid]

        with mock.patch('psutil.process_iter') as MockClass:
            MockClass.return_value = _mock_process_iter()
            process_name = 'dont-go-chasing-waterfalls'
            result = tests.runner('process', extra_args=[process_name])
            assert result['variables'] == {process_name: 0}
            assert result['exit_code'] == 1
