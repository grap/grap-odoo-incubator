# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestModule(TransactionCase):
    def setUp(self):
        super().setUp()

        self.unit_uom = self.env.ref("uom.product_uom_unit")
        self.supplier_with_package = self.env.ref("base.res_partner_1")
        self.supplier_without_package = self.env.ref("base.res_partner_3")
        self.product = self.env.ref("purchase_package_qty.product_product_package_6")
        self.purchase_order = self.env.ref("purchase_package_qty.purchase_order")
        self.purchase_order_line = self.env.ref(
            "purchase_package_qty.purchase_order_line"
        )
        self.supplierinfo = self.env.ref("purchase_package_qty.supplierinfo_supplier_1")

    def test_01_supplierinfo_change_min_qty_lower(self):
        # If we set min_qty to 3, the package_qty should be down to
        # 3 also
        self.supplierinfo.write(
            {
                "min_qty": 3,
            }
        )

        self.supplierinfo.onchange_min_qty()
        self.assertEqual(
            self.supplierinfo.min_qty,
            self.supplierinfo.package_qty,
            "set a min_qty lower than package_qty should decrease package_qty",
        )

        self.supplierinfo.write(
            {
                "min_qty": 0,
            }
        )

        self.supplierinfo.onchange_min_qty()
        self.assertEqual(
            self.supplierinfo.min_qty,
            self.supplierinfo.package_qty,
            "Set no min_qty should set no package_qty",
        )

    def test_01_supplierinfo_change_min_qty_not_rounded(self):
        # If we set min_qty to 601, with a package of 6, the min_qty should
        # be rounded to 606
        self.supplierinfo.write(
            {
                "min_qty": 601,
            }
        )

        self.supplierinfo.onchange_min_qty()
        self.assertEqual(
            self.supplierinfo.min_qty,
            606,
            "set a min_qty not a multiple of package_qty should round"
            " the min quantity.",
        )

    def test_03_supplierinfo_change_package_qty_upper(self):
        # If we set package_qty to 70, the min_qty should be up to
        # 70 also.
        self.supplierinfo.write(
            {
                "package_qty": 70,
            }
        )

        self.supplierinfo.onchange_package_qty()
        self.assertEqual(
            self.supplierinfo.min_qty,
            self.supplierinfo.package_qty,
            "set a package_qty greather than min_qty should increase min_qty",
        )

    def test_04_supplierinfo_change_package_qty_lower_not_rounded(self):
        # If we set package_qty to 25, the min_qty should be down to 50.
        self.supplierinfo.write(
            {
                "package_qty": 25,
            }
        )

        self.supplierinfo.onchange_package_qty()
        self.assertEqual(
            self.supplierinfo.min_qty,
            50,
            "set a package_qty lower than the min_qty should round" " the min_qty",
        )

    def test_05_supplierinfo_change_package_qty_lower_rounded(self):
        # If we set package_qty to 30, the min_qty should not change.
        self.supplierinfo.write(
            {
                "package_qty": 30,
            }
        )

        self.supplierinfo.onchange_package_qty()
        self.assertEqual(
            self.supplierinfo.min_qty,
            60,
            "set a package_qty lower than the min_qty should not change"
            " the min_qty if the packaging is ok.",
        )

    def test_06_supplierinfo_change_package_qty_null(self):
        # If we unset package_qty, min_qty should not change.
        self.supplierinfo.write(
            {
                "package_qty": 0,
            }
        )

        self.supplierinfo.onchange_package_qty()
        self.assertEqual(
            self.supplierinfo.min_qty,
            60,
            "Unset package_qty should not change min_qty.",
        )

    def test_10_purchase_order_line_onchange_package_strict(self):
        # [Functional Test] Check if onchange function changes
        # quantity (strict context)
        self.purchase_order.partner_id = self.supplier_with_package
        self.purchase_order_line.product_qty = 119
        self.purchase_order_line._onchange_quantity()
        self.assertEqual(
            self.purchase_order_line.product_qty,
            120,
            "On change with package defined should round quantity",
        )

    def test_11_purchase_order_line_onchange_no_package(self):
        # [Functional Test] Check if onchange function doesn't change
        # quantity (no package context)
        self.purchase_order.partner_id = self.supplier_without_package
        self.purchase_order_line.product_qty = 5
        self.purchase_order_line._onchange_quantity()
        self.assertEqual(
            self.purchase_order_line.product_qty,
            5,
            "On change without package defined should not change quantity",
        )
