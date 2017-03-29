Usage
=====

Run the ``monitorstack`` command without any arguments to review a list of
available commands and options:

.. code-block:: console

    $ monitorstack
    Usage: monitorstack [OPTIONS] COMMAND [ARGS]...

      A complex command line interface.

    Options:
      -f, --format [json|line|telegraf|rax-maas]
                                      Output format (valid options: json, line,
                                      telegraf, rax-maas
      -v, --verbose                   Enables verbose mode.
      --help                          Show this message and exit.

    Commands:
      kvm                    Get metrics from a KVM hypervisor.
      os_block_pools_totals  Get block storage totals from the available pools.
      os_block_pools_usage   Get block storage usage from the available pools.
      os_vm_quota_cores      Get nova cores quotas.
      os_vm_quota_instance   Get nova instance quotas.
      os_vm_quota_ram        Get nova ram quotas.
      os_vm_used_cores       Get nova used cores.
      os_vm_used_disk        Get nova used disk.
      os_vm_used_instance    Get nova used instances.
      os_vm_used_ram         Get nova used ram.
      process                Check if a process is running.
      uptime                 Get system uptime.

Executing simple plugins
------------------------

The most simple plugins do not require any arguments. For example, to get the
system uptime, use the ``uptime`` command to run the corresponding ``uptime``
plugin:

.. code-block:: console

    $ monitorstack uptime
    {
      "variables": {
        "uptime": "22613.26"
      },
      "message": "uptime is ok",
      "meta": {
        "platform": "Linux-4.10.5-200.fc25.x86_64-x86_64-with-fedora-25-Twenty_Five"
      },
      "exit_code": 0,
      "measurement_name": "system_uptime"
    }

The default output type is json, but this is configured with the ``-f,
--format`` option. Here is another example that outputs data in telegraf
format:

.. code-block:: console

    $ monitorstack -f telegraf uptime
    system_uptime platform=Linux-4.10.5-200.fc25.x86_64-x86_64-with-fedora-25-Twenty_Five uptime=23005.05 1490819061833774080

Executing plugins with arguments
--------------------------------

The ``process`` plugin searches the current list of running processes to find
any that match a string provided as an argument. Execute the plugin without any
arguments for some usage help:

.. code-block:: console

    $ monitorstack process
    Usage: monitorstack process [OPTIONS] PROCESS_NAME

    Error: Missing argument "process_name".

In this example, we want to ensure that the ``chronyd`` process is running:

.. code-block:: console

  $ monitorstack process chronyd
  {
    "variables": {
      "chronyd": 1
    },
    "message": "process check is ok",
    "meta": {
      "platform": "Linux-4.10.5-200.fc25.x86_64-x86_64-with-fedora-25-Twenty_Five"
    },
    "exit_code": 0,
    "measurement_name": "process"
  }

We can also see a negative result if we check for a non-existent process called
``processdoesntexist``:

.. code-block:: console

  $ monitorstack process processdoesntexist
  {
    "variables": {
      "processdoesntexist": 0
    },
    "message": "process failed -- Process processdoesntexist not found",
    "meta": {
      "platform": "Linux-4.10.5-200.fc25.x86_64-x86_64-with-fedora-25-Twenty_Five"
    },
    "exit_code": 1,
    "measurement_name": "process"
  }

Executing plugins with configuration files
------------------------------------------

Many of the OpenStack plugins require a configuration file that specifies the
URLs of OpenStack endpoints as well as valid credentials for those endpoints.
For more information on the format of these configuration files, refer to the
documentation on `configuration <configure.html>`_.

Here is an example with the ``os_vm_quota_ram`` plugin with a configuration
file in ``/home/user/openstack.ini``:

.. code-block:: console

  $ monitorstack os_vm_quota_ram --config-file=/etc/openstack/openstack.ini
