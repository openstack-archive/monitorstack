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
import sys

from click.testing import CliRunner

from monitorstack.cli import cli


class LibvirtStub(object):
    """Stubbed libvirt class."""

    class openReadOnly(object):  # noqa
        """Stubbed openReadOnly class."""

        def close(self, *args, **kwargs):  # noqa
            pass

        def listDomainsID(self, *args, **kwargs):  # noqa
            return ['a', 'b', 'c']

        def getCPUMap(self, *args, **kwargs):  # noqa
            return [1, 1, 1]

        class lookupByID(object):  # noqa
            """Stubbed lookupByID class."""
            def __init__(self, *args, **kwargs):
                pass

            def maxVcpus(self):  # noqa
                return 2


class TestKvm(object):
    """Tests for the uptime monitor class."""

    def test_run(self):
        """Ensure the run() method works."""

        sys.modules['libvirt'] = LibvirtStub

        runner = CliRunner()
        result = runner.invoke(cli, ['-f', 'json', 'kvm'])
        result_json = json.loads(result.output)

        variables = result_json['variables']
        meta = result_json['meta']
        assert 'kvm_vms' in variables
        assert variables['kvm_vms'] == 3
        assert 'kvm_total_vcpus' in variables
        assert variables['kvm_total_vcpus'] == 1
        assert 'kvm_scheduled_vcpus' in variables
        assert variables['kvm_scheduled_vcpus'] == 6
        assert 'platform' in meta
        assert 'kvm_host_id' in meta
        assert result.exit_code == 0
