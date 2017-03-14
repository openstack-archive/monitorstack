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
import unittest

from click.testing import CliRunner

from monitorstack.cli import cli


def _runner(module):
    runner = CliRunner()
    result = runner.invoke(cli, ['-f', 'json', module])
    try:
        return json.loads(result.output)
    except Exception:
        return result.exception


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
            def __init__(self, *args, **kwargs):  # noqa
                pass

            def maxVcpus(self):  # noqa
                return 2


class LibvirtStubFailed(object):
    """Stubbed libvirt class."""

    class openReadOnly(object):  # noqa
        """Stubbed openReadOnly class."""

        def close(self, *args, **kwargs):  # noqa
            pass

        def listDomainsID(self, *args, **kwargs):  # noqa
            raise RuntimeError('Failed')


class TestKvm(unittest.TestCase):
    """Tests for the kvm monitor."""

    def setUp(self):
        """Setup teardown."""
        self.orig_libvirt = sys.modules.pop('libvirt', None)
        sys.modules['libvirt'] = LibvirtStub()

    def tearDown(self):
        """Teardown method."""
        if self.orig_libvirt:
            sys.modules['libvirt'] = self.orig_libvirt

    def test_run_success(self):
        """Ensure the run() method works."""
        result = _runner('kvm')
        variables = result['variables']
        meta = result['meta']
        assert 'kvm_vms' in variables
        assert variables['kvm_vms'] == 3
        assert 'kvm_total_vcpus' in variables
        assert variables['kvm_total_vcpus'] == 1
        assert 'kvm_scheduled_vcpus' in variables
        assert variables['kvm_scheduled_vcpus'] == 6
        assert 'platform' in meta
        assert 'kvm_host_id' in meta
        assert result['exit_code'] == 0

    def test_run_failure_no_libvirt(self):
        """Ensure the run() method works."""
        sys.modules.pop('libvirt', None)
        result = _runner('kvm')
        self.assertTrue(isinstance(result, SystemExit))

    def test_run_failure(self):
        """Ensure the run() method works."""
        sys.modules['libvirt'] = LibvirtStubFailed()
        result = _runner('kvm')
        assert result['measurement_name'] == 'kvm'
        assert result['exit_code'] == 1
