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
"""Tests for the conntrack plugin."""
from monitorstack.plugins import conntrack

import tests


class TestConntrack(object):
    """Tests for the conntrack plugin."""

    def test_run_success(self, monkeypatch):
        """Ensure the run() method works."""
        def get_conntrack_data_success():
            """Simulate reading a file with success."""
            return {
                'nf_conntrack_count': '1',
                'nf_conntrack_max': '1'
            }

        monkeypatch.setattr(
            conntrack,
            'get_conntrack_data',
            get_conntrack_data_success
        )
        result = tests.runner('conntrack')
        assert result['variables']['nf_conntrack_count'] == '1'
        assert result['variables']['nf_conntrack_max'] == '1'
        assert result['exit_code'] == 0

    def test_run_failure(self, monkeypatch):
        """Ensure the run() method works."""
        def get_conntrack_data_failure():
            """Simulate reading a file with failure."""
            raise IOError(2, 'File does not exist', 'filename')

        monkeypatch.setattr(
            conntrack,
            'get_conntrack_data',
            get_conntrack_data_failure
        )
        result = tests.runner('conntrack')
        assert result['exit_code'] == 1
        assert 'Unable to read conntrack data' in result['message']

    def test_get_conntrack_data(self, monkeypatch):
        """Test the get_conntrack_data method."""
        def mock_read_file(path):
            """Mock up the read_file() method."""
            return '1'

        monkeypatch.setattr(conntrack, 'read_file', mock_read_file)
        result = conntrack.get_conntrack_data()
        assert result['nf_conntrack_count'] == '1'
        assert result['nf_conntrack_max'] == '1'
