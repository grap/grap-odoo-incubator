# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test import TestModule


class TestEkibio(TestModule):
    def test_ekibio(self):
        self._test_supplier_template(
            "ekibio",
            "ekibio__2023-02-07__792437.pdf",
            line_qty=6,
            expected_values={
                "date": datetime(day=7, month=2, year=2023),
                "invoice_number": "792437",
                "amount": 671.37,
            },
            expected_lines=[
                {
                    "product_code": "010118",
                    "product_name": "COUSCOUS DEMI COMPLET FILIERE FRANCE 5KG",
                    "quantity": 10.0,
                    "price_unit": 2.56,
                    "price_subtotal": 25.60,
                }
            ],
        )
