The current implementation inherit the original res.config.settings model.

For that reason, that module gives **read** access to user
with 'reduced configuration' settings for the following model:

* `ir.cron`,
* `ir.config_parameter`,
* `ir.module.module`,
* `ir.actions.act_window`.
