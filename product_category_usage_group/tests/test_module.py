# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from openerp.exceptions import Warning as UserError


class Tests(TransactionCase):
    """Tests for 'Product Category - Usage Group' Module"""

    def setUp(self):
        super(Tests, self).setUp()
        self.template_obj = self.env["product.template"]
        self.user_demo = self.env.ref("base.user_demo")
        self.user_root = self.env.ref("base.user_root")
        self.category_normal = self.env.ref("product.product_category_all")
        self.category_special = self.env.ref(
            "product_category_usage_group.category_usage_group"
        )
        self.product_group = self.env.ref("base.group_sale_manager")
        self.restricted_group = self.env.ref("base.group_no_one")
        # Set only Root user as member of the restricted group
        self.restricted_group.users = False
        self.restricted_group.users = [self.user_root.id]
        # Allow demo user to create template
        self.product_group.users = [self.user_demo.id]

    # Test Section
    def test_01_access_user_without_right(self):
        # Use a category without restricted access should success
        self._create_product(self.user_demo, self.category_normal)
        # Use a category with restricted access should fail
        with self.assertRaises(UserError):
            self._create_product(self.user_demo, self.category_special)

    def test_02_access_user_with_right(self):
        # Use a category without restricted access should success
        self._create_product(self.user_root, self.category_normal)
        # Use a category with restricted access should success
        self._create_product(self.user_root, self.category_special)

    def _create_product(self, user, category):
        self.template_obj.sudo(user).create(
            {"name": "Demo Product", "categ_id": category.id}
        )
