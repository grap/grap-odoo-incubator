# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class BaseImportImport(models.TransientModel):
    _inherit = "base_import.import"

    def execute_import(self, fields, columns, options, dryrun=False):
        self.ensure_one()
        return super(
            BaseImportImport, self.with_context(imported_model=self.res_model)
        ).execute_import(fields, columns, options, dryrun=dryrun)
