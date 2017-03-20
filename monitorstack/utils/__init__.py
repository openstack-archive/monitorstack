# Copyright 2017, Kevin Carter <kevin@cloudnull.com>
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
"""Common code for utils."""

import functools
import os
import sys
import time
import traceback

try:
    if sys.version_info > (3, 2, 0):  # pragma: no cover
        import configparser as ConfigParser
    else:  # pragma: no cover
        import ConfigParser
except ImportError:  # pragma: no cover
        raise SystemExit('No configparser module was found.')

import diskcache


def retry(ExceptionToCheck, tries=3, delay=1, backoff=1):  # noqa
    """Retry calling the decorated function using an exponential backoff.

    Attributes to sources of inspiration:
      http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
      http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param ExceptionToCheck: the exception to check. may be a tuple of
                             exceptions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
                    each retry
    :type backoff: int
    """
    def deco_retry(f):
        @functools.wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck:
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)
        return f_retry  # true decorator
    return deco_retry


def is_int(value):
    """Check if a variable is an integer.

    :param value: parameter to evaluate and return
    :type value: str || int || float
    :returns: str || int || float
    """
    for v_type in [int, float]:
        try:
            value = v_type(value)
        except ValueError:
            pass  # v was not a int, float, or long
        else:
            return value
    else:
        return value


class LocalCache(object):
    """Context Manager for opening and closing access to the cache objects."""

    def __init__(self, cache_path=None):
        """Set the Path cache object.

        :param cache_file: File path to store cache
        :type cache_file: str
        """
        # If a cache file is provided use it otherwise store one in
        #  the user home folder as a hidden folder.
        self.cache_path = cache_path
        if not self.cache_path:
            self.cache_path = os.path.join(
                os.path.expanduser('~'),
                '.cache/monitorstack.cache'
            )
        elif not self.cache_path.endswith('cache'):
            self.cache_path = '{}.cache'.format(self.cache_path)

        if not os.path.isdir(self.cache_path):
            os.makedirs(self.cache_path)

    def __enter__(self):
        """Open the cache object.

        :returns: object
        """
        return self.open_cache

    def __exit__(self, *args, **kwargs):
        """Close cache object."""
        self.lc_close()

    @property
    @retry(ExceptionToCheck=Exception)
    def open_cache(self):
        """Return open caching opbject.

        :returns: object
        """
        return diskcache.Cache(directory=self.cache_path)

    def lc_open(self):
        """Open shelved data.

        :param cache_file: File path to store cache
        :type cache_file: str
        :returns: object
        """
        return self.open_cache

    def lc_close(self):
        """Close shelved data."""
        self.open_cache.close()


def read_config(config_file):
    """Read an OpenStack configuration.

    :param config_file: path to configuration file.
    :type config_file: str
    """
    cfg = os.path.abspath(os.path.expanduser(config_file))
    if not os.path.isfile(cfg):
        raise IOError('Config file "{}" was not found'.format(cfg))

    parser = ConfigParser.ConfigParser()
    parser.optionxform = str
    parser.read([cfg])
    args = dict()
    defaults = dict([(k, v) for k, v in parser.items(section='DEFAULT')])
    for section in parser.sections():
        sec = args[section] = defaults
        for key, value in parser.items(section):
            sec[key] = is_int(value=value)

    return args


def log_exception(exp):
    """Return log entries.

    :param exp: Exception object or name.
    :type exp: str || object
    :return: str
    """
    _trace = [i.strip() for i in str(traceback.format_exc()).splitlines()]
    trace = ' -> '.join(_trace)
    _exception = [i.strip() for i in str(exp).splitlines()]
    exception = ' -> '.join(_exception)
    return 'Exception [ %s ]: Trace: [ %s ]' % (exception, trace)
