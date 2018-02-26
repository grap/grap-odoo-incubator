# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestSimpleTaxAccount(TransactionCase):
    """Tests for 'Simple Tax - Account' Module"""

    def setUp(self):
        super(TestSimpleTaxAccount, self).setUp()
        self.invoice_obj = self.env['account.invoice']
