When synchronizing module installation for the first time, it
can take a big while. during the installation, cron will be fired, but
due to the inconsistency of the registry, it will fail,
for exemple, once ``queue_job`` is installed:

``
Traceback (most recent call last):
  File "/src_code/odoo/odoo/addons/base/models/ir_cron.py", line 109, in _callback
    self.env['ir.actions.server'].browse(server_action_id).run()
  File "/src_code/odoo/odoo/addons/base/models/ir_actions.py", line 538, in run
    eval_context = self._get_eval_context(action)
  File "/src_code/odoo/addons/mail/models/ir_actions.py", line 150, in _get_eval_context
    eval_context = super(ServerActions, self)._get_eval_context(action=action)
  File "/src_code/odoo/odoo/addons/base/models/ir_actions.py", line 494, in _get_eval_context
    model = self.env[model_name]
  File "/src_code/odoo/odoo/api.py", line 831, in __getitem__
    return self.registry[model_name]._browse((), self)
  File "/src_code/odoo/odoo/modules/registry.py", line 177, in __getitem__
    return self.models[model_name]
KeyError: 'queue.job'
``

That is a non blocking errors, and all will be ok, once the installation
of all modules has been done.
