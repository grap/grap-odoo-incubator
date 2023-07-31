# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    purchase_order_ids = fields.Many2many(
        comodel_name="purchase.order",
        relation="mrp_production_purchase_order_rel",
        column1="mrp_production_id",
        column2="purchase_order_id",
    )

    purchase_order_qty = fields.Integer(
        string="Product Quantity", compute="_compute_purchase_order_qty"
    )

    @api.multi
    @api.depends("purchase_order_ids")
    def _compute_purchase_order_qty(self):
        for mrp_prod in self:
            mrp_prod.purchase_order_qty = len(mrp_prod.purchase_order_ids)

    @api.multi
    def _generate_moves(self):
        super(MrpProduction, self)._generate_moves()
        po_obj = self.env["purchase.order"]
        po_linked = po_obj.search([("origin", "ilike", "%" + self.name + "%")])
        self.purchase_order_ids = po_linked
        return True
