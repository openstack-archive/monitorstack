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


def _current_time():
    """Return the current time in nanoseconds."""
    return int(time.time() * 1000000000)


def _get_value_types(value, measurement_type=None):
    """Return the value and the measurement type.

    This method will evaluate a given value and cast it to the
    appropriate type. If the parameter `measurement_type` is
    not provided the method will assign the type based on the
    key set in the types list.

    :param value: item to evaluate.
    :param measurement_type: name of the measurement
    """
    def _check_value(c_type, c_value):
        try:
            c_value = c_type(c_value)
        except ValueError:
            return False, c_value
        else:
            return True, c_value

    success = False
    if isinstance(value, str) and '.' in value:
        success, value = _check_value(
            c_type=float,
            c_value=value
        )

    elif isinstance(value, float):
        success = True

    if success:
        _measurement_type = 'float'
    else:
        _, value = _check_value(
            c_type=int,
            c_value=value
        )
        if isinstance(value, int):
            if value > 2147483647:
                _measurement_type = 'int64'
            else:
                _measurement_type = 'int32'
        else:
            _measurement_type = 'string'

    if not measurement_type:
        measurement_type = _measurement_type

    return value, measurement_type


def _telegraf_line_format(sets, quote=False):
    """Return a comma separated string."""
    store = list()
    for k, v in sets.items():
        k = k.replace(' ', '_')
        v, _ = _get_value_types(value=v)
        if not isinstance(v, (int, float, bool)) and quote:
            store.append('{}="{}"'.format(k, v))
        else:
            store.append('{}={}'.format(k, v))
    return ','.join(store).rstrip(',')


def write_telegraf(result):
    """Output in telegraf format."""
    resultant = [result['measurement_name']]
    if 'meta' in result:
        resultant.append(_telegraf_line_format(sets=result['meta']))
    resultant.append(
        _telegraf_line_format(
            sets=result['variables'],
            quote=True
        )
    )
    resultant.append(str(_current_time()))
    click.echo(' '.join(resultant))

    return True


def write_rax_maas(result):
    """Output in Rackspace Monitoring as a Service format."""
    status = ['status']
    if result['exit_code'] == 0:
        status.append('okay')
    else:
        status.append('error')

    status.append(result['message'])
    click.echo(' '.join(status))

    for key, value in result['variables'].items():
        value, measurement_type = _get_value_types(
            value=value,
            measurement_type=result.get('measurement_type')
        )
        metric = ['metric', key, measurement_type, str(value)]
        if 'measurement_units' in result:
            metric.append(result['measurement_units'])
        click.echo(' '.join(metric))

    return True
