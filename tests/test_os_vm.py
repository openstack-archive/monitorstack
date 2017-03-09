# Copyright 2017, Kevin Carter <kevin@cloudnull.com>
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
"""Tests for the KVM plugin."""

import json

from click.testing import CliRunner

from monitorstack.cli import cli


def _runner(module):
    runner = CliRunner()
    result = runner.invoke(cli, ['-f', 'json', module])
    return json.loads(result.output)


class TestOs(object):
    """Tests for the os_vm.* monitors."""

    def test_os_vm_quota_cores(self):
        """Ensure the run() method works."""

        # result_json = _runner(module='os_vm_quota_cores')
        # variables = result_json['variables']
        # meta = result_json['meta']
        pass

    def test_os_vm_quota_instances(self):
        """Ensure the run() method works."""
        pass

    def test_os_vm_quota_ram(self):
        """Ensure the run() method works."""
        pass

    def test_os_vm_used_cores(self):
        """Ensure the run() method works."""
        pass

    def test_os_vm_used_disk(self):
        """Ensure the run() method works."""
        pass

    def test_os_vm_used_instances(self):
        """Ensure the run() method works."""
        pass

    def test_os_vm_used_ram(self):
        """Ensure the run() method works."""
        pass
