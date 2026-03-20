import odoo

from odoo.addons.point_of_sale.tests.common import TestPointOfSaleCommon


@odoo.tests.tagged("post_install", "-at_install")
class TestPointOfSaleFlow(TestPointOfSaleCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pos_config.open_ui()
        cls.pos_session = cls.pos_config.current_session_id
        cls.new_demo_sector = cls.env["pos.sector"].create(
            {
                "name": "Test",
                "company_id": cls.pos_config.company_id.id,
            }
        )

    def test_loader_params_product_product_1(self):
        self.assertIn(
            ("sector_id", "in", [False]),
            self.pos_session._loader_params_product_product()["search_params"][
                "domain"
            ],
        )

    def test_loader_params_product_product_2(self):
        self.pos_config.sector_ids += self.new_demo_sector

        self.assertIn(
            ("sector_id", "in", self.new_demo_sector.ids + [False]),
            self.pos_session._loader_params_product_product()["search_params"][
                "domain"
            ],
        )

    def test_load_products(self):
        params = self.pos_session._loader_params_product_product()
        domain = params["search_params"]["domain"]
        products = (
            self.env["product.product"].with_context(**params["context"]).search(domain)
        )
        product = products[0]

        product.write({"sector_id": self.new_demo_sector.id})

        products = (
            self.env["product.product"].with_context(**params["context"]).search(domain)
        )
        self.assertNotIn(product, products)

        self.pos_config.sector_ids += self.new_demo_sector
        params = self.pos_session._loader_params_product_product()
        domain = params["search_params"]["domain"]
        products = (
            self.env["product.product"].with_context(**params["context"]).search(domain)
        )
        self.assertIn(product, products)

    def test_get_pos_ui_product_product_by_params(self):
        products = self.pos_session.get_pos_ui_product_product_by_params({})
        product_id = products[0]["id"]
        product = self.env["product.product"].browse(product_id)

        product.write({"sector_id": self.new_demo_sector.id})
        products = self.pos_session.get_pos_ui_product_product_by_params({})
        self.assertNotIn(product_id, [x["id"] for x in products])

        self.pos_config.sector_ids += self.new_demo_sector
        products = self.pos_session.get_pos_ui_product_product_by_params({})
        self.assertIn(product_id, [x["id"] for x in products])
        products = self.pos_session.get_pos_ui_product_product_by_params(
            {"domain": [("id", "=", product_id)]}
        )
        self.assertIn(product_id, [x["id"] for x in products])
