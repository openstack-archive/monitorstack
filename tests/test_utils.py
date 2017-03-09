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
"""Tests for the uptime plugin."""

import os
import tempfile
import unittest

from monitorstack import utils


class TestUtils(unittest.TestCase):
    """Tests for the utilities."""

    def setUp(self):
        os_config_file = os.path.expanduser(
            os.path.abspath(__file__ + '/../../etc/openstack.ini')
        )
        self.config = utils.read_config(os_config_file)
        conf = utils.ConfigParser.RawConfigParser()
        conf.read([os_config_file])
        self.config_defaults = conf.defaults()

    def tearDown(self):
        local_cache = os.path.join(
            tempfile.gettempdir(),
            'monitorstack.openstack.dbm'
        )
        if os.path.exists(local_cache):
            os.remove(local_cache)

    def test_is_int_is_int(self):
        self.assertTrue(isinstance(utils.is_int(value=1), int))

    def test_is_int_is_int_str(self):
        self.assertTrue(isinstance(utils.is_int(value='1'), int))

    def test_is_int_is_not_int(self):
        self.assertTrue(isinstance(utils.is_int(value='a'), str))

    def test_read_config_not_found(self):
        self.assertRaises(
            IOError,
            utils.read_config,
            'not-a-file'
        )

    def test_read_config_found_dict_return(self):
        self.assertTrue(isinstance(self.config, dict))

    def test_read_config_found_defaults_in_sections(self):
        for k, v in self.config.items():
            for key in self.config_defaults.keys():
                self.assertTrue(key in v.keys())

    def test_local_cache(self):
        with utils.LocalCache() as c:
            c['test_key'] = True
            self.assertTrue('test_key' in c)
