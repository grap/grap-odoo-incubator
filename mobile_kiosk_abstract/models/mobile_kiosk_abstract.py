# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class MobileKioskAbstract(models.TransientModel):
    _name = "mobile.kiosk.abstract"
    _description = "Mobile Kiosk Abstract Proxy"

    @api.model
    def _prepare_result(self):
        return {
            "status": "ok",
            "messages": [],
        }

    def _add_result_error(self, result, title, message):
        result["status"] = "ko"
        result["messages"].append({
            "level": "error",
            "title": title,
            "message": message,
        })
        return result

    def _add_result_notify(self, result, title, message):
        result["messages"].append({
            "level": "notify",
            "title": title,
            "message": message,
        })
        return result

    @api.model
    def _prepare_product_data(self, result, product):
        result.update({
            "product_id": product.id,
            "product_name": product.name,
        })

    @api.model
    def _prepare_partner_data(self, result, partner):
        result.update({
            "partner_id": partner.id,
            "partner_name": partner.name,
        })

    @api.model
    def _prepare_supplierinfo_data(self, result, supplierinfo=False):
        result.update({
            "supplierinfo_price": supplierinfo and supplierinfo.price or 0.0,
            "supplierinfo_min_qty":
            supplierinfo and supplierinfo.min_qty or 0.0,
            "supplierinfo_uom_po_id":
            supplierinfo and supplierinfo.product_uom.id or False,
            "supplierinfo_uom_po_name":
            supplierinfo and supplierinfo.product_uom.name or False,
        })
