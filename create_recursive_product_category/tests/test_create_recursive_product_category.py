# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from odoo.modules.module import get_module_resource
from odoo.tests.common import TransactionCase

_logger = logging.getLogger(__name__)


class TestModule(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.ProductCategory = cls.env["product.category"]
        cls.Wizard = cls.env["base_import.import"]

        cls.parent_item = cls.ProductCategory.create({"name": "Parent"})

        cls.child_item = cls.ProductCategory.create(
            {"name": "Child", "parent_id": cls.parent_item.id}
        )
        cls.initial_category_ids = cls.ProductCategory.search([]).ids

    def _test_new_categories(self, category_count):
        new_categories = self.ProductCategory.search(
            [("id", "not in", self.initial_category_ids)], order="id"
        )
        _logger.info(
            "\n\n - " + "\n - ".join(new_categories.mapped("complete_name")) + "\n"
        )
        self.assertEqual(len(new_categories), category_count)

    def _import_file(self, model_name, file_name):
        preview_options = {
            "headers": True,
            "quoting": '"',
            "name_create_enabled_fields": {"categ_id": True},
        }
        import_options = {
            "has_headers": True,
            "quoting": '"',
            "name_create_enabled_fields": {"categ_id": True},
        }

        # Read File
        file_path = get_module_resource(
            "create_recursive_product_category", "tests/data/", model_name, file_name
        )
        file_content = open(file_path, "rb").read()

        # Create Wizard
        import_wizard = self.Wizard.create(
            {
                "res_model": model_name,
                "file_type": "text/csv",
                "file": file_content,
            }
        )

        # Run Preview
        result_parse = import_wizard.parse_preview(preview_options)
        column_list = [x[0] for x in result_parse["preview"]]

        # Execute Import
        results = import_wizard.execute_import(column_list, column_list, import_options)

        items = self.env[model_name].browse(results.get("ids"))
        return items, results["messages"]

    def test_01_remove_slash_create(self):
        item = self.ProductCategory.create({"name": "Fruits / Vegetables"})
        self.assertEqual(item.name, "Fruits - Vegetables")

    def test_02_remove_slash_write(self):
        self.parent_item.write({"name": "Fruits / Vegetables"})
        self.assertEqual(self.parent_item.name, "Fruits - Vegetables")

    def test_10_name_create(self):
        res = self.ProductCategory.name_create("Parent / Child / New Category")
        categ = self.ProductCategory.browse(res[0])
        self.assertEqual(categ.name, "New Category")
        self.assertEqual(categ.parent_id, self.child_item)

    def test_20_import_category_AA_5_root_categories(self):
        items, _res = self._import_file("product.category", "AA_5_root_categories.csv")
        self._test_new_categories(5)

    def test_21_import_category_AB_3_child_categories_without_2_explicit_parents(self):
        items, _res = self._import_file(
            "product.category", "AB_3_child_categories_without_2_explicit_parents.csv"
        )
        self._test_new_categories(5)

    def test_22_import_category_AC_1_parent_category_1_child_category(self):
        items, _res = self._import_file(
            "product.category", "AC_1_parent_category_1_child_category.csv"
        )
        self._test_new_categories(2)

    def test_30_import_product_BA_5_root_categories(self):
        items, _res = self._import_file("product.template", "BA_5_root_categories.csv")
        self._test_new_categories(5)

    def test_31_import_product_BB_3_child_categories_without_2_explicit_parents(self):
        items, _res = self._import_file(
            "product.template", "BB_3_child_categories_without_2_explicit_parents.csv"
        )
        self._test_new_categories(5)

    def test_32_import_category_BC_1_parent_category_1_child_category(self):
        items, _res = self._import_file(
            "product.template", "BC_1_parent_category_1_child_category.csv"
        )
        self._test_new_categories(2)
