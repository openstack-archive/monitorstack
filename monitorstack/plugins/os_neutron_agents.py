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
"""Get the neutron agents and their status."""

import click

from monitorstack import utils
from monitorstack.cli import pass_context
from monitorstack.utils import os_utils as ost

DOC = """Get nova used cores."""
COMMAND_NAME = 'os_neutron_agents'


@click.command(COMMAND_NAME, short_help=DOC)
@click.option('--config-file',
              help='OpenStack configuration file',
              default='openstack.ini')
@pass_context
def cli(ctx, config_file):
    """Get neutron agents."""
    setattr(cli, '__doc__', DOC)

    output = {
        'measurement_name': COMMAND_NAME,
        'meta': {
            'agent: is_alive': 'Neutron service agent and if it is alive'
        },
        'variables': {}
    }

    #nova_config = utils.read_config(config_file=config_file)['nova']
    neutron_config = utils.read_config(config_file=config_file)['neutron']
    _ost = ost.OpenStack(os_auth_args=neutron_config)

    try:
        # Get neutron agents
        neutron_agents = _ost.conn.network.agents()
        variables = output['variables']
        agents = dict()
        for agent in neutron_agents:
            agents[agent.binary] = agent.is_alive
        variables.update(agents)
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
