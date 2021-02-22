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
            # TODO, FIXME
            "intercompany_trade_account_invoice_supplier_ref_unique",
            # TODO, FIXME
            "intercompany_trade_purchase",
            # TODO, FIXME
            "mail_bot",
        ]

    @api.model
    def _synchronize_module_installed(self):
        external_odoo = self._get_external_odoo()
        IrModuleModule = self.env["ir.module.module"]

        external_installed_module_names = [
            x["name"]
            for x in self._external_search_read(
                external_odoo,
                "ir.module.module",
                [("state", "=", "installed")],
                ["name"],
            )
        ]

        installed_modules = []
        try:
            for module_name in external_installed_module_names:
                local_module = IrModuleModule.search([("name", "=", module_name)])
                if not local_module:
                    raise UserError(_("Module '%s' not found locally" % module_name))
                else:
                    if local_module.state != "installed":
                        _logger.info("installing module %s ..." % module_name)
                        # Avoid to install modules installed by dependency
                        local_module.button_immediate_install()
                        # the registry has changed
                        # reload self in the new registry
                        self.env.reset()
                        self = self.env()[self._name]
                    installed_modules.append(installed_modules)
        finally:
            # TODO send mail sending installed_modules
            pass

        local_only_installed_modules = IrModuleModule.search(
            [
                ("state", "=", "installed"),
                ("name", "not in", external_installed_module_names),
                ("name", "not in", self._get_ignored_installed_modules()),
            ]
        )
        if local_only_installed_modules:
            raise UserError(
                _(
                    "You have some module to uninstall manually:\n"
                    " - %s"
                    % ("\n- ".join([x.name for x in local_only_installed_modules]))
                )
            )
