# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (sylvain.legal@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestStockPickingValuation(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.uom_dozen = cls.env.ref("uom.product_uom_dozen")

        cls.product = cls.env["product.product"].create(
            {
                "name": "Product",
                "type": "product",
                "standard_price": 10,
                "uom_id": cls.uom_unit.id,
                "uom_po_id": cls.uom_unit.id,
                "categ_id": cls.env.ref("product.product_category_all").id,
            }
        )
        cls.picking_type = cls.env["stock.picking.type"].create(
            {
                "name": "Internal Use Case",
                "default_location_src_id": cls.env.ref("stock.stock_location_stock").id,
                "default_location_dest_id": cls.env.ref(
                    "stock.stock_location_suppliers"
                ).id,
                "sequence_code": "TST",
            }
        )
        cls.picking = cls.env["stock.picking"].create(
            {
                "picking_type_id": cls.picking_type.id,
                "location_id": cls.picking_type.default_location_src_id.id,
                "location_dest_id": cls.picking_type.default_location_dest_id.id,
            }
        )

        cls.move = cls.env["stock.move"].create(
            {
                "name": "Test Move",
                "picking_id": cls.picking.id,
                "product_id": cls.product.id,
                "location_id": cls.picking.location_id.id,
                "location_dest_id": cls.picking.location_dest_id.id,
                "product_uom_qty": 5,
            }
        )

    def test_valuations(self):
        # Test with same UoM
        self.move.product_uom = self.uom_unit
        self.assertEqual(self.move.unit_valuation, 10)
        self.assertEqual(self.move.total_valuation, 5 * 10)
        self.assertEqual(self.move.picking_id.total_valuation, 5 * 10)

        # Test with different UoM
        self.move.product_uom = self.uom_dozen
        self.assertEqual(self.move.unit_valuation, 120)
        self.assertEqual(self.move.total_valuation, 5 * 120)
        self.assertEqual(self.move.picking_id.total_valuation, 5 * 120)

    def test_direction(self):
        # correct direction
        self.picking.location_id = self.picking_type.default_location_src_id
        self.picking.location_dest_id = self.picking_type.default_location_dest_id
        self.assertEqual(self.move.picking_id.total_valuation, 5 * 10)

        # opposite direction
        self.picking.location_id = self.picking_type.default_location_dest_id
        self.picking.location_dest_id = self.picking_type.default_location_src_id
        self.assertEqual(self.move.picking_id.total_valuation, -5 * 10)

        # undefined direction
        self.picking.location_id = self.picking_type.default_location_dest_id
        self.picking.location_dest_id = self.picking_type.default_location_dest_id
        self.assertEqual(self.move.picking_id.total_valuation, 0)
