# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields
from odoo.tests.common import TransactionCase


class TestStockPickingAccountMove(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Picking = cls.env["stock.picking"]
        cls.Move = cls.env["stock.move"]
        cls.location_stock = cls.env.ref("stock.stock_location_stock")
        cls.location_customers = cls.env.ref("stock.stock_location_customers")

        # Create a picking type with journal and account
        cls.account = cls.env["account.account"].create(
            {
                "name": "Account Test",
                "code": "TEST",
                "account_type": "expense",
                "company_id": cls.env.company.id,
            }
        )
        cls.journal = cls.env["account.journal"].create(
            {
                "name": "Test Journal",
                "type": "general",
                "code": "TEST",
                "company_id": cls.env.company.id,
            }
        )

        cls.picking_type = cls.env["stock.picking.type"].create(
            {
                "name": "Test Picking Type",
                "code": "internal",
                "journal_id": cls.journal.id,
                "company_id": cls.env.company.id,
                "sequence_code": "TST",
                "account_id": cls.account.id,
                "default_location_src_id": cls.location_stock.id,
            }
        )

        # Create a product
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "type": "product",
                "uom_id": cls.env.ref("uom.product_uom_unit").id,
                "uom_po_id": cls.env.ref("uom.product_uom_unit").id,
            }
        )

        # Create a stock picking
        cls.picking = cls.Picking.create(
            {
                "picking_type_id": cls.picking_type.id,
                "location_id": cls.location_stock.id,
                "location_dest_id": cls.location_stock.id,
                "state": "done",
                "date_done": fields.Date.from_string("2025-07-14"),
            }
        )

        # Create a stock move linked to the picking
        cls.move = cls.Move.create(
            {
                "name": "Test Move",
                "product_id": cls.product.id,
                "product_uom_qty": 1,
                "quantity_done": 10,
                "location_id": cls.location_stock.id,
                "location_dest_id": cls.location_customers.id,
                "picking_id": cls.picking.id,
                "state": "done",
            }
        )

    def test_01_generate_account_move(self):
        """Test that the account move is generated correctly"""
        self.picking.generate_account_move()
        self.assertTrue(self.picking.account_move_id, "Account move was not created")
        self.assertEqual(
            self.picking.account_move_id.state, "posted", "Account move was not posted"
        )

    def test_02_create_return_picking(self):
        """Test that the return picking is well created with new field is_return"""
        wiz = (
            self.env["stock.return.picking"]
            .with_context(active_id=self.picking.id, active_model="stock.picking")
            .create({})
        )
        wiz._onchange_picking_id()
        picking_returned_id = wiz._create_returns()[0]
        picking_returned = self.Picking.browse(picking_returned_id)
        self.assertEqual(
            picking_returned.is_return, True, "Picking return should be True"
        )
