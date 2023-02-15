# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
from pathlib import Path

import invoice2data

from odoo import tools
from odoo.tests.common import TransactionCase


class TestModule(TransactionCase):
    def setUp(self):
        super().setUp()
        # Load Templates
        local_templates_dir = tools.config["invoice2data_templates_dir"]
        self.templates = invoice2data.extract.loader.read_templates(local_templates_dir)
        self.pdf_folder_path = Path(os.path.realpath(__file__)).parent / "invoices"

    def _test_supplier_template(
        self,
        supplier_name,
        invoice_file_name,
        line_qty,
        expected_values,
        expected_lines,
    ):
        invoice_path = self.pdf_folder_path / invoice_file_name
        result = invoice2data.main.extract_data(
            str(invoice_path), templates=self.templates
        )
        # print("=======")
        # print(result)
        # print("=======")
        for key, expected_value in expected_values.items():
            self.assertEqual(result[key], expected_value)

        for expected_line in expected_lines:
            line_found = False
            for real_line in result["lines"]:
                line_found = line_found or all(
                    [
                        real_line.get(key, False) == expected_line[key]
                        for key in expected_line.keys()
                    ]
                )

            self.assertTrue(
                line_found,
                "The following data has not been found %s" % str(expected_line),
            )

    # def _test_ekibio(self):
    #     self._test_supplier_template(
    #         "ekibio",
    #         "ekibio__2023-02-07__792437.pdf",
    #     )

    # def test_relais_local(self):
    #     self._test_supplier_template(
    #         "relais_local",
    #         "relais-local__2023_01_03__FC230116989.pdf",
    #         line_qty=13,
    #         expected_values={
    #             "date": datetime(day=3, month=1, year=2023),
    #             "invoice_number": "FC230116989",
    #             "amount": 336.96,
    #         },
    #         expected_lines=[
    #             {
    #                 "product_code": "102355",
    #                 "product_name": "TOME DE BREBIS VRAC",
    #                 "quantity": 3.0,
    #                 "price_unit": 24.38,
    #                 "price_subtotal": 73.14,
    #             }
    #         ],
    #     )

    # def _test_relais_vert(self):
    #     self._test_supplier_template(
    #         "relais_vert",
    #         "relais-vert_2023-02-06__FC11716389.pdf",
    #         line_qty=6,
    #         expected_values={
    #             "date": datetime(day=6, month=2, year=2023),
    #             "invoice_number": "FC230116989",
    #             "amount": 127.66,
    #         },
    #         expected_lines=[
    #             {
    #                 "product_code": "KIJAIT",
    #                 "product_name": "KIWI JAUNE VRAC CAT II",
    #                 "quantity": 10.0,
    #                 "price_unit": 3.73,
    #                 "price_subtotal": 37.30,
    #             }
    #         ],
    #     )
