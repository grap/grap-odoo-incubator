# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestDuplicationAccountInvoice(TransactionCase):
    """Tests for 'Duplication Tools - Account Invoice' Module"""

    def setUp(self):
        super(TestDuplicationAccountInvoice, self).setUp()
        self.wizard_obj = self.env["account.invoice.duplication.wizard"]
        self.invoice_obj = self.env["account.invoice"]
        self.invoice = self.env.ref("l10n_generic_coa.demo_invoice_1")

    # Test Section
    def test_01_duplicate_account_invoice(self):
        invoice_qty = len(self.invoice_obj.search([]))
        wizard = self.wizard_obj.create(
            {
                "invoice_id": self.invoice.id,
                "partner_id": self.invoice.partner_id.id,
                "begin_date": "09-09-2019",
                "include_current_date": False,
                "duplication_type": "week",
                "duplication_duration": 10,
            }
        )
        wizard.onchange_duplication_settings()
        wizard.duplicate_open_button()
        new_invoice_qty = len(self.invoice_obj.search([]))
        self.assertEqual(
            invoice_qty + 10,
            new_invoice_qty,
            "Duplication wizard should create new account invoices",
        )
