When synchronizing module installation for the first time, it
can take a big while. During the installation, some task could be failed.
In that case, simply restart the jobs.

.. code-block::

  File "/home/sylvain/grap_dev/grap-odoo-env-12.0/src/odoo/odoo/addons/base/models/ir_module.py", line 446, in button_immediate_install
    return self._button_immediate_function(type(self).button_install)
  File "/home/sylvain/grap_dev/grap-odoo-env-12.0/src/odoo/odoo/addons/base/models/ir_module.py", line 556, in _button_immediate_function
    raise UserError(_("The server is busy right now, module operations are not possible at"
  odoo.exceptions.UserError: ('The server is busy right now, module operations are not possible at this time, please try again later.', '')
