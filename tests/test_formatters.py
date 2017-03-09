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
"""Tests the output methods."""
import json

from monitorstack.common import formatters

SAMPLE_RESULT = {
    'exit_code': 0,
    'message': 'uptime is ok',
    'measurement_name': 'system_uptime',
    'meta': {
        'platform': 'example_platform',
    },
    'variables': {
        'uptime': '29587.75'
    }
}

SAMPLE_RESULT_NO_META = {
    'exit_code': 0,
    'message': 'uptime is ok',
    'measurement_name': 'system_uptime',
    'variables': {
        'uptime': '29587.75'
    }
}

SAMPLE_RESULT_NO_META_WITH_FLOAT = {
    'exit_code': 0,
    'message': 'uptime is ok',
    'measurement_name': 'system_uptime',
    'variables': {
        'uptime': float(29587.75)
    }
}


class TestFormatters(object):
    """Tests for the base cli module."""

    def test_current_time(self):
        """Test current_time()."""
        result = formatters._current_time()
        assert isinstance(result, int)
        assert result > 0

    def test_write_json(self, capsys):
        """Test write_json() module."""
        formatters.write_json(SAMPLE_RESULT)
        out, err = capsys.readouterr()
        result_json = json.loads(out)
        assert isinstance(result_json, dict)
        assert result_json['measurement_name'] == \
            SAMPLE_RESULT['measurement_name']

    def test_write_line(self, capsys):
        """Test write_line() module."""
        formatters.write_line(SAMPLE_RESULT)
        out, err = capsys.readouterr()
        assert out == "uptime {}\n".format(
            SAMPLE_RESULT['variables']['uptime']
        )

    def test_write_telegraf(self, capsys):
        """Test write_telegraf() module."""
        formatters.write_telegraf(SAMPLE_RESULT)
        out, err = capsys.readouterr()
        assert out.startswith(SAMPLE_RESULT['measurement_name'])

    def test_write_telegraf_without_meta(self, capsys):
        """Test write_telegrat() module without meta in result."""
        formatters.write_telegraf(SAMPLE_RESULT_NO_META)
        out, err = capsys.readouterr()
        assert out.startswith(SAMPLE_RESULT['measurement_name'])

    def test_write_telegraf_line_format_with_float(self):
        """Test _telegraf_line_format() with float in meta."""
        sets = {
            'platform': 'example_platform',
            'othervar': float(3)
        }
        result = formatters._telegraf_line_format(sets=sets, quote=True)
        assert isinstance(result, str)
        assert 'othervar=3' in result
        assert 'platform="example_platform"' in result
