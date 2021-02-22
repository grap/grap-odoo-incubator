# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from urllib.error import URLError

import odoorpc

from odoo import _, api, models
from odoo.exceptions import UserError
from odoo.release import version_info

_logger = logging.getLogger(__name__)


class SynchronizationAbstract(models.AbstractModel):
    _name = "synchronization.mixin"
    _description = "Odoo Module Synchronisation"

    @api.model
    def _get_external_odoo(self):
        # Get configurations
        IrConfigParameter = self.env["ir.config_parameter"].sudo()
        port = int(IrConfigParameter.get_param("database_synchronization.port"))
        host = IrConfigParameter.get_param("database_synchronization.host")
        database = IrConfigParameter.get_param("database_synchronization.database")
        login = IrConfigParameter.get_param("database_synchronization.login")
        password = IrConfigParameter.get_param("database_synchronization.password")

        if port == 443:
            protocol = "jsonrpc+ssl"
        else:
            protocol = "jsonrpc"

        # Connect to external Odoo
        _logger.info("Connecting to host %s ..." % host)
        try:
            external_odoo = odoorpc.ODOO(host, protocol, port=port)
        except URLError:
            raise UserError(
                _(
                    "The settings to connect to the external Odoo"
                    " are incorrect.\n"
                    " - host: %s\n"
                    " - protocol: %s\n"
                    " - port: %s" % (host, protocol, port)
                )
            )
        _logger.info("Login into %s ..." % database)
        try:
            external_odoo.login(database, login, password)
        except odoorpc.error.RPCError:
            raise UserError(
                _(
                    "Unable to login. The database or the credentials"
                    " are incorrect:\n"
                    " - database: %s\n"
                    " - login: %s\n" % (database, login)
                )
            )

        # Check versions on both instance
        local_version = ".".join(str(v) for v in version_info[:2])
        external_version = external_odoo.version
        if local_version != external_version:
            raise UserError(
                _(
                    "You try to synchronize your local Odoo (Version %s)"
                    " with an external Odoo (Version %s)"
                    % (local_version, external_version)
                )
            )

        # Check if local modules are correctly installed
        local_incorrect_state_modules = self.env["ir.module.module"].search(
            [("state", "in", ["to upgrade", "to remove", "to install"])]
        )
        if local_incorrect_state_modules:
            raise UserError(
                _(
                    "Unable to synchronize modules, because some modules"
                    " are in a bad state locally\n"
                    "- %s "
                    % (
                        "\n- ".join(
                            [
                                "{} : {}".format(x.name, x.state)
                                for x in local_incorrect_state_modules
                            ]
                        )
                    )
                )
            )

        # check if external modules are correctly installed
        external_incorrect_state_modules = self._external_search_read(
            external_odoo,
            "ir.module.module",
            [("state", "in", ["to upgrade", "to remove", "to install"])],
            ["name", "state"],
        )
        if len(external_incorrect_state_modules):
            raise UserError(
                _(
                    "Unable to synchronize modules, because some modules"
                    " are in a bad state on external Odoo\n"
                    "- %s "
                    % (
                        "\n- ".join(
                            [
                                "{} : {}".format(x["name"], x["state"])
                                for x in external_incorrect_state_modules
                            ]
                        )
                    )
                )
            )

        return external_odoo

    @api.model
    def _external_search_browse(self, external_odoo, model_name, domain):
        ExternalModel = external_odoo.env[model_name]
        item_ids = ExternalModel.search(domain)
        return ExternalModel.browse(item_ids)

    @api.model
    def _external_search_read(self, external_odoo, model_name, domain, field_names):
        return external_odoo.env[model_name].search_read(domain, field_names)

    @api.model
    def _cron_synchronize_all(self):
        # synchronize module installed
        # if works, synchronize also data
        SynchronisationModule = self.env["synchronization.module"]
        SynchronisationModule._synchronize_module_installed()
