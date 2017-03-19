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
"""Tests for the uptime plugin."""

from monitorstack.plugins.uptime import get_uptime

import tests  # Import the test base module


class TestUptime(object):
    """Tests for the uptime monitor class."""

    def test_run(self):
        """Ensure the run() method works."""
        result = tests.runner('uptime')
        assert 'uptime' in result['variables']
        assert result['exit_code'] == 0

    def test_get_uptime(self):
        """Ensure the cli() method works."""
        uptime = get_uptime()
        assert isinstance(uptime, float)
        assert uptime > 0
