``uptime`` - get system uptime
==============================

The uptime plugin returns the number of seconds since the server was powered
on.

Usage
-----

This plugin takes no arguments.

Example
-------

Run the plugin:

.. code-block:: console

    $ monitorstack uptime

Example output in JSON format:

.. code-block:: json

    {
      "variables": {
        "uptime": "18570.18"
      },
      "message": "uptime is ok",
      "meta": {
        "platform": "Linux-4.10.8-200.fc25.x86_64-x86_64-with-fedora-25-Twenty_Five"
      },
      "exit_code": 0,
      "measurement_name": "system_uptime"
    }
