* Go to "Settings > Technical > Parameters > System parameters" and
  set information regarding the target Odoo instance, and the credencials,
  with the following keys :

1. ``database_synchronization.host`` : host of the target Odoo instance, without ``http://``. set only ``localhost`` or the ``myerp.mywebsite.tld``.

2. ``database_synchronization.port``: port the target Odoo instance. Typically ``8069`` for dev instance, or ``443`` for test or production instance.

3. ``database_synchronization.database``: name of the database.

4. ``database_synchronization.login`` and ``database_synchronization.password``: credential used for the authentication.

* This module depends on ``queue_job`` module that requires specific
  configuration to works properly. Make sure your config file is correctly set.
  See https://github.com/OCA/queue/tree/12.0/queue_job

You should update your ``odoo.cfg`` file to add a new channel named
``root.database_synchronization_install_module``:


.. code-block::

  [queue_job]
  channels = root:2,root.database_synchronization_install_module:1

Otherwise, you'll have a non blocking warning in your log, like this one.

.. code-block::

  WARNING ? odoo.addons.queue_job.jobrunner.channels: unknown channel root.database_synchronization_install_module, using root channel for job 23f6b872-1d2c-4003-bd38-a8486bbec664
