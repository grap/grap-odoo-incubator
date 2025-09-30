import odoo

from odoo.addons.point_of_sale.tests.common import TestPointOfSaleCommon


@odoo.tests.tagged("post_install", "-at_install")
class TestPointOfSaleConfig(TestPointOfSaleCommon):
    def test_get_pos_ui_product_product_by_params(self):
        sector = self.env["pos.sector"].create(
            {
                "name": "Test",
                "company_id": self.pos_config.company_id.id,
            }
        )

        products = self.pos_config.get_limited_products_loading(["sector_id"])
        product_id = products[0]["id"]
        product = self.env["product.product"].browse(product_id)

        product.write({"sector_id": sector.id})
        products = self.pos_config.get_limited_products_loading(["sector_id"])
        self.assertNotIn(product_id, [x["id"] for x in products])

        self.pos_config.sector_ids += sector
        products = self.pos_config.get_limited_products_loading(["sector_id"])
        self.assertIn(product_id, [x["id"] for x in products])
