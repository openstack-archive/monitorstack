# Copyright 2017, Michael Rice <michael@michaelrice.org>
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

import platform

import click

from monitorstack import utils
from monitorstack.cli import pass_context
from monitorstack.utils.cli import run_command

DOC = """Check a given volume group"""
COMMAND_NAME = 'vg_check'


@click.command(COMMAND_NAME, short_help=DOC)
@click.option('--volume_group', nargs=1, type=str, required=True)
@pass_context
def cli(ctx, volume_group):
    """
    Given volume group name get the total size and free space

    :param ctx: Click context
    :param volume_group: Name of volume group
    :type volume_group: str
    :return:
    """
    exit_code, total_size, free = check_volgrp(volume_group)
    output = {
        'exit_code': exit_code,
        'measurement_name': COMMAND_NAME,
        'meta': {
            'platform': platform.platform(),
        }
    }
    if exit_code == 0:
        output['message'] = '{} check for volume group {} is ok'.format(
            COMMAND_NAME, volume_group)
        output['variables'] = {
            'vg_{}_total_size_M'.format(volume_group): total_size,
            'vg_{}_free_M'.format(volume_group): free,
            'vg_{}_used_M'.format(volume_group): total_size - free
        }
    if exit_code != 0:
        # if exit_code is not 0 then 'free' actually has our error output.
        # and with py3 it is bytes so we convert to str first.
        output['message'] = '{} for {} failed -- {}'.format(
            COMMAND_NAME, volume_group, utils.log_exception(str(free))
        )
    return output


def check_volgrp(name):
    command = ('vgs {} --noheadings --units M '
               '--nosuffix -o vg_size,vg_free'.format(name))
    retcode, output, err = run_command(command)
    if retcode != 0:
        return retcode, output, err
    totalsize, free = [int(float(x)) for x in output.split()]
    return retcode, totalsize, free
