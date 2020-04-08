# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from odoo.exceptions import Warning as UserError


class TestMultipleControl(TransactionCase):
    """Tests for 'Point of Sale - Multiple Control' Module"""

    def setUp(self):
        super(TestMultipleControl, self).setUp()
        self.session_obj = self.env["pos.session"]
        self.order_obj = self.env["pos.order"]
        self.payment_obj = self.env["pos.make.payment"]
        self.product = self.env.ref("product.product_product_3")
        self.product_cash_box = self.env.ref(
            "pos_multiple_control.demo_product_cash_box"
        )
        self.product_not_cash_box = self.env.ref(
            "pos_multiple_control.demo_product_not_cash_box"
        )
        self.pos_config = self.env.ref(
            "pos_multiple_control.pos_config_control"
        )
        self.check_journal = self.env.ref("pos_multiple_control.check_journal")
        self.cash_journal = self.env.ref("pos_multiple_control.cash_journal")

    def _sale(self, session, price, journal):
        order = self.order_obj.create(
            {
                "session_id": session.id,
                "lines": [
                    [
                        0,
                        False,
                        {
                            "name": "OL/0001",
                            "product_id": self.product.id,
                            "qty": 1.0,
                            "price_unit": price,
                        },
                    ]
                ],
            }
        )
        payment = self.payment_obj.create(
            {"journal_id": journal.id, "amount": price, }
        )
        payment.with_context(active_id=order.id).check()
        return order

    # Test Section
    def test_01_two_opening_session(self):
        # I create new session
        self.session_obj.create({"config_id": self.pos_config.id})

        # I Try to create a new session
        with self.assertRaises(ValidationError):
            self.session_obj.create({"config_id": self.pos_config.id})

    def test_02_opening_and_opened_session(self):
        # I create new session and open it
        session = self.session_obj.create({"config_id": self.pos_config.id})
        session.open_cb()

        # I Try to create a new session
        with self.assertRaises(ValidationError):
            self.session_obj.create({"config_id": self.pos_config.id})

    def test_03_check_close_session_with_draft_order(self):
        # I create new session and open it
        session = self.session_obj.create({"config_id": self.pos_config.id})
        session.open_cb()

        # Create a Draft order, and try to close the session
        self.order_obj.create({"session_id": session.id})
        with self.assertRaises(UserError):
            session.signal_workflow("cashbox_control")

    def test_04_check_bank_statement_control(self):
        # I create new session and open it
        session = self.session_obj.create({"config_id": self.pos_config.id})

        # Make 2 Sales of 1100 and check transactions and theoritical balance
        session.open_cb()
        self._sale(session, 100, self.check_journal)
        self._sale(session, 1000, self.check_journal)
        self.assertEqual(
            session.control_register_total_entry_encoding,
            1100,
            "Incorrect transactions total",
        )
        self.assertEqual(
            session.control_register_balance_end,
            1100,
            "Incorrect theoritical ending balance",
        )

        session.signal_workflow("cashbox_control")

        with self.assertRaises(UserError):
            session.signal_workflow("close")

    def test_05_check_autosolve(self):
        # I create new session and open it
        self.pos_config.write(
            {
                "autosolve_pos_move_reason": self.product_cash_box.id,
                "autosolve_limit": 20,
            }
        )
        session = self.session_obj.create({"config_id": self.pos_config.id})

        # Make sales and autosolve
        session.open_cb()
        sale = self._sale(session, 18, self.check_journal)
        sale.statement_ids[0].statement_id.automatic_solve()
        self.assertEqual(
            session.summary_statement_ids[1].control_difference,
            0,
            "Incorrect transactions total",
        )

        session.signal_workflow("cashbox_control")
        session.signal_workflow("close")

    def test_06_check_display_button(self):
        # I create new session and open it
        self.pos_config.write(
            {
                "autosolve_pos_move_reason": self.product_cash_box.id,
                "autosolve_limit": 30,
            }
        )
        session = self.session_obj.create({"config_id": self.pos_config.id})

        # Make sales too important
        session.open_cb()
        sale = self._sale(session, 31, self.check_journal)
        self.assertEqual(
            sale.statement_ids[0].statement_id.display_autosolve,
            False,
            "Autosolve button should be hidden",
        )

        # Autosolve and second sales
        sale.statement_ids[0].statement_id.automatic_solve()
        sale2 = self._sale(session, 29, self.check_journal)
        sale2.statement_ids[0].statement_id._compute_display_autosolve()
        self.assertEqual(
            sale2.statement_ids[0].statement_id.display_autosolve,
            True,
            "Autosolve button should not be hidden",
        )

        sale2.statement_ids[0].statement_id.automatic_solve()
        session.signal_workflow("cashbox_control")
        session.signal_workflow("close")
