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
"""Tests for the memcache plugin."""
import pymemcache

from monitorstack.plugins import memcache as monitorstack_memcache

import tests


class TestMemcache(object):
    """Tests for the memcache plugin."""

    def test_success(self, monkeypatch):
        """Ensure the run() method works."""
        def mock_get_memcached_stats(host, port):
            """Mock the get_memcached_stats() method."""
            return {'parameter': 'value'}

        monkeypatch.setattr(
            monitorstack_memcache,
            'get_memcached_stats',
            mock_get_memcached_stats
        )
        result = tests.runner('memcache')
        assert result['variables']['parameter'] == 'value'
        assert result['measurement_name'] == "memcache"
        assert result['exit_code'] == 0

    def test_failure(self, monkeypatch):
        """Ensure the run() method works."""
        def mock_get_memcached_stats(host, port):
            """Mock the get_memcached_stats() method."""
            raise Exception('Connection failed')

        monkeypatch.setattr(
            monitorstack_memcache,
            'get_memcached_stats',
            mock_get_memcached_stats
        )
        result = tests.runner('memcache')
        assert 'Connection failed' in result['message']
        assert result['measurement_name'] == "memcache"
        assert result['exit_code'] == 1

    def test_get_memcached_stats(self, monkeypatch):
        """Ensure that get_memcached_stats() works."""
        def mock_memcache_client(cls, (conn_tuple)):
            """Mock a memcache client class."""
            return None

        def mock_memcache_stats(toot):
            """Mock a memcache client class."""
            return {'parameter': 'value'}

        monkeypatch.setattr(
            pymemcache.client.base.Client,
            '__init__',
            mock_memcache_client
        )
        monkeypatch.setattr(
            pymemcache.client.base.Client,
            'stats',
            mock_memcache_stats
        )
        result = monitorstack_memcache.get_memcached_stats('localhost', 11211)
        assert result['parameter'] == 'value'
