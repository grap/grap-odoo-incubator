import odoo

from odoo.addons.point_of_sale.tests.common import TestPointOfSaleCommon


@odoo.tests.tagged("post_install", "-at_install")
class TestPointOfSaleFlow(TestPointOfSaleCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pos_config.open_ui()
        cls.pos_session = cls.pos_config.current_session_id
        cls.pos_sector_1 = cls.env.ref("pos_sector.sector_1")
        cls.pos_sector_2 = cls.env.ref("pos_sector.sector_2")

    def _test_loader_params_product_product(self):
        self.pos_config.sector_ids = False
        self.assertNotIn(
            "sector_id",
            str(
                self.pos_session._loader_params_product_product()["search_params"][
                    "domain"
                ]
            ),
        )

        self.pos_config.sector_ids += self.pos_sector_1
        self.assertIn(
            ("sector_id", "in", [self.pos_sector_1.id]),
            self.pos_session._loader_params_product_product()["search_params"][
                "domain"
            ],
        )

        self.pos_config.sector_ids += self.pos_sector_2
        self.assertIn(
            ("sector_id", "in", [self.pos_sector_1.id, self.pos_sector_2.id]),
            self.pos_session._loader_params_product_product()["search_params"][
                "domain"
            ],
        )

    def test_get_pos_ui_product_product_by_params(self):
        self.pos_config.sector_ids = False
        products = self.pos_session.get_pos_ui_product_product_by_params({})
        self.assertTrue(len(products) > 2)

        self.pos_config.sector_ids += self.pos_sector_1
        products = self.pos_session.get_pos_ui_product_product_by_params({})
        self.assertEqual(len(products), 1)

        self.pos_config.sector_ids += self.pos_sector_2
        products = self.pos_session.get_pos_ui_product_product_by_params({})
        self.assertEqual(len(products), 2)

    def test_get_limited_products_loading(self):
        self.pos_config.sector_ids = False
        products = self.pos_config.get_limited_products_loading(["sector_id"])
        self.assertTrue(len(products) > 2)

        self.pos_config.sector_ids += self.pos_sector_1
        products = self.pos_config.get_limited_products_loading(["sector_id"])
        self.assertEqual(len(products), 1)

        self.pos_config.sector_ids += self.pos_sector_2
        products = self.pos_config.get_limited_products_loading(["sector_id"])
        self.assertEqual(len(products), 2)
