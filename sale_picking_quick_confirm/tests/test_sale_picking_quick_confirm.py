# @author Quentin DUPONT <quentin.dupont@grap.coop>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestSalePickingQuickConfirm(TransactionCase):
    def setUp(self):
        super().setUp()
        partner = self.env["res.partner"].create(
            {
                "name": "Test",
            }
        )
        self.product_id_1 = self.env.ref("product.product_product_8")
        self.product_id_2 = self.env.ref("product.product_product_11")
        self.sale_order_1 = self.env["sale.order"].create(
            {
                "partner_id": partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": self.product_id_1.name,
                            "product_id": self.product_id_1.id,
                            "product_uom_qty": 5,
                            "product_uom": self.product_id_1.uom_id.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": self.product_id_2.name,
                            "product_id": self.product_id_2.id,
                            "product_uom_qty": 7,
                            "product_uom": self.product_id_2.uom_id.id,
                        },
                    ),
                ],
            }
        )

    def test_confirm_sale_and_picking(self):
        self.assertEqual(len(self.sale_order_1.picking_ids), 0)
        self.assertEqual(self.sale_order_1.action_quick_confirm(), True)
        self.assertEqual(len(self.sale_order_1.picking_ids), 1)
        for picking in self.sale_order_1.picking_ids:
            self.assertEqual(picking.state, "done")
