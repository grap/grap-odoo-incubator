# coding: utf-8
# Copyright (C) 2019 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestModule(TransactionCase):

    def setUp(self):
        super(TestModule, self).setUp()
        self.Wizard = self.env['mass.action.wizard']
        self.ResUsers = self.env['res.users']
        self.mass_action_duplicate_users = self.env.ref(
            'mass_action.mass_action_duplicate_users')

    # Test Section
    def test_01_mass_action(self):
        users = self.ResUsers.search([])

        wizard = self.Wizard.with_context(
            active_ids=users.ids,
            active_model='res.users',
            mass_operation_mixin_name='mass.action',
            mass_operation_mixin_id=self.mass_action_duplicate_users.id)
        wizard.button_apply()

        self.assertEqual(
            len(self.ResUsers.search([])), 2 * len(users),
            "Mass duplication failed")
