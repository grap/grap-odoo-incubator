# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    sector_ids = fields.Many2many(string="Sectors", comodel_name="pos.sector")

    def get_limited_products_loading(self, fields):
        """Overwrite the method, because the domain can not be passed in this case.

        The goal is to add a filter on the sector in this méthodes.
        """
        query = """
            WITH pm AS (
                  SELECT product_id,
                         Max(write_date) date
                    FROM stock_move_line
                GROUP BY product_id
                ORDER BY date DESC
            )
               SELECT p.id
                 FROM product_product p
            LEFT JOIN product_template t ON product_tmpl_id=t.id
            LEFT JOIN pm ON p.id=pm.product_id
                WHERE (
                        t.available_in_pos
                    AND t.sale_ok
                    AND (t.company_id=%(company_id)s OR t.company_id IS NULL)
                    AND %(available_categ_ids)s IS NULL
                    OR t.pos_categ_id=ANY(%(available_categ_ids)s)
                )    OR p.id=%(tip_product_id)s
            ORDER BY t.priority DESC,
                    case when t.detailed_type = 'service' then 1 else 0 end DESC,
                    pm.date DESC NULLS LAST,
                    p.write_date
            LIMIT %(limit)s
        """
        params = {
            "company_id": self.company_id.id,
            "available_categ_ids": (
                self.iface_available_categ_ids.mapped("id")
                if self.iface_available_categ_ids
                else None
            ),
            "tip_product_id": self.tip_product_id.id if self.tip_product_id else None,
            "limit": self.limited_products_amount,
        }
        self.env.cr.execute(query, params)
        product_ids = self.env.cr.fetchall()
        products = self.env["product.product"].search_read(
            [
                ("id", "in", product_ids),
                "|",
                ("sector_id", "=", False),
                ("sector_id", "in", self.sector_ids._ids),
            ],
            fields=fields,
        )
        return products
