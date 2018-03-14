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

    # Fields Function Section
    def _get_ean13_image(
            self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for pp in self.browse(cr, uid, ids, context):
            if pp.ean13:
                EAN = barcode.get_barcode_class('ean13')
                ean = EAN(pp.ean13)
                fullname = ean.save('/tmp/' + pp.ean13)
                f = open(fullname, 'r')
                output = StringIO.StringIO()
                svg = f.read()
                cairosvg.svg2png(
                    bytestring=svg, write_to=output, center_text=True, dpi=300)
                res[pp.id] = base64.b64encode(output.getvalue())
                os.remove(fullname)
            else:
                res[pp.id] = False
        return res

    _columns = {
        'ean13_image': fields.function(
            _get_ean13_image, string='Image of the EAN13', type='binary',
            store={
                'product.product': (
                    lambda self, cr, uid, ids, context=None: ids,
                    ['ean13'], 10)}),
    }
