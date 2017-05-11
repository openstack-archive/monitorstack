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

import mock
import unittest

from monitorstack.plugins.vg_check import check_volgrp


class VolumeGroupTestCases(unittest.TestCase):
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
        ret_code, total, free = check_volgrp("foo")
        assert ret_code == 5
        assert total == ""
        assert free == "Volume group foo not found"

if __name__ == '__main__':
    unittest.main()
