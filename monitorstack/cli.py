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
import importlib
import os
import pkgutil
import sys

import click


context_settings = dict(auto_envvar_prefix='MonitorStack')


class Context(object):
    """Set up a context object that we can pass."""

    def __init__(self):
        """Initialize class."""
        self.verbose = False
        self.home = os.getcwd()

    def log(self, msg, *args):
        """Log a message to stderr."""
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Log a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)


pass_context = click.make_pass_decorator(Context, ensure=True)


class MonitorStackCLI(click.MultiCommand):
    """Create a complex command finder."""

    @property
    def cmd_folder(self):
        """Get the path to the plugin directory."""

        return os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                'plugins'
            )
        )

    def list_commands(self, ctx):
        """Get a list of all available commands."""

        rv = list()
        for _, pkg_name, _ in pkgutil.iter_modules([self.cmd_folder]):
            rv.append(pkg_name)
        else:
            return sorted(rv)

    def get_command(self, ctx, name):
        """Load a command and run it."""

        for _, pkg_name, _ in pkgutil.iter_modules([self.cmd_folder]):
            if pkg_name == name:
                mod = importlib.import_module(
                    'monitorstack.plugins.{}'.format(name)
                )
                return getattr(mod, 'cli')

        else:
            raise SystemExit('Module "{}" Not Found.'.format(name))


VALID_OUTPUT_FORMATS = [
    'json',
    'line',
    'telegraf'
]


@click.command(cls=MonitorStackCLI, context_settings=context_settings)
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

    module_name = 'monitorstack.common.formatters'
    method_name = 'write_{}'.format(output_format)
    output_formatter = getattr(
        importlib.import_module(module_name),
        method_name
    )
    output_formatter(result)


if __name__ == '__main__':
    topdir = os.path.normpath(
        os.path.join(
            os.path.abspath(
                sys.argv[0]
            ),
            os.pardir,
            os.pardir
        )
    )
    sys.path.insert(0, topdir)

    cli()
