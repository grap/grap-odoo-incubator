# @author Quentin DUPONT <quentin.dupont@grap.coop>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import Command
from odoo.exceptions import UserError
from odoo.tests.common import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestAccountMovePartnerFields(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass(chart_template_ref="l10n_fr.l10n_fr_pcg_chart_template")

        cls.move_1 = cls.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "date": "1789-07-14",
                "invoice_date": "2027-05-02",
                "currency_id": cls.currency_data["currency"].id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "product_id": cls.product_a.id,
                            "price_unit": 1000.0,
                        },
                    )
                ],
            }
        )
        cls.child_agrolait_child = cls.env["res.partner"].create(
            {
                "name": "child of Agrolait",
                "parent_id": cls.partner_agrolait.id,
            }
        )

    def test_partner_is_company_parent(self):
        self._test_with_partner(self.partner_agrolait)

    def test_partner_individual_child(self):
        self._test_with_partner(self.child_agrolait_child)

    def _test_with_partner(self, partner):
        self.move_1.partner_id = partner

        # Simulate no data
        self.move_1.commercial_partner_id.write(
            {
                "street": False,
                "zip": False,
                "city": False,
                "siren": False,
                "is_company": True,
            }
        )

        self.move_1._compute_partner_has_required_fields()
        self.assertFalse(self.move_1.partner_has_siren, "SIREN should be False")
        self.assertFalse(self.move_1.partner_has_address, "Address should be False")
        self.assertTrue(
            self.move_1.partner_is_company, "partner_is_company should be True"
        )

        # Should fail
        with self.assertRaises(UserError):
            self.move_1.action_post()

        # Fill all needed informations
        self.move_1.commercial_partner_id.write(
            {
                "street": "25 PASSAGE DUBAIL",
                "zip": "75010",
                "city": "PARIS",
                "siren": "828130799",
                "nic": "00020",
            }
        )

        self.move_1._compute_partner_has_required_fields()
        self.assertTrue(self.move_1.partner_has_siren, "SIREN should be True")
        self.assertTrue(self.move_1.partner_has_address, "Address should be True")

        # Should not raise any error
        self.move_1.action_post()
