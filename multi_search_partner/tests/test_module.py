# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestModule(TransactionCase):
    def setUp(self):
        super(TestModule, self).setUp()
        self.partner_obj = self.env["res.partner"]
        self.separator = "*"
        self.setting_obj = self.env["base.config.settings"]
        self.name_with_separator = "Test%sAbc" % self.separator
        self.name_without_separator = "TestAbc"

    # Test Section
    def test_01_create_write_partner_enabled(self):
        self._enable_settings(True)
        # Create Partner
        vals = {"name": self.name_with_separator}
        partner = self.partner_obj.create(vals)
        self.assertEqual(
            partner.name,
            self.name_without_separator,
            "Special char in the field should be removed during creation",
        )

        partner.write(vals)
        self.assertEqual(
            partner.name,
            self.name_without_separator,
            "Special char in the field should be removed during update",
        )

    def test_02_create_write_partner_disbled(self):
        self._enable_settings(False)
        # Create Partner
        vals = {"name": self.name_with_separator}
        partner = self.partner_obj.create(vals)
        self.assertEqual(
            partner.name,
            self.name_with_separator,
            "Special char in the field shouldn't be removed during creation",
        )

        partner.write(vals)
        self.assertEqual(
            partner.name,
            self.name_with_separator,
            "Special char in the field shouldn't be removed during update",
        )

    def test_03_search_partner(self):
        ordered_domain = [
            ("display_name", "ilike", "Abc%sDef" % self.separator)
        ]
        unordered_domain = [
            ("display_name", "ilike", "Def%sAbc" % self.separator)
        ]

        # Initial Search
        self._enable_settings(False)
        initial_search = len(self.partner_obj.search(ordered_domain))

        # Create Partner
        vals = {"name": "Abc other Word Def"}
        self.partner_obj.create(vals)

        # First Search (Feature disabled)
        disabled_feature_search = len(self.partner_obj.search(ordered_domain))
        self.assertEqual(
            initial_search,
            disabled_feature_search,
            "Search function should not return items if settins is disabled",
        )

        # Second search (ordered) (Feature enabled)
        self._enable_settings(True)
        ensabled_feature_search_ordered = len(
            self.partner_obj.search(ordered_domain)
        )
        self.assertEqual(
            ensabled_feature_search_ordered,
            initial_search + 1,
            "Multi search in ordered mode failed.",
        )

        ensabled_feature_search_unordered = len(
            self.partner_obj.search(unordered_domain)
        )
        self.assertEqual(
            ensabled_feature_search_unordered,
            initial_search + 1,
            "Multi search in unordered mode failed.",
        )

    def _enable_settings(self, enable):
        setting = self.setting_obj.create({})
        if enable:
            setting.multi_search_partner_separator = self.separator
        else:
            setting.multi_search_partner_separator = False
        setting.set_multi_search_partner_separator()
