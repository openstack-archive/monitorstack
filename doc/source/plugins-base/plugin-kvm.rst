``kvm`` - get details from running KVM instances
================================================

The KVM plugin connects to libvirt and retrieves details about KVM instances on
the system. It returns basic information, including:

* number of instances on the host (``kvm_vms``)
* total number of virtual CPUs that libvirt can use (``kvm_total_vcpus``)
* the total number of virtual CPUs scheduled (``kvm_scheduled_vcpus``)

Usage
-----

This plugin takes no arguments.

Example
-------

Run the plugin:

.. code-block:: console

    $ monitorstack kvm

Example output in JSON format:

.. code-block:: json

    {
      "variables": {
        "kvm_vms": 1,
        "kvm_scheduled_vcpus": 2,
        "kvm_total_vcpus": 4
      },
      "meta": {
        "kvm_host_id": 2046744907101423228
      },
      "message": "kvm is ok",
      "exit_code": 0,
      "measurement_name": "kvm"
    }
