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

from monitorstack.utils.os_utils import OpenStack as Ost

import tests  # Import the test base module


def get_volume_pool_stats(*args, **kwargs):
    """Mocked get_consumer_usage()."""
    return [
        {
            'name': 'name1',
            'capabilities': {
                'pool_name': 'pool_name1',
                'total_capacity_gb': 100,
                'free_capacity_gb': 50
            }
        },
        {
            'name': 'name2',
            'capabilities': {
                'pool_name': 'pool_name2',
                'total_capacity_gb': 100,
                'free_capacity_gb': 50
            }
        }
    ]


class TestOsBlock(object):
    """Tests for the os_vm.* monitors."""

    def test_os_block_pools_totals_success(self, monkeypatch):
        """Ensure os_block_pools_totals method works with success."""
        monkeypatch.setattr(
            Ost,
            'get_volume_pool_stats',
            get_volume_pool_stats
        )
        result = tests.runner(
            'os_block_pools_totals',
            extra_args=[
                '--config-file',
                'tests/files/test-openstack.ini'
            ]
        )
        variables = result['variables']
        meta = result['meta']
        assert variables['cinder_total_free_capacity'] == 100
        assert variables['cinder_total_percent_used'] == 50
        assert variables['cinder_total_used_capacity'] == 100
        assert variables['cinder_total_capacity'] == 200
        assert meta['block_pools'] == 'totals'
        assert meta['pool_name1'] is True
        assert meta['pool_name2'] is True
        assert result['measurement_name'] == 'os_block_pools_totals'

    def test_os_block_pools_totals_failure(self):
        """Ensure os_block_pools_totals method works with success."""
        result = tests.runner(
            'os_block_pools_totals',
            extra_args=[
                '--config-file',
                'tests/files/test-openstack.ini'
            ]
        )
        assert result['measurement_name'] == 'os_block_pools_totals'
        assert result['exit_code'] == 1

    def test_os_block_pools_usage_success(self, monkeypatch):
        """Ensure os_block_pools_totals method works with success."""
        monkeypatch.setattr(
            Ost,
            'get_volume_pool_stats',
            get_volume_pool_stats
        )
        result = tests.runner(
            'os_block_pools_usage',
            extra_args=[
                '--config-file',
                'tests/files/test-openstack.ini'
            ]
        )
        variables = result['variables']
        meta = result['meta']
        assert variables['pool_name1_free_capacity_gb'] == 50
        assert variables['pool_name2_total_capacity_gb'] == 100
        assert variables['pool_name1_percent_used'] == 50
        assert variables['pool_name1_total_capacity_gb'] == 100
        assert variables['pool_name2_free_capacity_gb'] == 50
        assert variables['pool_name2_percent_used'] == 50
        assert meta['block_pools'] == 'usage'
        assert meta['pool_name1'] is True
        assert meta['pool_name2'] is True
        assert result['measurement_name'] == 'os_block_pools_usage'

    def test_os_block_pools_usage_failure(self):
        """Ensure os_block_pools_totals method works with success."""
        result = tests.runner(
            'os_block_pools_usage',
            extra_args=[
                '--config-file',
                'tests/files/test-openstack.ini'
            ]
        )
        assert result['measurement_name'] == 'os_block_pools_usage'
        assert result['exit_code'] == 1
