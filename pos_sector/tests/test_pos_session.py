import odoo

from odoo.addons.point_of_sale.tests.common import TestPointOfSaleCommon


@odoo.tests.tagged("post_install", "-at_install")
class TestPointOfSaleFlow(TestPointOfSaleCommon):
    def test_loader_params_product_product_1(self):
        self.pos_config.open_ui()
        pos_session = self.pos_config.current_session_id
        self.assertEqual(
            pos_session._loader_params_product_product(),
            {
                "search_params": {
                    "domain": [
                        "&",
                        "&",
                        "&",
                        ("sale_ok", "=", True),
                        ("available_in_pos", "=", True),
                        "|",
                        ("company_id", "=", self.pos_config.company_id.id),
                        ("company_id", "=", False),
                        "|",
                        ("sector_id", "=", False),
                        ("sector_id", "in", ()),
                    ],
                    "fields": [
                        "display_name",
                        "lst_price",
                        "standard_price",
                        "categ_id",
                        "pos_categ_id",
                        "taxes_id",
                        "barcode",
                        "default_code",
                        "to_weight",
                        "uom_id",
                        "description_sale",
                        "description",
                        "product_tmpl_id",
                        "tracking",
                        "available_in_pos",
                        "attribute_line_ids",
                        "active",
                        "__last_update",
                        "image_128",
                    ],
                    "order": "sequence,default_code,name",
                },
                "context": {"display_default_code": False},
            },
        )

    def test_loader_params_product_product_2(self):
        self.pos_config.open_ui()

        sector = self.env["pos.sector"].create(
            {
                "name": "Test",
                "company_id": self.pos_config.company_id.id,
            }
        )
        self.pos_config.sector_ids += sector

        pos_session = self.pos_config.current_session_id
        self.assertEqual(
            pos_session._loader_params_product_product(),
            {
                "search_params": {
                    "domain": [
                        "&",
                        "&",
                        "&",
                        ("sale_ok", "=", True),
                        ("available_in_pos", "=", True),
                        "|",
                        ("company_id", "=", self.pos_config.company_id.id),
                        ("company_id", "=", False),
                        "|",
                        ("sector_id", "=", False),
                        ("sector_id", "in", (sector.id,)),
                    ],
                    "fields": [
                        "display_name",
                        "lst_price",
                        "standard_price",
                        "categ_id",
                        "pos_categ_id",
                        "taxes_id",
                        "barcode",
                        "default_code",
                        "to_weight",
                        "uom_id",
                        "description_sale",
                        "description",
                        "product_tmpl_id",
                        "tracking",
                        "available_in_pos",
                        "attribute_line_ids",
                        "active",
                        "__last_update",
                        "image_128",
                    ],
                    "order": "sequence,default_code,name",
                },
                "context": {"display_default_code": False},
            },
        )

    def test_load_products(self):
        sector = self.env["pos.sector"].create(
            {
                "name": "Test",
                "company_id": self.pos_config.company_id.id,
            }
        )
        self.pos_config.open_ui()

        pos_session = self.pos_config.current_session_id
        params = pos_session._loader_params_product_product()
        domain = params["search_params"]["domain"]
        products = (
            self.env["product.product"].with_context(**params["context"]).search(domain)
        )
        product = products[0]

        product.write({"sector_id": sector.id})

        products = (
            self.env["product.product"].with_context(**params["context"]).search(domain)
        )
        self.assertNotIn(product, products)

        self.pos_config.sector_ids += sector
        params = pos_session._loader_params_product_product()
        domain = params["search_params"]["domain"]
        products = (
            self.env["product.product"].with_context(**params["context"]).search(domain)
        )
        self.assertIn(product, products)

    def test_get_pos_ui_product_product_by_params(self):
        sector = self.env["pos.sector"].create(
            {
                "name": "Test",
                "company_id": self.pos_config.company_id.id,
            }
        )
        self.pos_config.open_ui()

        pos_session = self.pos_config.current_session_id
        products = pos_session.get_pos_ui_product_product_by_params({})
        product_id = products[0]["id"]
        product = self.env["product.product"].browse(product_id)

        product.write({"sector_id": sector.id})
        products = pos_session.get_pos_ui_product_product_by_params({})
        self.assertNotIn(product_id, [x["id"] for x in products])

        self.pos_config.sector_ids += sector
        products = pos_session.get_pos_ui_product_product_by_params({})
        self.assertIn(product_id, [x["id"] for x in products])
        products = pos_session.get_pos_ui_product_product_by_params(
            {"domain": [("id", "=", product_id)]}
        )
        self.assertIn(product_id, [x["id"] for x in products])
