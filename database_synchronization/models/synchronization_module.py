# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import _, api, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SynchronizationModule(models.TransientModel):
    _name = "synchronization.module"
    _inherit = ["synchronization.mixin"]
    _description = "Odoo Module Synchronisation"

    @api.model
    def _get_ignored_installed_modules(self):
        return [
            "database_synchronization",
        ]

    @api.model
    def _synchronize_module_installed(self):
        QueueJob = self.env["queue.job"]
        IrModuleModule = self.env["ir.module.module"]

        # Do not execute the cron if they are pending job
        pending_jobs = QueueJob.search(
            [
                ("channel", "=", "root.database_synchronization_install_module"),
                ("state", "!=", "done"),
            ]
        )
        if pending_jobs:
            _logger.info(
                "Ignoring run of _synchronize_module_installed, because some jobs"
                " are not finished."
            )
            return

        # Get modules installed in the external instance
        external_odoo = self._get_external_odoo()
        external_installed_module_names = [
            x["name"]
            for x in external_odoo.env["ir.module.module"].search_read(
                [("state", "=", "installed")],
                ["name"],
            )
        ]

        # Enqueue module for each module installed
        # in the external instance and not installed in the local one
        for module_name in external_installed_module_names:
            local_module = IrModuleModule.search([("name", "=", module_name)])
            if not local_module:
                raise UserError(_("Module '%s' not found locally" % module_name))
            else:
                if local_module.state == "uninstalled":
                    _logger.info(
                        "Enqueue module in installation list %s ..." % module_name
                    )
                    local_module.with_delay()._database_synchronization_install_module()

        # Check if all the modules are correctly installed
        local_only_installed_modules = IrModuleModule.search(
            [
                ("state", "=", "installed"),
                ("name", "not in", external_installed_module_names),
                ("name", "not in", self._get_ignored_installed_modules()),
            ]
        )
        if local_only_installed_modules:
            _logger.error(
                "You have some module to uninstall manually:\n"
                " - %s" % ("\n- ".join([x.name for x in local_only_installed_modules]))
            )
