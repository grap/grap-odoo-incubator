# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (https://twitter.com/pondupont)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, models


class WizardStockInventoryMerge(models.TransientModel):
    _inherit = "wizard.stock.inventory.merge"

    # Compute Section
    # Force compute valuation when merging
    @api.multi
    def action_merge(self):
        action_data = super(WizardStockInventoryMerge, self).action_merge()
        self.env["stock.inventory"].browse(
            action_data["res_id"])._compute_valuation()
