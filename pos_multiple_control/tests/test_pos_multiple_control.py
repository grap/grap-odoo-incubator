# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestMultipleControl(TransactionCase):
    """Tests for 'Point of Sale - Multiple Control' Module"""

    def setUp(self):
        super(TestStockInternalUseOfProducts, self).setUp()

    # Test Section
    def test_01_xxx(self):
        self.assertEqual(
            4, 4,
            "xxx")
