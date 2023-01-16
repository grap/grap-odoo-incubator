# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class IrAttachment(models.AbstractModel):
    _inherit = "ir.attachment"

    def _get_attachment_count_models(self):
        res = super()._get_attachment_count_models()
        res.append("account.invoice")
        return res
