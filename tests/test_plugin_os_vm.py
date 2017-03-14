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
from monitorstack.utils.os_utils import OpenStack as Ost


def _runner(module):
    runner = CliRunner()
    result = runner.invoke(cli, [
        '-f', 'json',
        module,
        '--config-file', 'tests/files/test-openstack.ini',
    ])
    return json.loads(result.output)


class MockProject(object):
    """Mock class for OpenStack class."""

    def __init__(self):
        """Mock init."""
        self.id = 'testing'
        self.name = 'testing'
        self.project_id = 12345


def mock_get_consumer_usage(*args, **kwargs):
    """Mocked get_consumer_usage()."""
    return [{
        'name': 'test_name',
        'project_id': 12345,
        'flavor': {
            'id': 1,
            'name': 'flavor_one'
        }
    }]


def mock_get_flavors(*args, **kwargs):
    """Mocked get_flavors()."""
    return {
        1: {
            'name': 'flavor_one',
            'vcpus': 2,
            'disk': 10,
            'ram': 1024,
        }
    }


def mock_get_flavor(*args, **kwargs):
    """Mocked get_flavor(id)."""
    return {
        'name': 'flavor_one',
        'vcpus': 2,
        'disk': 10,
        'ram': 1024,
    }


def mock_get_project_name(*args, **kwargs):
    """Mocked get_projects()."""
    return 'test_name'


def mock_get_projects(*args, **kwargs):
    """Mocked get_projects()."""
    return [MockProject()]


def mock_get_compute_limits(*args, **kwargs):
    """Mocked get_compute_limits()."""
    return {
        'quota_set': {
            'instances': 10,
            'cores': 10,
            'ram': 1024,
        }
    }


class TestOs(object):
    """Tests for the os_vm.* monitors."""

    def test_os_vm_quota_cores_success(self, monkeypatch):
        """Ensure os_vm_quota_cores method works with success."""
        monkeypatch.setattr(Ost, 'get_projects', mock_get_projects)
        monkeypatch.setattr(Ost, 'get_compute_limits', mock_get_compute_limits)

        result = _runner('os_vm_quota_cores')
        assert result['measurement_name'] == 'os_vm_quota_cores'
        assert result['meta'] == {'quotas': 'cores'}

    def test_os_vm_quota_cores_failure(self):
        """Ensure os_vm_quota_cores method works with failure."""
        result = _runner('os_vm_quota_cores')
        assert result['measurement_name'] == 'os_vm_quota_cores'
        assert result['meta'] == {'quotas': 'cores'}

    def test_os_vm_quota_instance_success(self, monkeypatch):
        """Ensure os_vm_quota_cores method works with success."""
        monkeypatch.setattr(Ost, 'get_projects', mock_get_projects)
        monkeypatch.setattr(Ost, 'get_compute_limits', mock_get_compute_limits)

        result = _runner('os_vm_quota_instance')
        assert result['measurement_name'] == 'os_vm_quota_instance'
        assert result['meta'] == {'quotas': 'instances'}

    def test_os_vm_quota_instance_failure(self):
        """Ensure os_vm_quota_cores method works with failure."""
        result = _runner('os_vm_quota_instance')
        assert result['measurement_name'] == 'os_vm_quota_instance'
        assert result['meta'] == {'quotas': 'instances'}

    def test_os_vm_quota_ram_success(self, monkeypatch):
        """Ensure os_vm_quota_ram method works with success."""
        monkeypatch.setattr(Ost, 'get_projects', mock_get_projects)
        monkeypatch.setattr(Ost, 'get_compute_limits', mock_get_compute_limits)

        result = _runner('os_vm_quota_ram')
        assert result['measurement_name'] == 'os_vm_quota_ram'
        assert result['meta'] == {'quotas': 'ram'}

    def test_os_vm_quota_ram_failure(self):
        """Ensure os_vm_quota_ram method works with failure."""
        result = _runner('os_vm_quota_ram')
        assert result['measurement_name'] == 'os_vm_quota_ram'
        assert result['meta'] == {'quotas': 'ram'}

    def test_os_vm_used_cores_success(self, monkeypatch):
        """Ensure os_vm_used_cores method works with success."""
        monkeypatch.setattr(Ost, 'get_flavors', mock_get_flavors)
        monkeypatch.setattr(Ost, 'get_flavor', mock_get_flavor)
        monkeypatch.setattr(Ost, 'get_project_name', mock_get_project_name)
        monkeypatch.setattr(Ost, 'get_consumer_usage', mock_get_consumer_usage)

        result = _runner('os_vm_used_cores')
        assert result['measurement_name'] == 'os_vm_used_cores'
        assert result['meta']['used'] == 'cores'
        assert result['meta']['flavor_one']

    def test_os_vm_used_cores_failure(self):
        """Ensure os_vm_used_cores method works with failure."""
        result = _runner('os_vm_used_cores')
        assert result['measurement_name'] == 'os_vm_used_cores'
        assert result['meta'] == {'used': 'cores'}

    def test_os_vm_used_disk_success(self, monkeypatch):
        """Ensure os_vm_used_disk method works with success."""
        monkeypatch.setattr(Ost, 'get_flavors', mock_get_flavors)
        monkeypatch.setattr(Ost, 'get_flavor', mock_get_flavor)
        monkeypatch.setattr(Ost, 'get_project_name', mock_get_project_name)
        monkeypatch.setattr(Ost, 'get_consumer_usage', mock_get_consumer_usage)

        result = _runner('os_vm_used_disk')
        assert result['measurement_name'] == 'os_vm_used_disk'
        assert result['meta']['used'] == 'disk'
        assert result['meta']['flavor_one']

    def test_os_vm_used_disk_failure(self):
        """Ensure os_vm_used_disk method works with failure."""
        result = _runner('os_vm_used_disk')
        assert result['measurement_name'] == 'os_vm_used_disk'
        assert result['meta'] == {'used': 'disk'}

    def test_os_vm_used_instance_success(self, monkeypatch):
        """Ensure os_vm_used_instance method works with success."""
        monkeypatch.setattr(Ost, 'get_flavors', mock_get_flavors)
        monkeypatch.setattr(Ost, 'get_flavor', mock_get_flavor)
        monkeypatch.setattr(Ost, 'get_project_name', mock_get_project_name)
        monkeypatch.setattr(Ost, 'get_consumer_usage', mock_get_consumer_usage)

        result = _runner('os_vm_used_instance')
        assert result['measurement_name'] == 'os_vm_used_instance'
        assert result['meta']['used'] == 'instances'
        assert result['variables'] == {'test_name': 1}

    def test_os_vm_used_instance_failure(self):
        """Ensure os_vm_used_instance method works with failure."""
        result = _runner('os_vm_used_instance')
        assert result['measurement_name'] == 'os_vm_used_instance'
        assert result['meta'] == {'used': 'instances'}

    def test_os_vm_used_ram_success(self, monkeypatch):
        """Ensure os_vm_used_ram method works with success."""
        monkeypatch.setattr(Ost, 'get_flavors', mock_get_flavors)
        monkeypatch.setattr(Ost, 'get_flavor', mock_get_flavor)
        monkeypatch.setattr(Ost, 'get_project_name', mock_get_project_name)
        monkeypatch.setattr(Ost, 'get_consumer_usage', mock_get_consumer_usage)

        result = _runner('os_vm_used_ram')
        assert result['measurement_name'] == 'os_vm_used_ram'
        assert result['meta']['used'] == 'ram'
        assert result['meta']['flavor_one']
        assert result['variables'] == {'test_name': 1024}

    def test_os_vm_used_ram_failure(self):
        """Ensure os_vm_used_ram method works with failure."""
        result = _runner('os_vm_used_ram')
        assert result['measurement_name'] == 'os_vm_used_ram'
        assert result['meta'] == {'used': 'ram'}
