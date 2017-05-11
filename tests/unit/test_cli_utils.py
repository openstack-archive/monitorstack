# Copyright 2018, Kevin Carter <kevin@cloudnull.com>
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
"""Tests for the cli utils plugin."""

import unittest

import mock

from monitorstack.utils import cli

import tests  # Import the test base module


class TestCliUtils(unittest.TestCase):
    """Tests for the utilities."""

    def setUp(self):
        """Setup the test."""
        # load the base class for these tests.
        self.communicate_patched = mock.patch(
            'monitorstack.utils.cli.subprocess.Popen'
        )
        self.communicate = self.communicate_patched.start()

    def tearDown(self):
        """Tear down the test."""
        self.communicate_patched.stop()

    def test_run_command_success(self):
        self.communicate.return_value = tests.unit.FakePopen()
        ret, out, err = cli.run_command(
            arg='test_command'
        )
        self.assertEqual(out, 'stdout')
        self.assertEqual(ret, 0)

    def test_run_command_fail(self):
        self.communicate.return_value = tests.unit.FakePopen(
            return_code=1
        )
        ret, out, err = cli.run_command(
            arg='test_command'
        )
        self.assertEqual(err, 'stderr')
        self.assertEqual(ret, 1)
