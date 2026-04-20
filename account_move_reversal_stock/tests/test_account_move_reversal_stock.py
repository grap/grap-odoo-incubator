# Copyright 2016 Oihane Crucelaegui - AvanzOSC
# Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2017 Jacques-Etienne Baudoux <je@bcim.be>
# Copyright 2021 Tecnativa - João Marques
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
# Inspired by stock_picking_invoice_link test, that's why all the copyright
# Copyright 2026-Today: GRAP (https://www.grap.coop)
# Copyright Quentin DUPONT

from odoo.exceptions import UserError
from odoo.tests import tagged

from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT
from odoo.addons.sale.tests.common import TestSaleCommon


@tagged("post_install", "-at_install")
class TestAccountMoveReversalStock(TestSaleCommon):
    @classmethod
    def _update_product_qty(cls, product):
        product_qty = cls.env["stock.change.product.qty"].create(
            {
                "product_id": product.id,
                "product_tmpl_id": product.product_tmpl_id.id,
                "new_quantity": 100.0,
            }
        )
        product_qty.change_product_qty()
        return product_qty

    @classmethod
    def _create_sale_order_and_confirm(cls):
        so = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner_a.id,
                "partner_invoice_id": cls.partner_a.id,
                "partner_shipping_id": cls.partner_a.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": cls.prod_order.name,
                            "product_id": cls.prod_order.id,
                            "product_uom_qty": 20,
                            "product_uom": cls.prod_order.uom_id.id,
                            "price_unit": cls.prod_order.list_price,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": cls.prod_del.name,
                            "product_id": cls.prod_del.id,
                            "product_uom_qty": 20,
                            "product_uom": cls.prod_del.uom_id.id,
                            "price_unit": cls.prod_del.list_price,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": cls.serv_order.name,
                            "product_id": cls.serv_order.id,
                            "product_uom_qty": 20,
                            "product_uom": cls.serv_order.uom_id.id,
                            "price_unit": cls.serv_order.list_price,
                        },
                    ),
                ],
                "pricelist_id": cls.env.ref("product.list0").id,
                "picking_policy": "direct",
            }
        )
        so.action_confirm()

        # Create and validate picking
        pick_1 = so.picking_ids.filtered(
            lambda x: x.picking_type_code == "outgoing"
            and x.state in ("confirmed", "assigned", "partially_available")
        )
        pick_1.move_line_ids.write({"qty_done": 100})
        pick_1._action_done()

        return so

    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.env = cls.env(context=dict(cls.env.context, **DISABLED_MAIL_CONTEXT))
        for _, i in cls.company_data.items():
            if "type" in i and i.type == "product":
                cls._update_product_qty(i)
        cls.prod_order = cls.company_data["product_order_no"]
        cls.prod_order.invoice_policy = "delivery"
        cls.prod_del = cls.company_data["product_delivery_no"]
        cls.prod_del.invoice_policy = "delivery"
        cls.serv_order = cls.company_data["product_service_order"]
        cls.so = cls._create_sale_order_and_confirm()

    def test_01_invoice_refund_modify(self):
        # Create and validate invoice
        inv_1 = self.so._create_invoices()
        inv_1.action_post()

        # Launch Refund
        wiz_invoice_refund = (
            self.env["account.move.reversal"]
            .with_context(active_model="account.move", active_ids=inv_1.ids)
            .create(
                {
                    "refund_method": "modify",
                    "reason": "test",
                    "journal_id": inv_1.journal_id.id,
                }
            )
        )
        wiz_invoice_refund.reverse_moves()
        new_invoice = self.so.invoice_ids.filtered(
            lambda i: i.move_type == "out_invoice" and i.state == "draft"
        )

        # Test new_invoice
        self.assertEqual(new_invoice.stock_picking_could_be_returned, False)

        # Reverse will raise Error as there is no quantity differentials
        with self.assertRaises(UserError):
            new_invoice.reverse_stock_picking()

        # Change quantity and retest
        new_invoice.invoice_line_ids.write({"quantity": 40})
        new_invoice.action_post()
        self.assertEqual(new_invoice.stock_picking_could_be_returned, True)
        self.assertEqual(new_invoice.picking_count, 1)
        new_invoice.reverse_stock_picking()
        self.assertEqual(new_invoice.picking_count, 2)

    def test_02_invoice_refund_cancel(self):
        # Create and validate invoice
        inv = self.so._create_invoices()
        inv.action_post()

        # Launch Refund
        wiz_invoice_refund = (
            self.env["account.move.reversal"]
            .with_context(active_model="account.move", active_ids=inv.ids)
            .create(
                {
                    "refund_method": "cancel",
                    "reason": "test",
                    "journal_id": inv.journal_id.id,
                }
            )
        )
        wiz_invoice_refund.reverse_moves()
        new_invoice = self.so.invoice_ids.filtered(
            lambda i: i.move_type == "out_refund" and i.state == "posted"
        )

        # Test new_invoice
        self.assertEqual(new_invoice.stock_picking_could_be_returned, True)
        self.assertEqual(new_invoice.picking_count, 1)
        new_invoice.reverse_stock_picking()
        self.assertEqual(new_invoice.picking_count, 2)
