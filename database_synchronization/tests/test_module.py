# Copyright (C) 2019 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase, at_install, post_install


@at_install(False)
@post_install(True)
class TestModule(TransactionCase):
    def setUp(self):
        super().setUp()
        self.ResGroups = self.env["res.groups"]

    # # Test Section
    def test_00_fields_view_get(self):
        arch_form_view = self.ResGroups.fields_view_get(view_type="form")["arch"]
        self.assertIn("Readonly Table", arch_form_view)

        arch_tree_view = self.ResGroups.fields_view_get(view_type="tree")["arch"]
        self.assertNotIn("Readonly Table", arch_tree_view)
