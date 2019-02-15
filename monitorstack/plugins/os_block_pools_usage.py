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
"""Get block storage usage from the available pools."""

import click

from monitorstack import utils
from monitorstack.cli import pass_context


DOC = """Get block storage usage from the available pools."""
COMMAND_NAME = 'os_block_pools_usage'


@click.command(COMMAND_NAME, short_help=DOC)
@click.option('--config-file',
              help='MonitorStack configuration file',
              default='openstack.ini')
@pass_context
def cli(ctx, config_file):
    """Get nova cores quotas."""
    setattr(cli, '__doc__', DOC)

    # Lower level import because we only want to load this module
    # when this plugin is called.
    from monitorstack.utils import os_utils as ost

    output = {
        'measurement_name': COMMAND_NAME,
        'meta': {
            'block_pools': 'usage'
        },
        'variables': {}
    }
    os_config = utils.read_config(
        config_file=config_file,
        no_config_fatal=False
    )
    service_config = os_config.get('cinder')
    cloud_config = os_config.get('cloud')
    if service_config:
        interface = service_config.pop('interface', 'internal')
        _ost = ost.OpenStack(os_auth_args=service_config)
    else:
        interface = 'internal'
        _ost = ost.OpenStack(os_auth_args=cloud_config)

    try:
        variables = output['variables']
        for item in _ost.get_volume_pool_stats(interface=interface):
            cap = item['capabilities']
            total_capacity_gb = float(cap.get('total_capacity_gb', 0))
            free_capacity_gb = float(cap.get('free_capacity_gb', 0))
            percent_used = 100 * (free_capacity_gb / total_capacity_gb)
            pool_name = cap.get('pool_name')

            output['meta'][pool_name] = True

            free_metric = '{}_free_capacity_gb'.format(pool_name)
            variables[free_metric] = free_capacity_gb

            total_metric = '{}_total_capacity_gb'.format(pool_name)
            variables[total_metric] = total_capacity_gb

            percent_metric = '{}_percent_used'.format(pool_name)
            variables[percent_metric] = percent_used
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
