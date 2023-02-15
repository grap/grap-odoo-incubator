# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test import TestModule


class TestVitafrais(TestModule):
    def test_vitafrais(self):
        self._test_supplier_template(
            "vitafrais__2023-02-13__23013043.pdf",
            line_qty=27,
            expected_values={
                "issuer": "Vitafrais",
                "date": datetime(day=13, month=2, year=2023),
                "invoice_number": "23013043",
                "amount": 478.73,
                "amount_fuel_surcharge": 1.83,
            },
            expected_lines=[
                {
                    "product_code": "9314",
                    "product_name": "Brillat-Savarin affiné 200 g",
                    "quantity": 6.0,
                    "price_unit": 5.82,
                    "discount": 8.0,
                    "price_subtotal": 32.13,
                }
            ],
        )
