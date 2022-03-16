# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase, at_install, post_install


@at_install(False)
@post_install(True)
class TestModule(TransactionCase):
    def setUp(self):
        super().setUp()
        self.ResPartner = self.env["res.partner"]

    # Test Section
    def test_01_name_search_by_vat(self):
        vat_search_qty = len(self.ResPartner.name_search("987987987"))
        self.assertEqual(
            vat_search_qty, 0, "Name search should not be based on VAT field.",
        )

    def test_02_name_search_by_name(self):
        search_qty = len(self.ResPartner.name_search("Search Reset"))
        self.assertNotEqual(
            search_qty, 0, "Name search should be based on name field.",
        )
