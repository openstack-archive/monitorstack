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

import unittest

import mock

from monitorstack.plugins import vg_check

import tests.unit  # Import the test base module


class VolumeGroupTestCases(unittest.TestCase):

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

    @mock.patch("monitorstack.utils.cli.subprocess")
    def test_check_volgrp_returns_with_vg_not_found(self, mock_path):
        """
        When the volume group is not found an exit status code of 5 is
        returned by the system. When a non 0 is returned the expected
        result from this call is is an error message with a blank total
        """
        mock_path.Popen.return_value.returncode = 5
        mock_path.Popen.return_value.communicate.return_value = \
            ("", "Volume group foo not found")
        ret_code, total, free = vg_check.check_volgrp("foo")
        assert ret_code == 5
        assert total == ""
        assert free == "Volume group foo not found"


class TestVolumeGroup(object):
    def test_cli_would_exec_command(self, monkeypatch):
        def mock_get_vgs(name):
            """Mock the check_volgrp() method."""
            return 0, 100, 99

        monkeypatch.setattr(
            vg_check,
            'check_volgrp',
            mock_get_vgs
        )

        result = tests.runner(
            'vg_check',
            extra_args=['--volume_group', 'test']
        )
        variables = result['variables']
        assert 'vg_test_used_M' in variables
        assert variables['vg_test_used_M'] == 1
        assert 'vg_test_free_M' in variables
        assert variables['vg_test_free_M'] == 99
        assert 'vg_test_total_size_M' in variables
        assert variables['vg_test_total_size_M'] == 100
