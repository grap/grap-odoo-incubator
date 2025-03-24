# Copyright (C) 2023-Today: GRAP (<http://www.grap.coop/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.fields import Command
from odoo.tests import Form, common


class TestModule(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.main_company = cls.env.ref("base.main_company")
        cls.demo_company = cls.env.ref("product_uom_company_favorite.demo_company")
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.uom_kgm = cls.env.ref("uom.product_uom_kgm")
        cls.uom_unused = cls.env.ref("uom.product_uom_cubic_foot")
        cls.UomUom = cls.env["uom.uom"]
        cls.ProductTemplate = cls.env["product.template"]
        cls.ResCompany = cls.env["res.company"]
        # Add group 'UoM' to current Bot User, to make 'Form'
        # test working.
        cls.env.user.groups_id = [Command.link(cls.env.ref("uom.group_uom").id)]

    def test_1_default_uom_on_product_form(self):
        # Check without any favorite
        self.UomUom.search([]).write({"is_favorite": False})
        form_0_unit = Form(self.ProductTemplate)
        self.assertFalse(form_0_unit.uom_id)
        self.assertFalse(form_0_unit.uom_po_id)

        # Check with One Favorite
        self.uom_unit.is_favorite = True
        form_1_unit = Form(self.ProductTemplate)
        self.assertEqual(form_1_unit.uom_id, self.uom_unit)
        self.assertEqual(form_1_unit.uom_po_id, self.uom_unit)

        # Check with many Favorites
        self.uom_kgm.is_favorite = True
        form_2_units = Form(self.ProductTemplate)
        self.assertFalse(form_2_units.uom_id)
        self.assertFalse(form_2_units.uom_po_id)

    def test_2_create_new_company(self):
        new_company = self.ResCompany.create({"name": "New Company"})
        self.assertTrue(self.uom_unit.with_company(new_company).is_favorite)
        self.assertFalse(self.uom_unused.with_company(new_company).is_favorite)

    def test_3_name_search(self):
        self.assertTrue(self.UomUom.name_search(self.uom_unit.name))
        self.assertTrue(
            self.UomUom.with_context(display_only_favorite=True).name_search(
                self.uom_unit.name
            )
        )

        self.assertTrue(self.UomUom.name_search(self.uom_unused.name))
        self.assertFalse(
            self.UomUom.with_context(display_only_favorite=True).name_search(
                self.uom_unused.name
            )
        )
