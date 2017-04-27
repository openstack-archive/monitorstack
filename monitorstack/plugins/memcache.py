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
"""Get memcached stats."""
import click

from monitorstack import utils
from monitorstack.cli import pass_context

from pymemcache.client.base import Client

DOC = """Get memcached stats."""
COMMAND_NAME = 'memcache'


@click.command(COMMAND_NAME, short_help=DOC)
@click.option('--host', help='memcached host to query', default='127.0.0.1')
@click.option('--port', help='memcached server port', default=11211)
@pass_context
def cli(ctx, host, port):
    """Get memcached stats."""
    output = {
        'exit_code': 0,
        'message': 'memcached is ok',
        'measurement_name': 'memcache',
        'meta': {},
        'variables': {}
    }

    # Connect to memcache and retrieve our stats
    try:
        stats = get_memcached_stats(host, port)
        output['variables'] = stats
    except Exception as exp:
        output['exit_code'] = 1
        output['message'] = '{} failed -- {}'.format(
            COMMAND_NAME,
            utils.log_exception(exp=exp)
        )

    return output


def get_memcached_stats(host, port):
    """Connect to memcache server for stats."""
    conn = Client((host, port))
    return conn.stats()
