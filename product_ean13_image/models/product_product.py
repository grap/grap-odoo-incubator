# coding: utf-8
# Copyright (C) 2016 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
import base64
import StringIO
import logging

from openerp import api, fields, models

logger = logging.getLogger(__name__)

try:
    import cairosvg
except ImportError:
    logger.debug("grap_print_product - 'cairosvg' librairy not found")

try:
    import barcode
except ImportError:
    logger.debug("grap_print_product - 'barcode' librairy not found")


class ProductProduct(models.Model):
    _inherit = 'product.product'

    ean13_image = fields.Binary(compute='_compute_ean13_image', store=True)

    @api.multi
    @api.depends('ean13')
    def _compute_ean13_image(self):
        for product in self.filtered(lambda x: x.ean13):
            EAN = barcode.get_barcode_class('ean13')
            ean = EAN(product.ean13)
            fullname = ean.save('/tmp/' + product.ean13)
            f = open(fullname, 'r')
            output = StringIO.StringIO()
            svg = f.read()
            cairosvg.svg2png(
                bytestring=svg, write_to=output, center_text=True, dpi=300)
            product.ean13_image = base64.b64encode(output.getvalue())
            os.remove(fullname)
