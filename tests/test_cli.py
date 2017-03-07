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
"""Tests for the base cli module."""
import click

from monitorstack.cli import Context
from monitorstack.cli import MonitorStackCLI

import pytest


class TestCLI(object):
    """Tests for the base cli module."""

    def test_context_log(self, monkeypatch):
        """Test log() method of Context class."""
        def echofixer(msg, file):
            return msg
        monkeypatch.setattr(click, 'echo', echofixer)

        context = Context()
        result = context.log("TEST", 'test')
        assert callable(context.log)
        assert result is None

    def test_context_vlog_verbose_disabled(self, monkeypatch):
        """Test vlog() method of Context class."""
        def echofixer(msg, file):
            return msg
        monkeypatch.setattr(click, 'echo', echofixer)

        context = Context()
        context.verbose = False
        result = context.vlog("TEST", 'test')
        assert callable(context.vlog)
        assert result is None

    def test_context_vlog_verbose_enabled(self, monkeypatch):
        """Test vlog() method of Context class."""
        def echofixer(msg, file):
            return msg
        monkeypatch.setattr(click, 'echo', echofixer)

        context = Context()
        context.verbose = True
        result = context.vlog("TEST", 'test')
        assert callable(context.vlog)
        assert result is None

    def test_get_command_invalid(self):
        """Test MonitorStackCLI.get_command()."""
        ctx = Context()
        cli = MonitorStackCLI()
        with pytest.raises(SystemExit) as excinfo:
            cli.get_command(ctx, 'silly_rabbit_trix_are_for_kids')
        assert 'silly_rabbit_trix_are_for_kids' in str(excinfo.value)
        assert 'Not Found' in str(excinfo.value)

    def test_get_command_valid(self):
        """Test MonitorStackCLI.get_command()."""
        ctx = Context()
        cli = MonitorStackCLI()
        result = cli.get_command(ctx, 'uptime')
        assert isinstance(result, object)
        assert callable(result)

    def test_list_commands(self):
        """Test MonitorStackCLI.list_commands()."""
        ctx = Context()
        cli = MonitorStackCLI()
        result = cli.list_commands(ctx)
        assert isinstance(result, list)
        assert len(result) > 1
        assert 'uptime' in result
