# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from openerp.exceptions import Warning as UserError


class Tests(TransactionCase):
    """Tests for 'Account Product - Fiscal Classification - Usage Group'"""

    def setUp(self):
        super(Tests, self).setUp()
        self.template_obj = self.env['product.template']
        self.user_demo = self.env.ref('base.user_demo')
        self.user_root = self.env.ref('base.user_root')
        self.product_category = self.env.ref('product.product_category_all')
        self.product_group = self.env.ref('base.group_sale_manager')
        self.restricted_group = self.env.ref('account.group_account_manager')
        self.classification = self.env.ref(
            'account_product_fiscal_classification.fiscal_classification_1')
        # Set only Root user as member of the restricted group
        self.restricted_group.users = False
        self.restricted_group.users = [self.user_root.id]
        # Allow demo user to create template
        self.product_group.users = [self.user_demo.id]

    # Test Section
    def test_01_access_user_without_right(self):
        self._create_product(self.user_demo, True)
        self.classification.usage_group_id = self.restricted_group
        # Create a product without restricted fiscal classification
        # should success
        self._create_product(self.user_demo, False)
        # Create a product with restricted fiscal classification
        # should fail
        with self.assertRaises(UserError):
            self._create_product(self.user_demo, True)

    def test_01_access_user_with_right(self):
        self._create_product(self.user_root, True)
        self.classification.usage_group_id = self.restricted_group
        self._create_product(self.user_root, True)

    def _create_product(self, user, with_classification):
        vals = {
            'name': 'Demo Product',
            'categ_id': self.product_category.id,
        }
        if with_classification:
            vals.update({
                'fiscal_classification_id': self.classification.id,
            })
        self.template_obj.sudo(user).create(vals)
