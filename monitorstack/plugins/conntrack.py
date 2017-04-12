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
"""Retrieve current/max connection tracking counts."""
import click

from monitorstack.cli import pass_context
from monitorstack.utils import read_file

DOC = """Get current maximum conntrack table sizes."""
COMMAND_NAME = 'conntrack'


@click.command(COMMAND_NAME, short_help=DOC)
@pass_context
def cli(ctx):
    """Get current maximum conntrack table sizes."""
    setattr(cli, '__doc__', DOC)

    output = {
        'exit_code': 0,
        'message': 'conntrack check is ok',
        'measurement_name': 'conntrack',
        'meta': {},
        'variables': {}
    }

    try:
        output['variables'] = get_conntrack_data()
    except IOError:
        output['exit_code'] = 1
        output['message'] = 'Unable to read conntrack data ' \
                            '-- is the kernel module loaded?'

    return output


def get_conntrack_data():
    """Read conntrack data from proc."""
    conntrack_count_path = '/proc/sys/net/netfilter/nf_conntrack_count'
    conntrack_max_path = '/proc/sys/net/netfilter/nf_conntrack_max'

    result = {
        'nf_conntrack_count': read_file(conntrack_count_path),
        'nf_conntrack_max': read_file(conntrack_max_path)
    }

    return result
