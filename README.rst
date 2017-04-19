.. image:: doc/source/monitorstack-text.png
    :alt: monitorstack text

.. list-table::
    :stub-columns: 1

    * - Status:
      - | |travis| |codecov|

.. |travis| image:: https://img.shields.io/travis/major/monitorstack.svg
    :alt: Travis-CI Build Status
.. |codecov| image:: https://img.shields.io/codecov/c/github/major/monitorstack.svg
    :alt: Coverage Status

The monitorstack project provides a framework for writing monitoring plugins
that output data in various formats for different monitoring systems.
Developers can quickly add new monitoring plugins (along with tests) without
worrying about how to format the data.

For more details, including how to install/configure, a usage guide, and a
developer guide, review the `monitorstack documentation`_.

.. _monitorstack documentation: https://docs.openstack.org/developer/monitorstack/

Requirements
------------

Python 2.7 or higher is required for monitorstack.

Each commit is tested against Python 2.7, 3.3, 3.4, 3.5, and pypy.

License
-------

Apache 2.0

Community
---------

The monitorstack project is managed by the `OpenStack-Ansible community`_, but
it can be used with or without OpenStack-Ansible.

Contact information:

* ``#openstack-ansible`` on Freenode IRC

* `Launchpad Bugs`_

* Send email to ``openstack-dev@lists.openstack.org`` with
  ``[openstack-ansible][monitorstack]`` in the subject line.

.. _OpenStack-Ansible community: https://wiki.openstack.org/wiki/OpenStackAnsible
.. _Launchpad Bugs: https://bugs.launchpad.net/openstack-ansible
