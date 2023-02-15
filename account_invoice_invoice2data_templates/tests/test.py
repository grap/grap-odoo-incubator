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
        invoice_file_name,
        line_qty,
        expected_values,
        expected_lines,
    ):
        invoice_path = self.pdf_folder_path / invoice_file_name
        result = invoice2data.main.extract_data(
            str(invoice_path), templates=self.templates
        )
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
                "The following data has not been found %s\n"
                "===========\n"
                "%s"
                "===========\n" % (str(expected_line), str(result)),
            )
