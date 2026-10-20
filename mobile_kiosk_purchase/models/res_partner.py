# Copyright (C) 2026 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def mk_purchase_res_partner_select(self):
        self.ensure_one()
        return self.env["mobile.kiosk.purchase"]._hook_after_res_partner_selection(self)
