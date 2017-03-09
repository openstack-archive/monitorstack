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
    from openstack import exceptions as os_exp
except ImportError as e:
    raise SystemExit('OpenStack plugins require access to the OpenStackSDK.'
                     ' Please install "python-openstacksdk".'
                     ' ERROR: %s' % str(e))

from monitorstack import utils


class OpenStack(object):
    """Class for reusable OpenStack utility methods."""

    def __init__(self, os_auth_args):
        """Initialization method for class."""
        self.os_auth_args = os_auth_args

    @property
    def conn(self):
        """Return an OpenStackSDK connection."""
        return os_conn.Connection(**self.os_auth_args)

    def get_consumer_usage(self, servers=None, marker=None, limit=512):
        """Retrieve current usage by an OpenStack cloud consumer."""
        tenant_kwargs = {'details': True, 'all_tenants': True, 'limit': limit}
        if not servers:
            servers = list()

        if marker:
            tenant_kwargs['marker'] = marker

        count = 0
        for server in self.conn.compute.servers(**tenant_kwargs):
            servers.append(server)
            count += 1

        if count == limit:
            return self.get_consumer_usage(
                servers=servers,
                marker=servers[-1].id
            )

        return servers

    def get_compute_limits(self, project_id, interface='internal'):
        """Determine limits of compute resources."""
        url = self.conn.compute.session.get_endpoint(
            interface=interface,
            service_type='compute'
        )
        quota_data = self.conn.compute.session.get(
            url + '/os-quota-sets/' + project_id
        )
        return quota_data.json()

    def get_project_name(self, project_id):
        """Retrieve the name of a project."""
        with utils.LocalCache() as c:
            try:
                project_name = c.get(project_id)
                if not project_name:
                    project_info = self.conn.identity.get_project(project_id)
                    project_name = c[project_info.id] = project_info.name
            except os_exp.ResourceNotFound:
                return None
            else:
                return project_name

    def get_projects(self):
        """Retrieve a list of projects."""
        _consumers = list()
        with utils.LocalCache() as c:
            for project in self.conn.identity.projects():
                _consumers.append(project)
                c[project.id] = project.name
        return _consumers

    def get_flavors(self):
        """Retrieve a list of flavors."""
        flavor_cache = dict()
        for flavor in self.conn.compute.flavors():
            entry = flavor_cache[flavor['id']] = dict()
            entry.update(flavor)
        return flavor_cache
