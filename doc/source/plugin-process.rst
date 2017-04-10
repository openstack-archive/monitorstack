``process`` - monitor a running process
=======================================

The ``process`` plugin searches the list of running processes and checks
whether a particular process is running.

Usage
-----

The plugin takes only one argument: the name of the process to check. See the
examples below for more details.

Example
-------

In this example, the plugin searches the process list for the ``chronyd``
process:

.. code-block:: console

    $ monitorstack process chronyd

The default JSON output shows that the process was found:

.. code-block:: json

    {
      "variables": {
        "chronyd": 1
      },
      "message": "process check is ok",
      "meta": {
        "platform": "Linux"
      },
      "exit_code": 0,
      "measurement_name": "process"
    }

Here's another example where the plugin searches for ``nginx``. That process is
not running on this server:

.. code-block:: console

    $ monitorstack process nginx

This time, the process is not found:

.. code-block:: json

    {
      "variables": {
        "nginx": 0
      },
      "message": "process failed -- Process nginx not found",
      "meta": {
        "platform": "Linux-4.10.8-200.fc25.x86_64-x86_64-with-fedora-25-Twenty_Five"
      },
      "exit_code": 1,
      "measurement_name": "process"
    }
