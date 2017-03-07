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
"""Output methods."""
import json
import time

import click


def current_time():
    """Return the current time in nanoseconds."""
    return int(time.time() * 1000000000)


def write_json(result):
    """Output in raw JSON format."""
    output = json.dumps(result, indent=2)
    click.echo(output)
    return True


def write_line(result):
    """Output in line format."""
    for key, value in result['variables'].items():
        click.echo("{} {}".format(key, value))

    return True


def write_telegraf(result):
    """Output in telegraf format."""
    def line_format(sets, quote=False):
        store = list()
        for k, v in sets.items():
            k = k.replace(' ', '_')
            for v_type in [int, float]:
                try:
                    v = v_type(v)
                except ValueError:
                    pass  # v was not a int, float, or long
                else:
                    break
            if not isinstance(v, (int, float, bool)) and quote:
                store.append('{}="{}"'.format(k, v))
            else:
                store.append('{}={}'.format(k, v))
        return ','.join(store).rstrip(',')

    resultant = [result['measurement_name']]
    if 'meta' in result:
        resultant.append(line_format(sets=result['meta']))
    resultant.append(line_format(sets=result['variables'], quote=True))
    resultant.append(str(current_time()))
    click.echo(' '.join(resultant))

    return True
