# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test import TestModule


class TestAgrosourcing(TestModule):
    def test_agrosourcing(self):
        self._test_supplier_template(
            "agrosourcing__2023-01-11__082083.pdf",
            line_qty=11,
            expected_values={
                "issuer": "Agrosourcing",
                "date": datetime(day=11, month=1, year=2023),
                "invoice_number": "082083",
                "amount": 501.00,
            },
            expected_lines=[
                {
                    "product_code": "000431",
                    "product_name": "Raisins de Turquie - Sultanine - 12,5 kg",
                    "quantity": 12.0,
                    "price_unit": 4.24,
                    "discount": 15,
                    "price_subtotal": 45.05,
                }
            ],
        )
