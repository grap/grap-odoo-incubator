# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import Command
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestModule(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.demo_user = cls.env.ref("user_limited_access_settings.user_demo")
        cls.limited_group = cls.env.ref(
            "user_limited_access_settings.group_limited_settings"
        )
        cls.random_group = cls.env.ref("base.group_private_addresses")
        cls.user_vals = {
            "name": "User 1",
            "login": "login1",
            "groups_id": [Command.set(cls.random_group.ids)],
        }

    def test_access_escalation_forbidden(self):
        with self.assertRaises(ValidationError):
            self.env["res.users"].with_user(self.demo_user).create(self.user_vals)

    def test_access_escalation_allowed(self):
        self.demo_user.groups_id = [Command.link(self.random_group.id)]
        self.env["res.users"].with_user(self.demo_user).create(self.user_vals)
