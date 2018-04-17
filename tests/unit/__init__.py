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
"""This an __init__.py."""

import os

from monitorstack import utils


def read_config():
    """Load the test config file.

    :returns: dict
    """
    os_config_file = os.path.expanduser(
        os.path.abspath(
            os.path.dirname(__file__) + '/files/test-openstack.ini'
        )
    )
    return utils.read_config(os_config_file)


def fake_version_info(major, minor, serial):
    """Return tuple for fake python version info."""
    return major, minor, serial


class FakePopen(object):
    """Fake Shell Commands."""
    def __init__(self, return_code=0, *args, **kwargs):
        self.returncode = return_code

    @staticmethod
    def communicate():
        return 'stdout', 'stderr'
