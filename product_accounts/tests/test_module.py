# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestModule(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.AccountAccount = cls.env["account.account"]
        cls.product = cls.env.ref("product.product_product_25_product_template")
        cls.category = cls.env.ref("product.product_category_5")
        cls.company = cls.env.ref("base.main_company")
        cls.product.company_id = False
        cls.product.property_account_expense_id = False
        cls.product.property_account_income_id = False
        cls.category.property_account_expense_categ_id = False
        cls.category.property_account_income_categ_id = False
        cls.expense_account_1 = cls.AccountAccount.create(
            {
                "code": "6P.EXP1",
                "name": "6P.EXP1 Name",
                "account_type": "expense",
                "company_id": cls.company.id,
            }
        )
        cls.income_account_1 = cls.AccountAccount.create(
            {
                "code": "7P.INC1",
                "name": "7P.INC1 Name",
                "account_type": "income",
                "company_id": cls.company.id,
            }
        )
        cls.expense_account_2 = cls.AccountAccount.create(
            {
                "code": "6P.EXP2",
                "name": "6P.EXP2 Name",
                "account_type": "expense",
                "company_id": cls.company.id,
            }
        )
        cls.income_account_2 = cls.AccountAccount.create(
            {
                "code": "7P.INC2",
                "name": "7P.INC2 Name",
                "account_type": "income",
                "company_id": cls.company.id,
            }
        )

    def test_account_computation(self):
        self.assertEqual(self.product.accounts, False)

        self.product.company_id = self.company.id
        self.assertEqual(self.product.accounts, "- / -")

        self.category.property_account_expense_categ_id = self.expense_account_1.id
        self.assertEqual(self.product.accounts, "6P.EXP1 / -")

        self.category.property_account_income_categ_id = self.income_account_1.id
        self.assertEqual(self.product.accounts, "6P.EXP1 / 7P.INC1")

        self.product.property_account_expense_id = self.expense_account_2.id
        self.product.property_account_income_id = self.income_account_2.id
        self.assertEqual(self.product.accounts, "6P.EXP2 / 7P.INC2")
