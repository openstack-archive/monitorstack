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
"""Get system uptime."""
import os
import platform

import click

from monitorstack.cli import pass_context

import psutil

DOC = """Check if a process is running."""
COMMAND_NAME = 'process'


@click.command(COMMAND_NAME, short_help=DOC)
@click.argument('process_name', nargs=1, type=str, required=True)
@pass_context
def cli(ctx, process_name):
    """Check if a process is running."""
    setattr(cli, '__doc__', DOC)

    output = {
        'exit_code': 0,
        'message': 'process check is ok',
        'measurement_name': 'process',
        'meta': {
            'platform': platform.platform(),
        },
        'variables': {}
    }

    if check_process(process_name):
        output['variables'] = {process_name: 1}
    else:
        output['exit_code'] = 1
        output['message'] = '{} failed -- Process {} not found'.format(
            COMMAND_NAME,
            process_name
        )
        output['variables'] = {process_name: 0}

    return output


def check_process(process_name):
    """Check if a process is in the list of cmdlines."""
    matches = [x for x in get_cmdlines() if process_name in x]
    return True if len(matches) > 0 else False


def get_cmdlines():
    """Retrieve the cmdline of each process running on the system."""
    processes = []

    # Get our current PID as well as the parent so we can exclude them.
    current_pid = os.getpid()
    parent_pid = os.getppid()

    for proc in psutil.process_iter():
        try:
            if proc.pid not in [current_pid, parent_pid]:
                processes.append(' '.join(proc.cmdline()))
        except psutil.NoSuchProcess:
            pass

    return processes
