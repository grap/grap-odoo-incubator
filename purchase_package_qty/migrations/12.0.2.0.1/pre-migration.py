# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def migrate(cr, version):
    if not openupgrade.column_exists(cr, "product_supplierinfo", "multiplier_qty"):
        cr.execute(
            """
            ALTER TABLE product_supplierinfo
            ADD COLUMN multiplier_qty double precision;
            """
        )

    cr.execute(
        """
        UPDATE product_supplierinfo
        SET multiplier_qty = package_qty;
        """
    )
