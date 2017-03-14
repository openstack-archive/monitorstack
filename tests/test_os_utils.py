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
"""Tests for the os_utils plugin."""

import unittest

import mock

from monitorstack.utils import os_utils

import tests  # Import the test base module


class OpenStackObject(object):
    """Mocked server object."""

    def __init__(self, id=None, name=None):
        """Mocked server class."""
        self.id = id
        self.name = name

    def to_dict(self):
        """Mocked dict return."""
        return {
            'id': self.id,
            'name': self.name
        }


class MockedOpenStackConn(object):
    """Mocked OpenStack Connection object."""

    class compute(object):  # noqa
        """Mocked compute class."""

        @staticmethod
        def servers(*args, **kwargs):
            """Mocked servers method."""
            servers = [
                OpenStackObject(1, 'test1'),
                OpenStackObject(2, 'test2'),
                OpenStackObject(3, 'test3'),
                OpenStackObject(4, 'test4'),
                OpenStackObject(5, 'test5')
            ]
            if 'marker' in kwargs:
                for server in servers:
                    if server.id == kwargs['marker']:
                        index = servers.index(server)
                        servers.pop(index)
                        return servers[index:]
            return servers

        @staticmethod
        def flavors():
            """Mocked flavors return."""
            return [
                OpenStackObject(1, 'test1'),
                OpenStackObject(2, 'test2'),
                OpenStackObject(3, 'test3'),
                OpenStackObject(4, 'test4'),
                OpenStackObject(5, 'test5')
            ]

        @staticmethod
        def get_flavor(flavor_id):
            """Return mocked flavor object."""
            return OpenStackObject(
                flavor_id,
                'test_{}'.format(flavor_id)
            )

    class identity(object):  # noqa
        """Mocked identity object."""

        @staticmethod
        def projects():
            """Mocked projects return."""
            return [
                OpenStackObject(1, 'test1'),
                OpenStackObject(2, 'test2'),
                OpenStackObject(3, 'test3'),
                OpenStackObject(4, 'test4'),
                OpenStackObject(5, 'test5')
            ]

        @staticmethod
        def get_project(project_id):
            """Return mocked project object."""
            return OpenStackObject(
                project_id,
                'test_{}'.format(project_id)
            )

    class session(object):  # noqa
        """Mocked session object."""

        @staticmethod
        def get_endpoint(interface, service_type):
            """Mocked endpoint return."""
            return "https://127.0.1.1/{}/{}".format(interface, service_type)

        @staticmethod
        def get(url):
            """Mocked get return."""
            class SessionGet(object):
                """Mocked session object."""

                def __init__(self, url):
                    """Mocked session get."""
                    self.url = url

                def json(self):
                    """Mocked json return."""
                    return {'url': self.url}

            return SessionGet(url=url)


class TestOSUtilsConnection(unittest.TestCase):
    """Tests for the utilities."""

    def test_conn(self):
        """Test the OpenStack connection interface."""
        # load the base class for these tests.
        self.osu = os_utils.OpenStack(
            os_auth_args=tests.read_config()['keystone']
        )
        self.assertTrue(
            isinstance(
                self.osu.conn,
                os_utils.os_conn.Connection
            )
        )


class TestOsUtils(unittest.TestCase):
    """Tests for the utilities."""

    def setUp(self):
        """Setup the test."""
        # load the base class for these tests.
        self.osu = os_utils.OpenStack(
            os_auth_args=tests.read_config()['keystone']
        )

    def tearDown(self):
        """Tear down the test."""
        pass

    def test_get_consumer_usage(self):
        """Test retrieving consumer usage."""
        with mock.patch('openstack.connection.Connection') as MockClass:
            MockClass.return_value = MockedOpenStackConn()
            self.assertTrue(isinstance(self.osu.get_consumer_usage(), list))

    def test_get_consumer_usage_with_servers(self):
        """Test retrieving consumer usage with servers list."""
        with mock.patch('openstack.connection.Connection') as MockClass:
            MockClass.return_value = MockedOpenStackConn()
            servers = self.osu.get_consumer_usage(
                servers=[OpenStackObject(0, 'test0').to_dict()]
            )
            self.assertEquals(len(servers), 6)

    def test_get_consumer_usage_with_marker(self):
        """Test retrieving consumer usage."""
        with mock.patch('openstack.connection.Connection') as MockClass:
            MockClass.return_value = MockedOpenStackConn()
            servers = self.osu.get_consumer_usage(marker=5)
            self.assertEquals(len(servers), 0)

        with mock.patch('openstack.connection.Connection') as MockClass:
            MockClass.return_value = MockedOpenStackConn()
            servers = self.osu.get_consumer_usage(marker=2)
            self.assertEquals(len(servers), 3)

    def test_get_consumer_usage_with_limit(self):
        """Test retrieving consumer usage."""
        with mock.patch('openstack.connection.Connection') as MockClass:
            MockClass.return_value = MockedOpenStackConn()
            servers = self.osu.get_consumer_usage(limit=1)
            self.assertEquals(len(servers), 5)

    def test_get_compute_limits(self):
        """Test retrieving consumer limits."""
        with mock.patch('openstack.connection.Connection') as MockClass:
            MockClass.return_value = MockedOpenStackConn()
            limits = self.osu.get_compute_limits(project_id='not-a-uuid')
            u = 'https://127.0.1.1/internal/compute/os-quota-sets/not-a-uuid'
            self.assertEquals(limits, {'url': u})

    def test_get_projects(self):
        """Test retrieving project list."""
        with mock.patch('openstack.connection.Connection') as MockClass:
            MockClass.return_value = MockedOpenStackConn()
            projects = self.osu.get_projects()
            self.assertEquals(len(projects), 5)

    def test_get_project(self):
        """Test retrieving project dict."""
        with mock.patch('openstack.connection.Connection') as MockClass:
            MockClass.return_value = MockedOpenStackConn()
            project = self.osu.get_project(project_id='12345')
            self.assertEquals(project['id'], '12345')
            self.assertEquals(project['name'], 'test_12345')

    def test_get_project_name(self):
        """Test retrieving project name."""
        with mock.patch('openstack.connection.Connection') as MockClass:
            MockClass.return_value = MockedOpenStackConn()
            project_name = self.osu.get_project_name(project_id='12345')
            self.assertEquals(project_name, 'test_12345')

    def test_get_flavors(self):
        """Test retrieving flavors dict."""
        with mock.patch('openstack.connection.Connection') as MockClass:
            MockClass.return_value = MockedOpenStackConn()
            servers = self.osu.get_flavors()
            self.assertEquals(len(servers), 5)

    def test_get_flavor(self):
        """Test retrieving flavor dict."""
        with mock.patch('openstack.connection.Connection') as MockClass:
            MockClass.return_value = MockedOpenStackConn()
            flavor = self.osu.get_flavor(flavor_id=12345)
            self.assertEquals(flavor['id'], 12345)
            self.assertEquals(flavor['name'], 'test_12345')

    def test_get_flavor_name(self):
        """Test retrieving flavor name."""
        with mock.patch('openstack.connection.Connection') as MockClass:
            MockClass.return_value = MockedOpenStackConn()
            flavor_name = self.osu.get_flavor_name(flavor_id=12345)
            self.assertEquals(flavor_name, 'test_12345')
