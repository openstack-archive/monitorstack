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
"""Common code for utils."""

import os
import shelve
import sys
import tempfile

# Lower import to support conditional configuration parser
try:
    if sys.version_info > (3, 2, 0):
        import configparser as ConfigParser
    else:
        import ConfigParser
except ImportError:
        raise SystemExit('No configparser module was found.')


def is_int(value):
    """Check if a variable is an integer."""
    for v_type in [int, float]:
        try:
            value = v_type(value)
        except ValueError:
            pass  # v was not a int, float, or long
        else:
            return value
    else:
        return value


class LocalCache(object):
    """Context Manager for opening and closing access to the DBM."""

    def __init__(self):
        """Initialization method for class."""
        """Set the Path to the DBM to create/Open."""

        self.db_cache = os.path.join(
            tempfile.gettempdir(),
            'monitorstack.openstack.dbm'
        )

    def __enter__(self):
        """Open the DBM in r/w mode.

        :return: Open DBM
        """
        return self.open_shelve

    def __exit__(self, type, value, traceback):
        """Close DBM Connection."""
        self.close_shelve()

    def _open_shelve(self):
        return shelve.open(self.db_cache)

    @property
    def open_shelve(self):
        """Open shelved data."""
        return self._open_shelve()

    def close_shelve(self):
        """Close shelved data."""
        self.open_shelve.close()


def read_config(config_file):
    """Read an OpenStack configuration."""
    cfg = os.path.abspath(os.path.expanduser(config_file))
    if not os.path.isfile(cfg):
        raise IOError('Config file "{}" was not found'.format(cfg))

    parser = ConfigParser.ConfigParser()
    parser.optionxform = str
    parser.read([cfg])
    args = dict()
    defaults = dict([(k, v) for k, v in parser.items(section='DEFAULT')])
    for section in parser.sections():
        if section == 'DEFAULT':
            continue

        sec = args[section] = defaults
        for key, value in parser.items(section):
            sec[key] = is_int(value=value)

    return args
