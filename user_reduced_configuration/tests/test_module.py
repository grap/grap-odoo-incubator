# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from lxml import etree

from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestModule(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.demo_user = cls.env.ref("user_reduced_configuration.user_demo")
        cls.ClassicConfig = cls.env["res.config.settings"]
        cls.ReducedConfig = cls.env["res.reduced.config.settings"].with_user(
            cls.demo_user
        )
        cls.reduced_config = cls.ReducedConfig.create({})
        cls.ConfigParameter = cls.env["ir.config_parameter"]
        cls.configuration_1 = cls.env.ref(
            "user_reduced_configuration.reduced_configuration_user_default_rights"
        )

    def _get_value(self):
        return bool(self.ConfigParameter.get_param("base_setup.default_user_rights"))

    def test_write_ko(self):
        initial_value = self._get_value()
        self.configuration_1.unlink()
        self.reduced_config.user_default_rights = not initial_value
        self.reduced_config.execute()
        self.assertEqual(self._get_value(), initial_value)

    def test_write_ok(self):
        initial_value = self._get_value()
        self.reduced_config.user_default_rights = not initial_value
        self.reduced_config.execute()
        self.assertEqual(self._get_value(), not initial_value)

    def test_reduced_config_get_view(self):
        view = self.ReducedConfig.get_view()
        arch = etree.XML(view["arch"])
        hidden_elements = arch.xpath("//div[@name='users_setting_container']")
        self.assertEqual(len(hidden_elements), 1)
        self.assertEqual(hidden_elements[0].get("class"), "d-none")

    def test_classic_config_get_view(self):
        view = self.ClassicConfig.get_view()
        arch = etree.XML(view["arch"])
        visible_elements = arch.xpath("//div[@name='users_setting_container']")
        self.assertEqual(len(visible_elements), 1)
        self.assertNotEqual(visible_elements[0].get("class"), "d-none")
