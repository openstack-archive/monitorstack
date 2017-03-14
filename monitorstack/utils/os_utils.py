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
"""OpenStack-related utilities."""

try:
    from openstack import connection as os_conn
except ImportError as e:
    raise SystemExit('OpenStack plugins require access to the OpenStackSDK.'
                     ' Please install "python-openstacksdk".'
                     ' ERROR: %s' % str(e))

from monitorstack import utils


class OpenStack(object):
    """Class for reusable OpenStack utility methods."""

    def __init__(self, os_auth_args):
        """Initialization method for class.

        :param os_auth_args: dict containing auth creds.
        :type os_auth_args: dict
        """
        self.os_auth_args = os_auth_args

    @property
    def conn(self):
        """Return an OpenStackSDK connection.

        :returns: object
        """
        return os_conn.Connection(**self.os_auth_args)

    def get_consumer_usage(self, servers=None, marker=None, limit=512):
        """Retrieve current usage by an OpenStack cloud consumer.

        :param servers: ID of a given project to lookup.
        :type servers: str || uuid
        :param marker: ID of last server seen.
        :type marker: str || uuid
        :param limit: Number of items a single API call can return.
        :type limit: int
        :returns: list
        """
        tenant_kwargs = {'details': True, 'all_tenants': True, 'limit': limit}
        if not servers:
            servers = list()

        if marker:
            tenant_kwargs['marker'] = marker

        count = 0
        for server in self.conn.compute.servers(**tenant_kwargs):
            servers.append(server.to_dict())
            count += 1
            if count == limit:
                return self.get_consumer_usage(
                    servers=servers,
                    marker=servers[-1]['id']
                )

        return servers

    def get_compute_limits(self, project_id, interface='internal'):
        """Return compute resource limits for a project.

        :param project_id: ID of a given project to lookup.
        :type project_id: str || uuid
        :param interface: Interface name, normally [internal, public, admin].
        :type interface: str
        :returns: dict
        """
        url = self.conn.session.get_endpoint(
            interface=interface,
            service_type='compute'
        )
        quota_data = self.conn.session.get(
            url + '/os-quota-sets/' + project_id
        )
        return quota_data.json()

    def get_projects(self):
        """Retrieve a list of projects.

        :returns: list
        """
        _consumers = list()
        with utils.LocalCache() as c:
            for project in self.conn.identity.projects():
                _consumers.append(project)
                cache_key = 'projects_' + str(project.id)
                c.set(
                    cache_key,
                    project.to_dict(),
                    expire=43200,
                    tag='projects'
                )
        return _consumers

    def get_project(self, project_id):
        """Retrieve project data.

        :param project_id: ID of a given project to lookup.
        :type project_id: str || uuid
        :returns: dict
        """
        project = None
        cache_key = 'projects_{}'.format(project_id)
        with utils.LocalCache() as c:
            try:
                project = c.get(cache_key)
                if not project:
                    raise LookupError
            except LookupError:
                project_info = self.conn.identity.get_project(project_id)
                project = project_info.to_dict()
                c.set(cache_key, project, expire=43200, tag='projects')
            finally:
                return project

    def get_project_name(self, project_id):
        """Retrieve the name of a project."""
        return self.get_project(project_id=project_id)['name']

    def get_flavors(self):
        """Retrieve all of flavors.

        :returns: dict
        """
        flavors = dict()
        with utils.LocalCache() as c:
            for flavor in self.conn.compute.flavors():
                _flavor = flavor.to_dict()
                cache_key = 'flavor_' + str(flavor.id)
                c.set(
                    cache_key,
                    _flavor,
                    expire=43200,
                    tag='flavors'
                )
                entry = flavors[flavor.id] = dict()
                entry.update(_flavor)
        return flavors

    def get_flavor(self, flavor_id):
        """Retrieve a flavor.

        :param flavor_id: ID of a given flavor to lookup.
        :type flavor_id: int || str
        :returns: dict
        """
        flavor = None
        cache_key = 'flavor_{}'.format(flavor_id)
        with utils.LocalCache() as c:
            try:
                flavor = c.get(cache_key)
                if not flavor:
                    raise LookupError
            except LookupError:
                flavor_info = self.conn.compute.get_flavor(flavor_id)
                flavor = flavor_info.to_dict()
                c.set(cache_key, flavor, expire=43200, tag='flavors')
            finally:
                return flavor

    def get_flavor_name(self, flavor_id):
        """Retrieve the name of a flavor.

        :param flavor_id: ID of a given flavor to lookup.
        :type flavor_id: int || str
        :returns: str
        """
        return self.get_flavor(flavor_id=flavor_id)['name']
