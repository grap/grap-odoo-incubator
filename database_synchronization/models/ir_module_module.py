# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import api, models

from odoo.addons.queue_job.job import job

_logger = logging.getLogger(__name__)


class IrModuleModule(models.Model):
    _inherit = "ir.module.module"

    # Custom Section
    @api.multi
    @job(default_channel="root.database_synchronization_install_module")
    def _database_synchronization_install_module(self):
        for module in self:
            if module.state != "uninstalled":
                continue
            _logger.info("installing modules %s ..." % module.name)
            module.button_immediate_install()
            # # the registry has changed
            # # reload self in the new registry
            # self.env.reset()
            # self = self.env()[self._name]
