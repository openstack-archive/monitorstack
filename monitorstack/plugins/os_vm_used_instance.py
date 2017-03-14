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
"""Get nova used instances."""

import collections

import click

from monitorstack import utils
from monitorstack.cli import pass_context
from monitorstack.utils import os_utils as ost


DOC = """Get nova used instances."""
COMMAND_NAME = 'os_vm_used_instance'


@click.command(COMMAND_NAME, short_help=DOC)
@click.option('--config-file',
              help='OpenStack configuration file',
              default='openstack.ini')
@pass_context
def cli(ctx, config_file):
    """Get nova used instances."""
    setattr(cli, '__doc__', DOC)

    output = {
        'measurement_name': COMMAND_NAME,
        'meta': {
            'used': 'instances'
        },
        'variables': {}
    }

    used_collection = collections.Counter()
    nova_config = utils.read_config(config_file=config_file)['nova']
    _ost = ost.OpenStack(os_auth_args=nova_config)
    try:
        variables = output['variables']
        for used in _ost.get_consumer_usage():
            project_name = _ost.get_project_name(project_id=used['project_id'])
            used_collection[project_name] += 1
            flavor_id = used['flavor']['id']
            output['meta'][flavor_id] = True
            flavor_name = _ost.get_flavor_name(flavor_id=flavor_id)
            output['meta'][flavor_name] = True
        variables.update(used_collection)
    except Exception as exp:
        output['exit_code'] = 1
        output['message'] = '{} failed -- {}'.format(
            COMMAND_NAME,
            utils.log_exception(exp=exp)
        )
    else:
        output['exit_code'] = 0
        output['message'] = '{} is ok'.format(COMMAND_NAME)
    finally:
        return output
