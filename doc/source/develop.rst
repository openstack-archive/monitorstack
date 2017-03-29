===============
Developer guide
===============

One of the design goals of monitorstack is to make it easy to develop new
monitoring plugins.

Writing plugins
---------------

Start by adding a new python script in the ``plugins`` directory. The plugin
will inherit the same name as the file. For example, creating a plugin file
called ``my_plugin.py`` will create a new plugin called ``my_plugin``.

Use the ``uptime`` plugin as a guide for developing new plugins:

.. literalinclude:: ../../monitorstack/plugins/uptime.py

Every plugin will have a ``cli()`` method that is the equivalent of
``___main___`` in other Python scripts.

Testing plugins
---------------

Add tests in the ``tests`` directory and follow the ``uptime`` example. Here
are the contents of ``tests/test_plugin_uptime.py`` as an example:

.. literalinclude:: ../../tests/test_plugin_uptime.py

Running tests
-------------

There are two main sets of tests: pep8/flake8 tests and unit tests:

.. code-block:: console

    # PEP8 and flake8 checks
    tox -e linters

    # Unit tests
    tox -e functional
