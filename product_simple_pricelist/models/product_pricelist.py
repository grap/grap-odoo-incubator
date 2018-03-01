# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    is_simple = fields.Boolean(
        string="Is Simple", help="Check this box if you want to edit this"
        " pricelist by product")

    # Constraints Section
    @api.constrains('is_simple', 'company_id')
    def _check_company_id_is_simple(self):
        for pricelist in self:
            if pricelist.is_simple and not pricelist.company_id:
                raise UserError(_(
                    "Simple Pricelist must have a company defined"))

    # View Section
    @api.multi
    def button_edit_simple_pricelist(self):
        self.ensure_one()
        result = self.env.ref(
            'product_simple_pricelist.action_edit_simple_pricelist').read()[0]
        result['name'] = _("Edit '%s' By Product") % (self.name)
        result['context'] = {'pricelist_id': self.id}
        result['domain'] = "[('pricelist_id', '=', " + str(self.id) + ")]"
        return result
