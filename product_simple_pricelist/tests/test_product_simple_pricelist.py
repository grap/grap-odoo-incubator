# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestProductSimplePricelist(TransactionCase):
    """Tests for 'Product - Simple Pricelist' Module"""

    def setUp(self):
        super(TestProductSimplePricelist, self).setUp()
        self.simple_item_obj = self.env['product.simple.pricelist.item']
        self.update_wizard_obj = self.env[
            'product.simple.pricelist.item.update.wizard']
        self.simple_pricelist = self.env.ref(
            'product_simple_pricelist.simple_pricelist')
        self.simple_pricelist_version = self.env.ref(
            'product_simple_pricelist.simple_pricelist_version')
        self.service_product = self.env.ref(
            'product.product_product_consultant')
        self.windows_product = self.env.ref(
            'product.product_product_41')

    # Test Section
    def test_01_add_new_price(self):
        items = self.simple_item_obj.search([
            ('pricelist_id', '=', self.simple_pricelist.id),
            ('product_id', '=', self.service_product.id)])
        self.assertEqual(
            len(items), 1,
            "The simple pricelist item should display a line per product.")
        self.assertEqual(
            items[0].difference, 0,
            "Without any action, difference should be null.")

        # Call Set Price button
        res = items[0].set_price_wizard()
        context = res.get('context', {})
        self.assertEqual(
            context.get('product_id', False),
            self.service_product.id,
            "Calling the wizard to change price should contains product ID"
            " in the context")
        self.assertEqual(
            context.get('product_id', False),
            self.service_product.id,
            "Calling the wizard to change price should contains pricelist"
            " version ID in the context")

        # Call wizard
        wizard = self.update_wizard_obj.with_context(
            product_id=context['product_id'],
            pricelist_version_id=context['pricelist_version_id']).create({
                'specific_price': 50,
            })
        wizard.set_price()

        # Check if the correct pricelist item has been created
        items = self.simple_pricelist_version.mapped('items_id').filtered(
            lambda x: x.product_id.id == self.service_product.id)

        self.assertEqual(
            len(items), 1,
            "Setting a specific price should create a new pricelist item.")

    # Test Section
    def test_02_delete_pricelist_item(self):
        items = self.simple_item_obj.search([
            ('pricelist_id', '=', self.simple_pricelist.id),
            ('product_id', '=', self.windows_product.id)])
        self.assertEqual(
            len(items), 1,
            "The simple pricelist item should display a line per product.")
        items[0].remove_price()

        # Check if the correct pricelist item has been created
        items = self.simple_pricelist_version.mapped('items_id').filtered(
            lambda x: x.product_id.id == self.windows_product.id)
        self.assertEqual(
            len(items), 0,
            "dropping a simple item should drop the according pricelist item")
