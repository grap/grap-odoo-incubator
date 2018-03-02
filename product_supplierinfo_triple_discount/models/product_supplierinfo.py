# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models
import openerp.addons.decimal_precision as dp


class PricelistPartnerInfo(models.Model):
    _inherit = "pricelist.partnerinfo"

    discount2 = fields.Float(
        string='Discount 2 (%)', digits_compute=dp.get_precision('Discount'))

    discount3 = fields.Float(
        string='Discount 3 (%)', digits_compute=dp.get_precision('Discount'))
