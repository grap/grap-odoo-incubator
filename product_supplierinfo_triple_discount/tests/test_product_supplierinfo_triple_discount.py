# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import openerp.tests.common as common


class TestProductSupplierinfoTripleDiscount(common.TransactionCase):

    def setUp(self):
        super(TestProductSupplierinfoTripleDiscount, self).setUp()
        self.supplierinfo_model = self.env['product.supplierinfo']
        self.purchase_order_line_model = self.env['purchase.order.line']
        self.partner_1 = self.env.ref('base.res_partner_1')
        self.partner_3 = self.env.ref('base.res_partner_3')
        self.product = self.env.ref(
            'product_supplierinfo_triple_discount.product').\
                product_variant_ids[0]

    def test_purchase_order_partner_3_qty_1(self):
        res = self.purchase_order_line_model.onchange_product_id(
            self.partner_3.property_product_pricelist_purchase.id,
            self.product.id, 1, self.product.uom_id.id, self.partner_3.id)
        self.assertEqual(
            res['value']['discount2'], 10.0,
            "Incorrect discount 2 for product 6 with partner 3 and qty 1")
        self.assertEqual(
            res['value']['discount3'], 15.0,
            "Incorrect discount 3 for product 6 with partner 3 and qty 1")

    def test_purchase_order_partner_3_qty_10(self):
        res = self.purchase_order_line_model.onchange_product_id(
            self.partner_3.property_product_pricelist_purchase.id,
            self.product.id, 10, self.product.uom_id.id, self.partner_3.id)
        self.assertEqual(
            res['value']['discount2'], 20.0,
            "Incorrect discount 2 for product 6 with partner 3 and qty 10")
        self.assertEqual(
            res['value']['discount3'], 30.0,
            "Incorrect discount 3 for product 6 with partner 3 and qty 10")

    def test_purchase_order_partner_1_qty_1(self):
        res = self.purchase_order_line_model.onchange_product_id(
            self.partner_3.property_product_pricelist_purchase.id,
            self.product.id, 1, self.product.uom_id.id, self.partner_1.id)
        self.assertEqual(
            res['value'].get('discount2', 0.0), 0.0,
            "Incorrect discount 2 for product 6 with partner 1 and qty 1")
        self.assertEqual(
            res['value'].get('discount3', 0.0), 0.0,
            "Incorrect discount 2 for product 6 with partner 1 and qty 1")
