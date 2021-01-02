# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestModule(TransactionCase):
    """Tests for 'Database Synchronization' Module"""

    def setUp(self):
        super().setUp()

    # Test Section
    def test_01(self):
        self.assertEqual(True, True, "Cool.")
