# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    # Onchange Section
    @api.onchange('consignor_partner_id')
    def onchange_consignor_partner_id(self):
        if not self.consignor_partner_id:
            return
        else:
            self.standard_price = 0
            self.seller_ids = False
            if len(self.consignor_partner_id.consignor_tax_group_ids):
                self.tax_group_id =\
                    self.consignor_partner_id.consignor_tax_group_ids[0]
            else:
                self.tax_group_id = False
