# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.fields import Command
from odoo.tests import tagged

from odoo.addons.sale.tests.common import TestSaleCommon


@tagged("-at_install", "post_install")
class TestModule(TestSaleCommon):
    """Non regression test. We inherit from base sale test"""

    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        order_vals = {
            "partner_id": cls.partner_a.id,
            "partner_invoice_id": cls.partner_a.id,
            "partner_shipping_id": cls.partner_a.id,
            "pricelist_id": cls.company_data["default_pricelist"].id,
            "order_line": [
                Command.create(
                    {
                        "product_id": cls.company_data["product_service_order"].id,
                        "product_uom_qty": 3,
                        "tax_id": False,
                    }
                ),
            ],
        }
        cls.sale_order = (
            cls.env["sale.order"].with_context(tracking_disable=True).create(order_vals)
        )

        cls.tax_a = cls.env["account.tax"].create(
            {
                "name": "Test tax",
                "type_tax_use": "sale",
                "price_include": False,
                "amount_type": "percent",
                "amount": 15.0,
            }
        )

        cls.order_line = cls.sale_order.order_line[0]

        # Context
        cls.context = {
            "active_model": "sale.order",
            "active_ids": [cls.sale_order.id],
            "active_id": cls.sale_order.id,
            "default_journal_id": cls.company_data["default_journal_sale"].id,
        }

        cls.down_payment_product_no_vat = cls.env["product.product"].create(
            {
                "name": "Down Payment No Tax",
                "company_id": cls.env.company.id,
                "type": "service",
                "taxes_id": [],
            }
        )
        cls.down_payment_product_with_vat = cls.env["product.product"].create(
            {
                "name": "Down Payment With Tax",
                "company_id": cls.env.company.id,
                "type": "service",
                "taxes_id": [Command.link(cls.tax_a.id)],
            }
        )
        cls.env.company.down_payment_product_ids = [Command.clear()]

    def _confirm_and_create_wizard(self):
        self.sale_order.action_confirm()
        return (
            self.env["sale.advance.payment.inv"]
            .with_context(**self.context)
            .create({"advance_payment_method": "fixed", "fixed_amount": 50})
        )

    def test_downpayment_no_product(self):
        wizard = self._confirm_and_create_wizard()
        self.assertEqual(wizard.product_id.id, False)
        self.assertIn(
            "Unable to find a down payment product without taxes",
            wizard.product_message,
        )

    def test_downpayment_product_no_vat(self):
        wizard = self._confirm_and_create_wizard()
        self.env.company.down_payment_product_ids = [
            Command.link(self.down_payment_product_no_vat.id),
            Command.link(self.down_payment_product_with_vat.id),
        ]
        self.assertEqual(wizard.product_id, self.down_payment_product_no_vat)
        self.assertEqual(wizard.product_message, False)

    def test_downpayment_product_with_vat_absent(self):
        self.order_line.tax_id = [Command.link(self.tax_a.id)]
        wizard = self._confirm_and_create_wizard()
        self.assertEqual(wizard.product_id.id, False)
        self.assertIn(
            "Unable to find a down payment product with taxes",
            wizard.product_message,
        )

    def test_downpayment_product_with_vat_present(self):
        self.order_line.tax_id = [Command.link(self.tax_a.id)]
        self.env.company.down_payment_product_ids = [
            Command.link(self.down_payment_product_no_vat.id),
            Command.link(self.down_payment_product_with_vat.id),
        ]

        wizard = self._confirm_and_create_wizard()
        self.assertEqual(wizard.product_id, self.down_payment_product_with_vat)
        self.assertEqual(wizard.product_message, False)
