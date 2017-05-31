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
"""Tests for the utils."""

import os
import tempfile
import unittest

from monitorstack import utils


class TestUtils(unittest.TestCase):
    """Tests for the utilities."""

    def setUp(self):
        """Initial setup for class."""
        os_config_file = os.path.expanduser(
            os.path.abspath(
                os.path.dirname(__file__) + '/files/test-openstack.ini'
            )
        )
        self.config = utils.read_config(os_config_file)
        conf = utils.ConfigParser.RawConfigParser()
        conf.read([os_config_file])
        self.config_defaults = conf.defaults()

        self.g_testfile = os.path.join(
            os.path.expanduser('~'),
            '.cache/monitorstack.cache'
        )
        self.t_testfile = tempfile.mkdtemp()

    def tearDown(self):
        """Destroy the local cache."""
        for f in [self.g_testfile, self.t_testfile]:
            cache_db = os.path.join(f, 'cache.db')
            if os.path.exists(cache_db):
                os.remove(cache_db)

    def test_is_int_is_int(self):  # noqa
        self.assertTrue(isinstance(utils.is_int(value=1), int))

    def test_is_int_is_int_str(self):  # noqa
        self.assertTrue(isinstance(utils.is_int(value='1'), int))

    def test_is_int_is_not_int(self):  # noqa
        self.assertTrue(isinstance(utils.is_int(value='a'), str))

    def test_read_config_not_found(self):  # noqa
        self.assertRaises(
            IOError,
            utils.read_config,
            'not-a-file'
        )

    def test_read_config_found_dict_return(self):  # noqa
        self.assertTrue(isinstance(self.config, dict))

    def test_read_config_found_defaults_in_sections(self):
        """Read config defaults from each section."""
        for k, v in self.config.items():
            for key in self.config_defaults.keys():
                self.assertTrue(key in v.keys())

    def test_local_cache_no_file(self):
        """Test local cache."""
        with utils.LocalCache() as c:
            c['test_key1'] = True
            self.assertTrue('test_key1' in c)

    def test_local_cache_file(self):
        """Test local cache."""
        with utils.LocalCache(cache_path=self.t_testfile) as c:
            c['test_key2'] = True
            self.assertTrue('test_key2' in c)

    def test_local_cache_no_file_no_context(self):
        """Test local cache without a context manager."""
        c = utils.LocalCache()
        cache = c.lc_open()
        cache['test_key3'] = True
        try:
            self.assertTrue('test_key3' in cache)
        finally:
            c.lc_close()

        with utils.LocalCache() as c:
            self.assertTrue('test_key3' in c)

    def test_local_cache_file_no_context(self):
        """Test local cache without a context manager."""
        c = utils.LocalCache(cache_path=self.t_testfile)
        cache = c.lc_open()
        cache['test_key4'] = True
        try:
            self.assertTrue('test_key4' in cache)
        finally:
            c.lc_close()

        with utils.LocalCache(cache_path=self.t_testfile) as c:
            self.assertTrue('test_key4' in c)

    def test_local_cache_no_load(self):
        """Test local cache without loading anything."""
        c = utils.LocalCache(cache_path=self.t_testfile)
        c.lc_close()

    def test_local_cache_named_ext(self):
        """Test local cache without loading anything with a named extension."""
        utils.LocalCache(cache_path='{}.cache'.format(self.t_testfile))

    def test_retry_failure(self):
        """Test retry decorator for failure."""
        @utils.retry(ExceptionToCheck=BaseException, tries=3, backoff=0,
                     delay=1)
        def _failed():
            """Raise failure exception after retry."""
            raise BaseException

        self.assertRaises(BaseException, _failed)

    def test_retry_success(self):
        """Test retry decorator for success."""
        @utils.retry(ExceptionToCheck=BaseException, tries=3, backoff=0,
                     delay=1)
        def _success():
            """Return True after retry."""
            self.count += 1
            if self.count == 3:
                return True
            else:
                raise BaseException

        self.count = 0
        self.assertEquals(_success(), True)

    def test_log_exception(self):
        """Test traceback formatter for exception messages."""
        try:
            raise Exception('test-exception')
        except Exception as exp:
            message = utils.log_exception(exp=exp)

        self.assertTrue('Exception' in message)
        self.assertTrue('Trace' in message)
