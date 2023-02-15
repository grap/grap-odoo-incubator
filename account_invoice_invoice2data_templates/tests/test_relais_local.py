# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from .test import TestModule


class TestRelaisLocal(TestModule):
    def test_relais_local(self):
        self._test_supplier_template(
            "relais_local",
            "relais-local__2023_01_03__FC230116989.pdf",
            line_qty=13,
            expected_values={
                "date": datetime(day=3, month=1, year=2023),
                "invoice_number": "FC230116989",
                "amount": 336.96,
            },
            expected_lines=[
                {
                    "product_code": "102355",
                    "product_name": "TOME DE BREBIS VRAC",
                    "quantity": 3.0,
                    "price_unit": 24.38,
                    "price_subtotal": 73.14,
                }
            ],
        )
