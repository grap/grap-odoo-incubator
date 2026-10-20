# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestAbstract(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.ProductProduct = cls.env["product.product"]
        cls.product_1 = cls.env.ref("mobile_kiosk_abstract.product_1")
        cls.product_2 = cls.env.ref("mobile_kiosk_abstract.product_2")
        cls.random_product = cls.env.ref("product.product_product_5")
        cls.supplier = cls.env.ref("mobile_kiosk_abstract.supplier")

    def _assert_notification(self, result, expected_level):
        self.assertIn(
            expected_level,
            [x.get("type") for x in result.get("notifications", [])],
            result,
        )

    def _get_context(self, result):
        self.assertIn("action", result.keys(), result)
        self.assertNotEqual(result.get("action"), False, result)
        self.assertIn("context", result["action"].keys(), result)
        return result["action"]["context"]

    def _get_context_value(self, result, context_key):
        context = self._get_context(result)
        self.assertIn(context_key, context, result)
        return context[context_key]

    def _get_context_from_action(self, action):
        self.assertIn("context", action.keys(), action)
        return action["context"]

    def _get_context_value_from_action(self, action, context_key):
        context = self._get_context_from_action(action)
        self.assertIn(context_key, context, action)
        return context[context_key]
