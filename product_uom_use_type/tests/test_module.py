# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestModule(TransactionCase):

    def setUp(self):
        super(TestModule, self).setUp()
        self.template_obj = self.env['product.template']
        self.both_unit = self.env.ref('product.product_uom_unit')
        self.sale_unit = self.env.ref('product_uom_use_type.product_uom_pint')

    # Test Section
    def test_01_onchange_template(self):
        res = self.template_obj.onchange_uom(self.both_unit.id, False)
        self.assertEqual(
            res.get('value', {}).get('uom_po_id', False),
            self.both_unit.id,
            "Setting a 'both' unit as main UoM should set the same as Purchase"
            " UoM")
        res = self.template_obj.onchange_uom(self.sale_unit.id, False)
        self.assertEqual(
            res.get('value', {}).get('uom_po_id', False),
            False,
            "Setting a 'sale' unit as main UoM should remove the purchase"
            " UoM")
