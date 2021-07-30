# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class IrModuleModule(models.Model):
    _inherit = "ir.module.module"

    # Custom Section
    @api.multi
    def _database_synchronization_install_module(self):
        self.ensure_one()
        if self.state != "uninstalled":
            return
        _logger.info("installing modules %s ..." % self.name)
        self.button_immediate_install()
