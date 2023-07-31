# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestMrpProductionPurchaseOrderLink(TransactionCase):
    def setUp(self):
        super(TestMrpProductionPurchaseOrderLink, self).setUp()
        self.prod_screw = self.env.ref("mrp.product_product_computer_desk_screw")
        self.prod_bolt = self.env.ref("mrp.product_product_computer_desk_bolt")
        self.prod_table = self.env.ref("mrp.product_product_computer_desk")
        self.bom_table = self.env.ref("mrp.mrp_bom_desk")
        # Create sellers
        self.seller_screw = self.env["res.partner"].create(
            {
                "name": "SELLER_SCREW",
                "supplier": True,
            }
        )
        self.seller_bolt = self.env["res.partner"].create(
            {
                "name": "SELLER_BOLT",
                "supplier": True,
            }
        )
        # # Set products with the 'buy' route and supplierinfo
        # self.prod_screw.write({
        #     # 'route_ids': [(6, 0, [self.env.ref('stock.route_warehouse0_mto').id])],
        # })
        # self.prod_bolt.write({
        #     # 'route_ids': [(6, 0, [self.env.ref('stock.route_warehouse0_mto').id])],
        # })
        # Create 'supplierinfo' with prevously created sellers
        self.seller_screw_supp_info = self.env["product.supplierinfo"].create(
            {
                "name": self.seller_screw.id,
                "price": 0.2,
            }
        )
        self.seller_bolt_supp_info = self.env["product.supplierinfo"].create(
            {
                "name": self.seller_bolt.id,
                "price": 0.4,
            }
        )

        # Set products with the 'buy' route and supplierinfo
        route_buy_id = self.env.ref("purchase_stock.route_warehouse0_buy").id
        route_mto_id = self.env.ref("stock.route_warehouse0_mto").id
        self.prod_screw.write(
            {
                "seller_ids": [(4, self.seller_screw_supp_info.id, 0)],
                "route_ids": [(6, 0, [route_buy_id, route_mto_id])],
            }
        )
        self.prod_bolt.write(
            {
                "seller_ids": [(4, self.seller_bolt_supp_info.id, 0)],
                "route_ids": [(6, 0, [route_buy_id, route_mto_id])],
            }
        )

    def test_purchase_order_link(self):
        # Create an mrp.production object with the BOM
        mrp_production = self.env["mrp.production"].create(
            {
                "product_id": self.prod_table.id,
                "product_uom_id": self.prod_table.uom_id.id,
                "bom_id": self.bom_table.id,
                "product_qty": 1.0,
            }
        )
        # Check if the link is well created with 2 purchase orders
        self.assertTrue(mrp_production.purchase_order_qty, 2)

        # Check if 2 purchase orders are really created
        po_obj = self.env["purchase.order"]
        po_linked = po_obj.search(
            [("origin", "ilike", "%" + mrp_production.name + "%")]
        )
        self.assertTrue(len(po_linked), 2)
