#!/usr/bin/env python
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
"""Handle all shell commands/arguments/options."""
import json
import os
import sys


import click


CONTEXT_SETTINGS = dict(auto_envvar_prefix='MonitorStack')


class Context(object):
    """Set up a context object that we can pass."""

    def __init__(self):
        """Initialize class."""
        self.verbose = False
        self.home = os.getcwd()

    def log(self, msg, *args):
        """Log a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Log a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)


pass_context = click.make_pass_decorator(Context, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          'plugins'))


class MonitorStackCLI(click.MultiCommand):
    """Create a complex command finder."""

    def list_commands(self, ctx):
        """Get a list of all available commands."""
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and not filename.startswith('__'):
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        """Load a command and run it."""
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__('monitorstack.plugins.' + name,
                             None, None, ['cli'])
        except ImportError:
            return
        return mod.cli


VALID_OUTPUT_FORMATS = [
    'json',
    'line',
]


@click.command(cls=MonitorStackCLI, context_settings=CONTEXT_SETTINGS)
@click.option(
    '-f', '--format', 'output_format',
    type=click.Choice(VALID_OUTPUT_FORMATS),
    default='json',
    help="Output format (valid options: {}".format(
        ', '.join(VALID_OUTPUT_FORMATS)
    ),
)
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode.')
@pass_context
def cli(ctx, output_format, verbose):
    """A complex command line interface."""
    ctx.verbose = verbose
    pass


@cli.resultcallback(replace=True)
def process_result(result, output_format, verbose):
    """Render the output into the proper format."""
    if output_format == 'json':
        click.echo(json.dumps(result, indent=2))

    elif output_format == 'line':
        for key, value in result['variables'].items():
            click.echo("{} {}".format(key, value))

    elif output_format == 'csv':
        pass

if __name__ == '__main__':
    cli()
