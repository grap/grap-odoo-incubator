# @author Quentin DUPONT <quentin.dupont@grap.coop>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.exceptions import UserError
from odoo.tests.common import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestAccountMovePartnerFields(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.move_1 = cls.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "date": "1789-07-14",
                "invoice_date": "2027-05-02",
                "partner_id": cls.partner_a.id,
                "currency_id": cls.currency_data["currency"].id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product_a.id,
                            "price_unit": 1000.0,
                            "tax_ids": [],
                        },
                    )
                ],
            }
        )

    def test_action_post_partner_required_fields(self):
        partner = self.move_1.partner_id

        # Simulate no data
        partner.write(
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
        partner.write(
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

        # Should succeed
        try:
            self.move_1.action_post()
        except UserError:
            self.fail("action_post raised UserError even though all fields are filled")
