# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestDuplicationSaleOrder(TransactionCase):
    """Tests for 'Duplication Tools - Sale Order' Module"""

    def setUp(self):
        super(TestDuplicationSaleOrder, self).setUp()
        self.wizard_obj = self.env["sale.order.duplication.wizard"]
        self.order_obj = self.env["sale.order"]
        self.order = self.env.ref("sale.sale_order_6")

    # Test Section
    def test_01_duplicate_quotation(self):
        quotation_qty = len(self.order_obj.search([]))
        wizard = self.wizard_obj.create(
            {
                "order_id": self.order.id,
                "partner_id": self.order.partner_id.id,
                "begin_date": "01-01-2018",
                "include_current_date": False,
                "duplication_type": "week",
                "duplication_duration": 10,
            }
        )
        wizard.onchange_duplication_settings()
        wizard.duplicate_open_button()
        new_quotation_qty = len(self.order_obj.search([]))
        self.assertEqual(
            quotation_qty + 10,
            new_quotation_qty,
            "Duplication wizard should create new sale orders",
        )
