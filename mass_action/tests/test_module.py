# coding: utf-8
# Copyright (C) 2019 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestModule(TransactionCase):

    # TODO: FIXME
    def fix_mail_bug(self, function):
        """ Tests are failing on a database with 'mail' module installed,
        Because the load of the registry in TransactionCase seems to be bad.
        To be sure, run "print self.registry('res.partner')._defaults and see
        that the mandatory field 'notify_email' doesn't appear.
        So this is a monkey patch that drop and add not null constraint
        to make that tests working."""
        self.cr.execute("""
            SELECT A.ATTNAME
                FROM PG_ATTRIBUTE A, PG_CLASS C
                WHERE A.ATTRELID = C.OID
                AND A.ATTNAME = 'notify_email'
                AND C.relname= 'res_partner';""")
        if self.cr.fetchone():
            if function == 'SET':
                self.cr.execute("""
                    ALTER TABLE res_partner
                    ALTER COLUMN notify_email SET NOT NULL;""")
            else:
                self.cr.execute("""
                    ALTER TABLE res_partner
                    ALTER COLUMN notify_email DROP NOT NULL;""")
        self.cr.execute("""
            SELECT A.ATTNAME
                FROM PG_ATTRIBUTE A, PG_CLASS C
                WHERE A.ATTRELID = C.OID
                AND A.ATTNAME = 'alias_id'
                AND C.relname= 'res_users';""")
        if self.cr.fetchone():
            if function == 'SET':
                self.cr.execute("""
                    ALTER TABLE res_users
                    ALTER COLUMN alias_id SET NOT NULL;""")
            else:
                self.cr.execute("""
                    ALTER TABLE res_users
                    ALTER COLUMN alias_id DROP NOT NULL;""")

    def setUp(self):
        super(TestModule, self).setUp()
        self.Wizard = self.env['mass.action.wizard']
        self.ResUsers = self.env['res.users']
        self.mass_action_duplicate_users = self.env.ref(
            'mass_action.mass_action_duplicate_users')
        self.fix_mail_bug("DROP")

    def tearDown(self):
        self.cr.rollback()
        self.fix_mail_bug("SET")
        super(TestModule, self).tearDown()

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
