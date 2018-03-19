# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestModule(TransactionCase):

    def setUp(self):
        super(TestModule, self).setUp()
        self.purchase_obj = self.env['purchase.order']
        self.wizard_obj = self.env[
            'product.supplierinfo.create.purchase.order']
        self.asustek = self.env.ref('base.res_partner_1')

        self.laptop_E5023 = self.env.ref(
            'product.product_product_25_product_template')
        self.laptop_E5023_suppinfo = self.laptop_E5023.seller_ids[0]
        self.laptop_S3450 = self.env.ref(
            'product.product_product_26_product_template')
        self.laptop_S3450_suppinfo = self.laptop_S3450.seller_ids[0]
        self.active_ids = [
            self.laptop_E5023_suppinfo.id,
            self.laptop_S3450_suppinfo.id,
        ]

    # Test Section
    def test_01_purchase_mixed_product_option_enabled(self):
        self.laptop_E5023.active = False
        wizard = self.wizard_obj.with_context(
            active_ids=self.active_ids).create(
                {'purchase_disabled_products': True})
        res = wizard.create_purchase_order()
        order_ids = res.setdefault('active_ids', [])
        self.assertEqual(
            len(order_ids), 1, "Test 1 - should create 1 one purchase order.")
        order = self.purchase_obj.browse(int(order_ids[0]))
        self.assertEqual(
            len(order.order_line), 2,
            "Purchase disabled product with enabled option should order"
            " the buy of the product.")

    def test_02_purchase_mixed_product_option_disabled(self):
        self.laptop_E5023.active = False
        wizard = self.wizard_obj.with_context(
            active_ids=self.active_ids).create(
                {'purchase_disabled_products': False})
        res = wizard.create_purchase_order()
        order_ids = res.setdefault('active_ids', [])
        self.assertEqual(
            len(order_ids), 1, "Test 2 - should create 1 one purchase order.")
        order = self.purchase_obj.browse(int(order_ids[0]))
        self.assertEqual(
            len(order.order_line), 1,
            "Purchase disabled product with disabled option should not"
            " order the buy of the product.")
