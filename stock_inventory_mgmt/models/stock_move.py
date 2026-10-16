# Part of Odoo CE V12. LGPL.

from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    inventory_id = fields.Many2one(
        comodel_name="stock.inventory", string="Inventory", readonly=True
    )

    # Rename core field which string is also 'Inventory', to avoid conflict
    is_inventory = fields.Boolean(string="Is Inventory")  # pylint: disable=attribute-string-redundant
