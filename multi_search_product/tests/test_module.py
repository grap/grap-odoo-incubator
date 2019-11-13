# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestModule(TransactionCase):
    def setUp(self):
        super(TestModule, self).setUp()
        self.product_obj = self.env["product.product"]
        self.product_category = self.env.ref("product.product_category_all")
        self.separator = "*"
        self.setting_obj = self.env["base.config.settings"]
        self.name_with_separator = "Test%sAbc" % self.separator
        self.name_without_separator = "TestAbc"

    # Test Section
    def test_01_create_write_product_product_enabled(self):
        self._enable_settings(True)
        # Create Product
        vals = {
            "name": self.name_with_separator,
            "categ_id": self.product_category.id,
        }
        product = self.product_obj.create(vals)
        self.assertEqual(
            product.name,
            self.name_without_separator,
            "Special char in the field should be removed during creation",
        )

        product.write(vals)
        self.assertEqual(
            product.name,
            self.name_without_separator,
            "Special char in the field should be removed during update",
        )

    def test_02_create_write_product_product_disbled(self):
        self._enable_settings(False)
        # Create Product
        vals = {
            "name": self.name_with_separator,
            "categ_id": self.product_category.id,
        }
        product = self.product_obj.create(vals)
        self.assertEqual(
            product.name,
            self.name_with_separator,
            "Special char in the field shouldn't be removed during creation",
        )

        product.write(vals)
        self.assertEqual(
            product.name,
            self.name_with_separator,
            "Special char in the field shouldn't be removed during update",
        )

    def test_03_search_product_product(self):
        ordered_domain = [("name", "ilike", "Abc%sDef" % self.separator)]
        unordered_domain = [("name", "ilike", "Def%sAbc" % self.separator)]

        # Initial Search
        self._enable_settings(False)
        initial_search = len(self.product_obj.search(ordered_domain))

        # Create Product
        vals = {
            "name": "Abc other Word Def",
            "categ_id": self.product_category.id,
        }
        self.product_obj.create(vals)

        # First Search (Feature disabled)
        disabled_feature_search = len(self.product_obj.search(ordered_domain))
        self.assertEqual(
            initial_search,
            disabled_feature_search,
            "Search function should not return items if settins is disabled",
        )

        # Second search (ordered) (Feature enabled)
        self._enable_settings(True)
        ensabled_feature_search_ordered = len(
            self.product_obj.search(ordered_domain)
        )
        self.assertEqual(
            ensabled_feature_search_ordered,
            initial_search + 1,
            "Multi search in ordered mode failed.",
        )

        ensabled_feature_search_unordered = len(
            self.product_obj.search(unordered_domain)
        )
        self.assertEqual(
            ensabled_feature_search_unordered,
            initial_search + 1,
            "Multi search in unordered mode failed.",
        )

    def test_04_update_database(self):
        # Create Product
        vals = {
            "name": self.name_with_separator,
            "categ_id": self.product_category.id,
        }
        product = self.product_obj.create(vals)

        # Enable and disable mechanism
        self._enable_settings(True)
        self._enable_settings(False)
        self.assertEqual(
            product.name,
            self.name_without_separator,
            "Enable multi search should remove the special character"
            " from the current database.",
        )

    def _enable_settings(self, enable):
        setting = self.setting_obj.create({})
        if enable:
            setting.multi_search_product_separator = self.separator
        else:
            setting.multi_search_product_separator = False
        setting.set_multi_search_product_separator()
