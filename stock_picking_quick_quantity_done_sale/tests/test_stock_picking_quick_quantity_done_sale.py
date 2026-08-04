# @author Quentin DUPONT <quentin.dupont@grap.coop>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import Command
from odoo.tests.common import TransactionCase


class TestStockPickingQuickQuantityDoneSale(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        partner = cls.env.ref("base.res_partner_2")
        cls.product_id_1 = cls.env.ref("product.product_product_8")
        cls.product_id_2 = cls.env.ref("product.product_product_11")
        cls.sale_order_1 = cls.env["sale.order"].create(
            {
                "partner_id": partner.id,
                "order_line": [
                    Command.create(
                        {
                            "name": cls.product_id_1.name,
                            "product_id": cls.product_id_1.id,
                            "product_uom_qty": 10,
                            "product_uom": cls.product_id_1.uom_id.id,
                        },
                    ),
                    Command.create(
                        {
                            "name": cls.product_id_2.name,
                            "product_id": cls.product_id_2.id,
                            "product_uom_qty": 11,
                            "product_uom": cls.product_id_2.uom_id.id,
                        },
                    ),
                ],
            }
        )

    def test_01_confirm_sale_and_picking(self):
        self.assertEqual(len(self.sale_order_1.picking_ids), 0)
        self.sale_order_1.action_quick_confirm_sale_and_picking()
        self.assertEqual(len(self.sale_order_1.picking_ids), 1)
        self.assertEqual(self.sale_order_1.mapped("picking_ids.state"), ["done"])

    def test_02_mass_confirm_sale_and_picking(self):
        self.sale_order_2 = self.sale_order_1.copy()
        res = (
            self.env["sale.order"]
            .with_context(active_ids=[self.sale_order_1.id, self.sale_order_2.id])
            .action_mass_quick_confirm_sale_and_picking()
        )
        self.assertEqual(res.get("name"), "Confirm")
