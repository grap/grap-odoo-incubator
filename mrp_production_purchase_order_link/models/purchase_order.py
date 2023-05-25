# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    mrp_production_ids = fields.Many2many(
        comodel_name="mrp.production",
        relation="mrp_production_purchase_order_rel",
        column1="purchase_order_id",
        column2="mrp_production_id",
    )

    mrp_prod_qty = fields.Integer(
        string="Manufacturing Orders Quantity", compute="_compute_mrp_prod_qty"
    )

    @api.multi
    @api.depends("mrp_production_ids")
    def _compute_mrp_prod_qty(self):
        for po in self:
            po.mrp_prod_qty = len(po.mrp_production_ids)
