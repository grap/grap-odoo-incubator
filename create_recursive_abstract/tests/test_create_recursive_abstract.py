# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo_test_helper import FakeModelLoader

from odoo.tests.common import TransactionCase


class TestModule(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Load a test model using odoo_test_helper
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .fake_models import ModelCreateRecursiveMixin

        cls.loader.update_registry((ModelCreateRecursiveMixin,))

        cls.model = cls.env["model.create.recursive.mixin"]

        cls.parent_item = cls.model.create({"name": "Parent"})

        cls.child_item = cls.model.create(
            {"name": "Child", "parent_id": cls.parent_item.id}
        )

    @classmethod
    def tearDownClass(cls):
        cls.loader.restore_registry()
        return super().tearDownClass()

    def test_remove_slash_create(self):
        item = self.model.create({"name": "Fruits / Vegetables"})
        self.assertEqual(item.name, "Fruits - Vegetables")

    def test_remove_slash_write(self):
        self.parent_item.write({"name": "Fruits / Vegetables"})
        self.assertEqual(self.parent_item.name, "Fruits - Vegetables")

    def test_name_create(self):
        res = self.model.name_create("Parent / Child / New Category")
        categ = self.model.browse(res[0])
        self.assertEqual(categ.name, "New Category")
        self.assertEqual(categ.parent_id, self.child_item)

    def test_create_via_import(self):
        categ = self.model.with_context(imported_model=self.model._name).create(
            {"name": "Parent / Child"}
        )
        self.assertEqual(categ.name, "Child")
        self.assertTrue(categ.parent_id)
        self.assertEqual(categ.parent_id.name, "Parent")
