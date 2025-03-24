# Copyright (C) 2023-Today: GRAP (<http://www.grap.coop/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ResCompany(models.Model):
    _inherit = "res.company"

    def _configure_favorite_uom(self):
        for company in self:
            result = self.env["product.template"].read_group(
                [("company_id", "in", [company.id, False])], ["uom_id"], ["uom_id"]
            )
            uom_ids = [x["uom_id"][0] for x in result]

            uoms = (
                self.env["uom.uom"]
                .sudo()
                .with_company(company)
                .search([("id", "in", uom_ids)])
            )
            uoms.write({"is_favorite": True})

    @api.model_create_multi
    def create(self, vals_list):
        companies = super().create(vals_list)
        companies._configure_favorite_uom()
        return companies
