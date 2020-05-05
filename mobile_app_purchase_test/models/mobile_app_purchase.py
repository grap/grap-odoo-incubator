# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class MobileAppPurchase(models.TransientModel):
    _name = "mobile.app.purchase"
    _description = "Mobile App Purchase Proxy"

    def _scan_barcode(self, barcode):
        return
