# coding: utf-8
# Copyright (C) 2018-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests import common


class TestModule(common.TransactionCase):

    def setUp(self):
        super(TestModule, self).setUp()
        self.MobileAppPurchase = self.env['mobile.app.purchase']
