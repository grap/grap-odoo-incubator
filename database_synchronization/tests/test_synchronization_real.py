# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase, at_install, post_install
from odoo.tools import config


@at_install(False)
@post_install(True)
class TestSynchronizationReal(TransactionCase):
    def setUp(self):
        super().setUp()
        self.synchronization_group = self.env.ref(
            "database_synchronization.synchronisation_res_groups"
        )
        self.synchronization_company = self.env.ref(
            "database_synchronization.synchronisation_res_company"
        )

    def _configure_auto_call(self):
        # Configure settings to auto-call
        self.env.ref(
            "database_synchronization.parameter_database"
        ).value = self.env.cr.dbname
        self.env.ref("database_synchronization.parameter_host").value = "localhost"
        self.env.ref("database_synchronization.parameter_port").value = config.options[
            "http_port"
        ]

    def test_20_high_level_synchronize_id(self):
        self._configure_auto_call()
        self.synchronization_group.action_synchronize()
        self.synchronization_group.action_full_synchronize()

    def test_21_high_level_synchronize_data(self):
        self._configure_auto_call()
        self.synchronization_company.action_synchronize()
        self.synchronization_company.action_full_synchronize()
